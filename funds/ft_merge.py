"""Merge FT price lines into funds/ft_prices.json.

Input (a text file, or stdin): lines of "TICKER#YYMMDD price,YYMMDD price,..." as
returned by funds/ft_fetch.js. Existing dates are overwritten only when the
new price is within 1% (FT sometimes revises the last price); bigger
differences and day-on-day moves over 15% are reported and skipped.

Usage: python funds/ft_merge.py lines.txt
Prints a short summary and exits 1 if anything looked wrong.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STORE = ROOT / "funds" / "ft_prices.json"


def main() -> int:
    text = Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else sys.stdin.read()
    data = json.loads(STORE.read_text())
    prices = data["prices"]
    funds = {f["ticker"] for f in json.loads((ROOT / "funds" / "funds.json").read_text())["funds"] if f.get("ft")}
    problems, added = [], {}
    for line in text.splitlines():
        line = line.strip()
        if not line or "#" not in line:
            continue
        t, body = line.split("#", 1)
        if t not in funds:
            problems.append(f"{t}: not an FT-priced fund in funds.json")
            continue
        cur = dict(prices.get(t, []))
        n = 0
        for item in filter(None, (x.strip() for x in body.split(","))):
            if item.startswith("ERR"):
                problems.append(f"{t}: FT returned {item}")
                continue
            m = re.fullmatch(r"(\d{6}) ([\d.]+)", item)
            if not m:
                problems.append(f"{t}: could not read '{item}'")
                continue
            d = f"20{m[1][:2]}-{m[1][2:4]}-{m[1][4:]}"
            p = float(m[2])
            if p <= 0:
                continue
            if d in cur and abs(cur[d] / p - 1) > 0.01:
                problems.append(f"{t}: {d} was {cur[d]}, FT now says {p}; kept the old value")
                continue
            if d not in cur:
                n += 1
            cur[d] = p
        rows = sorted(cur.items())
        for (d0, p0), (d1, p1) in zip(rows, rows[1:]):
            if abs(p1 / p0 - 1) > 0.15:
                problems.append(f"{t}: price moved {p0} to {p1} between {d0} and {d1}; please check")
        prices[t] = [[d, p] for d, p in rows]
        added[t] = n
    STORE.write_text(json.dumps(data, indent=0) + "\n")
    print("New prices added:", ", ".join(f"{k} +{v}" for k, v in added.items()) or "none")
    for p in problems:
        print("PROBLEM:", p)
    missing = sorted(funds - set(added))
    if missing:
        print("No data received for:", ", ".join(missing))
    return 1 if problems or missing else 0


if __name__ == "__main__":
    sys.exit(main())
