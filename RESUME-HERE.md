- 23 Nov 2026: GitHub Actions BLOCKED for this private repo until 1 Dec (account's private minutes spent). TEMPORARY Mac
  LaunchAgent com.hussain.linkedin-schedule runs scripts/local_schedule.sh at 06:00/07:30/20:00 local + on load: books
  pending posts with the keychain key, commits buffer_id.txt, ntfy on failure, REMOVES ITSELF on 1 Dec. Log:
  log/local_schedule.log. Only runs while the Mac is awake. 23 Nov Nvidia post moved to 13:20 UTC (missed 09:00 KSA).
# RESUME HERE: LinkedIn autopilot (saved 10 Nov 2026)

## 13 Nov 2026 (night) — END-TO-END CHECK + FIXES
- Cloud routines (env env_01485b9bHjK4NVP9E31BqLLN): daily post 05:00 KSA, engagement 08:00, sweep Sun 04:00, deep dive 1st 06:00 — all enabled, next runs set.
- FOUND: the cloud env's api.buffer.com secret is rejected (401) since the env was recreated. FIX: Buffer scheduling moved to
  GitHub Action `.github/workflows/buffer.yml` (+ scripts/schedule_pending.py): routine pushes queue/<date>/post.json → Action
  schedules with repo secret BUFFER_API_KEY → writes queue/<date>/buffer_id.txt. Daily 06:15 KSA safety-net run. Never re-posts
  (skips buffer_id.txt or a Buffer id already in post.md).
- DONE 13 Nov 17:17Z: repo secret BUFFER_API_KEY set; Action run 43471329787 green with "Buffer key OK" (key checked live every run).
- FOUND + FIXED: render_card.py f-string broke on Python 3.11 (cloud default) — fixed; the Action compiles all scripts on 3.11.
- Mon 16 Nov Acwa Q3 carousel (built by the cloud test) scheduled from the Mac: Buffer 6af7440ff27e6d89214393ab.
- Queue: 14 Unity (scheduled), 15 Savvy (scheduled), 16 Acwa carousel (scheduled), 17 = routine builds on 14 Nov 05:00, 18 Ma'aden video DRAFT (silent).

## 13 Nov 2026 (evening) — formats status
- Newsletter "Gulf Deal Notes" LIVE: https://www.linkedin.com/newsletters/7527033995272978432/ (weekly; tagline "Where Gulf money goes: the deals, funds and results that matter, at home and abroad."). Sunday sweep drafts each issue (SWEEP 4B), he publishes.
- Arabic: style guide guidance/arabic-style.md (write natively, banned translation phrases, Saudi finance glossary). Test v2 = Buffer draft 6af739ca38a1decc74968097 (v3, shortened) (due 30 Dec, not for publishing). He said Arabic needs more work: waiting for his notes on v2. Fridays stay DRAFT (arabic_mode: review).
- Video experiment: Ma'aden Q3 2026 reel, 45 s, his cloned EN voice + captions, figures OCR-verified. Buffer DRAFT 6af73e8a22cd418aa2da5797 (SILENT, no voice — his call) due Wed 18 Nov 09:00 KSA; posts only if he approves. queue/2026-11-18 reserved so the routine skips that day. Voice job: Making Audio/voice-clone/jobs/maaden-reel-2026-11 (say "Mah-ah-den" for Ma'aden).
- Old test drafts still in Buffer: carousel test 6af7106c4f78da1d8ba47de5 (delete after he has seen it).

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
A daily cloud pipeline with no Mac involved. A Claude cloud routine researches the news, writes the post in his voice, renders the card in his house style and schedules it in Buffer. Buffer publishes on LinkedIn at 09:00 KSA, with the first comment and company tags. He steers it from his phone (Buffer app + CONTROL.md). There is a 30-day standing approval (`CONTROL.md` → `approval_until: 2026-12-31`).

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
- Buffer key in Mac Keychain (`security find-generic-password -s buffer-api-key -w`) and as network secret in cloud env "LinkedIn Autopilot" (env_01485b9bHjK4NVP9E31BqLLN since 13 Nov — old env archived; secrets api.buffer.com + api.apify.com, Full network).
- config.json: org 6af2e67f1fcb3809252ef525, channel 6af2e6fd62b70b94b0dffb14. linkedin_orgs still empty (company tags off).
- Claude GitHub app installed on ALL repos.
- Routine trig_01GAp2AkZDTXmm7MptzDUptN, cron `0 2 * * *` UTC = 05:00 KSA daily (switched 10 Nov), Opus 5.5, no connectors: https://claude.ai/code/routines/trig_01GAp2AkZDTXmm7MptzDUptN
- Test run 10 Nov (review mode) PASSED: researched, wrote, rendered card, hosted image, created Buffer draft, committed. Draft deleted after check (queue/2026-11-11 kept as record). Mode back to `auto`; approval_until 2026-12-10.
- First real post: run Wed 11 Nov 05:00 KSA schedules Thu 12 Nov 09:00 KSA.

