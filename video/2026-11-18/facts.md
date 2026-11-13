# Maaden Q3 2026: fact sheet for "Saudi results, in motion" ep. 2

Company: Saudi Arabian Mining Company (Maaden), Tadawul 1211.
Data file: `report.json` in this folder (validator PASS, 13 Nov 2026).

## Why Maaden

Revenue rose 11% in Q3 2026 while EBITDA fell 24% and operating profit almost halved. One segment explains it. Phosphate EBITDA dropped 83% on high sulfur costs and no ammonia export sales, and Maaden ties both to Middle East logistics. Aluminum and gold each posted record results and covered most of the gap. It is a mining story, so it reads differently from episode 1 (Aramco, oil). The company publishes quarterly segment revenue and segment EBITDA for both years.

## Source documents (all from Maaden's own IR site, maaden.com > Investor Relations > Financial Information > Results)

| # | Document | Date | URL |
|---|---|---|---|
| A | Condensed consolidated interim financial statements for the quarter and nine months ended 30 September 2026 (unaudited, reviewed) | Q3 2026 | https://axvpvthrjz64.compat.objectstorage.me-jeddah-1.oraclecloud.com/maaden-website-assets/reports/results-centre/2026/financial-statements.pdf |
| B | Maaden Q3-2026 Results Presentation | 9 November 2026 | https://axvpvthrjz64.compat.objectstorage.me-jeddah-1.oraclecloud.com/maaden-website-assets/reports/results-centre/2026/maaden-q3-2026-results-presentation.pdf |
| C | Condensed consolidated interim financial statements, quarter and nine months ended 30 September 2025 (auditor review report dated 5 November 2025) | Q3 2025 | https://axvpvthrjz64.compat.objectstorage.me-jeddah-1.oraclecloud.com/maaden-website-assets/reports/results-centre/2025/maaden-q3-25-cfs---eng---final--signed.pdf |
| D | Q3 2025 earnings release and Q3-FY25 presentation (cross-check only) | 6 November 2025 | .../results-centre/2025/28113_370_2025-11-06_09-21-45_en.pdf and .../results-centre/2025/q3-fy25---maaden-ec-presentation_final.pdf |
| E | Q3 2026 earnings call transcript (cross-check only) | Nov 2026 | .../results-centre/2026/earning-call-transcript.pdf |

Where each block comes from:
- Segment revenue and segment EBITDA, Q3 26 and Q3 25 (US$ m): B, slides 13 to 15 (Phosphate, Aluminum, GGM). Group revenue $2,971m and EBITDA $870m / $1,140m: B, slides 6 and 10.
- Income statement (US$ thousands): A, page 5, the US$ convenience columns (Maaden converts at a fixed US$1 = SAR 3.75).
- Q3 2025 group revenue $2,670m: A, page 5, US$ column 2,669,685 thousand.
- Q3 2024 revenue: C, page 6, SAR 8,044,911,493 (C has no US$ column).

## Figure check

