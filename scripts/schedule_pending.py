#!/usr/bin/env python3
"""Schedule every queued post that Buffer does not have yet (runs in GitHub Actions with the BUFFER_API_KEY secret).

A post is pending when queue/<date>/post.json exists, <date> is today or later (UTC), and queue/<date>/buffer_id.txt
does not. On success it writes buffer_id.txt and appends the id to post.md. Exit code 1 if any post failed.
"""
import datetime as dt, json, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
today = dt.datetime.now(dt.timezone.utc).date().isoformat()
failed = 0
for pj in sorted(ROOT.glob("queue/*/post.json")):
    d = pj.parent
    if d.name < today or (d / "buffer_id.txt").exists():
        continue
    md0 = (d / "post.md").read_text() if (d / "post.md").exists() else ""
    if re.search(r"Buffer post id[^:]*:\s*[0-9a-f]{24}", md0):   # scheduled earlier by the routine itself
        continue
    r = subprocess.run([sys.executable, str(ROOT / "scripts/buffer.py"), "schedule", str(pj)], capture_output=True, text=True)
    try:
        post = json.loads(r.stdout)["post"]
        pid = post["id"]
    except Exception:
        print(f"FAILED {d.name}: {r.stdout[-400:]} {r.stderr[-400:]}"); failed += 1; continue
    (d / "buffer_id.txt").write_text(pid + "\n")
    md = d / "post.md"
    if md.exists():
        md.write_text(md.read_text() + f"\nBuffer post id (scheduled by GitHub Action): {pid} · status {post.get('status')}\n")
    print(f"SCHEDULED {d.name} {pid} {post.get('status')} due {post.get('dueAt')}")
sys.exit(1 if failed else 0)
