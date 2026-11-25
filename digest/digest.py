"""Weekly "what changed" email for the Nisba savings accounts and funds lists.

Compares the live data (docs/rates.json, docs/funds.json) with the snapshot that was in the
last email that actually went out (digest/baseline.json), and writes a ready-to-send email.

  python digest/digest.py init     Set the baseline to today's data (first run only).
  python digest/digest.py build    Write digest/out/summary.json, digest/out/email.html and
                                   digest/out/snapshot.json. summary.json says whether
                                   anything changed.
  python digest/digest.py sent     The last draft was sent: make digest/pending.json's
                                   snapshot the new baseline and remove pending.json.

The email lists the best rate in each term bucket (BUCKETS) now against the baseline, plus new or
removed funds, the top and bottom 3 fund price moves since the baseline
(from docs/funds.json hist_gbp), and any lines in digest/notes.md (optional, hand written "other news"; "sent" clears it).
summary.json "due" is true once the baseline is at least MIN_DAYS old, so the email goes out every
two weeks; "suspicious" lists best rates that moved more than SUSPICIOUS_MOVE points (likely a data
problem, do not draft).

The weekly scheduled task creates the Kajabi broadcast draft from email.html, saves its id and
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


def fund_moves(since_iso, n=3):
    """Biggest GBP price moves on the funds list since the baseline date, from docs/funds.json weekly history."""
    since = since_iso[:10]
    out = []
    for x in load(ROOT / "docs" / "funds.json")["funds"]:
        h = x.get("hist_gbp") or []
        start = [p for p in h if p[0] <= since]
        if not start or not h or h[-1][0] <= start[-1][0] or not start[-1][1]:
            continue
        chg = (h[-1][1] / start[-1][1] - 1) * 100
        out.append({"name": x["name"], "ticker": x["ticker"].split(".")[0], "asset_class": x.get("asset_class"),
                    "change": round(chg, 1), "from": start[-1][0], "to": h[-1][0]})
    out.sort(key=lambda r: -r["change"])
    total = len(out)
    seen, uniq = set(), []
    for r in out:  # one line per fund: share classes (e.g. HINS and HIND) share a name
        if r["name"] not in seen:
            seen.add(r["name"]); uniq.append(r)
    out = uniq
    return {"top": out[:n], "bottom": out[-n:][::-1] if len(out) > n else [], "count": total}


def pct(v):
    return f"+{v:.1f}%" if v > 0 else f"{v:.1f}%"


PURPLE, AMBER, CREAM, INK, GREY, GREEN, RED = "#5E3EAD", "#FF8E0F", "#FFF3E0", "#1A1A1A", "#6B6B6B", "#1E7B4A", "#B3261E"
FONT = "font-family:Helvetica,Arial,sans-serif;"


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def h2(t):
    return (f'<h2 style="{FONT}color:{PURPLE};font-size:20px;line-height:1.3;margin:28px 0 10px 0;">{esc(t)}</h2>')


def para(html, extra=""):
    return f'<p style="{FONT}color:{INK};font-size:16px;line-height:1.55;margin:0 0 14px 0;{extra}">{html}</p>'


def button(text, url):
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:16px 0 8px 0;"><tr>'
            f'<td style="background:{PURPLE};border-radius:6px;">'
            f'<a href="{esc(url)}" style="{FONT}display:inline-block;padding:12px 22px;color:#ffffff;font-size:15px;'
            f'font-weight:bold;text-decoration:none;">{esc(text)}</a></td></tr></table>')


def table(head, rows, highlight):
    """rows: lists of html cells; highlight: list of bools (row gets a cream background)."""
    # Kajabi's sanitiser drops <th> and <div>, so headers are <td> and cards use <p>
    th = "".join(f'<td align="left" style="{FONT}font-size:13px;color:#ffffff;background:{PURPLE};padding:8px 10px;">'
                 f'<strong>{esc(h)}</strong></td>' for h in head)
    body = ""
    for cells, hl in zip(rows, highlight):
        bg = CREAM if hl else "#ffffff"
        body += "<tr>" + "".join(
            f'<td style="{FONT}font-size:14px;color:{INK};padding:8px 10px;border-bottom:1px solid #EEE6F7;background:{bg};">{c}</td>'
            for c in cells) + "</tr>"
    return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" '
            f'style="border-collapse:collapse;margin:6px 0 6px 0;"><tr>{th}</tr>{body}</table>')


def email(d, base, notes, fm):
    since = fmt_date(base["taken_at"])
    moved = [r for r in d["rows"] if r["changed"] and r["old"]]
    ups = sorted([r for r in moved if r["move"] > 0], key=lambda r: -r["move"])
    downs = sorted([r for r in moved if r["move"] < 0], key=lambda r: r["move"])
    lead = (ups or downs or [None])[0]
    if lead:
        word = "up" if lead["move"] > 0 else "down"
        subject = f"Best {lead['label'].lower()} rate {word} to {lead['new']['rate']:.2f}%"
        k = len(moved)
        preview = f"{k} of the best Islamic savings rates moved since {since}, plus the biggest halal fund moves."
    elif d["new_funds"]:
        subject = f"{len(d['new_funds'])} new halal fund{'s' if len(d['new_funds']) > 1 else ''} on the Nisba list"
        preview = "Best savings rates held steady. Here is what is new on the funds list."
    else:
        subject = "Your Nisba savings and funds round up"
        preview = "Where the best Islamic savings rates stand, plus the biggest halal fund moves."

    H = [para("Salam,"),
         para(f"Here is your fortnightly round up: where the best Islamic savings rates stand today, and how the "
              f"halal funds on our list have moved since our last update on {esc(since)}.")]
    if moved:
        H.append(h2("What moved"))
        for r in ups + downs:
            n, o = r["new"], r["old"]
            colour, arrow = (GREEN, "&#9650;") if r["move"] > 0 else (RED, "&#9660;")
            src = (f"now with {esc(who(n))}" if (o["bank"], o.get("platform")) != (n["bank"], n.get("platform"))
                   else f"with {esc(who(n))}")
            H.append(
                f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 10px 0;">'
                f'<tr><td style="background:{CREAM};border-left:4px solid {AMBER};border-radius:4px;padding:12px 14px;">'
                f'<p style="{FONT}margin:0;font-size:13px;color:{GREY};text-transform:uppercase;letter-spacing:0.5px;">{esc(r["label"])}</p>'
                f'<p style="{FONT}font-size:22px;font-weight:bold;color:{INK};margin:2px 0;">{n["rate"]:.2f}% '
                f'<span style="font-size:14px;color:{colour};">{arrow} from {o["rate"]:.2f}%</span></p>'
                f'<p style="{FONT}margin:0;font-size:14px;color:{INK};">{src}</p></td></tr></table>')
    H.append(h2("Best rates right now"))
    rows, hl = [], []
    for r in d["rows"]:
        n, o = r["new"], r["old"]
        if not o:
            ch = f'<span style="color:{PURPLE};font-weight:bold;">new</span>'
        elif not r["changed"]:
            ch = f'<span style="color:{GREY};">same</span>'
        elif r["move"] > 0:
            ch = f'<span style="color:{GREEN};font-weight:bold;">&#9650; {r["move"]:.2f}</span>'
        else:
            ch = f'<span style="color:{RED};font-weight:bold;">&#9660; {abs(r["move"]):.2f}</span>'
        rows.append([esc(r["label"]), f"<strong>{n['rate']:.2f}%</strong>", esc(who(n)), ch])
        hl.append(r["changed"])
    H.append(table(["Account", "Best rate", "With", "Change"], rows, hl))
    H.append(button("Compare every account", SAVINGS_URL))

    if fm["top"] or d["new_funds"] or d["removed_funds"]:
        H.append(h2("Halal funds"))
        if fm["top"]:
            H.append(para(f"The biggest price moves on our list of {fm['count']} funds since {esc(since)}, in pounds:"))
            rows = [[f'<span style="color:{GREEN};font-weight:bold;">Top</span>', f"{esc(x['name'])} ({esc(x['ticker'])})",
                     esc(x.get("asset_class") or "fund"), f'<strong style="color:{GREEN};">{pct(x["change"])}</strong>']
                    for x in fm["top"]]
            rows += [[f'<span style="color:{RED};font-weight:bold;">Bottom</span>', f"{esc(x['name'])} ({esc(x['ticker'])})",
                      esc(x.get("asset_class") or "fund"), f'<strong style="color:{RED};">{pct(x["change"])}</strong>']
                     for x in fm["bottom"]]
            H.append(table(["", "Fund", "Type", "Change"], rows, [False] * len(rows)))
            H.append(para("A few weeks is a very short time for an investment, and past performance is not a guide to the future.",
                          f"font-size:13px;color:{GREY};font-style:italic;margin-top:8px;"))
        if d["new_funds"]:
            H.append(para("<strong>New on the list</strong>"))
            H.append("<ul style='margin:0 0 14px 18px;padding:0;'>" + "".join(
                f'<li style="{FONT}font-size:15px;color:{INK};margin:0 0 6px 0;"><strong>{esc(x["name"])}</strong> '
                f'({esc(x["ticker"].split(".")[0])}): {esc(x.get("asset_class") or "fund")}, {x["fee"]:.2f}% a year, '
                f'available on {esc(plats(x["platforms"]))}</li>' for x in d["new_funds"]) + "</ul>")
        if d["removed_funds"]:
            H.append(para("<strong>Taken off the list:</strong> " + esc(", ".join(x["name"] for x in d["removed_funds"]))))
        H.append(button("See all the funds side by side", FUNDS_URL))
    if notes:
        H.append(h2("Also new at Nisba"))
        H += [para(esc(line.lstrip("- ").strip())) for line in notes.splitlines() if line.strip()]
    H += [f'<hr style="border:none;border-top:1px solid #EEE6F7;margin:28px 0 20px 0;">',
          para("A good rate or a strong few weeks is a tool, not a plan. What suits you depends on what the money is for, "
               "when you need it and how much risk you can take, which is what the Nisba six step framework walks you through."),
          para("<strong>Are these updates useful?</strong> One click tells us: "
               f'<a href="{FEEDBACK_URL}?vote=more" style="color:{PURPLE};">More like this</a> | '
               f'<a href="{FEEDBACK_URL}?vote=same" style="color:{PURPLE};">Fine as they are</a> | '
               f'<a href="{FEEDBACK_URL}?vote=less" style="color:{PURPLE};">Less often, please</a>'),
          para("Jzk"),
          para("Ahmad and Adel<br>Nisba"),
          para("Rates are expected profit rates read from each provider's own website and can change at any time. "
               "Always check with the provider before you open an account or invest. Education only, not personalised "
               "financial advice. Investing carries risk and you may get back less than you put in. "
               "We send this every two weeks, or less often if nothing moves.",
               f"font-size:12px;color:{GREY};line-height:1.5;")]
    body = "\n".join(H) + "\n"
    for bad in ("\u2014", "\u2013", "{%", "|"):
        assert bad not in subject and bad not in preview, "bad character in subject/preview"
    for bad in ("\u2014", "\u2013", "{{", "{%"):
        assert bad not in body, f"{bad!r} found in body"
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
        fm = fund_moves(base["taken_at"])
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
                   "notes": bool(notes), "suspicious": suspicious,
                   "fund_moves": {"top": fm["top"], "bottom": fm["bottom"]}}
        if summary["has_changes"]:
            subject, preview, body = email(d, base, notes, fm)
            summary.update(subject=subject, preview=preview)
            (OUT / "email.html").write_text(body)
        (OUT / "snapshot.json").write_text(json.dumps(cur, indent=1, sort_keys=True))
        (OUT / "summary.json").write_text(json.dumps(summary, indent=1))
        print(json.dumps(summary, indent=1))
    else:
        sys.exit("unknown command " + cmd)


if __name__ == "__main__":
    main()
