<!-- Adapted for LinkedIn posts from Anthropic's financial-services plugins (equity-research: catalyst-calendar
and earnings-analysis, v0.1.2). Paid-data parts (FactSet/Bloomberg consensus, positioning) removed: we use
free public sources only. -->

# Research methods (read by SWEEP.md and ROUTINE.md)

## A. Catalyst calendar (weekly sweep, step 1)

### Coverage universe
- Listed (Tadawul and GCC): Aramco, SABIC, Ma'aden, ACWA Power, stc, Mobily, Al Rajhi, SNB, Alinma, Riyad Bank,
  SAB, Bahri, Elm, Savola, Almarai, Jarir, Dr. Sulaiman Al Habib, Emaar, ADNOC companies, e&, First Abu Dhabi Bank.
- Private and state: PIF, HUMAIN, Savvy Games (Scopely, ESL FACEIT), Qiddiya, NEOM, Red Sea Global, SVC, Jada,
  Sanabil, STV, Merak Capital, Impact46, Raed, BECO.
- Data publishers: MAGNiTT, Wamda, Dealroom, SAMA, GASTAT, Tadawul monthly reports, PocketGamer.biz/Newzoo.

### Event types to search for (every sweep, cover each type)
1. Earnings and financial: results release dates, AGMs and EGMs, dividend record and payment dates, rights issues,
   IPO subscription and listing dates, sukuk and bond issues.
2. Corporate: product or data-centre launches, contract awards, M&A closes and regulatory approvals,
   management changes, lock-up expiries.
3. Industry: conferences (LEAP, FII, Biban, GITEX, Saudi Games/Esports World Cup, Gamescom/GDC-type),
   which companies present there, trade shows, regulator consultations, monthly or quarterly data releases.
4. Macro: SAMA rate decisions (follow the Fed), GASTAT GDP, CPI and PMI, OPEC+ meetings, budget statements.

### Rules
- List an event only when a source gives the date. Verify results dates on the company's IR page or the
  Tadawul announcements page; dates shift.
- Rate impact for his audience: H = market-moving for Saudi/GCC investors or his pillars, M = sector-relevant,
  L = routine. Keep H and M only.
- Recurring releases (MAGNiTT quarterly, Tadawul monthly, SAMA monthly) go in every week they fall in.
- Archive: when an event passes, the daily run notes the actual outcome in research/topics.md, which builds
  pattern recognition ("ACWA beat its own guidance three quarters running").

Calendar line format in research/topics.md:
`- <YYYY-MM-DD>: <event> · <company/sector> · <Earnings|Corporate|Industry|Macro> · Impact <H|M> — <source URL>`

## B. Results read ("Saudi results, in motion" posts)

1. Date check first: write today's date and the release date. The release must be from the latest reporting
   period (within the last 3 months). Never use figures from memory; search and open the filing.
2. Sources, in this order: the Tadawul (or ADX/DFM) announcement, the company's results press release or
   investor presentation, then the earnings-call transcript if one exists, then Argaam, Arab News or Reuters
   for confirmation.
3. What to pull:
   - The headline: net profit or revenue, quarter and year to date, versus the same quarter last year and the
     previous quarter.
   - One-offs: gains or losses, impairments, zakat or tax lines, disposals. Report profit with and without them
     when they matter ("adjusted, it's +9%, not +35%").
   - Drivers: segments, volumes versus prices, margins (gross, operating), provisions or cost of risk for banks.
   - Guidance or outlook changes, quoted from the company, compared with prior guidance.
   - Consensus: use it only if a free source names it with a date (Argaam, Reuters). Otherwise don't say
     "beat" or "miss"; compare with last year and the prior quarter instead.
4. The post's "so what" is what is new and what an investor should watch next, not company background.
5. The card shows the 3–5 numbers that carry the story (bars or compare), each with a source in post.md.
