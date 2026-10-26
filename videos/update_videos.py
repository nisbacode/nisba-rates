"""Write the latest Nisba YouTube uploads to docs/videos.json.

Uses the YouTube Data API v3 (secret YOUTUBE_API_KEY, free quota is plenty:
this uses about 3 units a day). The newsletter task reads docs/videos.json
from raw.githubusercontent.com, the same way the funds page reads funds.json.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "videos.json"

CHANNEL_ID = "UC6krRYvoFZfzV_3_wEY9A4w"  # youtube.com/@nisbainvest
KEY = os.environ.get("YOUTUBE_API_KEY", "").strip()
MAX_VIDEOS = 30


def api(path: str, params: dict) -> dict:
    r = requests.get(
        f"https://www.googleapis.com/youtube/v3/{path}",
        params={**params, "key": KEY},
        timeout=40,
    )
    r.raise_for_status()
    return r.json()


def main() -> int:
    if not KEY:
        print("YOUTUBE_API_KEY is not set", file=sys.stderr)
        return 1

    # Every channel has an "uploads" playlist; listing it costs 1 unit per page.
    ch = api("channels", {"part": "contentDetails", "id": CHANNEL_ID})
    uploads = ch["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    pl = api(
        "playlistItems",
        {"part": "snippet,contentDetails", "playlistId": uploads, "maxResults": MAX_VIDEOS},
    )
    ids = [it["contentDetails"]["videoId"] for it in pl.get("items", [])]

    # One more call to get durations, so Shorts can be told apart from videos.
    details = api("videos", {"part": "contentDetails,snippet", "id": ",".join(ids)}) if ids else {"items": []}
    by_id = {v["id"]: v for v in details.get("items", [])}

    videos = []
    for vid in ids:
        v = by_id.get(vid)
        if not v:
            continue
        sn = v["snippet"]
        duration = v["contentDetails"].get("duration", "")
        videos.append(
            {
                "id": vid,
                "title": sn["title"],
                "published_at": sn["publishedAt"],
                "url": f"https://www.youtube.com/watch?v={vid}",
                "duration": duration,
                "is_short": _seconds(duration) <= 180 and "#shorts" in sn.get("description", "").lower()
                or _seconds(duration) <= 60,
                "thumbnail": (sn.get("thumbnails", {}).get("high") or sn.get("thumbnails", {}).get("default") or {}).get("url"),
                "description": sn.get("description", "")[:300],
            }
        )

    OUT.write_text(
        json.dumps(
            {
                "checked_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                "channel": "https://www.youtube.com/@nisbainvest",
                "videos": videos,
            },
            indent=1,
        )
        + "\n"
    )
    print(f"wrote {len(videos)} videos to {OUT.relative_to(ROOT)}")
    return 0


def _seconds(iso: str) -> int:
    """ISO 8601 duration like PT1H2M3S to seconds."""
    if not iso.startswith("PT"):
        return 0
    total, num = 0, ""
    for c in iso[2:]:
        if c.isdigit():
            num += c
        else:
            total += int(num or 0) * {"H": 3600, "M": 60, "S": 1}.get(c, 0)
            num = ""
    return total


if __name__ == "__main__":
    sys.exit(main())
