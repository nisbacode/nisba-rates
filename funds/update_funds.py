"""Refresh fund performance from Alpha Vantage and write docs/funds.json.

Nisba has a premium Alpha Vantage key, so every fund is refreshed every run
using full daily price history (adjusted for distributions), plus one USD/GBP
call. DAILY_FUND_CALLS caps calls per run as a safety limit.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
SEED = ROOT / "funds" / "funds.json"
OUT = ROOT / "docs" / "funds.json"
REPORT = ROOT / "funds-report.md"

KEY = os.environ.get("ALPHA_VANTAGE_API_KEY", "").strip()
DAILY_FUND_CALLS = int(os.environ.get("DAILY_FUND_CALLS", "100"))
PAUSE = 1.5  # seconds between calls; premium plans allow 75 a minute
STALE_DAYS = 7


class AVError(RuntimeError):
    pass


def av(params: dict) -> dict:
    params = {**params, "apikey": KEY}
    r = requests.get("https://www.alphavantage.co/query", params=params, timeout=40)
    r.raise_for_status()
    j = r.json()
    for k in ("Note", "Information", "Error Message"):
        if k in j:
            raise AVError(f"{k}: {j[k][:200]}")
    return j


def price_series(symbol: str) -> list[tuple[dt.date, float]]:
    """Daily closes, newest first, adjusted for distributions where available."""
    try:
        j = av({"function": "TIME_SERIES_DAILY_ADJUSTED", "symbol": symbol, "outputsize": "full"})
        data = j["Time Series (Daily)"]
        field = "5. adjusted close"
    except (AVError, KeyError):
        time.sleep(PAUSE)
        j = av({"function": "TIME_SERIES_DAILY", "symbol": symbol, "outputsize": "full"})
        data = j["Time Series (Daily)"]
        field = "4. close"
    rows = [(dt.date.fromisoformat(d), float(v[field])) for d, v in data.items()]
    rows.sort(reverse=True)
    if not rows:
        raise AVError("no data")
    return rows


def fx_series() -> list[tuple[dt.date, float]]:
    """GBP per 1 USD, daily, newest first."""
    j = av({"function": "FX_DAILY", "from_symbol": "USD", "to_symbol": "GBP", "outputsize": "full"})
    data = j["Time Series FX (Daily)"]
    rows = [(dt.date.fromisoformat(d), float(v["4. close"])) for d, v in data.items()]
    rows.sort(reverse=True)
    return rows


def value_on_or_before(rows, day):
    for d, v in rows:  # newest first
        if d <= day:
            return d, v
    return None, None


def performance(rows, fx=None) -> dict:
    """Returns in % for standard periods. fx converts a USD series into GBP terms."""
    end_d, end_v = rows[0]
    targets = {
        "1d": rows[1][0] if len(rows) > 1 else end_d,
        "1w": end_d - dt.timedelta(days=7),
        "1m": end_d - dt.timedelta(days=30),
        "6m": end_d - dt.timedelta(days=182),
        "ytd": dt.date(end_d.year - 1, 12, 31),
        "1y": end_d - dt.timedelta(days=365),
    }
    out = {}
    for k, day in targets.items():
        d0, v0 = value_on_or_before(rows, day)
        if v0 is None or v0 == 0 or (day - d0).days > 7:
            out[k] = None
            continue
        r = end_v / v0
        if fx is not None:
            _, f1 = value_on_or_before(fx, end_d)
            _, f0 = value_on_or_before(fx, d0)
            if not f0 or not f1:
                out[k] = None
                continue
            r *= f1 / f0
        out[k] = round((r - 1) * 100, 2)
    return out


def main() -> int:
    seed = json.loads(SEED.read_text())["funds"]
    prev = {}
    if OUT.exists():
        try:
            prev = {f["ticker"]: f for f in json.loads(OUT.read_text())["funds"]}
        except Exception:  # noqa: BLE001
            prev = {}
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    today = now.date()
    problems, notes = [], []

    if not KEY:
        REPORT.write_text("ALPHA_VANTAGE_API_KEY secret is missing, so fund prices could not be refreshed.\n")
        print(REPORT.read_text())
        return 1

    # Oldest data first, never-fetched first of all.
    av_funds = [f for f in seed if f.get("alpha_vantage_ticker")]
    av_funds.sort(key=lambda f: prev.get(f["ticker"], {}).get("updated_at") or "")
    batch = av_funds[:DAILY_FUND_CALLS]

    fx = None
    try:
        fx = fx_series()
    except Exception as e:  # noqa: BLE001
        problems.append(f"- USD/GBP exchange rate: {e}")

    fresh = {}
    for f in batch:
        time.sleep(PAUSE)
        sym = f["alpha_vantage_ticker"].replace("﻿", "").strip()
        try:
            rows = price_series(sym)
            perf = performance(rows)
            if f["currency"] == "USD" and fx:
                perf_gbp = performance(rows, fx)
            elif f["currency"] == "GBP":
                perf_gbp = perf
            else:
                perf_gbp = {k: None for k in perf}
            fresh[f["ticker"]] = {"as_of": rows[0][0].isoformat(), "perf": perf, "perf_gbp": perf_gbp,
                                  "updated_at": now.isoformat()}
        except AVError as e:
            if "Note" in str(e) or "rate limit" in str(e).lower() or "25 requests" in str(e):
                problems.append(f"- Alpha Vantage daily limit reached after {len(fresh)} funds; the rest roll over to tomorrow.")
                break
            problems.append(f"- {f['name']} ({sym}): {e}")
        except Exception as e:  # noqa: BLE001
            problems.append(f"- {f['name']} ({sym}): {e}")

    out_funds = []
    for f in seed:
        rec = dict(f)
        old = prev.get(f["ticker"], {})
        new = fresh.get(f["ticker"])
        src = new or old
        rec["as_of"] = src.get("as_of")
        rec["perf"] = src.get("perf")
        rec["perf_gbp"] = src.get("perf_gbp")
        rec["updated_at"] = src.get("updated_at")
        rec["data_source"] = "Alpha Vantage" if f.get("alpha_vantage_ticker") else None
        if rec["as_of"]:
            age = (today - dt.date.fromisoformat(rec["as_of"])).days
            rec["stale"] = age > STALE_DAYS
            if rec["stale"] and f.get("alpha_vantage_ticker"):
                problems.append(f"- {f['name']}: latest price is from {rec['as_of']}")
        else:
            rec["stale"] = True
        out_funds.append(rec)

    payload = {
        "checked_at": now.isoformat(),
        "fund_count": len(out_funds),
        "with_data": sum(1 for f in out_funds if f["perf"]),
        "funds": out_funds,
    }
    OUT.write_text(json.dumps(payload, indent=1, ensure_ascii=False) + "\n")

    missing = [f["name"] for f in out_funds if not f.get("alpha_vantage_ticker")]
    report = [f"Fund check {today}: refreshed {len(fresh)} of {len(av_funds)} Alpha Vantage funds today; "
              f"{payload['with_data']} of {len(out_funds)} funds have performance data.\n"]
    if problems:
        report += ["## Needs a look\n", *problems, ""]
    if missing:
        notes.append(f"- {len(missing)} funds have no Alpha Vantage code and need another price source.")
    if notes:
        report += ["## Notes\n", *notes, ""]
    REPORT.write_text("\n".join(report))
    print("\n".join(report))
    real = [p for p in problems if "daily limit" not in p]
    return 1 if real else 0


if __name__ == "__main__":
    sys.exit(main())
