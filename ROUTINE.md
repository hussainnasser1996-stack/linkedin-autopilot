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

## Format by weekday (target date, Asia/Riyadh)
| Day | Format | How |
|---|---|---|
| Sun | card | as below (the Sunday sweep also drafts the weekly newsletter issue) |
| Mon | **carousel** | PDF document post, 6-8 slides (step 3B) |
| Tue | card | as below |
| Wed | card | (video is a separate experiment made on the Mac, always SILENT with on-screen captions, no voice; skip Wed only if `queue/<date>/` already exists) |
| Thu | **carousel** | PDF document post, 6-8 slides (step 3B) |
| Fri | **Arabic** | Arabic caption + Arabic card (`"lang": "ar"`), step 3C. Saved as a Buffer DRAFT while CONTROL.md `arabic_mode: review` |
| Sat | **poll** | Buffer cannot post polls: write `queue/<date>/poll.md` only (step 3D), no Buffer call |
If `queue/<date>/` already exists for the target date (made by hand), treat that date as taken and move on.

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
- Sensitivity check (read the caption and card as a GCC government official would): anything that could read as criticism of a
  GCC state body, ruler or sovereign fund, any geopolitics/conflict, anything that blames or mocks a person or company → remove it,
  or skip the day. Simplicity check: 80-150 words, one idea, max 2 points; cut anything a busy reader doesn't need.
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


## 3B. Carousel (Mon, Thu) instead of the card
- Write `queue/<date>/carousel.json` (schema in `scripts/render_carousel.py` docstring, example `examples/carousel.json`):
  cover (dark) → 1 slide per key number (stat/bars) → points (max 4, one idea each) → end (dark: what you'll watch + the question).
  6-8 slides. One idea per slide, short lines; every figure must match the caption and the sources.
- Render: `python3 scripts/render_carousel.py queue/<date>/carousel.json queue/<date>/` → carousel.pdf + cover.png.
  Open cover.png and render 2-3 inner pages to PNG (PyMuPDF if available, else Chrome screenshot) and look at them;
  fix overflow and re-render. Caption: same rules, but end the hook with a reason to swipe; keep it shorter (the slides carry the detail).
- Host: copy carousel.pdf to the cards repo `docs/<date>-<slug>.pdf` and cover.png to `cards/<date>-<slug>-cover.png`; push; check both URLs return 200.
- post.json: `document_url`, `document_title` (max 58 chars), `thumbnail_url` (the cover) instead of `image_url`.

## 3C. Arabic (Fri)
- FIRST read `guidance/arabic-style.md` and follow it fully (write in Arabic from the facts, never translate an English draft; banned translation phrases; glossary; final check).
- Same research and fact rules. Write the caption in clear Modern Standard Arabic as a Saudi finance professional would write it on
  LinkedIn: short lines, plain words, no flowery phrases, no religious openers, Western digits (2026, 56%), company names in their usual
  form (Latin names like MAGNiTT stay Latin). Keep his structure: hook number → list → "أمران ألاحظهما:" style points → one question.
  Hashtags: 2 Arabic + 1-2 English. No harakat. Then the humanizer pass, applied to Arabic (cut filler, inflated words, triads).
- Card: same JSON with `"lang": "ar"` (all text in Arabic, sources may stay Latin). Render and look at it.
- If CONTROL.md `arabic_mode: review` (default) → post.json `"draft": true` even when mode is auto. Push title says "Arabic DRAFT".

## 3D. Poll (Sat)
- Write `queue/<date>/poll.md`: an intro text (2-4 short lines with the one fact that sets it up + source), the question
  (max 140 chars), 2-4 options (max 30 chars each), duration 1 week. Options must be neutral and mutually exclusive, never about a government, policy or country comparison; no option that
  needs a figure we can't source. Humanizer pass on the intro.
- No Buffer call. Commit, then push to the phone: Title `LinkedIn POLL ready <date>`, body = intro, question and options exactly as
  they should be pasted. (The Mac session or Hussain posts it at 09:00.)

## 4. Host the image (card days)
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
