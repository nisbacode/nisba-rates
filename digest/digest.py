"""Weekly "what changed" email for the Nisba savings accounts and funds lists.

Compares the live data (docs/rates.json, docs/funds.json) with the snapshot that was in the
last email that actually went out (digest/baseline.json), and writes a ready-to-send email.

  python digest/digest.py init     Set the baseline to today's data (first run only).
  python digest/digest.py build    Write digest/out/summary.json, digest/out/email.html and
                                   digest/out/snapshot.json. summary.json says whether
                                   anything changed.
  python digest/digest.py build --first   Same, with the one-off introduction for the very first issue.
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
            "stale": bool(a.get("stale")), "link": a.get("link"),
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
                    "factsheet": x.get("factsheet"),
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


# Design (researched 25 Nov 2026).
# Readability: one column, 600px, 16px sans-serif body, about 200 words of prose (Constant Contact: ~200 words gets
# the best click rate; Nielsen Norman: ~51 seconds per newsletter), one button 44px+ tall, moves shown with words
# and arrows not colour alone, light backgrounds behind dark text for dark mode.
# Not looking AI-made / templated: no coloured left-border cards, no uppercase letter-spaced labels, no pills,
# gradients, shadows or emoji; sentence case headings; plain prose written like a person with concrete numbers;
# one button, everything else plain links. Colours are the website's: navy and Nisba orange.
# Kajabi's sanitiser drops <div> and <th>, so only p, span, strong, a, table/tr/td, h2, hr, br are used.
NAVY, ORANGE, INK, GREY, GREEN, RED, LINE, SOFT = ("#081426", "#FF8E0F", "#1A1A1A", "#5F6368", "#1E7B4A",
                                                   "#B3261E", "#E6E1D8", "#FBF7F0")
SANS = "font-family:Helvetica,Arial,sans-serif;"
SERIF = "font-family:Georgia,'Times New Roman',serif;"  # stands in for the site's Playfair Display
CORE = ["Easy access", "Notice accounts", "6 month fixed", "1 year fixed", "2 year fixed", "3 year fixed",
        "5 year fixed", "Cash ISA, easy access", "Cash ISA, fixed"]  # rows in the table; any bucket can move
INTRO = ("This is a new email from us. Every two weeks we check the Islamic savings accounts and halal funds "
         "on Nisba and send you the best rates in one short email. If nothing changes, we stay quiet.")


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def p(html, style=""):
    return f'<p style="{SANS}color:{INK};font-size:16px;line-height:1.6;margin:0 0 16px 0;{style}">{html}</p>'


def h2(t):
    return f'<h2 style="{SERIF}color:{NAVY};font-size:21px;line-height:1.3;font-weight:bold;margin:30px 0 10px 0;">{esc(t)}</h2>'


def link(text_html, url, bold=False):
    if not url:
        return text_html
    return (f'<a href="{esc(url)}" style="color:{NAVY};text-decoration:underline;'
            f'{"font-weight:bold;" if bold else ""}">{text_html}</a>')


def button(text, url):
    # navy text on orange: white on #FF8E0F fails contrast (about 2.2:1)
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:18px 0 6px 0;"><tr>'
            f'<td style="background:{ORANGE};border-radius:4px;">'
            f'<a href="{esc(url)}" style="{SANS}display:inline-block;padding:14px 24px;color:{NAVY};font-size:16px;'
            f'font-weight:bold;text-decoration:none;">{esc(text)}</a></td></tr></table>')


def td(html, style=""):
    return f'<td style="{SANS}font-size:15px;color:{INK};padding:10px 8px;border-bottom:1px solid {LINE};vertical-align:top;{style}">{html}</td>'


def email(d, base, notes, fm, first=False, n_accounts=None, n_funds=None):
    since = fmt_date(base["taken_at"])
    moved = [r for r in d["rows"] if r["changed"] and r["old"]]
    ups = sorted([r for r in moved if r["move"] > 0], key=lambda r: -r["move"])
    downs = sorted([r for r in moved if r["move"] < 0], key=lambda r: r["move"])
    lead = (ups or downs or [None])[0]
    if first:
        subject = "New from Nisba: the best Islamic savings rates, every two weeks"
        preview = (f"Best {lead['label'].lower()} rate now {lead['new']['rate']:.2f}%, plus the biggest halal fund moves."
                   if lead else "The best Islamic savings rates and the biggest halal fund moves, in one short email.")
    elif lead:
        word = "up" if lead["move"] > 0 else "down"
        subject = f"Best {lead['label'].lower()} rate {word} to {lead['new']['rate']:.2f}%"
        preview = f"{len(moved)} of the best Islamic savings rates moved since {since}, plus the biggest halal fund moves."
    elif d["new_funds"]:
        subject = f"{len(d['new_funds'])} new halal fund{'s' if len(d['new_funds']) > 1 else ''} on the Nisba list"
        preview = "Best savings rates held steady. Here is what is new on the funds list."
    else:
        subject = "Your Nisba savings and funds update"
        preview = "Where the best Islamic savings rates stand, plus the biggest halal fund moves."

    H = [p("Salam,")]
    if first:
        H.append(p(INTRO))
    if moved:
        n = len(moved)
        word = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five"}.get(n, str(n))
        dirn = "went up" if not downs else ("came down" if not ups else "moved")
        H.append(p(f"{word} of the best rates {dirn} since {esc(since)}:"))
        items = ""
        for r in ups + downs:
            nw, o = r["new"], r["old"]
            same = (o["bank"], o.get("platform")) == (nw["bank"], nw.get("platform"))
            arrow = "&#9650; up" if r["move"] > 0 else "&#9660; down"
            colour = GREEN if r["move"] > 0 else RED
            was = f"from {o['rate']:.2f}%" + ("" if same else f" with {esc(who(o))}")
            items += (f'<tr><td style="{SANS}font-size:16px;line-height:1.5;color:{INK};padding:0 0 10px 0;">'
                      f'<strong>{esc(r["label"])}:</strong> {nw["rate"]:.2f}% with '
                      f'{link(esc(who(nw)), nw.get("link"))} '
                      f'<span style="color:{colour};white-space:nowrap;">({arrow} {was})</span></td></tr>')
        H.append(f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{items}</table>')
    else:
        H.append(p(f"The best savings rates have held steady since {esc(since)}."))

    H.append(h2("Best rates right now"))
    rows = ""
    for r in d["rows"]:
        if r["label"] not in CORE:
            continue
        nw = r["new"]
        bg = f"background:{SOFT};" if r["changed"] else ""
        mark = (f' <span style="color:{GREEN if r["move"] > 0 else RED};font-size:13px;">'
                f'{"&#9650;" if r["move"] > 0 else "&#9660;"}</span>') if r["changed"] and r["old"] else ""
        rows += ("<tr>" + td(esc(r["label"]), bg) +
                 td(f'<strong style="color:{NAVY};">{nw["rate"]:.2f}%</strong>{mark}', bg + "white-space:nowrap;") +
                 td(link(esc(who(nw)), nw.get("link")), bg) + "</tr>")
    H.append(f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" '
             f'style="border-collapse:collapse;border-top:2px solid {NAVY};">{rows}</table>')
    H.append(p("Tap a bank to go to the account. Some of these are affiliate links, which may pay Nisba a fee at no "
               "cost to you. Rates can change at any time, so check the rate on the provider's page before you apply." + (" Shaded rows moved since " + esc(since) + "." if moved else ""),
               f"font-size:13px;color:{GREY};margin:8px 0 0 0;"))
    H.append(button(f"Compare all {n_accounts} accounts" if n_accounts else "Compare every account", SAVINGS_URL))

    if fm["top"] or d["new_funds"] or d["removed_funds"]:
        H.append(h2("Halal funds"))
        if fm["top"]:
            H.append(p(f"The biggest price moves since {esc(since)} across the {fm['count']} funds on our list, in pounds."))

            def fund_rows(xs, title, colour, arrow):
                out = (f'<tr><td colspan="2" style="{SANS}font-size:15px;color:{colour};font-weight:bold;'
                       f'padding:14px 8px 4px 8px;">{arrow} {title}</td></tr>')
                for x in xs:
                    out += ("<tr>" + td(f'{link(esc(x["name"]), FUNDS_URL)}<br>'
                                        f'<span style="font-size:13px;color:{GREY};">{esc(x.get("asset_class") or "Fund")}, {esc(x["ticker"])}</span>') +
                            td(f'<strong style="color:{colour};">{pct(x["change"])}</strong>', "text-align:right;white-space:nowrap;") + "</tr>")
                return out
            H.append(f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" '
                     f'style="border-collapse:collapse;">{fund_rows(fm["top"], "Up the most", GREEN, "&#9650;")}'
                     f'{fund_rows(fm["bottom"], "Down the most", RED, "&#9660;")}</table>')
            H.append(p("A few weeks is a very short time for an investment, and past "
                       "performance is not a guide to the future.", f"font-size:13px;color:{GREY};margin-top:8px;"))
        if d["new_funds"]:
            H.append(p("<strong>New on the list:</strong> " + "; ".join(
                f'{link(esc(x["name"]), FUNDS_URL)} ({esc(x.get("asset_class") or "fund")}, {x["fee"]:.2f}% a year)'
                for x in d["new_funds"])))
        if d["removed_funds"]:
            H.append(p("<strong>Taken off the list:</strong> " + esc(", ".join(x["name"] for x in d["removed_funds"]))))
        H.append(p(link(f"See all {n_funds} funds side by side" if n_funds else "See all the funds side by side",
                        FUNDS_URL, bold=True)))
    if notes:
        H.append(h2("Also new at Nisba"))
        H += [p(esc(line.lstrip("- ").strip())) for line in notes.splitlines() if line.strip()]
    H += [f'<hr style="border:none;border-top:1px solid {LINE};margin:28px 0 20px 0;">',
          p("A good rate is a tool, not a plan. What suits you depends on what the money is for and when you need it, "
            "which is what the Nisba six step framework walks you through."),
          p("Is this useful? One click tells us: "
            f'{link("More like this", FEEDBACK_URL + "?vote=more")}, '
            f'{link("fine as it is", FEEDBACK_URL + "?vote=same")} or '
            f'{link("less often, please", FEEDBACK_URL + "?vote=less")}.'),
          p("Jzk<br>Ahmad and Adel"),
          p("Rates are expected profit rates read from each provider's own website. Education only, not personalised "
            "financial advice. Investing carries risk and you may get back less than you put in. "
            "You can stop these updates with the link at the bottom of this email.",
            f"font-size:12px;color:{GREY};line-height:1.5;")]
    body = "\n".join(H) + "\n"
    for bad in ("\u2014", "\u2013", "{%", "|"):
        assert bad not in subject and bad not in preview, "bad character in subject/preview"
    for bad in ("\u2014", "\u2013", "{{", "{%", "<div", "<th"):
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
            subject, preview, body = email(d, base, notes, fm, first="--first" in sys.argv,
                                          n_accounts=sum(1 for a in cur["accounts"].values() if not a["stale"]),
                                          n_funds=len(cur["funds"]))
            summary.update(subject=subject, preview=preview)
            (OUT / "email.html").write_text(body)
        (OUT / "snapshot.json").write_text(json.dumps(cur, indent=1, sort_keys=True))
        (OUT / "summary.json").write_text(json.dumps(summary, indent=1))
        print(json.dumps(summary, indent=1))
    else:
        sys.exit("unknown command " + cmd)


if __name__ == "__main__":
    main()
