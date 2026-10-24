"""Daily check of UK Islamic savings rates.

Reads accounts.json, visits each bank's own pages, and writes docs/rates.json.
If a rate cannot be read, or looks wrong, the last good figure is kept and the
account is marked stale. A summary of anything that needs a human is written
to report.md, and the script exits with code 1 so the workflow can raise an
issue.
"""

from __future__ import annotations

import datetime as dt
import json
import re
import sys
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "accounts.json"
OUT = ROOT / "docs" / "rates.json"
REPORT = ROOT / "report.md"
DEBUG = ROOT / "debug"

MIN_RATE, MAX_RATE = 0.1, 10.0      # anything outside this is treated as a misread
MAX_JUMP = 1.5                      # percentage points in one day before we ask a human

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/129.0 Safari/537.36"
)
session = requests.Session()
session.headers.update({"User-Agent": UA, "Accept-Language": "en-GB,en;q=0.9"})

_cache: dict[str, str] = {}


def fetch(url: str) -> str:
    if url in _cache:
        return _cache[url]
    last = None
    for attempt in range(3):
        try:
            r = session.get(url, timeout=30)
            r.raise_for_status()
            _cache[url] = r.text
            return r.text
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"could not load {url}: {last}")


def text_lines(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    for t in soup(["script", "style", "noscript"]):
        t.decompose()
    lines = [re.sub(r"\s+", " ", l).strip() for l in soup.get_text("\n").split("\n")]
    return [l for l in lines if l]


def row_texts(html: str) -> list[str]:
    """Each table row (or row-like block) as one line of text."""
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    for tr in soup.find_all("tr"):
        cells = [re.sub(r"\s+", " ", c.get_text(" ")).strip() for c in tr.find_all(["td", "th"])]
        cells = [c for c in cells if c]
        if cells:
            rows.append(" | ".join(cells))
    return rows


def term_to_months(s: str) -> int | None:
    m = re.search(r"(\d+)\s*(month|year)", s, re.I)
    if not m:
        return None
    n = int(m.group(1))
    return n * 12 if m.group(2).lower().startswith("year") else n


def save_debug(name: str, content) -> None:
    DEBUG.mkdir(exist_ok=True)
    p = DEBUG / f"{name}.txt"
    if isinstance(content, (list, dict)):
        content = json.dumps(content, indent=1, ensure_ascii=False)
    p.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------- parsers
# Each parser returns {key: rate} for one page. Keys are matched to accounts below.

GATEHOUSE_URL = "https://www.gatehousebank.com/personal/savings"


def parse_gatehouse() -> dict[str, float]:
    html = fetch(GATEHOUSE_URL)
    found: dict[str, float] = {}
    candidates = row_texts(html) + text_lines(html)
    # Also try joining consecutive short lines, in case cells render on separate lines.
    lines = text_lines(html)
    for i in range(len(lines) - 1):
        candidates.append(lines[i] + " " + lines[i + 1])
    for line in candidates:
        m = re.match(r"^(.+?)\s*\|?\s+(\d+\.\d{1,2})\s*%", line)
        if m:
            label = m.group(1).replace("|", " ").strip()
            label = re.sub(r"\s+", " ", label)
            if len(label) < 80 and label not in found:
                found[label] = float(m.group(2))
    save_debug("gatehouse", found)
    return found


def parse_alrayan(url: str) -> dict[str, float]:
    html = fetch(url)
    found: dict[str, float] = {}
    for line in row_texts(html) + text_lines(html):
        m = re.match(r"^(.+?)\s*\|?\s*£[\d,]+\s*\|?\s*(\d+\.\d{1,2})\s*%", line)
        if m:
            label = m.group(1).replace("|", " ").strip()
            if label not in found:
                found[label] = float(m.group(2))
    save_debug("alrayan-" + url.rstrip("/").split("/")[-1], found)
    return found


def parse_blme_premier(url: str) -> dict[str, float]:
    """Table rows: term | gross | AER. Returns {months: AER}."""
    html = fetch(url)
    found: dict[str, float] = {}
    for line in row_texts(html):
        cells = [c.strip() for c in line.split("|")]
        if len(cells) < 2:
            continue
        months = term_to_months(cells[0])
        pcts = [float(x) for c in cells[1:] for x in re.findall(r"(\d+\.\d{1,2})\s*%", c)]
        if months and pcts and str(months) not in found:
            found[str(months)] = pcts[-1]  # last % in the row is the AER column
    save_debug("blme-premier", found)
    return found


def parse_blme_notice(url: str) -> dict[str, float]:
    html = fetch(url)
    txt = " ".join(text_lines(html))
    m = re.search(r"(\d+\.\d{1,2})\s*%\s*Gross\s*AER", txt, re.I)
    found = {"aer": float(m.group(1))} if m else {}
    save_debug("blme-notice", found)
    return found


HABIB_URL = "https://www.habibbank.com/gb/our-services/edeposits/hbz-sirat-edeposit/"


def parse_habib() -> dict[str, float]:
    html = fetch(HABIB_URL)
    txt = "\n".join(text_lines(html))
    found: dict[str, float] = {}
    for m in re.finditer(r"(\d+)\s*(Months?|Years?)\s*\n\s*(\d+\.\d{1,2})\s*%\s*EPR", txt, re.I):
        months = term_to_months(m.group(1) + " " + m.group(2))
        if months and str(months) not in found:
            found[str(months)] = float(m.group(3))
    save_debug("habib", found)
    return found


def parse_raisin(bank_slug: str, any_product: str) -> dict[str, dict]:
    """Every offer Raisin lists for one bank, keyed by product id."""
    url = f"https://www.raisin.com/en-gb/bank/{bank_slug}/{any_product}/"
    html = fetch(url)
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
    if not m:
        raise RuntimeError(f"Raisin page layout changed for {bank_slug}")
    data = json.loads(m.group(1))
    offers = data["props"]["pageProps"]["bankPage"]["bank_offers"]
    if isinstance(offers, dict):
        offers = list(offers.values())
    found = {}
    for o in offers:
        pid = str(o.get("id") or o.get("product_id") or "").upper()
        rate = (o.get("interest_rates") or {}).get("interest_rate_effective")
        if not pid or rate is None:
            continue
        rate = float(rate)
        if rate < 0.5:  # given as a fraction, e.g. 0.0485
            rate = round(rate * 100, 2)
        found[pid] = {
            "rate": rate,
            "name": (o.get("display") or {}).get("product_name"),
            "type": o.get("product_type"),
            "months": (o.get("term_normalized") or {}).get("months"),
        }
    save_debug("raisin-" + bank_slug, found)
    return found


# ---------------------------------------------------------------- matching

def match_label(found: dict[str, float], pattern: str) -> float | None:
    rx = re.compile(pattern, re.I)
    hits = {k: v for k, v in found.items() if rx.search(k)}
    if not hits:
        return None
    # The shortest matching label is the cleanest (longer ones are usually two lines joined).
    return hits[min(hits, key=len)]


def read_rate(acc: dict, raisin_pages: dict) -> float | None:
    src = acc["source"]
    kind = src["kind"]
    if kind == "gatehouse":
        return match_label(parse_gatehouse(), src["match"])
    if kind == "alrayan":
        return match_label(parse_alrayan(src["page"]), src["match"])
    if kind == "blme_premier":
        return parse_blme_premier(src["page"]).get(str(acc["term_months"]))
    if kind == "blme_notice":
        return parse_blme_notice(src["page"]).get("aer")
    if kind == "habib_sirat":
        return parse_habib().get(str(acc["term_months"]))
    if kind == "raisin":
        offers = raisin_pages.setdefault(src["bank_slug"], parse_raisin(src["bank_slug"], src["product"]))
        o = offers.get(src["product"].upper())
        return o["rate"] if o else None
    raise RuntimeError(f"unknown source kind {kind}")


# ---------------------------------------------------------------- main

def main() -> int:
    cfg = json.loads(CONFIG.read_text())
    prev = {}
    if OUT.exists():
        try:
            prev = {a["id"]: a for a in json.loads(OUT.read_text())["accounts"]}
        except Exception:  # noqa: BLE001
            prev = {}

    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    today = now.date().isoformat()
    problems: list[str] = []
    notes: list[str] = []
    raisin_pages: dict[str, dict] = {}
    out_accounts = []

    for acc in cfg["accounts"]:
        old = prev.get(acc["id"], {})
        last_good = old.get("rate", acc["rate"])
        rec = {k: v for k, v in acc.items() if k != "source"}
        rec["rate"] = last_good
        rec["last_verified"] = old.get("last_verified")
        rec["rate_changed"] = old.get("rate_changed")
        rec["stale"] = False
        rec["stale_since"] = None
        error = None
        try:
            rate = read_rate(acc, raisin_pages)
            if rate is None:
                error = "not found on the page (may have been withdrawn or renamed)"
            elif not (MIN_RATE <= rate <= MAX_RATE):
                error = f"read {rate}% which looks wrong"
            elif abs(rate - last_good) > MAX_JUMP:
                error = f"read {rate}%, a jump of more than {MAX_JUMP} points from {last_good}%; kept the old figure until checked"
        except Exception as e:  # noqa: BLE001
            error = f"error: {e}"
            rate = None

        if error:
            rec["stale"] = True
            rec["stale_since"] = old.get("stale_since") or today
            problems.append(f"- **{cfg['banks'][acc['bank']]['name']} ({acc['platform']}) {acc['name']}** `{acc['id']}`: {error}")
        else:
            if rate != last_good:
                notes.append(f"- {cfg['banks'][acc['bank']]['name']} ({acc['platform']}) {acc['name']}: {last_good}% to {rate}%")
                rec["previous_rate"] = last_good
                rec["rate_changed"] = today
            rec["rate"] = rate
            rec["last_verified"] = now.isoformat()
        out_accounts.append(rec)

    # New products on Raisin that we do not list yet.
    known = {a["source"]["product"].upper() for a in cfg["accounts"] if a["source"]["kind"] == "raisin"}
    for slug, offers in raisin_pages.items():
        for pid, o in offers.items():
            if pid not in known:
                notes.append(f"- New on Raisin ({slug}): `{pid}` {o.get('name')} at {o['rate']}% (not on the site yet; add it to accounts.json if it is Islamic)")

    banks = {k: {"name": v["name"], "logo": v["logo"]} for k, v in cfg["banks"].items()}
    payload = {
        "checked_at": now.isoformat(),
        "account_count": len(out_accounts),
        "stale_count": sum(a["stale"] for a in out_accounts),
        "banks": banks,
        "accounts": out_accounts,
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=1, ensure_ascii=False) + "\n")

    fetch_logos(cfg)

    report = [f"Rate check {today}: {len(out_accounts)} accounts, {payload['stale_count']} could not be confirmed.\n"]
    if problems:
        report += ["## Needs a look\nThe site is still showing the last confirmed figure for these, marked as not confirmed today.\n", *problems, ""]
    if notes:
        report += ["## Changes and new products\n", *notes, ""]
    REPORT.write_text("\n".join(report))
    print("\n".join(report))
    return 1 if problems else 0


def fetch_logos(cfg: dict) -> None:
    for b in cfg["banks"].values():
        dest = ROOT / "docs" / b["logo"]
        if dest.exists() or not b.get("logo_src"):
            continue
        try:
            r = session.get(b["logo_src"], timeout=30)
            r.raise_for_status()
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(r.content)
        except Exception as e:  # noqa: BLE001
            print(f"logo download failed for {b['name']}: {e}")


if __name__ == "__main__":
    sys.exit(main())
