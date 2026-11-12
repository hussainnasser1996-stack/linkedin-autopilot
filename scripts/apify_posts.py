#!/usr/bin/env python3
"""Find fresh LinkedIn posts for the engagement pack via Apify (no cookies: his LinkedIn login is never used).

Actor: harvestapi/linkedin-post-search (pay per result, ~USD 0.002/post; budget kept inside Apify's free monthly credit).
Token: env APIFY_TOKEN, or macOS Keychain service "apify-token". Never printed.

Usage:
  apify_posts.py search  [--max 12]   -> engage/candidates-<date>.json  (keyword queries from engage/queries.txt, last 24h)
  apify_posts.py mine                 -> engage/mine-<date>.json        (his posts from the last 3 days + their comments)
"""
import datetime as dt, json, os, subprocess, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ACTOR = "harvestapi~linkedin-post-search"
HIS_PROFILE = "https://www.linkedin.com/in/hussain-nasser-8b3a4917b"
TODAY = dt.datetime.now(dt.timezone(dt.timedelta(hours=3))).date().isoformat()


def token():
    t = os.environ.get("APIFY_TOKEN")
    if not t:
        try:
            t = subprocess.run(["security", "find-generic-password", "-s", "apify-token", "-w"],
                               capture_output=True, text=True).stdout.strip()
        except FileNotFoundError:
            t = ""
    if not t:
        sys.exit("APIFY_TOKEN missing (env or Keychain 'apify-token')")
    return t


def run(inp, timeout=280):
    url = f"https://api.apify.com/v2/acts/{ACTOR}/run-sync-get-dataset-items?timeout={timeout}"
    req = urllib.request.Request(url, data=json.dumps(inp).encode(), method="POST",
                                 headers={"Content-Type": "application/json", "Authorization": f"Bearer {token()}"})
    with urllib.request.urlopen(req, timeout=timeout + 30) as r:
        return json.loads(r.read())


def slim(p):
    a = p.get("author") or {}
    return {"url": p.get("linkedinUrl") or p.get("url") or p.get("postUrl"),
            "author": a.get("name") or p.get("authorName"),
            "headline": (a.get("info") or a.get("position") or a.get("headline") or "")[:140],
            "posted": (p.get("postedAt") or {}).get("date") if isinstance(p.get("postedAt"), dict) else p.get("postedAt"),
            "text": (p.get("content") or p.get("text") or "")[:1500],
            "comments": [{"author": (c.get("actor") or c.get("author") or {}).get("name"),
                          "text": (c.get("commentary") or c.get("text") or "")[:500]}
                         for c in (p.get("comments") or [])]}


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "search"
    mx = int(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 12
    out_dir = ROOT / "engage"; out_dir.mkdir(exist_ok=True)
    if cmd == "search":
        qs = [q.strip() for q in (ROOT / "engage" / "queries.txt").read_text().splitlines() if q.strip() and not q.startswith("#")]
        items = run({"searchQueries": qs, "maxPosts": mx, "postedLimit": "24h", "sortBy": "relevance",
                     "profileScraperMode": "short", "scrapeComments": False, "scrapeReactions": False})
        path = out_dir / f"candidates-{TODAY}.json"
    elif cmd == "mine":
        items = run({"authorUrls": [HIS_PROFILE], "maxPosts": 3, "postedLimit": "week", "sortBy": "date",
                     "scrapeComments": True, "maxComments": 20, "commentsPostedLimit": "week",
                     "postNestedComments": True, "scrapeReactions": False})
        path = out_dir / f"mine-{TODAY}.json"
    else:
        sys.exit(__doc__)
    data = [slim(p) for p in items if isinstance(p, dict) and (p.get("type") in (None, "post"))]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1))
    print(f"{cmd}: {len(data)} posts -> {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
