#!/bin/zsh
# TEMPORARY (23 Nov - 1 Dec 2026): GitHub Actions for this private repo are blocked until the private-minutes reset on
# 1 Dec, so this Mac LaunchAgent (com.hussain.linkedin-schedule) books pending posts instead. Removes itself on 1 Dec.
cd ~/Developer/linkedin-autopilot || exit 1
L=log/local_schedule.log; mkdir -p log
if [[ "$(date -u +%F)" > "2026-11-30" ]]; then
  echo "$(date -u +%FT%TZ) 1 Dec: Actions are back, removing the LaunchAgent" >> $L
  /Users/hussainnasser/.local/gh/bin/gh workflow enable buffer.yml >> $L 2>&1   # re-enable the GitHub job (disabled 23 Nov so it stops emailing failures)
  rm -f ~/Library/LaunchAgents/com.hussain.linkedin-schedule.plist
  launchctl bootout gui/$(id -u)/com.hussain.linkedin-schedule 2>/dev/null; exit 0
fi
git pull -q --rebase --autostash >> $L 2>&1
export BUFFER_API_KEY="$(security find-generic-password -s buffer-api-key -w)"
echo "$(date -u +%FT%TZ) run" >> $L
/usr/bin/python3 scripts/schedule_pending.py >> $L 2>&1; rc=$?
git add queue && git commit -qm "buffer: scheduled $(date -u +%F) (Mac LaunchAgent, Actions blocked until 1 Dec)" >> $L 2>&1 && git push -q >> $L 2>&1
[ $rc = 0 ] || curl -s -H "Priority: high" -H "Title: LinkedIn - Buffer scheduling FAILED (Mac job)" -d "See ~/Developer/linkedin-autopilot/log/local_schedule.log" "https://ntfy.sh/$(python3 -c "import json;print(json.load(open('config.json'))['ntfy_topic'])")" > /dev/null
exit $rc
