"""Works out how closely the funds on nisba.co.uk/correlations have moved together.

Called by funds/update_funds.py, which already downloads every fund's daily
prices each morning, so this needs no extra Alpha Vantage calls. The result is
written to docs/correlations.json, which the correlations page reads live.

Method
- Weekly returns in pounds (US dollar lines converted at that day's rate).
- A two year window ending on the last day of the previous month, so the table
  changes once a month and stays put in between.
- Each pair uses the weeks where both funds have a price. A fund that launched
  inside the window therefore shows a shorter history, which the page flags.
- A pair needs at least MIN_WEEKS shared weeks, otherwise it shows as "n/a".
- Price spikes of more than 15% that fully reverse the next day or week are
  treated as wrong closes in the data feed and left out (see drop_bad_prints
  and drop_weekly_spikes).

To change which funds appear, edit FUNDS below. "ticker" must match a ticker in
funds/funds.json that has an alpha_vantage_ticker. Funds in the same "group" sit
next to each other on the page.
"""

from __future__ import annotations

import datetime as dt
import json
import math
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "correlations.json"

WEEKS = 104      # two years of weekly returns
MIN_WEEKS = 26   # shared weeks a pair needs before a figure is shown
MAX_GAP_DAYS = 6  # a weekly price older than this counts as missing

FUNDS = [
    {"ticker": "HIUS", "name": "HSBC MSCI USA Islamic", "group": 1},
    {"ticker": "ISUS", "name": "iShares MSCI USA Islamic", "group": 1},
    {"ticker": "SPWI", "name": "Wahed S&P 500 Shariah", "group": 1},
    {"ticker": "HIWS", "name": "HSBC MSCI World Islamic", "group": 2},
    {"ticker": "ISWD", "name": "iShares MSCI World Islamic", "group": 2},
    {"ticker": "IGDA", "name": "Invesco DJ Islamic Developed", "group": 2},
    {"ticker": "AMAL", "name": "Saturna Al-Kawthar Global", "group": 2},
    {"ticker": "HIPS", "name": "HSBC MSCI Europe Islamic", "group": 3},
    {"ticker": "HIJS", "name": "HSBC MSCI Japan Islamic", "group": 3},
    {"ticker": "ISDE", "name": "iShares MSCI EM Islamic", "group": 4},
    {"ticker": "HIES", "name": "HSBC MSCI EM Islamic", "group": 4},
    {"ticker": "HINS", "name": "HSBC FTSE Islamic REIT", "group": 4},
    {"ticker": "SKUK", "name": "iShares $ Sukuk", "group": 5},
    {"ticker": "HBKS", "name": "HSBC Global Sukuk", "group": 5},
    {"ticker": "SLVP", "name": "Invesco Physical Silver", "group": 6},
    {"ticker": "RMAP", "name": "Royal Mint Physical Gold", "group": 6},
    {"ticker": "SGLN", "name": "iShares Physical Gold", "group": 6},
    {"ticker": "IB1T.L", "name": "iShares Bitcoin ETP", "group": 7},
]


def window_end(today: dt.date) -> dt.date:
    """Last day of the month before `today`."""
    return today.replace(day=1) - dt.timedelta(days=1)


def _on_or_before(rows, day):
    for d, v in rows:  # newest first
        if d <= day:
            return d, v
    return None, None


def drop_bad_prints(rows):
    """Remove one-day price spikes that reverse the next day (a wrong close in the data feed).

    A day is dropped when it sits more than SPIKE away from both the day before and the
    day after, while those two are within SETTLE of each other.
    """
    SPIKE, SETTLE = 0.15, 0.08
    keep, dropped = [], []
    for i, (d, v) in enumerate(rows):  # newest first
        if 0 < i < len(rows) - 1:
            newer, older = rows[i - 1][1], rows[i + 1][1]
            if newer > 0 and older > 0 and v > 0 and abs(v / older - 1) > SPIKE \
                    and abs(v / newer - 1) > SPIKE and abs(newer / older - 1) < SETTLE:
                dropped.append(d)
                continue
        keep.append((d, v))
    return keep, dropped


