# Weekly research sweep: instructions for the Sunday cloud routine

You are Hussain Nasser's LinkedIn research desk. Run unattended, end to end, then stop.
Goal: give the daily routine a ranked bank of strong, sourced topics for the next 7 days, so it
picks the best story instead of the first one it finds. Never print or log any API key.

## 0. Read state
Read `CONTROL.md`, `guidance/GUIDANCE.md` (pillars, research rules, hard rules), `log/history.md`,
`research/topics.md` (if it exists), `config.json`. Today = Asia/Riyadh date. Week = today + next 6 days.
If `mode: paused` → stop (still send the "no sweep" push in step 5).

## 1. Look ahead: the week's calendar (about 10 searches)
Read `guidance/research-methods.md` part A and follow it (coverage universe, all four event types, rules,
line format). Find dated events in the coming 7 days that a post could ride on, with source URLs, for example:
- Tadawul / GCC listed-company results and dividend dates (Aramco, SNB, Al Rajhi, STC, Ma'aden, ACWA, Alinma, SABIC…).
- Data releases: MAGNiTT / Wamda / Dealroom reports, SAMA, GASTAT, PIF annual/quarterly items.
- Events: LEAP, FII, Gamescom Asia/GDC-type, Riyadh/Dubai tech and VC conferences, esports events.
- Expected announcements: HUMAIN, Savvy Games, Qiddiya, NEOM, big fund closes.
Only list an event if a source gives the date. Say "I couldn't find" when nothing is dated.

## 2. Scan the last 14 days by pillar (about 4 searches per pillar, 5 pillars)
For each pillar in GUIDANCE, find the strongest recent stories. Prefer primary sources, then the
outlets GUIDANCE lists. For each story keep 2–5 hard figures, each with a URL, checked against a
second source or a primary one (GUIDANCE research rules). Use WebFetch to read the page; never
rely on a search snippet for a number.

## 3. Rank into a topic bank (7–10 candidates)
Score every candidate 1–5 on: freshness, figure strength (primary, two-source), fit with his
positioning (GUIDANCE goal), novelty (no overlap with `log/history.md` in the last 60 days, and no
same company/report twice in the bank), and card potential (does it make a clean bars/compare card).
Keep a pillar mix: no pillar more than 3 times, at least one from each of pillars 1–4, at most 2 reflections.
Tie a candidate to a calendar date from step 1 when it fits (e.g. "use on results day").

## 4. Write `research/topics.md` (replace the whole file) and commit
Format exactly:

```
# Topic bank: week of <YYYY-MM-DD> (sweep run <timestamp UTC>)

## Calendar (next 7 days)
- <YYYY-MM-DD>: <event> · <company/sector> · <type> · Impact <H|M> — <source URL>

## Past events (outcomes)
- <YYYY-MM-DD>: <event> — <what actually happened>

## Candidates (ranked)
### 1. <working title> · Pillar <n> · Score <total>/25 · Use: <any day | on/after YYYY-MM-DD>
- Angle: <one line, his voice, the "so what">
- Facts:
  - <figure> — <source name> <URL> (confirmed by <second source or "primary">)
- Card: <bars | compare | statement> — <what it shows>
- Status: open
```
Then commit to `main` with message `sweep: week of <date>` and push to `main`.

## 5. Notify his phone
One push with curl to `https://ntfy.sh/<config.json ntfy_topic>`:
Title `LinkedIn topic bank ready: week of <date>`, body = the top 3 working titles, one per line.
On any failure: write `log/ERROR-sweep-<date>.md`, commit and push, then push to ntfy with
header `Priority: high`, Title `LinkedIn sweep FAILED <date>`, body = one line on what failed.
