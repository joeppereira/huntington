<!-- source: raw/models/Capital_Planning_Model.xlsx | converted by tools/convert_corpus.py -->
# Excel model: Capital_Planning_Model.xlsx

This file is a text rendering of an Excel workbook. Each sheet is shown as a value grid, followed by the list of formulas in that sheet (cell, row label, column header, formula, computed value). Blue-font cells in the workbook are inputs; black cells are formulas; green cells link to other sheets.

## Sheet: README


### Capital Planning & Stress Projection Model  (MDL-CAP-003)


### Meridian Harbor Financial Corp. - model documentation sheet

SYNTHETIC DOCUMENT FOR A PROOF OF CONCEPT. Meridian Harbor Financial Corp. is a fictional institution. All names, figures and events are invented and do not describe any real company.
- **Model ID** MDL-CAP-003
- **Model name** Capital Planning & Stress Projection Model
- **Risk tier** Tier 1 (High)
- **Model owner** Corporate Treasury - Capital Management
- **Independent validator** Model Risk Governance & Review (MRGR)
- **Last validation** 2026-02-27
- **Next validation due** 2027-02-28
- **Purpose** Projects CET1 capital, RWA and capital ratios over a nine-quarter horizon under baseline and severely adverse scenarios to size distributions.
- **Upstream data feeds (APIs)** API-16 Regulatory Reporting API; API-14 Macroeconomic Scenario API; API-15 Treasury Liquidity Positions API
- **Downstream disclosures** Annual Report - Capital Risk Management; Pillar 3 - Capital Planning and Stress Testing
- **Units** USD millions unless stated otherwise; rates stored as decimals
- **As-of date** See Assumptions sheet

### Sheets

- **Assumptions** Starting capital position (Q2 2026), distribution plan, growth and requirement stack.
- **Baseline_Projection** Nine-quarter CET1 projection under the firm's baseline plan.
- **Stress_Projection** Nine-quarter projection under the severely adverse scenario.
- **Summary** Minimum ratios, capital headroom and an indicative stress capital buffer (SCB).

### How the model works

- **1.** CET1(t) = CET1(t-1) + net income - preferred dividends - common dividends - share repurchases + other CET1 movements.
- **2.** Common dividends = shares outstanding x dividend per share; shares fall by buyback dollars / assumed share price.
- **3.** RWA(t) = RWA(t-1) x (1 + quarterly growth).
- **4.** Stress: pre-tax income = PPNR - provisions - trading & counterparty losses; tax at the effective rate (tax benefit recognised on losses); buybacks suspended; dividends held flat.
- **5.** Indicative SCB = start CET1 ratio - minimum stressed CET1 ratio + four quarters of planned dividends / starting RWA, floored at 2.5%.

### Key inputs

- **1.** Starting CET1 capital and RWA from API-16 Regulatory Reporting API (FR Y-9C / FFIEC 101 extract).
- **2.** Scenario paths from API-14 Macroeconomic Scenario API (severely adverse, CCAR 2026 analogue).
- **3.** Liquidity constraints on distributions cross-checked against API-15 Treasury Liquidity Positions API.
- **4.** Distribution plan (dividends, buybacks) approved by the Board Capital Committee.

### Key outputs

- **1.** Quarter-end CET1 ratio path versus management target and regulatory requirement.
- **2.** Minimum stressed CET1 ratio and indicative SCB.
- **3.** Capacity for additional buybacks at the management target.

### Limits, controls and known limitations

- **1.** Management target CET1 ratio: 13.0%; regulatory requirement = 4.5% + SCB + G-SIB surcharge.
- **2.** Simplified: no AOCI volatility modelling, no deferred-tax-asset threshold deductions.
- **3.** Stress losses are top-down inputs supplied by the enterprise stress testing program.

### Colour legend

- Blue text = hard-coded input / scenario lever
- Black text = formula
- Green text = link to another sheet
- Yellow fill = key assumption

## Sheet: Summary

> Capital Planning Summary
> Feeds Annual Report (Capital Risk Management) and Pillar 3 (stress testing)
> SYNTHETIC DOCUMENT FOR A PROOF OF CONCEPT. Meridian Harbor Financial Corp. is a fictional institution. All names, figures and events are invented and do not describe any real company.

| Row | A | B | C |
|---|---|---|---|
| 5 | Metric | Value | Note |
| 6 | Starting CET1 ratio (Q2 2026) | 0.1514 |  |
| 7 | Ending CET1 ratio - baseline (Q3 2028) | 0.1615 |  |
| 8 | Minimum CET1 ratio - baseline | 0.1523 |  |
| 9 | Minimum CET1 ratio - severely adverse | 0.1290 |  |
| 10 | Peak-to-trough CET1 decline (stress) | 0.0224 | Starting ratio minus minimum stressed ratio |
| 11 | Four quarters of planned dividends / starting RWA | 0.0094 | Dividend add-on in SCB formula |
| 12 | Indicative stress capital buffer (SCB) | 0.0318 | Floored at 2.5% |
| 13 | Regulatory CET1 requirement (current SCB) | 0.1020 | 4.5% + SCB + G-SIB surcharge |
| 14 | Regulatory CET1 requirement (indicative SCB) | 0.1018 |  |
| 15 | Management target | 0.1300 |  |
| 16 | Cumulative buybacks over horizon ($mm) | 27,000 |  |
| 17 | Excess CET1 vs target at Q3 2028 ($mm) | 22,994.91 | Additional distribution capacity at the target |
| 18 | Stress minimum above requirement? | YES |  |

### Formulas in Summary (13)