def weekly_values(rows, fx, end: dt.date, weeks: int = WEEKS):
    """Values in pounds at `end` and each 7 days before it, oldest first. None where there is no recent price."""
    out = []
    for w in range(weeks, -1, -1):
        day = end - dt.timedelta(days=7 * w)
        d, v = _on_or_before(rows, day)
        if d is None or not v or (day - d).days > MAX_GAP_DAYS:
            out.append(None)
            continue
        if fx is not None:
            _, f = _on_or_before(fx, d)
            if not f:
                out.append(None)
                continue
            v = v * f
        out.append(v)
    return out


def drop_weekly_spikes(values):
    """Same idea as drop_bad_prints, for a wrong price that lasted a few days and landed on a weekly point."""
    SPIKE, SETTLE = 0.15, 0.08
    out, dropped = list(values), 0
    for i in range(1, len(values) - 1):
        a, v, b = values[i - 1], values[i], values[i + 1]
        if a and v and b and abs(v / a - 1) > SPIKE and abs(v / b - 1) > SPIKE and abs(b / a - 1) < SETTLE:
            out[i] = None
            dropped += 1
    return out, dropped


def weekly_returns(values):
    return [(b / a - 1) if (a and b) else None for a, b in zip(values, values[1:])]


def pearson(xs, ys):
    """Correlation over the weeks both series have, and how many weeks that was."""
    pairs = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    n = len(pairs)
    if n < MIN_WEEKS:
        return None, n
    mx = sum(x for x, _ in pairs) / n
    my = sum(y for _, y in pairs) / n
    sxx = sum((x - mx) ** 2 for x, _ in pairs)
    syy = sum((y - my) ** 2 for _, y in pairs)
    if sxx <= 0 or syy <= 0:
        return None, n
    sxy = sum((x - mx) * (y - my) for x, y in pairs)
    return sxy / math.sqrt(sxx * syy), n


def build(series: dict, fx, today: dt.date, now_iso: str) -> dict:
    """series maps ticker -> (rows newest first, currency). Raises ValueError if a fund has no prices."""
    missing = [f["ticker"] for f in FUNDS if f["ticker"] not in series]
    if missing:
        raise ValueError("no prices today for " + ", ".join(missing))
    end = window_end(today)
    rets, funds = [], []
    for f in FUNDS:
        rows, ccy = series[f["ticker"]]
        cutoff = end - dt.timedelta(days=7 * WEEKS + 14)
        rows, bad = drop_bad_prints([r for r in rows if r[0] >= cutoff])
        if bad:
            print(f"Correlations: ignored {len(bad)} suspect price(s) for {f['ticker']}: " + ", ".join(d.isoformat() for d in bad))
        if ccy == "USD" and not fx:
            raise ValueError("no USD/GBP exchange rate today")
        vals, spikes = drop_weekly_spikes(weekly_values(rows, fx if ccy == "USD" else None, end))
        if spikes:
            print(f"Correlations: ignored {spikes} suspect weekly price(s) for {f['ticker']}")
        r = weekly_returns(vals)
        rets.append(r)
        if os.environ.get("CORR_DEBUG"):
            print("CORRDBG", f["ticker"], ccy, "missing", sum(1 for x in vals if x is None),
                  " ".join(f"{x:.4g}" if x else "-" for x in vals))
        have = [i for i, x in enumerate(r) if x is not None]
        first = (end - dt.timedelta(days=7 * (WEEKS - have[0]))).isoformat() if have else None
        funds.append({**f, "weeks": len(have), "since": first})
    n = len(FUNDS)
    matrix = [[None] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            if i == j:
                c = 1.0 if funds[i]["weeks"] >= MIN_WEEKS else None
            else:
                c, _ = pearson(rets[i], rets[j])
            v = None if c is None else round(c, 2) + 0.0
            matrix[i][j] = matrix[j][i] = v
    return {
        "updated_at": now_iso,
        "window": {"end": end.isoformat(), "start": (end - dt.timedelta(days=7 * WEEKS)).isoformat(),
                   "weeks": WEEKS, "min_weeks": MIN_WEEKS, "interval": "weekly", "currency": "GBP"},
        "funds": funds,
        "matrix": matrix,
    }


def current_window_end() -> str | None:
    try:
        return json.loads(OUT.read_text())["window"]["end"]
    except Exception:  # noqa: BLE001
        return None


def write(payload: dict) -> None:
    OUT.write_text(json.dumps(payload, indent=1, ensure_ascii=False) + "\n")