## Added 10 Nov (later)
- Company tags: Merak Capital (18948009, merakcapital) and Impact46 (13045287, impact-46), verified Riyadh pages; in config.json.
- Humanizer (official blader v3.1.0) in guidance/humanizer.md; routine runs it and must log draft + tells in post.md.
- Phone alerts: ntfy topic `hn-autopilot-ad181bce3712d192` (config.json). ntfy app installed on his OnePlus 8T via adb, subscribed, notifications ON, battery-exempt; test push verified. Routine pushes on success / no-post / failure (high priority). Runs also send a Claude app push.
- Live auto run PASSED 10 Nov: Thu 12 Nov 09:00 post scheduled (Buffer 6af2f24a0f3180d1203e86b0). 11 Nov banks post = Buffer DRAFT 6af2ee60eea2cc573bb58249, needs his tap to publish.

## Added 10 Nov (evening)
- DAILY posting (cron 0 2 * * *). 9 pillars rebuilt from Singular Link deck (Oct 2026) + games + venture building; table in GUIDANCE.md.
- Weekly sweep: routine trig_01KaSruTcfp31EVmJakni97o, Sun 04:00 KSA, SWEEP.md → research/topics.md. Methods in guidance/research-methods.md (catalyst calendar + results read, adapted from Anthropic equity-research).
- Monthly deep dive: routine trig_01Jorz5o1rj8QFoXuPB1rgmC, 1st 06:00 KSA, DEEPDIVE.md → research/deep-dives/ + long post on the 5th.
- Queue now: 11 Nov banks (scheduled), 12 Nov Saudi VC, 13 Nov deep dive "who keeps the margin in AI data centres" (all scheduled, verified).

## Added 12 Nov: daily engagement pack (cloud)
- Routine trig_01AHkHLQzdEBtXDU4Zz7gZzX "LinkedIn Engagement Pack", 05:00 UTC = 08:00 KSA, follows ENGAGE.md. Draft only, pushes to phone (scripts/ntfy_pack.py).
- Connects: 15/day from engage/targets.md (tested OK 12 Nov). Comments + replies on his posts: Apify harvestapi/linkedin-post-search (no cookies) via scripts/apify_posts.py; queries in engage/queries.txt; ~USD 3/month inside Apify free credit.
- WAITING ON HIM: Apify account (free, his own sign-up) -> API token -> Keychain `apify-token` + cloud env "LinkedIn Autopilot" secret APIFY_TOKEN. Until then the pack skips comments.
- Reviewed 10 repos 12 Nov: use linkedin-skills (Apify read idea), li-comment comment types (in ENGAGE.md); skip auto job applier, linkedin-mcp-server, linkedin_scraper, linkedin2username. agent-browser 0.42.0 INSTALLED 12 Nov (+ its own Chrome 157), tested on his site: opens, reads page, screenshots. Use for job portals (e.g. Oracle HCM), never for LinkedIn.
