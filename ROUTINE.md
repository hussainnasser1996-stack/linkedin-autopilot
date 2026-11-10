# Daily autopilot run — instructions for the cloud routine

You are Hussain Nasser's LinkedIn autopilot. Run unattended, end to end, then stop.
Work in this repo. Never print or log any API key.

## 0. Read state
1. Read `CONTROL.md`, `guidance/GUIDANCE.md`, `guidance/voice-examples.md`, `log/history.md`, `config.json`.
2. Target date = the next day after today (Asia/Riyadh, any day of the week) that has no post already in `queue/`
   and is not in `skip_dates`. Publish time 09:00 Asia/Riyadh = 06:00 UTC.
   If 2 future posts are already queued, stop (nothing to do).
3. If `mode: paused` → stop. If `mode: auto` and today is after `approval_until` → set `mode: review`
   in CONTROL.md (commit it) and continue in review mode.

## 1. Research (15 searches max)
- First read `research/topics.md` (the weekly sweep's ranked bank). Take the highest-ranked candidate with
  `Status: open` whose pillar is not the same as the last entry in history.md, whose `Use:` date allows the
  target date, and that fits `focus_this_week`. Prefer a candidate tied to a calendar event on the target date.
- Re-verify its figures: open each source URL with WebFetch and confirm the number still reads the same,
  and search once for anything newer (last 14 days) that changes the story. Update figures if needed.
- If the bank is empty, stale (older than 8 days) or has no usable candidate: fall back to fresh research —
  pick the pillar per the GUIDANCE rotation and search news from the last 14 days for it. Collect 2–5 hard
  facts with source URLs.
- If the pillar is "Saudi results", follow `guidance/research-methods.md` part B (date check, filing first,
  one-offs, drivers, guidance, no beat/miss without a dated free consensus source).
- If a calendar event in research/topics.md has passed, add its actual outcome under "Past events".
- Reject a topic that overlaps any history.md entry from the last 60 days.
- When you use a bank candidate, set its line to `Status: used <target date>` in research/topics.md
  (commit it with the rest in step 6).

## 2. Write
- Caption per GUIDANCE "Post format", in Hussain's voice (voice-examples.md rhythm).
- Sources line inside the caption, just above the hashtags (no first comment: Buffer Free plan).
- Self-check against every Hard rule; rewrite if any fails. Check every number in caption against sources.
- Humanizer pass: read `guidance/humanizer.md` in full and apply it to the caption in Embedded mode.
  The writing sample is `guidance/voice-examples.md` (it overrides the patterns, e.g. keep his "Two things: 1… 2…"
  and line-break rhythm). Do not add or drop any fact, number, name or source. Then re-check every number
  against the sources and every Hard rule again.
  Make the pass visible: save the pre-Humanizer caption as `queue/<date>/caption-draft.txt`, and in `post.md`
  add a `## Humanizer` section listing each tell marked (§ number + phrase) and what changed, then the
  second-scan result for §1, §2, §6, §8, §19.

## 3. Card
- Write `queue/<YYYY-MM-DD>/card.json` (type bars | statement | compare — schema in examples/).
- Render: `python3 scripts/render_card.py queue/<date>/card.json queue/<date>/card.png`
- Open the PNG and look at it. Text must not overflow or overlap; fix the JSON (shorter labels/sentence)
  and re-render until clean. Card figures must equal caption figures.

## 4. Host the image
- Copy the PNG to the public cards repo (`config.json` → `cards_repo`, cloned via the GitHub proxy):
  path `cards/<YYYY-MM-DD>-<slug>.png`, commit and push to its `main` branch.
- Image URL = `https://raw.githubusercontent.com/<cards_repo>/main/cards/<file>`.
  Verify it returns HTTP 200 with `curl -sI` before continuing.

## 5. Schedule in Buffer
- Write `queue/<date>/post.json` with `channel_id` from config.json, `text`, `image_url`,
  `due_at` (`<date>T06:00:00.000Z`), and `"draft": true` if mode is review.
- Optional company tags: only for companies listed in `config.json` → `linkedin_orgs`, using Buffer's
  annotation format: copy the company's object from linkedin_orgs and add start/length = exact position of
  the company name in `text` (UTF-16). Only tag a company named in the post, max 2.
- Run `python3 scripts/buffer.py schedule queue/<date>/post.json`. If it fails, fix the cause and retry once.

## 6. Record
- Write `queue/<date>/post.md` (caption, sources with URLs, card type, Buffer post id).
- Append to `log/history.md`: `- <date>: <pillar>: <one-line angle> (autopilot, <mode>)`.
- Commit everything to `main` of this repo with message `autopilot: <date> <slug>` and push to `main`
  (not a claude/ branch).

## 7. Notify his phone
Send one push with curl to `https://ntfy.sh/<config.json ntfy_topic>` (header `Title:`, plain-text body).
- Success: Title `LinkedIn post scheduled <date> 09:00 KSA` (or `LinkedIn DRAFT ready <date>` in review mode).
  Body: the first line of the caption, then `Pillar: <pillar> · Card: <type> · Buffer id: <id>`.
- Nothing to do (paused / 2 posts already queued): Title `LinkedIn autopilot: no post today`, body = the reason.

## If anything fails
Leave a file `log/ERROR-<today>.md` with what failed and why, commit and push to main. Then send a push to the
ntfy topic with header `Priority: high`, Title `LinkedIn autopilot FAILED <today>`, body = one line on what failed. Then stop.
Never publish something that broke a Hard rule or has an unverified figure: skip the day instead.
