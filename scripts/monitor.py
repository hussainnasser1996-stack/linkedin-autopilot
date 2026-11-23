#!/usr/bin/env python3
"""Delivery monitor (GitHub Actions, every 2 h). Checks that every LinkedIn post is written, booked and published:
- today and tomorrow (Asia/Riyadh) must have a queue folder (post, poll or hand-made), unless in CONTROL.md skip_dates;
- every post.json from today on must have a buffer_id.txt (schedule_pending.py runs just before this and books it);
- each booked post must be in Buffer with the right status: scheduled/draft before 09:00 KSA, sent after 09:20 KSA.
Problems go to log/failures.json (one open entry per date + problem) and the run fails, so triage.yml and the
FIXER routine pick them up. A clean check closes earlier monitor entries. Appends one line to log/delivery.md.
--dry prints only."""
import datetime as dt, json, os, pathlib, re, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
DRY = "--dry" in sys.argv
now = dt.datetime.now(dt.timezone.utc)
ksa = now + dt.timedelta(hours=3)
today = ksa.date()
ctrl = (ROOT / "CONTROL.md").read_text()
skips = set(re.findall(r"\d{4}-\d{2}-\d{2}", ctrl.split("skip_dates:", 1)[1])) if "skip_dates:" in ctrl else set()
paused = re.search(r"^mode:\s*paused", ctrl, re.M)


def status(pid):
    q = 'query($i: PostId!){ post(input:{id:$i}){ status dueAt sentAt } }'
    req = urllib.request.Request("https://api.buffer.com", method="POST",
        data=json.dumps({"query": q, "variables": {"i": pid}}).encode(),
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + os.environ["BUFFER_API_KEY"]})
    with urllib.request.urlopen(req, timeout=60) as r:
        b = json.loads(r.read())
    if b.get("errors"):
        return {"status": "MISSING IN BUFFER: " + b["errors"][0].get("message", "")[:120]}
    return b["data"]["post"]


problems, ok = [], []
for off in (0, 1, 2):
    d = (today + dt.timedelta(days=off)).isoformat()
    q = ROOT / "queue" / d
    if d in skips or paused:
        ok.append(f"{d} skipped"); continue
    if not q.is_dir():
        if off <= 1:   # the routine writes each post 2 days ahead, so today and tomorrow must exist
            problems.append((d, "missing", f"no queue/{d} folder: the daily routine did not write this post"))
        continue
    pj, bid = q / "post.json", q / "buffer_id.txt"
    if not pj.exists() and not bid.exists():
        ok.append(f"{d} no Buffer post ({', '.join(sorted(p.name for p in q.iterdir()))})"); continue   # poll day / hand-made
    if not bid.exists():
        problems.append((d, "unbooked", f"queue/{d}/post.json is not booked in Buffer (no buffer_id.txt)")); continue
    pid = bid.read_text().strip()
    p = status(pid)
    st = p.get("status", "")
    draft = pj.exists() and json.loads(pj.read_text()).get("draft")
    due_passed = off == 0 and ksa.time() >= dt.time(9, 20)
    if st.startswith("MISSING") or st == "error":
        problems.append((d, "buffer", f"Buffer post {pid}: {st}"))
    elif due_passed and not draft and st != "sent":
        problems.append((d, "not-sent", f"Buffer post {pid} should have published at 09:00 KSA but status is '{st}'"))
    elif not due_passed and st not in ("scheduled", "draft", "sent", "sending"):
        problems.append((d, "buffer", f"Buffer post {pid} has unexpected status '{st}'"))
    else:
        ok.append(f"{d} {st}" + (f" {p.get('sentAt','')}" if st == "sent" else ""))

stamp = now.strftime("%Y-%m-%dT%H:%MZ")
line = f"- {stamp}: " + ("; ".join(ok) or "-") + ("" if not problems else " | PROBLEMS: " + "; ".join(f"{d} {k}" for d, k, _ in problems))
print(line)
for d, k, m in problems:
    print(f"PROBLEM target: {d} kind: {k} :: {m}")
if DRY:
    sys.exit(1 if problems else 0)
(ROOT / "log").mkdir(exist_ok=True)
with open(ROOT / "log/delivery.md", "a") as f:
    f.write(line + "\n")
F = ROOT / "log/failures.json"
db = json.loads(F.read_text()) if F.exists() else []
keys = {(d, k) for d, k, _ in problems}
for e in db:   # close monitor entries that are fine now
    if e["workflow"] == "monitor" and e["status"] != "resolved" and (e["target"], e["problem"]) not in keys:
        e.update(status="resolved", resolved=stamp, resolved_by="monitor check green")
for d, k, m in problems:
    e = next((x for x in db if x["workflow"] == "monitor" and x["status"] != "resolved" and x["target"] == d and x["problem"] == k), None)
    if not e:
        e = {"id": f"mon-{d}-{k}", "workflow": "monitor", "target": d, "problem": k, "kind": "delivery",
             "opened": stamp, "status": "open", "runs": []}
        db.append(e)
    e["runs"].append({"at": stamp, "error": m, "run": os.environ.get("RUN_URL", "")})
F.write_text(json.dumps(db, indent=1) + "\n")
sys.exit(1 if problems else 0)
