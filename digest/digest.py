"""Weekly "what changed" email for the Nisba savings accounts and funds lists.

Compares the live data (docs/rates.json, docs/funds.json) with the snapshot that was in the
last email that actually went out (digest/baseline.json), and writes a ready-to-send email.

  python digest/digest.py init     Set the baseline to today's data (first run only).
  python digest/digest.py build    Write digest/out/summary.json, digest/out/email.md and
                                   digest/out/snapshot.json. summary.json says whether
                                   anything changed.
  python digest/digest.py sent     The last draft was sent: make digest/pending.json's
                                   snapshot the new baseline and remove pending.json.

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


def diff(base, cur):
    ba, ca = base["accounts"], cur["accounts"]
    bf, cf = base["funds"], cur["funds"]
    new_acc = [ca[k] for k in ca if k not in ba and not ca[k]["stale"]]
    gone_acc = [ba[k] for k in ba if k not in ca]
    ups, downs = [], []
    for k, a in ca.items():
        if k in ba and not a["stale"]:
            d = round(a["rate"] - ba[k]["rate"], 2)
            if d >= RATE_MOVE:
                ups.append((a, ba[k]["rate"]))
            elif d <= -RATE_MOVE:
                downs.append((a, ba[k]["rate"]))
    new_funds = [cf[k] | {"ticker": k} for k in cf if k not in bf]
    gone_funds = [bf[k] | {"ticker": k} for k in bf if k not in cf]
    new_acc.sort(key=lambda a: -a["rate"])
    ups.sort(key=lambda t: -(t[0]["rate"] - t[1]))
    downs.sort(key=lambda t: t[0]["rate"] - t[1])
    return {"new_accounts": new_acc, "removed_accounts": gone_acc, "rate_rises": ups, "rate_cuts": downs,
            "new_funds": new_funds, "removed_funds": gone_funds}


def best_now(cur):
    live = [a for a in cur["accounts"].values() if not a["stale"]]
    out = []
    for t, label in (("easy", "Easy access"), ("notice", "Notice"), ("fixed", "Fixed term")):
        pool = [a for a in live if a["type"] == t]
        if pool:
            a = max(pool, key=lambda a: a["rate"])
            out.append(f"- **{label}:** {a['rate']:.2f}% with {acc_label(a)}")
    isas = [a for a in live if a["isa"]]
    if isas:
        a = max(isas, key=lambda a: a["rate"])
        out.append(f"- **Cash ISA:** {a['rate']:.2f}% with {acc_label(a)}")
    return out


def email(d, cur):
    n_acc = len(d["new_accounts"]) + len(d["rate_rises"]) + len(d["rate_cuts"]) + len(d["removed_accounts"])
    n_fund = len(d["new_funds"]) + len(d["removed_funds"])
    bits = []
    if d["new_accounts"]:
        bits.append(f"{len(d['new_accounts'])} new savings account{'s' if len(d['new_accounts']) > 1 else ''}")
    if d["rate_rises"] or d["rate_cuts"]:
        k = len(d["rate_rises"]) + len(d["rate_cuts"])
        bits.append(f"{k} rate change{'s' if k > 1 else ''}")
    if d["new_funds"]:
        bits.append(f"{len(d['new_funds'])} new halal fund{'s' if len(d['new_funds']) > 1 else ''}")
    if not bits and (d["removed_accounts"] or d["removed_funds"]):
        bits.append("a few accounts and funds removed")
    subject = "This week on Nisba: " + (", ".join(bits[:-1]) + " and " + bits[-1] if len(bits) > 1 else bits[0])
    if d["new_accounts"]:
        top = d["new_accounts"][0]
        preview = f"New: {top['bank']} at {top['rate']:.2f}%. Plus the best Islamic savings rates right now."
    elif d["rate_rises"]:
        a, old = d["rate_rises"][0]
        preview = f"{a['bank']} up from {old:.2f}% to {a['rate']:.2f}%. Plus the best rates right now."
    elif d["new_funds"]:
        preview = f"New on the list: {d['new_funds'][0]['name']}."
    else:
        preview = "The latest changes to our Islamic savings and halal funds lists."

    L = ["Salam {{ first_name | default: \"there\" }},", "",
         "Here is what changed on our Islamic savings and halal funds lists this week."]
    if n_acc:
        L += ["", "## Savings accounts"]
        if d["new_accounts"]:
            L += ["", "**New accounts**"] + [f"- {acc_label(a)}: **{a['rate']:.2f}%**, minimum £{a['min']:,}" for a in d["new_accounts"]]
        if d["rate_rises"]:
            L += ["", "**Rates up**"] + [f"- {acc_label(a)}: {old:.2f}% to **{a['rate']:.2f}%**" for a, old in d["rate_rises"]]
        if d["rate_cuts"]:
            L += ["", "**Rates down**"] + [f"- {acc_label(a)}: {old:.2f}% to **{a['rate']:.2f}%**" for a, old in d["rate_cuts"]]
        if d["removed_accounts"]:
            L += ["", "**No longer available**"] + [f"- {acc_label(a)}" for a in d["removed_accounts"]]
        L += ["", "**Best rates right now**"] + best_now(cur)
        L += ["", f"[Compare every account]({SAVINGS_URL})"]
    if n_fund:
        L += ["", "## Halal funds"]
        if d["new_funds"]:
            L += ["", "**New on the list**"] + [
                f"- **{x['name']}** ({x['ticker'].split('.')[0]}): {x.get('asset_class') or 'fund'}, "
                f"{x['fee']:.2f}% a year, available on {plats(x['platforms'])}" for x in d["new_funds"]]
        if d["removed_funds"]:
            L += ["", "**Taken off the list**"] + [f"- {x['name']}" for x in d["removed_funds"]]
        L += ["", f"[See all the funds side by side]({FUNDS_URL})"]
    L += ["", "A good rate or a popular fund is a tool, not a plan. What suits you depends on what the money is for, "
              "when you need it and how much risk you can take, which is what the Nisba six step framework walks you through.",
          "", "Rates are expected profit rates read from each provider's own website and can change at any time. "
              "Always check with the provider before you open an account or invest. Education only, not personalised "
              "financial advice. Investing carries risk and you may get back less than you put in.",
          "", "Jzk", "", "Ahmad and Adel  ", "Nisba"]
    body = "\n".join(L) + "\n"
    for bad in ("—", "–"):
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
        print("baseline moved to", p["snapshot"]["taken_at"])
    elif cmd == "build":
        OUT.mkdir(exist_ok=True)
        cur = snapshot()
        d = diff(load(BASELINE), cur)
        counts = {k: len(v) for k, v in d.items()}
        has = any(counts[k] for k in ("new_accounts", "rate_rises", "rate_cuts", "new_funds")) or \
            (counts["removed_accounts"] + counts["removed_funds"]) > 0
        summary = {"has_changes": has, "counts": counts, "baseline_taken_at": load(BASELINE)["taken_at"]}
        if has:
            subject, preview, body = email(d, cur)
            summary.update(subject=subject, preview=preview)
            (OUT / "email.md").write_text(body)
        (OUT / "snapshot.json").write_text(json.dumps(cur, indent=1, sort_keys=True))
        (OUT / "summary.json").write_text(json.dumps(summary, indent=1))
        print(json.dumps(summary, indent=1))
    else:
        sys.exit("unknown command " + cmd)


if __name__ == "__main__":
    main()
