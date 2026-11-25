"""Weekly "what changed" email for the Nisba savings accounts and funds lists.

Compares the live data (docs/rates.json, docs/funds.json) with the snapshot that was in the
last email that actually went out (digest/baseline.json), and writes a ready-to-send email.

  python digest/digest.py init     Set the baseline to today's data (first run only).
  python digest/digest.py build    Write digest/out/summary.json, digest/out/email.md and
                                   digest/out/snapshot.json. summary.json says whether
                                   anything changed.
  python digest/digest.py sent     The last draft was sent: make digest/pending.json's
                                   snapshot the new baseline and remove pending.json.

The email lists the best rate in each term bucket (BUCKETS) now against the baseline, plus new or
removed funds and any lines in digest/notes.md (optional, hand written "other news"; "sent" clears it).
summary.json "due" is true once the baseline is at least MIN_DAYS old, so the email goes out every
two weeks; "suspicious" lists best rates that moved more than SUSPICIOUS_MOVE points (likely a data
problem, do not draft).

The weekly scheduled task creates the Kajabi broadcast draft from email.md, saves its id and
the snapshot in digest/pending.json, and runs "sent" the next week once Kajabi shows the
broadcast as delivered. Until then the baseline stays put, so a skipped week is not lost.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = ROOT / "digest"
OUT = HERE / "out"
BASELINE = HERE / "baseline.json"
PENDING = HERE / "pending.json"
RATE_MOVE = 0.05  # percentage points; smaller moves are ignored
SAVINGS_URL = "https://www.nisba.co.uk/savings-accounts?unlocked=1"
FUNDS_URL = "https://www.nisba.co.uk/funds?unlocked=1"
FEEDBACK_URL = "https://www.nisba.co.uk/update-feedback"  # Kajabi thank-you page; votes = link clicks per broadcast
PLATFORM_NAMES = {"Trading212": "Trading 212", "AjBell": "AJ Bell", "InteractiveInvestor": "Interactive Investor",
                  "HL": "Hargreaves Lansdown", "Hargreaves": "Hargreaves Lansdown"}


def load(p):
    return json.loads(Path(p).read_text())


def snapshot():
    r = load(ROOT / "docs" / "rates.json")
    f = load(ROOT / "docs" / "funds.json")
    banks = r.get("banks", {})
    accounts = {}
    for a in r["accounts"]:
        accounts[a["id"]] = {
            "bank": (banks.get(a["bank"]) or {}).get("name", a["bank"]),
            "name": a["name"], "type": a["type"], "term_months": a.get("term_months"),
            "notice_days": a.get("notice_days"), "isa": a.get("isa", False),
            "platform": a.get("platform"), "min": a.get("min"), "rate": a["rate"],
            "stale": bool(a.get("stale")),
        }
    funds = {}
    for x in f["funds"]:
        funds[x["ticker"]] = {
            "name": x["name"], "asset_class": x.get("asset_class"), "currency": x.get("currency"),
            "fee": x.get("fee"), "platforms": x.get("platforms") or [], "category": x.get("category"),
        }
    return {"taken_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "rates_checked_at": r.get("checked_at"), "funds_checked_at": f.get("checked_at"),
            "accounts": accounts, "funds": funds}


def term(a):
    if a["type"] == "easy":
        return "easy access"
    if a["type"] == "notice":
        return f"{a.get('notice_days') or (a.get('term_months') or 0) * 30} day notice"
    m = a.get("term_months") or 0
    if m and m % 12 == 0:
        return f"{m // 12} year fixed"
    return f"{m} month fixed"


def acc_label(a):
    via = " via Raisin" if a.get("platform") == "Raisin" else ""
    return f"{a['bank']} {a['name']} ({term(a)}{', Cash ISA' if a.get('isa') else ''}{via})"


def plats(p):
    return ", ".join(PLATFORM_NAMES.get(x, x) for x in p) or "platforms to be confirmed"


BUCKETS = [  # (label, test) for the best-rate table; ISAs are kept separate
    ("Easy access", lambda a: a["type"] == "easy" and not a["isa"]),
    ("Notice accounts", lambda a: a["type"] == "notice" and not a["isa"]),
    ("3 month fixed", lambda a: a["type"] == "fixed" and a.get("term_months") == 3 and not a["isa"]),
    ("6 month fixed", lambda a: a["type"] == "fixed" and a.get("term_months") == 6 and not a["isa"]),
    ("9 month fixed", lambda a: a["type"] == "fixed" and a.get("term_months") == 9 and not a["isa"]),
    ("1 year fixed", lambda a: a["type"] == "fixed" and a.get("term_months") == 12 and not a["isa"]),
    ("18 month fixed", lambda a: a["type"] == "fixed" and a.get("term_months") == 18 and not a["isa"]),
    ("2 year fixed", lambda a: a["type"] == "fixed" and a.get("term_months") == 24 and not a["isa"]),
    ("3 year fixed", lambda a: a["type"] == "fixed" and a.get("term_months") == 36 and not a["isa"]),
    ("5 year fixed", lambda a: a["type"] == "fixed" and a.get("term_months") == 60 and not a["isa"]),
    ("Cash ISA, easy access", lambda a: a["isa"] and a["type"] != "fixed"),
    ("Cash ISA, fixed", lambda a: a["isa"] and a["type"] == "fixed"),
]
SUSPICIOUS_MOVE = 1.5  # percentage points; a best rate moving more than this is probably a data problem
MIN_DAYS = 13          # the email goes out every two weeks: build says due only once the baseline is this old
NOTES = HERE / "notes.md"  # optional "other news" lines Ahmad adds by hand; cleared by "sent"


def best(snap, test):
    pool = [a for a in snap["accounts"].values() if not a["stale"] and test(a)]
    return max(pool, key=lambda a: a["rate"]) if pool else None


def who(a):
    via = " via Raisin" if a.get("platform") == "Raisin" else (" via Prosper" if a.get("platform") == "Prosper" else "")
    t = f", {term(a)}" if a["type"] == "notice" or (a["isa"] and a["type"] == "fixed") else ""
    return f"{a['bank']}{via}{t}"


def diff(base, cur):
    rows = []
    for label, test in BUCKETS:
        o, n = best(base, test), best(cur, test)
        if not n:
            continue
        move = round(n["rate"] - o["rate"], 2) if o else None
        rows.append({"label": label, "old": o, "new": n, "move": move,
                     "changed": o is None or abs(move) >= RATE_MOVE})
    bf, cf = base["funds"], cur["funds"]
    new_funds = [cf[k] | {"ticker": k} for k in cf if k not in bf]
    gone_funds = [bf[k] | {"ticker": k} for k in bf if k not in cf]
    return {"rows": rows, "new_funds": new_funds, "removed_funds": gone_funds}


def fmt_date(iso):
    d = datetime.fromisoformat(iso)
    return f"{d.day} {d.strftime('%b %Y')}"


def email(d, base, notes):
    moved = [r for r in d["rows"] if r["changed"] and r["old"]]
    ups = sorted([r for r in moved if r["move"] > 0], key=lambda r: -r["move"])
    downs = sorted([r for r in moved if r["move"] < 0], key=lambda r: r["move"])
    lead = (ups or downs or [None])[0]
    if lead:
        subject = f"Nisba savings update: best {lead['label'].lower()} rate now {lead['new']['rate']:.2f}%"
        k = len(moved)
        preview = (f"{k} best rate{'s' if k > 1 else ''} moved since {fmt_date(base['taken_at'])}. "
                   "Here is where the top Islamic savings rates stand.")
    elif d["new_funds"]:
        subject = f"Nisba update: {len(d['new_funds'])} new halal fund{'s' if len(d['new_funds']) > 1 else ''} on the list"
        preview = "Best Islamic savings rates unchanged. Here is what is new on the funds list."
    else:
        subject = "Nisba update: what is new this fortnight"
        preview = "The latest from Nisba, plus the best Islamic savings rates right now."

    L = ["Salam,", "",
         f"Here are the best Islamic savings rates on Nisba right now, against our last update on {fmt_date(base['taken_at'])}."]
    L += ["", "## Best savings rates", ""]
    for r in d["rows"]:
        n, o = r["new"], r["old"]
        if not o:
            L.append(f"- **{r['label']}:** **{n['rate']:.2f}%** with {who(n)} (new on the list)")
        elif not r["changed"]:
            L.append(f"- **{r['label']}:** {n['rate']:.2f}% with {who(n)} (no change)")
        else:
            arrow = "up" if r["move"] > 0 else "down"
            was = f"{o['rate']:.2f}% with {who(o)}" if o["bank"] != n["bank"] or o.get("platform") != n.get("platform") \
                else f"{o['rate']:.2f}%"
            L.append(f"- **{r['label']}:** **{n['rate']:.2f}%** with {who(n)}, {arrow} from {was}")
    L += ["", f"[Compare every account]({SAVINGS_URL})"]
    if d["new_funds"] or d["removed_funds"]:
        L += ["", "## Halal funds"]
        if d["new_funds"]:
            L += ["", "**New on the list**"] + [
                f"- **{x['name']}** ({x['ticker'].split('.')[0]}): {x.get('asset_class') or 'fund'}, "
                f"{x['fee']:.2f}% a year, available on {plats(x['platforms'])}" for x in d["new_funds"]]
        if d["removed_funds"]:
            L += ["", "**Taken off the list**"] + [f"- {x['name']}" for x in d["removed_funds"]]
        L += ["", f"[See all the funds side by side]({FUNDS_URL})"]
    if notes:
        L += ["", "## Also new at Nisba", "", notes]
    L += ["", "A good rate is a tool, not a plan. What suits you depends on what the money is for, "
              "when you need it and how much risk you can take, which is what the Nisba six step framework walks you through.",
          "", "Rates are expected profit rates read from each provider's own website and can change at any time. "
              "Always check with the provider before you open an account or invest. Education only, not personalised "
              "financial advice. Investing carries risk and you may get back less than you put in.",
          "", "**Are these updates useful?** One click tells us: "
              f"[More like this]({FEEDBACK_URL}?vote=more) | "
              f"[Fine as they are]({FEEDBACK_URL}?vote=same) | "
              f"[Less often, please]({FEEDBACK_URL}?vote=less)",
          "", "We now send this every two weeks, or less often if nothing moves.",
          "", "Jzk", "", "Ahmad and Adel  ", "Nisba"]
    body = "\n".join(L) + "\n"
    for bad in ("\u2014", "\u2013"):
        assert bad not in body and bad not in subject and bad not in preview, "dash found"
    return subject, preview, body


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "build"
    if cmd == "init":
        BASELINE.write_text(json.dumps(snapshot(), indent=1, sort_keys=True))
        print("baseline set")
    elif cmd == "sent":
        p = load(PENDING)
        BASELINE.write_text(json.dumps(p["snapshot"], indent=1, sort_keys=True))
        PENDING.unlink()
        if NOTES.exists():
            NOTES.unlink()
        print("baseline moved to", p["snapshot"]["taken_at"])
    elif cmd == "build":
        OUT.mkdir(exist_ok=True)
        base, cur = load(BASELINE), snapshot()
        d = diff(base, cur)
        notes = NOTES.read_text().strip() if NOTES.exists() else ""
        moved = [r for r in d["rows"] if r["changed"]]
        age = (datetime.now(timezone.utc) - datetime.fromisoformat(base["taken_at"])).days
        suspicious = [f"{r['label']}: {r['old']['rate']:.2f}% to {r['new']['rate']:.2f}%"
                      for r in moved if r["old"] and abs(r["move"]) > SUSPICIOUS_MOVE]
        summary = {"has_changes": bool(moved or d["new_funds"] or d["removed_funds"] or notes),
                   "due": age >= MIN_DAYS, "baseline_age_days": age, "baseline_taken_at": base["taken_at"],
                   "best_rate_moves": [{"bucket": r["label"], "old": r["old"] and r["old"]["rate"],
                                        "old_with": r["old"] and who(r["old"]), "new": r["new"]["rate"],
                                        "new_with": who(r["new"])} for r in moved],
                   "new_funds": len(d["new_funds"]), "removed_funds": len(d["removed_funds"]),
                   "notes": bool(notes), "suspicious": suspicious}
        if summary["has_changes"]:
            subject, preview, body = email(d, base, notes)
            summary.update(subject=subject, preview=preview)
            (OUT / "email.md").write_text(body)
        (OUT / "snapshot.json").write_text(json.dumps(cur, indent=1, sort_keys=True))
        (OUT / "summary.json").write_text(json.dumps(summary, indent=1))
        print(json.dumps(summary, indent=1))
    else:
        sys.exit("unknown command " + cmd)


if __name__ == "__main__":
    main()