| Cell | Row label | Column header | Formula | Value |
|---|---|---|---|---|
| B6 | Starting CET1 ratio (Q2 2026) | Value | `=Baseline_Projection!B15` | 0.1514 |
| B7 | Ending CET1 ratio - baseline (Q3 2028) | Value | `=Baseline_Projection!K15` | 0.1615 |
| B8 | Minimum CET1 ratio - baseline | Value | `=MIN(Baseline_Projection!C15:K15)` | 0.1523 |
| B9 | Minimum CET1 ratio - severely adverse | Value | `=MIN(Stress_Projection!C20:K20)` | 0.1290 |
| B10 | Peak-to-trough CET1 decline (stress) | Value | `=B6-B9` | 0.0224 |
| B11 | Four quarters of planned dividends / starting RWA | Value | `=-SUM(Baseline_Projection!C9:F9)/Baseline_Projection!B14` | 0.0094 |
| B12 | Indicative stress capital buffer (SCB) | Value | `=MAX(0.025,B10+B11)` | 0.0318 |
| B13 | Regulatory CET1 requirement (current SCB) | Value | `=Assumptions!$B$23` | 0.1020 |
| B14 | Regulatory CET1 requirement (indicative SCB) | Value | `=Assumptions!$B$18+B12+Assumptions!$B$20` | 0.1018 |
| B15 | Management target | Value | `=Assumptions!$B$21` | 0.1300 |
| B16 | Cumulative buybacks over horizon ($mm) | Value | `=-SUM(Baseline_Projection!C10:K10)` | 27,000 |
| B17 | Excess CET1 vs target at Q3 2028 ($mm) | Value | `=Baseline_Projection!K17` | 22,994.91 |
| B18 | Stress minimum above requirement? | Value | `=IF(B9>=B13,"YES","NO - capital action required")` | YES |

## Sheet: Assumptions

> Assumptions
> Starting point: Q2 2026 actuals
> SYNTHETIC DOCUMENT FOR A PROOF OF CONCEPT. Meridian Harbor Financial Corp. is a fictional institution. All names, figures and events are invented and do not describe any real company.

| Row | A | B | C |
|---|---|---|---|
| 5 | Assumption | Value | Source / note |
| 6 | Starting CET1 capital ($mm) | 101,200 | API-16, Q2 2026 regulatory capital |
| 7 | Starting standardized RWA ($mm) | 668,400 | API-16, Q2 2026 |
| 8 | Starting common shares outstanding (mm) | 1,381 | Transfer agent, 2026-06-30 |
| 9 | Baseline quarterly net income ($mm) | 6,600 | Financial plan 2026-2028 |
| 10 | Net income growth per quarter | 0.0080 | Financial plan |
| 11 | Preferred dividends per quarter ($mm) | 260 | Contractual |
| 12 | Common dividend per share per quarter ($) | 1.15 | Board-declared; flat in projection |
| 13 | Share repurchases per quarter ($mm) | 3,000 | Board-authorised program ($30bn, 2025-2028) |
| 14 | Assumed share price ($) | 262 | Flat assumption for share count roll-forward |
| 15 | Baseline RWA growth per quarter | 0.0100 | Balance sheet plan |
| 16 | Other CET1 movements per quarter ($mm) | -150 | AOCI, deductions, employee stock plans (net) |
| 17 | Effective tax rate | 0.2200 | FY2025 effective rate |
| 18 | CET1 regulatory minimum | 0.0450 | 12 CFR 217 |
| 19 | Stress capital buffer (current) | 0.0320 | Effective 2025-10-01 |
| 20 | G-SIB surcharge | 0.0250 | Method 2 |
| 21 | Management target CET1 ratio | 0.1300 | Board Capital Committee |
| 23 | Regulatory CET1 requirement | 0.1020 |  |

### Formulas in Assumptions (1)

| Cell | Row label | Column header | Formula | Value |
|---|---|---|---|---|
| B23 | Regulatory CET1 requirement | Value | `=B18+B19+B20` | 0.1020 |

## Sheet: Baseline_Projection

> Baseline Projection
> Quarterly, $mm
> SYNTHETIC DOCUMENT FOR A PROOF OF CONCEPT. Meridian Harbor Financial Corp. is a fictional institution. All names, figures and events are invented and do not describe any real company.

| Row | A | B | C | D | E | F | G | H | I | J | K |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 | Line item | Q2 2026 (actual) | Q3 2026 | Q4 2026 | Q1 2027 | Q2 2027 | Q3 2027 | Q4 2027 | Q1 2028 | Q2 2028 | Q3 2028 |
| 6 | Beginning CET1 capital |  | 101,200 | 102,801.85 | 104,469.67 | 106,203.88 | 108,004.90 | 109,873.17 | 111,809.12 | 113,813.18 | 115,885.79 |
| 7 | Net income |  | 6,600 | 6,652.80 | 6,706.02 | 6,759.67 | 6,813.75 | 6,868.26 | 6,923.20 | 6,978.59 | 7,034.42 |
| 8 | Preferred dividends |  | -260 | -260 | -260 | -260 | -260 | -260 | -260 | -260 | -260 |
| 9 | Common dividends |  | -1,588.15 | -1,574.98 | -1,561.81 | -1,548.65 | -1,535.48 | -1,522.31 | -1,509.14 | -1,495.97 | -1,482.81 |
| 10 | Share repurchases |  | -3,000 | -3,000 | -3,000 | -3,000 | -3,000 | -3,000 | -3,000 | -3,000 | -3,000 |
| 11 | Other CET1 movements |  | -150 | -150 | -150 | -150 | -150 | -150 | -150 | -150 | -150 |
| 12 | Ending CET1 capital | 101,200 | 102,801.85 | 104,469.67 | 106,203.88 | 108,004.90 | 109,873.17 | 111,809.12 | 113,813.18 | 115,885.79 | 118,027.41 |
| 13 | RWA growth |  | 0.0100 | 0.0100 | 0.0100 | 0.0100 | 0.0100 | 0.0100 | 0.0100 | 0.0100 | 0.0100 |
| 14 | Standardized RWA | 668,400 | 675,084 | 681,834.84 | 688,653.19 | 695,539.72 | 702,495.12 | 709,520.07 | 716,615.27 | 723,781.42 | 731,019.24 |
| 15 | CET1 ratio | 0.1514 | 0.1523 | 0.1532 | 0.1542 | 0.1553 | 0.1564 | 0.1576 | 0.1588 | 0.1601 | 0.1615 |
| 16 | Shares outstanding (mm) | 1,381 | 1,369.55 | 1,358.10 | 1,346.65 | 1,335.20 | 1,323.75 | 1,312.30 | 1,300.85 | 1,289.40 | 1,277.95 |
| 17 | Headroom vs management target ($mm) |  | 15,040.93 | 15,831.14 | 16,678.96 | 17,584.74 | 18,548.81 | 19,571.51 | 20,653.19 | 21,794.21 | 22,994.91 |
| 18 | Headroom vs regulatory requirement ($mm) |  | 33,943.28 | 34,922.51 | 35,961.25 | 37,059.85 | 38,218.67 | 39,438.07 | 40,718.42 | 42,060.09 | 43,463.44 |

