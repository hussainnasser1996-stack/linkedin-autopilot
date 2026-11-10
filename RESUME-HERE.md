# RESUME HERE: LinkedIn autopilot (saved 10 Nov 2026)

## Hussain's absolute rules (apply in every session)
Copied from `~/Developer/Personal Business/Fixing My Problems/Gaming & PC/CLAUDE.md`:
1. His rules ("don't", "never", "only", "hard rule") bind the whole session, word for word.
2. Don't reinterpret them, look for loopholes, or decide one doesn't apply.
3. Do exactly what he asked. Nothing extra, nothing less.
4. Don't ask questions, give warnings, opinions or advice, or push back. Just do it.
5. Don't research anything he said not to.
6. Check every action against his rules first.
7. Do everything fully, start to finish. Never stop halfway.
8. Never say something is done until it's tested and works.
9. Short replies only. Results, nothing else.
10. Read every script, command and file in full before executing it.

## Goal
A daily cloud pipeline with no Mac involved. A Claude cloud routine researches the news, writes the post in his voice, renders the card in his house style and schedules it in Buffer. Buffer publishes on LinkedIn at 09:00 KSA, with the first comment and company tags. He steers it from his phone (Buffer app + CONTROL.md). There is a 30-day standing approval (`CONTROL.md` → `approval_until: 2026-12-10`).

## Done
- Research finished. Chosen design: Claude cloud scheduled task + Buffer API. The LinkedIn API was rejected because its self-serve access can't post comments and makes you log in again every 60 days.
- Local repo `~/Developer/linkedin-autopilot` (git, 2 commits, NOT pushed):
  - `ROUTINE.md`: the routine's step-by-step instructions.
  - `CONTROL.md`: mode auto / review / paused, focus, skip dates.
  - `guidance/GUIDANCE.md`: pillars, rules, format, hashtags.
  - `guidance/voice-examples.md`: 5 of his posts.
  - `log/history.md`: 23 past topics.
  - `scripts/render_card.py`: card types bars / statement / compare. TESTED; output matches the house style. Inter fonts are bundled in `templates/fonts`.
  - `scripts/buffer.py`: GraphQL client for createPost with customScheduled + dueAt, `metadata.linkedin.firstComment`, annotations (company tags), saveToDraft (review mode) and aiAssisted. Not yet tested against the live API.
  - `config.json`: `channel_id` and `buffer_organization_id` are still TODO. Channel id = **6af2e6fd62b70b94b0dffb14** (Hussain Nasser LinkedIn). Get the organization id with `python3 scripts/buffer.py orgs`.
- Local repo `~/Developer/linkedin-cards` (public image host for Buffer; git, NOT pushed).
- Buffer account: hussainnasser.bahrain@gmail.com, email verified, LinkedIn profile connected, time zone Bahrain. Still on the **Free plan**.
- Buffer API key "LinkedIn Autopilot" created (1 year, posts read/write, account/insights/engagements read). The value was shown once to Hussain. It is NOT stored anywhere by Claude.

## LIVE (10 Nov 2026)
- Buffer Free plan (no upgrade). Sources go in the post above the hashtags; no first comment.
- Buffer key in Mac Keychain (`security find-generic-password -s buffer-api-key -w`) and as network secret in cloud env "LinkedIn Autopilot" (env_01KxKYZEnh5kCRNDjGJYebt1, Full network).
- config.json: org 6af2e67f1fcb3809252ef525, channel 6af2e6fd62b70b94b0dffb14. linkedin_orgs still empty (company tags off).
- Claude GitHub app installed on ALL repos.
- Routine trig_01GAp2AkZDTXmm7MptzDUptN, cron `0 2 * * 0-4` UTC = 05:00 KSA Sun–Thu, Opus 5.5, no connectors: https://claude.ai/code/routines/trig_01GAp2AkZDTXmm7MptzDUptN
- Test run 10 Nov (review mode) PASSED: researched, wrote, rendered card, hosted image, created Buffer draft, committed. Draft deleted after check (queue/2026-11-11 kept as record). Mode back to `auto`; approval_until 2026-12-10.
- First real post: run Wed 11 Nov 05:00 KSA schedules Thu 12 Nov 09:00 KSA.