| Claim in report.json | Source figure | Check |
|---|---|---|
| Revenue $2,971m, +11% | B slide 6: $2,971m, 11% YoY. A: US$ 2,970,751k vs 2,669,685k (SAR 11,140,316k vs 10,011,322k) | 2,970,751 / 2,669,685 − 1 = +11.28%; SAR basis +11.28% |
| EBITDA $870m, −24% | B slides 6 and 10: $870m, (24)%; Q3 25 $1,140m | 870 / 1,140 − 1 = −23.7% |
| EBITDA bridge closes | B slide 10: 1,140 − 172 + 478 − 672 + 96 | = 870 |
| EBITDA margin 29%, −13 pts | B slide 6: 29%, 13pp | 870 / 2,971 = 29.3%; 1,140 / 2,670 = 42.7%; diff −13.4 pts |
| Phosphate revenue 1,370 vs 1,501; EBITDA 135 vs 774 (−83%) | B slide 13 | 1,370 / 1,501 − 1 = −8.7% (slide: (9)%); 135 / 774 − 1 = −82.6%; margin 9.9% (slide: 10%) |
| Aluminum revenue 985 vs 748; EBITDA 419 vs 201 (+108%) | B slide 14 | +31.7% (slide: 32%); 419 / 201 − 1 = +108.5%; margin 42.5% (slide: 43%) |
| GGM revenue 596 vs 400; EBITDA 403 vs 236 (+71%) | B slide 15 (and slide 31 "EBITDA reported") | +49.0%; 403 / 236 − 1 = +70.8%; margin 67.6% (slide: 68%) |
| Segment revenue ties to the statutory accounts | A note 6, SAR k: Phosphate 5,136,390; Aluminum 3,692,110; GGM 2,233,164 | ÷ 3.75 = $1,369.7m, $984.6m, $595.5m, so the slide figures match |
| Prior-year segment EBITDA ties to the 2025 deck | D (SAR m): Phosphate 2,904; Aluminum 755; GGM 887; total 4,276 | ÷ 3.75 = 774.4, 201.3, 236.5, 1,140.3, so they match B |
| Corporate & other: revenue 20 vs 21; EBITDA (87) vs (71) | Not printed; balancing figure | 2,971 − 1,370 − 985 − 596 = 20; 2,670 − 1,501 − 748 − 400 = 21; 870 − 957 = −87; 1,140 − 1,211 = −71. A note 6 "Construction revenue" SAR 78,652k = $21.0m (Q3 25: $21.3m), so the rounded residual is consistent |
| Revenue bridge | from segment table | 2,670 − 131 + 237 + 196 − 1 = 2,971 |
| Gross profit 743,845 vs 1,055,476 | A p.5 | revenue − cost of sales, both columns foot |
| Operating expenses, net (325,205) vs (272,431) | A p.5, sum of 5 printed lines (selling, G&A, exploration, ECL, other operating income) | 743,845 − 325,205 = 418,640 = printed operating profit; 1,055,476 − 272,431 = 783,045 = printed |
| Operating profit 418,640 vs 783,045 (−46.5%) | A p.5 (SAR 1,569,899k vs 2,936,424k) | −46.54% on both currency bases |
| Share of JVs 125,860 vs 25,137 | A p.5 | printed |
| Net finance cost (71,522) vs (92,260) | A p.5: finance income 34,626 / 38,461; finance cost (106,148) / (130,721) | summed |
| Zakat, income tax and severance (44,798) vs (38,555) | A p.5: (862) + 11,252 + (55,188); (1,599) + (31,558) + (5,398) | summed |
| Profit for the quarter 428,180 vs 677,367 | A p.5 (SAR 1,605,673k vs 2,540,122k) | rows foot to the printed figure; −36.8% |
| Net profit to shareholders (not in the file, for the caption) | A p.5: US$ 448,626k vs 588,035k (SAR 1,682,345k vs 2,205,130k) | −23.7% |
| Revenue history Q3 24 = 2.145 ($B) | C p.6: SAR 8,044,911,493 | ÷ 3.75 = $2,145.3m (converted at Maaden's fixed rate) |
| Revenue history Q3 25 = 2.670, Q3 26 = 2.971 ($B) | A US$ column 2,669,685k; B $2,971m | Q3 24 → Q3 26: +38.5% |

## Two takeaways

1. **Headline vs real story.** Revenue grew 11% to $2,971m, the highest of the three third quarters shown (Q3 24: $2,145m). Profit went the other way. EBITDA fell 24% to $870m, operating profit fell 46.5% (US$ 418.6m from 783.0m), and net profit to shareholders fell 24% to SAR 1,682m. Most of the gap is cost. Maaden's EBITDA bridge shows +$478m from prices and −$672m from costs, with sulfur named as the main cost driver.
2. **The profit engine changed in a year.** Phosphate is still the largest business by revenue (46% of the group, $1,370m), but its EBITDA fell from $774m to $135m. In Q3 2025 phosphate made 64% of segment EBITDA (774 of 1,211). In Q3 2026 it made 14% (135 of 957). Aluminum (EBITDA $419m, +108%) and gold (EBITDA $403m, +71%) now earn 86% of it, with gold doing that on 20% of revenue at a 68% margin.

## Conflicts and caveats

- **Currency labels in Maaden's own 2025 documents.** The Q3 2025 earnings release says "revenue growth to $27.9 billion" and the Q3-FY25 deck heads its table "($ million)" with revenue 10,011. The Q3 2025 statements show these are SAR (SAR 10,011,321,916 for the quarter, 27,938,003,742 for nine months). Every 2025 figure used here comes from the SAR statements, and the 2026 deck's US$ prior-year numbers match them at ÷ 3.75.
- **Segment EBITDA is non-IFRS.** It comes from the results presentation. The statements report segment profit only for nine months, not for the quarter. Slide 27 says the aluminum sub-segment figures are not audited.
- **GGM EBITDA has two versions on slide 31:** $346m before JV income and $403m "EBITDA reported". The file uses $403m, which matches slides 6 and 15.
- **Corporate & other** is a balancing line (group total less the three segments). It is not a printed figure.
- **Q3 2024 revenue** is the SAR figure converted at Maaden's fixed 3.75 rate. Maaden's documents do not print it in US$.
- **Currency choice.** Maaden's statutory statements are in SAR, while its 2026 deck reports in US$ and gives segment EBITDA only in US$. The file is in US$ so the segment table and the income statement use the same currency. Episode 1 (Aramco) was in SAR.
- **Validator limitation (finance-motion).** The validator cannot pass a negative segment growth string (`rounds_to` compares the signed recomputed value with the absolute displayed value). The `growth` display was left out for Phosphate (−8.7%) and Corporate & other (−4.8%). The video does not show segment growth. The PDF renderer reads `display.growth` for every segment and would need these two restored ("−9%", "−4.8%") after the skill is fixed. The skill was not edited.
- News coverage was used only to find the company. No figures come from news.