### Formulas in Baseline_Projection (121)

| Cell | Row label | Column header | Formula | Value |
|---|---|---|---|---|
| C6 | Beginning CET1 capital | Q3 2026 | `=B12` | 101,200 |
| D6 | Beginning CET1 capital | Q4 2026 | `=C12` | 102,801.85 |
| E6 | Beginning CET1 capital | Q1 2027 | `=D12` | 104,469.67 |
| F6 | Beginning CET1 capital | Q2 2027 | `=E12` | 106,203.88 |
| G6 | Beginning CET1 capital | Q3 2027 | `=F12` | 108,004.90 |
| H6 | Beginning CET1 capital | Q4 2027 | `=G12` | 109,873.17 |
| I6 | Beginning CET1 capital | Q1 2028 | `=H12` | 111,809.12 |
| J6 | Beginning CET1 capital | Q2 2028 | `=I12` | 113,813.18 |
| K6 | Beginning CET1 capital | Q3 2028 | `=J12` | 115,885.79 |
| C7 | Net income | Q3 2026 | `=Assumptions!$B$9*(1+Assumptions!$B$10)^0` | 6,600 |
| D7 | Net income | Q4 2026 | `=Assumptions!$B$9*(1+Assumptions!$B$10)^1` | 6,652.80 |
| E7 | Net income | Q1 2027 | `=Assumptions!$B$9*(1+Assumptions!$B$10)^2` | 6,706.02 |
| F7 | Net income | Q2 2027 | `=Assumptions!$B$9*(1+Assumptions!$B$10)^3` | 6,759.67 |
| G7 | Net income | Q3 2027 | `=Assumptions!$B$9*(1+Assumptions!$B$10)^4` | 6,813.75 |
| H7 | Net income | Q4 2027 | `=Assumptions!$B$9*(1+Assumptions!$B$10)^5` | 6,868.26 |
| I7 | Net income | Q1 2028 | `=Assumptions!$B$9*(1+Assumptions!$B$10)^6` | 6,923.20 |
| J7 | Net income | Q2 2028 | `=Assumptions!$B$9*(1+Assumptions!$B$10)^7` | 6,978.59 |
| K7 | Net income | Q3 2028 | `=Assumptions!$B$9*(1+Assumptions!$B$10)^8` | 7,034.42 |
| C8 | Preferred dividends | Q3 2026 | `=-Assumptions!$B$11` | -260 |
| D8 | Preferred dividends | Q4 2026 | `=-Assumptions!$B$11` | -260 |
| E8 | Preferred dividends | Q1 2027 | `=-Assumptions!$B$11` | -260 |
| F8 | Preferred dividends | Q2 2027 | `=-Assumptions!$B$11` | -260 |
| G8 | Preferred dividends | Q3 2027 | `=-Assumptions!$B$11` | -260 |
| H8 | Preferred dividends | Q4 2027 | `=-Assumptions!$B$11` | -260 |
| I8 | Preferred dividends | Q1 2028 | `=-Assumptions!$B$11` | -260 |
| J8 | Preferred dividends | Q2 2028 | `=-Assumptions!$B$11` | -260 |
| K8 | Preferred dividends | Q3 2028 | `=-Assumptions!$B$11` | -260 |
| C9 | Common dividends | Q3 2026 | `=-B16*Assumptions!$B$12` | -1,588.15 |
| D9 | Common dividends | Q4 2026 | `=-C16*Assumptions!$B$12` | -1,574.98 |
| E9 | Common dividends | Q1 2027 | `=-D16*Assumptions!$B$12` | -1,561.81 |
| F9 | Common dividends | Q2 2027 | `=-E16*Assumptions!$B$12` | -1,548.65 |
| G9 | Common dividends | Q3 2027 | `=-F16*Assumptions!$B$12` | -1,535.48 |
| H9 | Common dividends | Q4 2027 | `=-G16*Assumptions!$B$12` | -1,522.31 |
| I9 | Common dividends | Q1 2028 | `=-H16*Assumptions!$B$12` | -1,509.14 |
| J9 | Common dividends | Q2 2028 | `=-I16*Assumptions!$B$12` | -1,495.97 |
| K9 | Common dividends | Q3 2028 | `=-J16*Assumptions!$B$12` | -1,482.81 |
| C10 | Share repurchases | Q3 2026 | `=-Assumptions!$B$13` | -3,000 |
| D10 | Share repurchases | Q4 2026 | `=-Assumptions!$B$13` | -3,000 |
| E10 | Share repurchases | Q1 2027 | `=-Assumptions!$B$13` | -3,000 |
| F10 | Share repurchases | Q2 2027 | `=-Assumptions!$B$13` | -3,000 |
| G10 | Share repurchases | Q3 2027 | `=-Assumptions!$B$13` | -3,000 |
| H10 | Share repurchases | Q4 2027 | `=-Assumptions!$B$13` | -3,000 |
| I10 | Share repurchases | Q1 2028 | `=-Assumptions!$B$13` | -3,000 |
| J10 | Share repurchases | Q2 2028 | `=-Assumptions!$B$13` | -3,000 |
| K10 | Share repurchases | Q3 2028 | `=-Assumptions!$B$13` | -3,000 |
| C11 | Other CET1 movements | Q3 2026 | `=Assumptions!$B$16` | -150 |
| D11 | Other CET1 movements | Q4 2026 | `=Assumptions!$B$16` | -150 |
| E11 | Other CET1 movements | Q1 2027 | `=Assumptions!$B$16` | -150 |
| F11 | Other CET1 movements | Q2 2027 | `=Assumptions!$B$16` | -150 |
| G11 | Other CET1 movements | Q3 2027 | `=Assumptions!$B$16` | -150 |
| H11 | Other CET1 movements | Q4 2027 | `=Assumptions!$B$16` | -150 |
| I11 | Other CET1 movements | Q1 2028 | `=Assumptions!$B$16` | -150 |
| J11 | Other CET1 movements | Q2 2028 | `=Assumptions!$B$16` | -150 |
| K11 | Other CET1 movements | Q3 2028 | `=Assumptions!$B$16` | -150 |
| B12 | Ending CET1 capital | Q2 2026 (actual) | `=Assumptions!$B$6` | 101,200 |
| C12 | Ending CET1 capital | Q3 2026 | `=C6+C7+C8+C9+C10+C11` | 102,801.85 |
| D12 | Ending CET1 capital | Q4 2026 | `=D6+D7+D8+D9+D10+D11` | 104,469.67 |
| E12 | Ending CET1 capital | Q1 2027 | `=E6+E7+E8+E9+E10+E11` | 106,203.88 |
| F12 | Ending CET1 capital | Q2 2027 | `=F6+F7+F8+F9+F10+F11` | 108,004.90 |
| G12 | Ending CET1 capital | Q3 2027 | `=G6+G7+G8+G9+G10+G11` | 109,873.17 |
| H12 | Ending CET1 capital | Q4 2027 | `=H6+H7+H8+H9+H10+H11` | 111,809.12 |
| I12 | Ending CET1 capital | Q1 2028 | `=I6+I7+I8+I9+I10+I11` | 113,813.18 |
| J12 | Ending CET1 capital | Q2 2028 | `=J6+J7+J8+J9+J10+J11` | 115,885.79 |
| K12 | Ending CET1 capital | Q3 2028 | `=K6+K7+K8+K9+K10+K11` | 118,027.41 |
| C13 | RWA growth | Q3 2026 | `=Assumptions!$B$15` | 0.0100 |
| D13 | RWA growth | Q4 2026 | `=Assumptions!$B$15` | 0.0100 |
| E13 | RWA growth | Q1 2027 | `=Assumptions!$B$15` | 0.0100 |
| F13 | RWA growth | Q2 2027 | `=Assumptions!$B$15` | 0.0100 |
| G13 | RWA growth | Q3 2027 | `=Assumptions!$B$15` | 0.0100 |
| H13 | RWA growth | Q4 2027 | `=Assumptions!$B$15` | 0.0100 |
| I13 | RWA growth | Q1 2028 | `=Assumptions!$B$15` | 0.0100 |
| J13 | RWA growth | Q2 2028 | `=Assumptions!$B$15` | 0.0100 |
| K13 | RWA growth | Q3 2028 | `=Assumptions!$B$15` | 0.0100 |
| B14 | Standardized RWA | Q2 2026 (actual) | `=Assumptions!$B$7` | 668,400 |
| C14 | Standardized RWA | Q3 2026 | `=B14*(1+C13)` | 675,084 |
| D14 | Standardized RWA | Q4 2026 | `=C14*(1+D13)` | 681,834.84 |
| E14 | Standardized RWA | Q1 2027 | `=D14*(1+E13)` | 688,653.19 |
| F14 | Standardized RWA | Q2 2027 | `=E14*(1+F13)` | 695,539.72 |
| G14 | Standardized RWA | Q3 2027 | `=F14*(1+G13)` | 702,495.12 |
| H14 | Standardized RWA | Q4 2027 | `=G14*(1+H13)` | 709,520.07 |
| I14 | Standardized RWA | Q1 2028 | `=H14*(1+I13)` | 716,615.27 |
| J14 | Standardized RWA | Q2 2028 | `=I14*(1+J13)` | 723,781.42 |
| K14 | Standardized RWA | Q3 2028 | `=J14*(1+K13)` | 731,019.24 |
| B15 | CET1 ratio | Q2 2026 (actual) | `=B12/B14` | 0.1514 |
| C15 | CET1 ratio | Q3 2026 | `=IF(C14=0,0,C12/C14)` | 0.1523 |
| D15 | CET1 ratio | Q4 2026 | `=IF(D14=0,0,D12/D14)` | 0.1532 |
| E15 | CET1 ratio | Q1 2027 | `=IF(E14=0,0,E12/E14)` | 0.1542 |
| F15 | CET1 ratio | Q2 2027 | `=IF(F14=0,0,F12/F14)` | 0.1553 |
| G15 | CET1 ratio | Q3 2027 | `=IF(G14=0,0,G12/G14)` | 0.1564 |
| H15 | CET1 ratio | Q4 2027 | `=IF(H14=0,0,H12/H14)` | 0.1576 |
| I15 | CET1 ratio | Q1 2028 | `=IF(I14=0,0,I12/I14)` | 0.1588 |
| J15 | CET1 ratio | Q2 2028 | `=IF(J14=0,0,J12/J14)` | 0.1601 |
| K15 | CET1 ratio | Q3 2028 | `=IF(K14=0,0,K12/K14)` | 0.1615 |
| B16 | Shares outstanding (mm) | Q2 2026 (actual) | `=Assumptions!$B$8` | 1,381 |
| C16 | Shares outstanding (mm) | Q3 2026 | `=B16+C10/Assumptions!$B$14` | 1,369.55 |
| D16 | Shares outstanding (mm) | Q4 2026 | `=C16+D10/Assumptions!$B$14` | 1,358.10 |
| E16 | Shares outstanding (mm) | Q1 2027 | `=D16+E10/Assumptions!$B$14` | 1,346.65 |
| F16 | Shares outstanding (mm) | Q2 2027 | `=E16+F10/Assumptions!$B$14` | 1,335.20 |
| G16 | Shares outstanding (mm) | Q3 2027 | `=F16+G10/Assumptions!$B$14` | 1,323.75 |
| H16 | Shares outstanding (mm) | Q4 2027 | `=G16+H10/Assumptions!$B$14` | 1,312.30 |
| I16 | Shares outstanding (mm) | Q1 2028 | `=H16+I10/Assumptions!$B$14` | 1,300.85 |
| J16 | Shares outstanding (mm) | Q2 2028 | `=I16+J10/Assumptions!$B$14` | 1,289.40 |
| K16 | Shares outstanding (mm) | Q3 2028 | `=J16+K10/Assumptions!$B$14` | 1,277.95 |
| C17 | Headroom vs management target ($mm) | Q3 2026 | `=C12-Assumptions!$B$21*C14` | 15,040.93 |
| D17 | Headroom vs management target ($mm) | Q4 2026 | `=D12-Assumptions!$B$21*D14` | 15,831.14 |
| E17 | Headroom vs management target ($mm) | Q1 2027 | `=E12-Assumptions!$B$21*E14` | 16,678.96 |
| F17 | Headroom vs management target ($mm) | Q2 2027 | `=F12-Assumptions!$B$21*F14` | 17,584.74 |
| G17 | Headroom vs management target ($mm) | Q3 2027 | `=G12-Assumptions!$B$21*G14` | 18,548.81 |
| H17 | Headroom vs management target ($mm) | Q4 2027 | `=H12-Assumptions!$B$21*H14` | 19,571.51 |
| I17 | Headroom vs management target ($mm) | Q1 2028 | `=I12-Assumptions!$B$21*I14` | 20,653.19 |
| J17 | Headroom vs management target ($mm) | Q2 2028 | `=J12-Assumptions!$B$21*J14` | 21,794.21 |
| K17 | Headroom vs management target ($mm) | Q3 2028 | `=K12-Assumptions!$B$21*K14` | 22,994.91 |
| C18 | Headroom vs regulatory requirement ($mm) | Q3 2026 | `=C12-Assumptions!$B$23*C14` | 33,943.28 |
| D18 | Headroom vs regulatory requirement ($mm) | Q4 2026 | `=D12-Assumptions!$B$23*D14` | 34,922.51 |
| E18 | Headroom vs regulatory requirement ($mm) | Q1 2027 | `=E12-Assumptions!$B$23*E14` | 35,961.25 |
| F18 | Headroom vs regulatory requirement ($mm) | Q2 2027 | `=F12-Assumptions!$B$23*F14` | 37,059.85 |
| G18 | Headroom vs regulatory requirement ($mm) | Q3 2027 | `=G12-Assumptions!$B$23*G14` | 38,218.67 |
| H18 | Headroom vs regulatory requirement ($mm) | Q4 2027 | `=H12-Assumptions!$B$23*H14` | 39,438.07 |
| I18 | Headroom vs regulatory requirement ($mm) | Q1 2028 | `=I12-Assumptions!$B$23*I14` | 40,718.42 |
| J18 | Headroom vs regulatory requirement ($mm) | Q2 2028 | `=J12-Assumptions!$B$23*J14` | 42,060.09 |
| K18 | Headroom vs regulatory requirement ($mm) | Q3 2028 | `=K12-Assumptions!$B$23*K14` | 43,463.44 |

