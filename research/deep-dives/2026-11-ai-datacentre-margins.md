# Who keeps the margin in AI data centres: the chipmaker, the GPU cloud, or the landlord?

Monthly deep dive · 2026-11 · Pillar 2 (Data centres & power for AI) · Written 2026-11-10

## Question
Who keeps the margin in AI data centres: the chipmaker, the GPU cloud, or the landlord? And where does a Gulf builder like HUMAIN sit in that chain?

## Answer in 3 lines
1. The chip layer keeps most of it: Nvidia turned 66% of revenue into operating profit in its latest quarter (75.0% gross margin).
2. The landlord earns a steady, utility-like margin (Equinix: 51% adjusted EBITDA, 23% operating margin). The GPU cloud in the middle has a similar EBITDA margin (CoreWeave 59%) but depreciation and interest turn it into a loss (-2% operating, net interest about a quarter of revenue).
3. HUMAIN is building in the two thinner layers (buildings and GPU cloud). Its levers are the two lines that hurt the middle: power cost and cost of capital.

## Market size & growth
- Worldwide data-centre capex is on track to exceed $1 trillion in 2026 (Dell'Oro 1Q26 report, published 10 Jun 2026). Sources: Converge Digest, TED Magazine (both citing Dell'Oro).
- Amazon, Google, Meta and Microsoft raised data-centre capex 78% year on year in 1Q26 (Dell'Oro, same two sources).
- Key assumption behind the forecast: acceleration in 2H26 as Nvidia Rubin systems enter production deployment and hyperscalers refresh custom accelerators; rising memory and storage prices also lift server costs (Dell'Oro via Converge Digest).
- Hype TAM vs realistic spend: a secondary blog reports Dell'Oro raised its 2030 forecast to more than $3 trillion (from $1.7 trillion in Feb 2026). I couldn't confirm the $3 trillion figure on Dell'Oro's own pages, so treat it as unverified. The realistic, near-term number is the ~$1 trillion 2026 run rate.
- Hyperscaler 2026 capex guidance: sources conflict (Microsoft ~$170bn vs ~$190bn; Alphabet $180–190bn vs $195–205bn). I couldn't verify a single aggregate against company transcripts, so it is left out of the post.

## Value chain & margins
Latest reported quarter for each company (different quarter ends, so compare shape, not timing):

| Layer | Company | Quarter | Revenue | Gross / EBITDA margin | Operating margin | Source |
|---|---|---|---|---|---|---|
| Chips | Nvidia | Q2 FY27 (to 26 Jul 2026) | $96.2bn (Data Center $89.0bn, +117%) | Gross 75.0% | 66.2% ($63,734m / $96,221m) | Nvidia 8-K and 10-Q |
| GPU cloud (neocloud) | CoreWeave | Q2 2026 (to 30 Jun 2026) | $2,575m (+112%) | Adj. EBITDA 59% ($1,510m) | GAAP -2% (-$49m); adjusted +5% ($128m) | CoreWeave Q2 release |
| Landlord (colocation) | Equinix | Q3 2026 (to 30 Sep 2026) | $2.571bn (+11%) | Adj. EBITDA 51% ($1.321bn) | 23.3% ($600m / $2,571m) | Equinix Q3 release (SEC 8-K) |

Per $100 of revenue: Nvidia kept $66 of operating profit, Equinix $23, CoreWeave lost $2.

What the table says:
- Nvidia's margin comes from pricing power on the scarce input. Guidance for the quarter to October: revenue $108.0bn ±2%, gross margin 74.0% ±50 bp (Nvidia 8-K).
- CoreWeave's EBITDA margin (59%) is close to Equinix's (51%); the difference is below EBITDA. GPUs depreciate over a few years (vs decades for buildings), and the build is debt-funded: net interest expense was $640m in Q2, about 25% of revenue; net loss $626m (CoreWeave release). Q2 purchases of property and equipment: $6.4bn.
- Demand is not the constraint for the middle layer: CoreWeave backlog about $104bn at 30 Jun 2026, excluding more than $25bn of net new commitments added in early Q3 (CoreWeave release).
- Equinix: record annualized gross bookings $533m (+35%), AFFO $1.156bn (+20% as reported, incl. a one-off atNorth fee), FY26 guidance raised (revenue $10.325–10.365bn, adj. EBITDA $5.290–5.330bn, capex $5–6bn) (Equinix release).
- Concentration: Nvidia dominates the merchant accelerator layer; five direct customers made up 22%, 14%, 13%, 11% and 10% of Nvidia's accounts receivable at 26 Jul 2026 (10-Q). That is a receivables split, not a revenue split.
- Barriers to entry: chips (design + supply chain + software); neocloud (access to GPU allocation and cheap debt); landlord (land, power connections, permits).

## Key players

| Company | What it does | Latest fact | Source |
|---|---|---|---|
| Nvidia | AI accelerators and systems | Q2 FY27 revenue $96.2bn, gross margin 75.0%; Q3 results 17 Nov 2026 | https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000073/q2fy27pr.htm |
| CoreWeave | GPU cloud (neocloud) | Q2 2026 revenue $2,575m, GAAP operating margin -2%, backlog ~$104bn; Q3 results due 10 Nov 2026 after US close | https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Second-Quarter-2026-Results/default.aspx |
| Equinix | Colocation / interconnection landlord | Q3 2026 revenue $2.571bn (+11%), adj. EBITDA margin 51%, record bookings $533m | https://www.sec.gov/Archives/edgar/data/0001101239/000110123926000178/a991eqix-q326xpr.htm |
| HUMAIN | Saudi AI infrastructure, cloud and models (PIF 51% / Aramco 49% since 1 Nov 2026) | Up to 84 MW / ~27,000 Nvidia GPUs: 14 MW Blackwell B300 from Q4 2026, 70 MW Vera Rubin from mid-2027 (50 MW for a US client), subject to final agreements | https://www.thenationalnews.com/future/technology/2026/10/22/saudi-arabias-humain-expands-nvidia-deal-with-84mw-ai-computing-plan/ |
| DataVolt | Saudi data-centre developer (Vision Invest subsidiary) | Oxagon (NEOM) campus: 1.5 GW total, 360 MW first phase; HUMAIN takes 100 MW, expected 2028 | https://w.media/datavolt-and-humain-break-ground-on-first-ai-data-center-in-neom/ |
| G42 (Stargate UAE) | UAE AI infrastructure; 1 GW Stargate UAE cluster with OpenAI, Oracle, Nvidia, SoftBank, Cisco | First 200 MW targeted to be operational by end-2026; I couldn't find a go-live confirmation | https://gulfnews.com/business/markets/stargate-uae-first-phase-of-200mw-to-complete-by-2026-1.500310364 |
| Microsoft | Hyperscaler | Saudi Arabia East region (three availability zones) to open to customers in November 2026 | https://news.microsoft.com/source/emea/2026/08/microsoft-announces-saudi-arabia-east-datacenter-region-will-be-available-in-november-2026/ |

## Trends
Tailwinds
1. Spend keeps rising: >$1 trillion data-centre capex in 2026 (Dell'Oro).
2. Neocloud demand visible in contracts: CoreWeave backlog ~$104bn plus >$25bn added in early Q3.
3. Inference and interconnection demand in colocation: Equinix record bookings, Inference Exchange with Nvidia and Together AI (Equinix release).

Headwinds
1. Depreciation risk: the useful-life debate (books at 5–6 years vs a shorter economic life). Bear estimates (e.g. Michael Burry's ~$176bn understated depreciation for 2026–28) are a single analyst's view and unverified here. Amazon shortened some server lives from 6 to 5 years. Source: SiliconANGLE https://siliconangle.com/2025/11/22/resetting-gpu-depreciation-ai-factories-bend-dont-break-useful-life-assumptions/ (single source, treat as reported).
2. Cost of capital for the middle layer: CoreWeave net interest $640m in one quarter.

Regulation
- US export licensing applies to advanced chips going to Middle East projects (reported in Stargate UAE coverage); HUMAIN's Vera Rubin phase remains subject to final agreements (The National).

## GCC angle
- HUMAIN capital structure: PIF and Aramco closed the HUMAIN transaction on 1 Nov 2026 (PIF 51%, Aramco 49%), with SAR 9.9bn ($2.6bn) cash from Aramco in 2026; 3 GW target by 2030 — Aramco https://www.aramco.com/en/news-media/news/2026/pif-and-aramco-close-humain-transaction-to-accelerate-humains-global-growth
- Debt: National Infrastructure Fund (Infra) signed up to SAR 2.5bn ($667m) in two facilities with HUMAIN on 9 Nov 2026 (GPU facility up to SAR 1.1bn, power facility up to SAR 1.4bn) — Asharq Al-Awsat https://english.aawsat.com/business/5339534-humain-secures-667-million-infra-financing-advance-saudi-arabia%E2%80%99s-ai ; TechAfrica News https://techafricanews.com/2026/11/09/saudi-arabia-commits-667-million-to-humain-ai-infrastructure/
- Compute: up to 84 MW / ~27,000 Nvidia GPUs (The National; Middle East AI News https://www.middleeastainews.com/p/humain-27000-nvidia-gpus-vera-rubin). 3 GW by 2030, >6 GW by 2034 (both).
- Power: Saudi public-cloud operators licensed by CITC (now CST) pay 18 halalas/kWh (~$0.048), approved by the Council of Ministers in March 2021 — Arab News https://www.arabnews.com/saudi-arabia/saudi-arabia-reduces-power-tariff-to-boost-cloud-computing-1825521 (also listed in SEC's tariff schedule per search view; I couldn't load the SEC page).
- So what: HUMAIN is building in the landlord and GPU-cloud layers, where margins are thinnest. Equity from Aramco/PIF and state-backed debt lower its cost of capital, and the cloud tariff lowers power cost. Neither changes what the chips cost.

## Bull vs bear
- Bull: Sovereign capital and cheap power let Gulf builders earn neocloud-style EBITDA without neocloud-style interest bills, so the middle layer makes money here.
- Bear: Chip pricing power keeps most of the profit at Nvidia, and if GPUs lose value faster than depreciation schedules assume, the middle layer's thin operating margin goes negative wherever it is built.
- What would settle it: CoreWeave's operating margin over the next few quarters (does it turn positive?), Nvidia's gross margin vs its 74% guide, and HUMAIN's first contracted utilisation once the 14 MW Blackwell phase is live.

## Catalysts (dated)
- 2026-11-10: CoreWeave Q3 2026 results and call (5 pm ET) — https://investors.coreweave.com/news/news-details/2026/CoreWeave-Announces-Date-of-Third-Quarter-2026-Financial-Results-and-Conference-Call/default.aspx
- 2026-11-17: Nvidia Q3 FY27 results (quarter ended 25 Oct 2026), call 2 pm PT — https://nvidianews.nvidia.com/news/nvidia-sets-conference-call-for-third-quarter-financial-results-6928873
- November 2026 (no day given): Microsoft Saudi Arabia East region opens to customers — Microsoft (link above)
- Q4 2026: HUMAIN's first 14 MW of Blackwell B300 systems begin deployment — The National
- By end-2026 (target): first 200 MW of Stargate UAE operational — Gulf News (link above)

## Sources
- https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000073/q2fy27pr.htm
- https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000075/nvda-20260726.htm
- https://nvidianews.nvidia.com/news/nvidia-sets-conference-call-for-third-quarter-financial-results-6928873
- https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Second-Quarter-2026-Results/default.aspx
- https://investors.coreweave.com/news/news-details/2026/CoreWeave-Announces-Date-of-Third-Quarter-2026-Financial-Results-and-Conference-Call/default.aspx
- https://www.sec.gov/Archives/edgar/data/0001101239/000110123926000178/a991eqix-q326xpr.htm
- https://convergedigest.com/delloro-ai-infrastructure-spending-pushes-2026-data-center-capex-above-1-trillion/
- https://tedmag.com/report-global-data-center-capex-projection-passes-1-trillion/
- https://www.thenationalnews.com/future/technology/2026/10/22/saudi-arabias-humain-expands-nvidia-deal-with-84mw-ai-computing-plan/
- https://www.middleeastainews.com/p/humain-27000-nvidia-gpus-vera-rubin
- https://www.aramco.com/en/news-media/news/2026/pif-and-aramco-close-humain-transaction-to-accelerate-humains-global-growth
- https://english.aawsat.com/business/5339534-humain-secures-667-million-infra-financing-advance-saudi-arabia%E2%80%99s-ai
- https://techafricanews.com/2026/11/09/saudi-arabia-commits-667-million-to-humain-ai-infrastructure/
- https://www.arabnews.com/saudi-arabia/saudi-arabia-reduces-power-tariff-to-boost-cloud-computing-1825521
- https://w.media/datavolt-and-humain-break-ground-on-first-ai-data-center-in-neom/
- https://gulfnews.com/business/markets/stargate-uae-first-phase-of-200mw-to-complete-by-2026-1.500310364
- https://news.microsoft.com/source/emea/2026/08/microsoft-announces-saudi-arabia-east-datacenter-region-will-be-available-in-november-2026/
- https://siliconangle.com/2025/11/22/resetting-gpu-depreciation-ai-factories-bend-dont-break-useful-life-assumptions/
