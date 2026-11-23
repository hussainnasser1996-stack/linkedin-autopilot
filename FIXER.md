# LinkedIn autopilot: failure fixer (Claude cloud routine, every 2 h)

The whole pipeline runs without Hussain's Mac: daily routine (ROUTINE.md) writes `queue/<date>/` 2 days ahead and
pushes → GitHub Action "Schedule in Buffer" books it → Buffer publishes at 09:00 KSA. "Delivery monitor" (every 2 h)
books anything pending and checks today/tomorrow are written, booked and sent. Every failure lands in
`log/failures.json` (via `scripts/triage.py` and `scripts/monitor.py`). Your job: make every open entry green WITHOUT
Hussain having to report it. Hard rules: verify, never assume. Never touch the Mac. Never post anything that breaks
ROUTINE.md / GUIDANCE.md hard rules. Never delete or rename a `buffer_id.txt`. $0 only.

1. `git pull --rebase origin main`. Read `log/failures.json`. Take entries with status `open` (or `retrying` older than
   1 h). None → append one line `- <UTC> no open failures` to `log/fixer.md`, commit, push to main, STOP.
2. For each open entry (oldest first, max 3 per run) find the ROOT CAUSE from `runs[-1].error`, the code and the
   queue files. Check `log/fixer.md`: same cause as an earlier fix → that fix was incomplete, fix it properly now.
3. Fix by kind / problem:
   - `missing` (no queue folder for today/tomorrow): run ROUTINE.md end to end with that date as the target date
     (it writes the post and pushes; the Action books it). If today's 09:00 KSA slot has already passed, set
     `due_at` to the next full quarter-hour at least 20 minutes from now (UTC) instead of 06:00.
   - `unbooked`: commit an empty `queue/<date>/retry` file to main (triggers "Schedule in Buffer"). If it still fails,
     read the run log (`gh run view <id> --log-failed` if gh works; otherwise the error in failures.json) and fix
     post.json or scripts/ (often: due_at in the past → move it as above; image URL not 200 → re-host the card per
     ROUTINE.md step 4). Then commit `retry` again.
   - `not-sent` / `buffer` (Buffer error or post vanished): if the post is still within 12 h of its slot, move the
     date's `buffer_id.txt` content into `post.md` as `Old Buffer id: <id> (<status>)`, delete buffer_id.txt ONLY in
     this case, set a new future `due_at`, commit `retry`. Older than 12 h → set entry `status: "stale"` with reason.
   - `code`: fix the script on main, but only after `python3 -m py_compile scripts/*.py` passes and the change is
     checked with `BUFFER_API_KEY` absent (dry logic only). Then commit `retry` for the affected date.
   - `transient` that failed twice: commit `retry` once more; fails again → treat as `code`.
   - `owner` (billing, Actions minutes, Buffer key 401, LinkedIn disconnected in Buffer): you cannot fix it. Make sure
     ONE alert went out (`notified` set; if not, send it to ntfy as in ROUTINE.md step 7 with Priority high), write the
     exact click he needs in `log/fixer.md`, set `status: "owner"`.
4. Set the entry `status: "fixing"`, `fix: "<what you changed, commit>"`, push. The next green run of that workflow
   (or a clean monitor check) closes it; verify on your next run that it did.
5. Append to `log/fixer.md`: time, entry, cause, fix, result. Push to main. If the same entry is still open after 3 of
   your attempts, send ONE high ntfy push "<what's stuck and why>" and keep trying.