## Sheet: Stress_Projection

> Severely Adverse Projection
> Quarterly, $mm - stress losses from enterprise stress testing program
> SYNTHETIC DOCUMENT FOR A PROOF OF CONCEPT. Meridian Harbor Financial Corp. is a fictional institution. All names, figures and events are invented and do not describe any real company.

| Row | A | B | C | D | E | F | G | H | I | J | K |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 | Line item | Q2 2026 (actual) | Q3 2026 | Q4 2026 | Q1 2027 | Q2 2027 | Q3 2027 | Q4 2027 | Q1 2028 | Q2 2028 | Q3 2028 |
| 6 | Beginning CET1 capital |  | 101,200 | 95,067.85 | 93,303.70 | 91,851.55 | 90,867.40 | 90,507.25 | 90,771.10 | 91,580.95 | 92,780.80 |
| 7 | Pre-provision net revenue (PPNR) |  | 7,400 | 7,100 | 6,800 | 6,600 | 6,500 | 6,600 | 6,800 | 7,000 | 7,200 |
| 8 | Provision for credit losses |  | -7,300 | -6,800 | -6,100 | -5,300 | -4,400 | -3,700 | -3,200 | -2,900 | -2,700 |
| 9 | Trading & counterparty losses |  | -5,400 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 10 | Pre-tax income |  | -5,300 | 300 | 700 | 1,300 | 2,100 | 2,900 | 3,600 | 4,100 | 4,500 |
| 11 | Income tax (benefit) |  | 1,166 | -66 | -154 | -286 | -462 | -638 | -792 | -902 | -990 |
| 12 | Net income |  | -4,134 | 234 | 546 | 1,014 | 1,638 | 2,262 | 2,808 | 3,198 | 3,510 |
| 13 | Preferred dividends |  | -260 | -260 | -260 | -260 | -260 | -260 | -260 | -260 | -260 |
| 14 | Common dividends |  | -1,588.15 | -1,588.15 | -1,588.15 | -1,588.15 | -1,588.15 | -1,588.15 | -1,588.15 | -1,588.15 | -1,588.15 |
| 15 | Share repurchases |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 16 | Other CET1 movements |  | -150 | -150 | -150 | -150 | -150 | -150 | -150 | -150 | -150 |
| 17 | Ending CET1 capital | 101,200 | 95,067.85 | 93,303.70 | 91,851.55 | 90,867.40 | 90,507.25 | 90,771.10 | 91,580.95 | 92,780.80 | 94,292.65 |
| 18 | RWA growth |  | 0.0220 | 0.0150 | 0.0080 | 0.0040 | 0 | -0.0020 | -0.0040 | -0.0040 | -0.0040 |
| 19 | Standardized RWA | 668,400 | 683,104.80 | 693,351.37 | 698,898.18 | 701,693.78 | 701,693.78 | 700,290.39 | 697,489.23 | 694,699.27 | 691,920.47 |
| 20 | CET1 ratio | 0.1514 | 0.1392 | 0.1346 | 0.1314 | 0.1295 | 0.1290 | 0.1296 | 0.1313 | 0.1336 | 0.1363 |
| 21 | Shares outstanding (mm) | 1,381 | 1,381 | 1,381 | 1,381 | 1,381 | 1,381 | 1,381 | 1,381 | 1,381 | 1,381 |
| 22 | Headroom vs management target ($mm) |  | 6,264.23 | 3,168.02 | 994.79 | -352.79 | -712.94 | -266.65 | 907.35 | 2,469.89 | 4,342.99 |
| 23 | Headroom vs regulatory requirement ($mm) |  | 25,391.16 | 22,581.86 | 20,563.94 | 19,294.63 | 18,934.48 | 19,341.48 | 20,437.05 | 21,921.47 | 23,716.76 |

