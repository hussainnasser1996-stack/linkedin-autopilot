#!/usr/bin/env python3
"""triage.py <run_id>: called by triage.yml after every "Schedule in Buffer" / "Delivery monitor" run.
Failure: read the failed log, classify it, re-run once if transient, else open an entry in log/failures.json for the
FIXER routine (FIXER.md, every 2 h). Owner-only problems (billing, minutes quota, bad key) get ONE phone alert.
A later green run of the same workflow closes its open entries. Nobody has to report a failure: this is the record.
(Monitor entries are opened and closed by monitor.py itself.) --dry: classify only."""
import datetime as dt, json, re, subprocess, sys, pathlib, urllib.request

R = pathlib.Path(__file__).resolve().parent.parent
F = R / "log/failures.json"
rid = sys.argv[1]; DRY = "--dry" in sys.argv
gh = lambda *a: subprocess.run(["gh", *a], capture_output=True, text=True).stdout
run = json.loads(gh("run", "view", rid, "--json", "conclusion,attempt,url,workflowName"))
wf = run["workflowName"]
db = json.loads(F.read_text()) if F.exists() else []
now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")

if run["conclusion"] == "success":
    for e in db:
        if e["status"] != "resolved" and e["workflow"] == wf:
            e.update(status="resolved", resolved=now, resolved_by=run["url"])
    F.write_text(json.dumps(db, indent=1) + "\n"); sys.exit(0)
if run["conclusion"] != "failure":
    sys.exit(0)

log = gh("run", "view", rid, "--log-failed") or gh("run", "view", rid, "--log")
lines = [re.sub(r"^﻿?\d{4}-\d\d-\d\dT[\d:.]+Z ?", "", l.split("\t")[-1]) for l in log.splitlines()]
lines = [l for l in lines if l.strip() and "\x1b[36;1m" not in l and not l.startswith(("##[group]", "##[endgroup]"))]
err = [l for l in lines if re.search(r"error|fail|exception|traceback|rejected|denied|problem|missing", l, re.I)]
tail = "\n".join(err[-20:] or lines[-20:])[-2500:]
if not log.strip():   # no log at all = the job never started (minutes quota / billing)
    tail = "job did not start (no log): " + gh("api", f"repos/{{owner}}/{{repo}}/actions/runs/{rid}/jobs", "-q",
                                                ".jobs[].steps | length")[:200]
TRANSIENT = r"Could not resolve host|Connection (reset|refused|timed out)|timed? ?out|HTTP Error 5\d\d|\b50[234]\b|Internal Server Error|rate.?limit|429|ECONNRESET|Temporary failure|TLS|non-fast-forward|\[rejected\]|RemoteDisconnected|IncompleteRead"
OWNER = r"spending limit|billing|payments have failed|minutes|BUFFER KEY CHECK FAILED|Unauthorized|401|job did not start"
kind = "owner" if re.search(OWNER, tail, re.I) else "transient" if re.search(TRANSIENT, tail, re.I) else "code"
if wf == "Delivery monitor" and kind == "code":
    kind = "delivery"   # monitor.py already opened the detailed entries; this one points at the run
e = next((x for x in db if x["status"] != "resolved" and x["workflow"] == wf and x.get("kind") == kind), None)
if not e:
    e = {"id": rid, "workflow": wf, "target": "", "kind": kind, "opened": now, "status": "open", "runs": []}
    db.append(e)
e["runs"].append({"run": run["url"], "attempt": run["attempt"], "at": now, "error": tail})
if kind == "transient" and run["attempt"] < 2:
    DRY or subprocess.run(["gh", "run", "rerun", rid, "--failed"]); e["status"] = "retrying"
else:
    e["status"] = "open"
    if kind == "owner" and not e.get("notified") and not DRY:
        topic = json.load(open(R / "config.json"))["ntfy_topic"]
        urllib.request.urlopen(urllib.request.Request(f"https://ntfy.sh/{topic}", method="POST",
            data=f"{wf}: {tail.splitlines()[-1][:200] if tail else 'failed'} ({run['url']})".encode(),
            headers={"Title": "LinkedIn autopilot needs you", "Priority": "high"}), timeout=30)
        e["notified"] = now
DRY or F.write_text(json.dumps(db, indent=1) + "\n")
print(json.dumps({k: e[k] for k in ("workflow", "kind", "status")}), "\n", tail[-600:])
