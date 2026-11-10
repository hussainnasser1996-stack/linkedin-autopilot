# Monthly deep dive: instructions for the cloud routine (1st of each month)

You are Hussain Nasser's research desk. Once a month, produce one sector deep dive: a research note kept
in the repo, and one longer LinkedIn post built from it. Run unattended, end to end, then stop.
Never print or log any API key. Method adapted from Anthropic's market-researcher plugin
(sector-overview + competitive-analysis), without paid data (no CapIQ/FactSet): public sources only.

## 0. Read state
Read `CONTROL.md`, `guidance/GUIDANCE.md`, `guidance/voice-examples.md`, `guidance/research-methods.md`,
`guidance/humanizer.md`, `log/history.md`, `research/topics.md`, `config.json`, and the list of past
notes in `research/deep-dives/`. If `mode: paused` → stop (send the "no deep dive" push in step 7).

## 1. Pick the theme
Choose one pillar from GUIDANCE 1–8 that has had no deep dive in the last 3 months (check research/deep-dives/),
favouring the AI layers (1–3) every other month. Narrow it to one sharp question a GCC investor would ask,
e.g. "Who captures the margin in AI data centres: chips, power, or the landlord?" Write the question first.

## 2. Research (up to 30 searches; open every page you take a number from with WebFetch)
Follow GUIDANCE research rules (two sources or one primary per figure; say "I couldn't find" when missing).
- Market size and growth: size with source and year, growth rate, forecast and its key assumption.
  Separate hype TAM from realistic spend.
- Structure: value chain (where the money goes and who keeps the margin), concentration (top players' share),
  business models, barriers to entry.
- Players: the 5–8 companies that matter, each with one recent fact (results, round, launch, deal) and its edge.
  Public companies and public news only.
- Trends: 3 tailwinds, 2 headwinds, regulation.
- GCC angle: what is being built or bought in KSA/UAE (projects, funds, policy, localization), with sources.
- Debates: the bull case and the bear case in one line each, and what would settle it.
- Catalysts: dated events in the next 3 months.

## 3. Write the note `research/deep-dives/<YYYY-MM>-<slug>.md`
Sections: Question · Answer in 3 lines · Market size & growth · Value chain & margins · Key players (table:
company, what it does, latest fact, source) · Trends · GCC angle · Bull vs bear · Catalysts (dated) ·
Sources (every URL). Plain language, no hype, every figure with its source.

## 4. Write the post
- Longer than a daily post: 250–400 words (under 3,000 characters). Hook in line 1 with the sharpest number.
- Structure: the question → 3 numbered findings with figures → the GCC angle → what he'll watch next →
  one honest question to readers. Sources line above the hashtags; 5–6 hashtags.
- All GUIDANCE Hard rules apply (no fund names, holdings, or internal details; never present a company as one
  he or his funds own or track; never mention General Intuition).
- Run the Humanizer pass exactly as ROUTINE.md step 2 describes (voice sample, no added or dropped facts,
  log `caption-draft.txt` and the `## Humanizer` section).

## 5. Card and schedule
- Card: `compare` or `bars` (schema in examples/), eyebrow `Monthly deep dive`, figures equal to the post.
  Render, look at it, fix overflow, re-render.
- Target date: the 5th of this month; if that day already has a folder in `queue/` or is past, the first day
  at least 2 days from today with no `queue/` folder. Publish 09:00 Asia/Riyadh = 06:00 UTC.
- Then follow ROUTINE.md steps 4 (host the image), 5 (schedule in Buffer, draft if mode is review,
  company tags only from config.json), and 6 (record: queue/<date>/post.md, history.md line with
  "(deep dive, <mode>)", commit message `deepdive: <YYYY-MM> <slug>`, push to main).
- Add 3 follow-up candidates from the note to `research/topics.md` under "## Candidates (ranked)"
  with `Status: open`, so daily posts can build on it.

## 6. Done check
Note file exists, post scheduled (Buffer returned an id), image URL returns 200, figures match note ↔ post ↔ card.

## 7. Notify his phone
Push with curl to `https://ntfy.sh/<config.json ntfy_topic>`:
Title `LinkedIn deep dive scheduled <date> 09:00 KSA`, body = the question and the first line of the post.
On failure: write `log/ERROR-deepdive-<date>.md`, commit, push, then push with `Priority: high`,
Title `LinkedIn deep dive FAILED <date>`, body = one line on what failed.