### Formulas in Stress_Projection (121)

| Cell | Row label | Column header | Formula | Value |
|---|---|---|---|---|
| C6 | Beginning CET1 capital | Q3 2026 | `=B17` | 101,200 |
| D6 | Beginning CET1 capital | Q4 2026 | `=C17` | 95,067.85 |
| E6 | Beginning CET1 capital | Q1 2027 | `=D17` | 93,303.70 |
| F6 | Beginning CET1 capital | Q2 2027 | `=E17` | 91,851.55 |
| G6 | Beginning CET1 capital | Q3 2027 | `=F17` | 90,867.40 |
| H6 | Beginning CET1 capital | Q4 2027 | `=G17` | 90,507.25 |
| I6 | Beginning CET1 capital | Q1 2028 | `=H17` | 90,771.10 |
| J6 | Beginning CET1 capital | Q2 2028 | `=I17` | 91,580.95 |
| K6 | Beginning CET1 capital | Q3 2028 | `=J17` | 92,780.80 |
| C10 | Pre-tax income | Q3 2026 | `=SUM(C7:C9)` | -5,300 |
| D10 | Pre-tax income | Q4 2026 | `=SUM(D7:D9)` | 300 |
| E10 | Pre-tax income | Q1 2027 | `=SUM(E7:E9)` | 700 |
| F10 | Pre-tax income | Q2 2027 | `=SUM(F7:F9)` | 1,300 |
| G10 | Pre-tax income | Q3 2027 | `=SUM(G7:G9)` | 2,100 |
| H10 | Pre-tax income | Q4 2027 | `=SUM(H7:H9)` | 2,900 |
| I10 | Pre-tax income | Q1 2028 | `=SUM(I7:I9)` | 3,600 |
| J10 | Pre-tax income | Q2 2028 | `=SUM(J7:J9)` | 4,100 |
| K10 | Pre-tax income | Q3 2028 | `=SUM(K7:K9)` | 4,500 |
| C11 | Income tax (benefit) | Q3 2026 | `=-C10*Assumptions!$B$17` | 1,166 |
| D11 | Income tax (benefit) | Q4 2026 | `=-D10*Assumptions!$B$17` | -66 |
| E11 | Income tax (benefit) | Q1 2027 | `=-E10*Assumptions!$B$17` | -154 |
| F11 | Income tax (benefit) | Q2 2027 | `=-F10*Assumptions!$B$17` | -286 |
| G11 | Income tax (benefit) | Q3 2027 | `=-G10*Assumptions!$B$17` | -462 |
| H11 | Income tax (benefit) | Q4 2027 | `=-H10*Assumptions!$B$17` | -638 |
| I11 | Income tax (benefit) | Q1 2028 | `=-I10*Assumptions!$B$17` | -792 |
| J11 | Income tax (benefit) | Q2 2028 | `=-J10*Assumptions!$B$17` | -902 |
| K11 | Income tax (benefit) | Q3 2028 | `=-K10*Assumptions!$B$17` | -990 |
| C12 | Net income | Q3 2026 | `=C10+C11` | -4,134 |
| D12 | Net income | Q4 2026 | `=D10+D11` | 234 |
| E12 | Net income | Q1 2027 | `=E10+E11` | 546 |
| F12 | Net income | Q2 2027 | `=F10+F11` | 1,014 |
| G12 | Net income | Q3 2027 | `=G10+G11` | 1,638 |
| H12 | Net income | Q4 2027 | `=H10+H11` | 2,262 |
| I12 | Net income | Q1 2028 | `=I10+I11` | 2,808 |
| J12 | Net income | Q2 2028 | `=J10+J11` | 3,198 |
| K12 | Net income | Q3 2028 | `=K10+K11` | 3,510 |
| C13 | Preferred dividends | Q3 2026 | `=-Assumptions!$B$11` | -260 |
| D13 | Preferred dividends | Q4 2026 | `=-Assumptions!$B$11` | -260 |
| E13 | Preferred dividends | Q1 2027 | `=-Assumptions!$B$11` | -260 |
| F13 | Preferred dividends | Q2 2027 | `=-Assumptions!$B$11` | -260 |
| G13 | Preferred dividends | Q3 2027 | `=-Assumptions!$B$11` | -260 |
| H13 | Preferred dividends | Q4 2027 | `=-Assumptions!$B$11` | -260 |
| I13 | Preferred dividends | Q1 2028 | `=-Assumptions!$B$11` | -260 |
| J13 | Preferred dividends | Q2 2028 | `=-Assumptions!$B$11` | -260 |
| K13 | Preferred dividends | Q3 2028 | `=-Assumptions!$B$11` | -260 |
| C14 | Common dividends | Q3 2026 | `=-B21*Assumptions!$B$12` | -1,588.15 |
| D14 | Common dividends | Q4 2026 | `=-C21*Assumptions!$B$12` | -1,588.15 |
| E14 | Common dividends | Q1 2027 | `=-D21*Assumptions!$B$12` | -1,588.15 |
| F14 | Common dividends | Q2 2027 | `=-E21*Assumptions!$B$12` | -1,588.15 |
| G14 | Common dividends | Q3 2027 | `=-F21*Assumptions!$B$12` | -1,588.15 |
| H14 | Common dividends | Q4 2027 | `=-G21*Assumptions!$B$12` | -1,588.15 |
| I14 | Common dividends | Q1 2028 | `=-H21*Assumptions!$B$12` | -1,588.15 |
| J14 | Common dividends | Q2 2028 | `=-I21*Assumptions!$B$12` | -1,588.15 |
| K14 | Common dividends | Q3 2028 | `=-J21*Assumptions!$B$12` | -1,588.15 |
| C16 | Other CET1 movements | Q3 2026 | `=Assumptions!$B$16` | -150 |
| D16 | Other CET1 movements | Q4 2026 | `=Assumptions!$B$16` | -150 |
| E16 | Other CET1 movements | Q1 2027 | `=Assumptions!$B$16` | -150 |
| F16 | Other CET1 movements | Q2 2027 | `=Assumptions!$B$16` | -150 |
| G16 | Other CET1 movements | Q3 2027 | `=Assumptions!$B$16` | -150 |
| H16 | Other CET1 movements | Q4 2027 | `=Assumptions!$B$16` | -150 |
| I16 | Other CET1 movements | Q1 2028 | `=Assumptions!$B$16` | -150 |
| J16 | Other CET1 movements | Q2 2028 | `=Assumptions!$B$16` | -150 |
| K16 | Other CET1 movements | Q3 2028 | `=Assumptions!$B$16` | -150 |
| B17 | Ending CET1 capital | Q2 2026 (actual) | `=Assumptions!$B$6` | 101,200 |
| C17 | Ending CET1 capital | Q3 2026 | `=C6+C12+C13+C14+C15+C16` | 95,067.85 |
| D17 | Ending CET1 capital | Q4 2026 | `=D6+D12+D13+D14+D15+D16` | 93,303.70 |
| E17 | Ending CET1 capital | Q1 2027 | `=E6+E12+E13+E14+E15+E16` | 91,851.55 |
| F17 | Ending CET1 capital | Q2 2027 | `=F6+F12+F13+F14+F15+F16` | 90,867.40 |
| G17 | Ending CET1 capital | Q3 2027 | `=G6+G12+G13+G14+G15+G16` | 90,507.25 |
| H17 | Ending CET1 capital | Q4 2027 | `=H6+H12+H13+H14+H15+H16` | 90,771.10 |
| I17 | Ending CET1 capital | Q1 2028 | `=I6+I12+I13+I14+I15+I16` | 91,580.95 |
| J17 | Ending CET1 capital | Q2 2028 | `=J6+J12+J13+J14+J15+J16` | 92,780.80 |
| K17 | Ending CET1 capital | Q3 2028 | `=K6+K12+K13+K14+K15+K16` | 94,292.65 |
| B19 | Standardized RWA | Q2 2026 (actual) | `=Assumptions!$B$7` | 668,400 |
| C19 | Standardized RWA | Q3 2026 | `=B19*(1+C18)` | 683,104.80 |
| D19 | Standardized RWA | Q4 2026 | `=C19*(1+D18)` | 693,351.37 |
| E19 | Standardized RWA | Q1 2027 | `=D19*(1+E18)` | 698,898.18 |
| F19 | Standardized RWA | Q2 2027 | `=E19*(1+F18)` | 701,693.78 |
| G19 | Standardized RWA | Q3 2027 | `=F19*(1+G18)` | 701,693.78 |
| H19 | Standardized RWA | Q4 2027 | `=G19*(1+H18)` | 700,290.39 |
| I19 | Standardized RWA | Q1 2028 | `=H19*(1+I18)` | 697,489.23 |
| J19 | Standardized RWA | Q2 2028 | `=I19*(1+J18)` | 694,699.27 |
| K19 | Standardized RWA | Q3 2028 | `=J19*(1+K18)` | 691,920.47 |
| B20 | CET1 ratio | Q2 2026 (actual) | `=B17/B19` | 0.1514 |
| C20 | CET1 ratio | Q3 2026 | `=IF(C19=0,0,C17/C19)` | 0.1392 |
| D20 | CET1 ratio | Q4 2026 | `=IF(D19=0,0,D17/D19)` | 0.1346 |
| E20 | CET1 ratio | Q1 2027 | `=IF(E19=0,0,E17/E19)` | 0.1314 |
| F20 | CET1 ratio | Q2 2027 | `=IF(F19=0,0,F17/F19)` | 0.1295 |
| G20 | CET1 ratio | Q3 2027 | `=IF(G19=0,0,G17/G19)` | 0.1290 |
| H20 | CET1 ratio | Q4 2027 | `=IF(H19=0,0,H17/H19)` | 0.1296 |
| I20 | CET1 ratio | Q1 2028 | `=IF(I19=0,0,I17/I19)` | 0.1313 |
| J20 | CET1 ratio | Q2 2028 | `=IF(J19=0,0,J17/J19)` | 0.1336 |
| K20 | CET1 ratio | Q3 2028 | `=IF(K19=0,0,K17/K19)` | 0.1363 |
| B21 | Shares outstanding (mm) | Q2 2026 (actual) | `=Assumptions!$B$8` | 1,381 |
| C21 | Shares outstanding (mm) | Q3 2026 | `=B21+C15/Assumptions!$B$14` | 1,381 |
| D21 | Shares outstanding (mm) | Q4 2026 | `=C21+D15/Assumptions!$B$14` | 1,381 |
| E21 | Shares outstanding (mm) | Q1 2027 | `=D21+E15/Assumptions!$B$14` | 1,381 |
| F21 | Shares outstanding (mm) | Q2 2027 | `=E21+F15/Assumptions!$B$14` | 1,381 |
| G21 | Shares outstanding (mm) | Q3 2027 | `=F21+G15/Assumptions!$B$14` | 1,381 |
| H21 | Shares outstanding (mm) | Q4 2027 | `=G21+H15/Assumptions!$B$14` | 1,381 |
| I21 | Shares outstanding (mm) | Q1 2028 | `=H21+I15/Assumptions!$B$14` | 1,381 |
| J21 | Shares outstanding (mm) | Q2 2028 | `=I21+J15/Assumptions!$B$14` | 1,381 |
| K21 | Shares outstanding (mm) | Q3 2028 | `=J21+K15/Assumptions!$B$14` | 1,381 |
| C22 | Headroom vs management target ($mm) | Q3 2026 | `=C17-Assumptions!$B$21*C19` | 6,264.23 |
| D22 | Headroom vs management target ($mm) | Q4 2026 | `=D17-Assumptions!$B$21*D19` | 3,168.02 |
| E22 | Headroom vs management target ($mm) | Q1 2027 | `=E17-Assumptions!$B$21*E19` | 994.79 |
| F22 | Headroom vs management target ($mm) | Q2 2027 | `=F17-Assumptions!$B$21*F19` | -352.79 |
| G22 | Headroom vs management target ($mm) | Q3 2027 | `=G17-Assumptions!$B$21*G19` | -712.94 |
| H22 | Headroom vs management target ($mm) | Q4 2027 | `=H17-Assumptions!$B$21*H19` | -266.65 |
| I22 | Headroom vs management target ($mm) | Q1 2028 | `=I17-Assumptions!$B$21*I19` | 907.35 |
| J22 | Headroom vs management target ($mm) | Q2 2028 | `=J17-Assumptions!$B$21*J19` | 2,469.89 |
| K22 | Headroom vs management target ($mm) | Q3 2028 | `=K17-Assumptions!$B$21*K19` | 4,342.99 |
| C23 | Headroom vs regulatory requirement ($mm) | Q3 2026 | `=C17-Assumptions!$B$23*C19` | 25,391.16 |
| D23 | Headroom vs regulatory requirement ($mm) | Q4 2026 | `=D17-Assumptions!$B$23*D19` | 22,581.86 |
| E23 | Headroom vs regulatory requirement ($mm) | Q1 2027 | `=E17-Assumptions!$B$23*E19` | 20,563.94 |
| F23 | Headroom vs regulatory requirement ($mm) | Q2 2027 | `=F17-Assumptions!$B$23*F19` | 19,294.63 |
| G23 | Headroom vs regulatory requirement ($mm) | Q3 2027 | `=G17-Assumptions!$B$23*G19` | 18,934.48 |
| H23 | Headroom vs regulatory requirement ($mm) | Q4 2027 | `=H17-Assumptions!$B$23*H19` | 19,341.48 |
| I23 | Headroom vs regulatory requirement ($mm) | Q1 2028 | `=I17-Assumptions!$B$23*I19` | 20,437.05 |
| J23 | Headroom vs regulatory requirement ($mm) | Q2 2028 | `=J17-Assumptions!$B$23*J19` | 21,921.47 |
| K23 | Headroom vs regulatory requirement ($mm) | Q3 2028 | `=K17-Assumptions!$B$23*K19` | 23,716.76 |

### Cell notes in Stress_Projection

- C15: Buybacks suspended under stress (CCAR convention).
- D15: Buybacks suspended under stress (CCAR convention).
- E15: Buybacks suspended under stress (CCAR convention).
- F15: Buybacks suspended under stress (CCAR convention).
- G15: Buybacks suspended under stress (CCAR convention).
- H15: Buybacks suspended under stress (CCAR convention).
- I15: Buybacks suspended under stress (CCAR convention).
- J15: Buybacks suspended under stress (CCAR convention).
- K15: Buybacks suspended under stress (CCAR convention).
