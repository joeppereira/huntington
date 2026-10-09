<!-- source: raw/models/CECL_Allowance_Model.xlsx | converted by tools/convert_corpus.py -->
# Excel model: CECL_Allowance_Model.xlsx

This file is a text rendering of an Excel workbook. Each sheet is shown as a value grid, followed by the list of formulas in that sheet (cell, row label, column header, formula, computed value). Blue-font cells in the workbook are inputs; black cells are formulas; green cells link to other sheets.

## Sheet: Allowance_Summary

> Allowance for Loan Losses - Summary and Reconciliation
> Feeds Annual Report Note 6 and the earnings supplement
> SYNTHETIC DOCUMENT FOR A PROOF OF CONCEPT. Meridian Harbor Financial Corp. is a fictional institution. All names, figures and events are invented and do not describe any real company.

| Row | A | B | C | D | E | F | G | H | I | J | K | L |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 | Segment | Upside ECL | Baseline ECL | Downside ECL | Weighted (modeled) ($mm) | Qualitative overlay ($mm) | Total allowance ($mm) | Reported allowance ($mm) | Difference | Overlay % of modeled | Allowance / loans | Coverage of NCOs (yrs) |
| 6 | Credit Card | 6,894.36 | 7,641.79 | 10,611.39 | 8,383.18 | 256.82 | 8,640 | 8,640 | 0 | 0.0306 | 0.0624 | 1.87 |
| 7 | Residential Mortgage | 580.96 | 662.27 | 1,058.80 | 764.97 | 55.03 | 820.00 | 820 | 0 | 0.0719 | 0.0038 | 20.50 |
| 8 | Auto | 627.11 | 675.41 | 868.10 | 723.56 | -33.56 | 690 | 690 | 0 | -0.0464 | 0.0106 | 1.68 |
| 9 | Commercial Real Estate | 1,653.82 | 1,936.21 | 3,150.43 | 2,244.00 | 226.00 | 2,470 | 2,470 | 0 | 0.1007 | 0.0252 | 6.50 |
| 10 | Commercial & Industrial | 2,222.31 | 2,416.26 | 3,188.96 | 2,609.28 | 150.72 | 2,760 | 2,760 | 0 | 0.0578 | 0.0160 | 4.93 |
| 11 | Other Consumer & Wholesale | 456.21 | 485.11 | 600.45 | 513.93 | 26.07 | 540 | 540 | 0 | 0.0507 | 0.0109 | 6 |
| 12 | Total | 12,434.76 | 13,817.04 | 19,478.13 | 15,238.91 | 681.09 | 15,920 | 15,920 | 0 | 0.0447 | 0.0214 | 2.61 |
| 14 | Overlay control check (/overlay/ <= 15% of modeled per segment) |  |  |  |  | OK |  |  |  |  |  |  |

### Formulas in Allowance_Summary (78)

| Cell | Row label | Column header | Formula | Value |
|---|---|---|---|---|
| A6 | Credit Card | Segment | `=Segment_Inputs!A6` | Credit Card |
| B6 | Credit Card | Upside ECL | `=ECL_Calc!G7` | 6,894.36 |
| C6 | Credit Card | Baseline ECL | `=ECL_Calc!G17` | 7,641.79 |
| D6 | Credit Card | Downside ECL | `=ECL_Calc!G27` | 10,611.39 |
| E6 | Credit Card | Weighted (modeled) ($mm) | `=B6*Scenarios!$B$6+C6*Scenarios!$B$7+D6*Scenarios!$B$8` | 8,383.18 |
| G6 | Credit Card | Total allowance ($mm) | `=E6+F6` | 8,640 |
| H6 | Credit Card | Reported allowance ($mm) | `=Segment_Inputs!K6` | 8,640 |
| I6 | Credit Card | Difference | `=G6-H6` | 0 |
| J6 | Credit Card | Overlay % of modeled | `=IF(E6=0,0,F6/E6)` | 0.0306 |
| K6 | Credit Card | Allowance / loans | `=IF(Segment_Inputs!C6=0,0,G6/Segment_Inputs!C6)` | 0.0624 |
| L6 | Credit Card | Coverage of NCOs (yrs) | `=IF(Segment_Inputs!J6=0,0,G6/Segment_Inputs!J6)` | 1.87 |
| A7 | Residential Mortgage | Segment | `=Segment_Inputs!A7` | Residential Mortgage |
| B7 | Residential Mortgage | Upside ECL | `=ECL_Calc!G8` | 580.96 |
| C7 | Residential Mortgage | Baseline ECL | `=ECL_Calc!G18` | 662.27 |
| D7 | Residential Mortgage | Downside ECL | `=ECL_Calc!G28` | 1,058.80 |
| E7 | Residential Mortgage | Weighted (modeled) ($mm) | `=B7*Scenarios!$B$6+C7*Scenarios!$B$7+D7*Scenarios!$B$8` | 764.97 |
| G7 | Residential Mortgage | Total allowance ($mm) | `=E7+F7` | 820.00 |
| H7 | Residential Mortgage | Reported allowance ($mm) | `=Segment_Inputs!K7` | 820 |
| I7 | Residential Mortgage | Difference | `=G7-H7` | 0 |
| J7 | Residential Mortgage | Overlay % of modeled | `=IF(E7=0,0,F7/E7)` | 0.0719 |
| K7 | Residential Mortgage | Allowance / loans | `=IF(Segment_Inputs!C7=0,0,G7/Segment_Inputs!C7)` | 0.0038 |
| L7 | Residential Mortgage | Coverage of NCOs (yrs) | `=IF(Segment_Inputs!J7=0,0,G7/Segment_Inputs!J7)` | 20.50 |
| A8 | Auto | Segment | `=Segment_Inputs!A8` | Auto |
| B8 | Auto | Upside ECL | `=ECL_Calc!G9` | 627.11 |
| C8 | Auto | Baseline ECL | `=ECL_Calc!G19` | 675.41 |
| D8 | Auto | Downside ECL | `=ECL_Calc!G29` | 868.10 |
| E8 | Auto | Weighted (modeled) ($mm) | `=B8*Scenarios!$B$6+C8*Scenarios!$B$7+D8*Scenarios!$B$8` | 723.56 |
| G8 | Auto | Total allowance ($mm) | `=E8+F8` | 690 |
| H8 | Auto | Reported allowance ($mm) | `=Segment_Inputs!K8` | 690 |
| I8 | Auto | Difference | `=G8-H8` | 0 |
| J8 | Auto | Overlay % of modeled | `=IF(E8=0,0,F8/E8)` | -0.0464 |
| K8 | Auto | Allowance / loans | `=IF(Segment_Inputs!C8=0,0,G8/Segment_Inputs!C8)` | 0.0106 |
| L8 | Auto | Coverage of NCOs (yrs) | `=IF(Segment_Inputs!J8=0,0,G8/Segment_Inputs!J8)` | 1.68 |
| A9 | Commercial Real Estate | Segment | `=Segment_Inputs!A9` | Commercial Real Estate |
| B9 | Commercial Real Estate | Upside ECL | `=ECL_Calc!G10` | 1,653.82 |
| C9 | Commercial Real Estate | Baseline ECL | `=ECL_Calc!G20` | 1,936.21 |
| D9 | Commercial Real Estate | Downside ECL | `=ECL_Calc!G30` | 3,150.43 |
| E9 | Commercial Real Estate | Weighted (modeled) ($mm) | `=B9*Scenarios!$B$6+C9*Scenarios!$B$7+D9*Scenarios!$B$8` | 2,244.00 |
| G9 | Commercial Real Estate | Total allowance ($mm) | `=E9+F9` | 2,470 |
| H9 | Commercial Real Estate | Reported allowance ($mm) | `=Segment_Inputs!K9` | 2,470 |
| I9 | Commercial Real Estate | Difference | `=G9-H9` | 0 |
| J9 | Commercial Real Estate | Overlay % of modeled | `=IF(E9=0,0,F9/E9)` | 0.1007 |
| K9 | Commercial Real Estate | Allowance / loans | `=IF(Segment_Inputs!C9=0,0,G9/Segment_Inputs!C9)` | 0.0252 |
| L9 | Commercial Real Estate | Coverage of NCOs (yrs) | `=IF(Segment_Inputs!J9=0,0,G9/Segment_Inputs!J9)` | 6.50 |
| A10 | Commercial & Industrial | Segment | `=Segment_Inputs!A10` | Commercial & Industrial |
| B10 | Commercial & Industrial | Upside ECL | `=ECL_Calc!G11` | 2,222.31 |
| C10 | Commercial & Industrial | Baseline ECL | `=ECL_Calc!G21` | 2,416.26 |
| D10 | Commercial & Industrial | Downside ECL | `=ECL_Calc!G31` | 3,188.96 |
| E10 | Commercial & Industrial | Weighted (modeled) ($mm) | `=B10*Scenarios!$B$6+C10*Scenarios!$B$7+D10*Scenarios!$B$8` | 2,609.28 |
| G10 | Commercial & Industrial | Total allowance ($mm) | `=E10+F10` | 2,760 |
| H10 | Commercial & Industrial | Reported allowance ($mm) | `=Segment_Inputs!K10` | 2,760 |
| I10 | Commercial & Industrial | Difference | `=G10-H10` | 0 |
| J10 | Commercial & Industrial | Overlay % of modeled | `=IF(E10=0,0,F10/E10)` | 0.0578 |
| K10 | Commercial & Industrial | Allowance / loans | `=IF(Segment_Inputs!C10=0,0,G10/Segment_Inputs!C10)` | 0.0160 |
| L10 | Commercial & Industrial | Coverage of NCOs (yrs) | `=IF(Segment_Inputs!J10=0,0,G10/Segment_Inputs!J10)` | 4.93 |
| A11 | Other Consumer & Wholesale | Segment | `=Segment_Inputs!A11` | Other Consumer & Wholesale |
| B11 | Other Consumer & Wholesale | Upside ECL | `=ECL_Calc!G12` | 456.21 |
| C11 | Other Consumer & Wholesale | Baseline ECL | `=ECL_Calc!G22` | 485.11 |
| D11 | Other Consumer & Wholesale | Downside ECL | `=ECL_Calc!G32` | 600.45 |
| E11 | Other Consumer & Wholesale | Weighted (modeled) ($mm) | `=B11*Scenarios!$B$6+C11*Scenarios!$B$7+D11*Scenarios!$B$8` | 513.93 |
| G11 | Other Consumer & Wholesale | Total allowance ($mm) | `=E11+F11` | 540 |
| H11 | Other Consumer & Wholesale | Reported allowance ($mm) | `=Segment_Inputs!K11` | 540 |
| I11 | Other Consumer & Wholesale | Difference | `=G11-H11` | 0 |
| J11 | Other Consumer & Wholesale | Overlay % of modeled | `=IF(E11=0,0,F11/E11)` | 0.0507 |
| K11 | Other Consumer & Wholesale | Allowance / loans | `=IF(Segment_Inputs!C11=0,0,G11/Segment_Inputs!C11)` | 0.0109 |
| L11 | Other Consumer & Wholesale | Coverage of NCOs (yrs) | `=IF(Segment_Inputs!J11=0,0,G11/Segment_Inputs!J11)` | 6 |
| B12 | Total | Upside ECL | `=SUM(B6:B11)` | 12,434.76 |
| C12 | Total | Baseline ECL | `=SUM(C6:C11)` | 13,817.04 |
| D12 | Total | Downside ECL | `=SUM(D6:D11)` | 19,478.13 |
| E12 | Total | Weighted (modeled) ($mm) | `=SUM(E6:E11)` | 15,238.91 |
| F12 | Total | Qualitative overlay ($mm) | `=SUM(F6:F11)` | 681.09 |
| G12 | Total | Total allowance ($mm) | `=SUM(G6:G11)` | 15,920 |
| H12 | Total | Reported allowance ($mm) | `=SUM(H6:H11)` | 15,920 |
| I12 | Total | Difference | `=SUM(I6:I11)` | 0 |
| J12 | Total | Overlay % of modeled | `=IF(E12=0,0,F12/E12)` | 0.0447 |
| K12 | Total | Allowance / loans | `=IF(Segment_Inputs!C12=0,0,G12/Segment_Inputs!C12)` | 0.0214 |
| L12 | Total | Coverage of NCOs (yrs) | `=IF(Segment_Inputs!J12=0,0,G12/Segment_Inputs!J12)` | 2.61 |
| F14 | Overlay control check (/overlay/ <= 15% of modeled per segment) | Qualitative overlay ($mm) | `=IF(SUMPRODUCT(--(ABS(J6:J11)>0.15))=0,"OK","REVIEW")` | OK |

### Cell notes in Allowance_Summary

- F6: Management qualitative adjustment approved by the Allowance Committee (Dec-2025): captures model limitations, concentration and emerging-risk factors.
- F7: Management qualitative adjustment approved by the Allowance Committee (Dec-2025): captures model limitations, concentration and emerging-risk factors.
- F8: Management qualitative adjustment approved by the Allowance Committee (Dec-2025): captures model limitations, concentration and emerging-risk factors.
- F9: Management qualitative adjustment approved by the Allowance Committee (Dec-2025): captures model limitations, concentration and emerging-risk factors.
- F10: Management qualitative adjustment approved by the Allowance Committee (Dec-2025): captures model limitations, concentration and emerging-risk factors.
- F11: Management qualitative adjustment approved by the Allowance Committee (Dec-2025): captures model limitations, concentration and emerging-risk factors.

## Sheet: README


### CECL Lifetime Expected Credit Loss Model  (MDL-CR-007)


### Meridian Harbor Financial Corp. - model documentation sheet

SYNTHETIC DOCUMENT FOR A PROOF OF CONCEPT. Meridian Harbor Financial Corp. is a fictional institution. All names, figures and events are invented and do not describe any real company.
- **Model ID** MDL-CR-007
- **Model name** CECL Lifetime Expected Credit Loss Model
- **Risk tier** Tier 1 (High)
- **Model owner** Consumer & Wholesale Credit Risk - Allowance Methodology
- **Independent validator** Model Risk Governance & Review (MRGR)
- **Last validation** 2025-11-04
- **Next validation due** 2026-11-30
- **Purpose** Estimates the allowance for credit losses under ASC 326 (CECL) using probability-weighted macroeconomic scenarios and PD x LGD x EAD.
- **Upstream data feeds (APIs)** API-10 Credit Risk Scoring API; API-11 Loan Servicing API; API-14 Macroeconomic Scenario API
- **Downstream disclosures** Annual Report - Allowance for Credit Losses (Note 6); Q2 2026 Earnings Supplement - Credit Trends
- **Units** USD millions unless stated otherwise; rates stored as decimals
- **As-of date** See Assumptions sheet

### Sheets

- **Scenarios** Probability-weighted macroeconomic scenarios (Upside / Baseline / Downside).
- **Segment_Inputs** Exposure at default, remaining life, PD and LGD parameters and macro sensitivities.
- **ECL_Calc** Scenario-conditional lifetime expected credit loss by segment.
- **Allowance_Summary** Probability-weighted allowance, qualitative overlay, reconciliation to the reported allowance and coverage metrics.
- **Sensitivity** Allowance under 100% weight on each single scenario.

### How the model works

- **1.** Scenario PD = base annual PD x (1 + elasticity x (scenario peak unemployment - baseline unemployment) x 100), floored at 0.
- **2.** Lifetime PD = 1 - (1 - scenario PD) ^ remaining life (years).
- **3.** Scenario LGD = base LGD x (1 - LGD sensitivity x collateral price change), capped at 100%. Mortgages use the house price index (HPI); CRE uses the commercial property price index.
- **4.** Scenario ECL = EAD x lifetime PD x scenario LGD. Modeled allowance = sum of scenario weight x ECL.
- **5.** Total allowance = modeled allowance + qualitative overlay approved by the Allowance Committee.

### Key inputs

- **1.** Loan balances (EAD) and remaining life from API-11 Loan Servicing API.
- **2.** PD and LGD parameters from API-10 Credit Risk Scoring API (pool-level, refreshed quarterly).
- **3.** Scenario paths and weights from API-14 Macroeconomic Scenario API (approved by the Scenario Committee).

### Key outputs

- **1.** Allowance for loan losses by portfolio segment and in total.
- **2.** Allowance coverage ratio (allowance / loans) and coverage of annual net charge-offs.
- **3.** Sensitivity of the allowance to a 100% Downside weighting.

### Limits, controls and known limitations

- **1.** Simplified pool-level approach for demonstration; production model uses loan-level cash flows.
- **2.** Unfunded commitments (off-balance-sheet allowance) are excluded.
- **3.** Qualitative overlays must be documented and fall within +/-15% of the modeled allowance per segment.
- **4.** Scenario weights must sum to 100% (check cell on Scenarios sheet).

### Colour legend

- Blue text = hard-coded input / scenario lever
- Black text = formula
- Green text = link to another sheet
- Yellow fill = key assumption

## Sheet: Scenarios

> Macroeconomic Scenarios
> Source: API-14 Macroeconomic Scenario API, scenario set MSC-2025Q4
> SYNTHETIC DOCUMENT FOR A PROOF OF CONCEPT. Meridian Harbor Financial Corp. is a fictional institution. All names, figures and events are invented and do not describe any real company.

| Row | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| 5 | Scenario | Weight | Peak unemployment | Real GDP growth 2026 | House price index chg | CRE price index chg |
| 6 | Upside | 0.2000 | 0.0380 | 0.0260 | 0.0450 | 0.0300 |
| 7 | Baseline | 0.5000 | 0.0440 | 0.0170 | 0.0220 | -0.0100 |
| 8 | Downside | 0.3000 | 0.0680 | -0.0120 | -0.0850 | -0.1400 |
| 9 | Weight check | 1 | OK |  |  |  |
| 11 | Baseline unemployment (anchor) | 0.0440 |  |  |  |  |

### Formulas in Scenarios (3)

| Cell | Row label | Column header | Formula | Value |
|---|---|---|---|---|
| B9 | Weight check | Weight | `=SUM(B6:B8)` | 1 |
| C9 | Weight check | Peak unemployment | `=IF(ABS(B9-1)<0.0001,"OK","WEIGHTS MUST SUM TO 100%")` | OK |
| B11 | Baseline unemployment (anchor) | Weight | `=C7` | 0.0440 |

## Sheet: Segment_Inputs

> Portfolio Segment Inputs
> Balances $mm at 2025-12-31
> SYNTHETIC DOCUMENT FOR A PROOF OF CONCEPT. Meridian Harbor Financial Corp. is a fictional institution. All names, figures and events are invented and do not describe any real company.

| Row | A | B | C | D | E | F | G | H | I | J | K |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 | Segment | Owning LOB | EAD / balance ($mm) | Remaining life (yrs) | Base annual PD | Base LGD | PD elasticity (per 1pp unemp.) | LGD sensitivity to price | Price driver | FY2025 net charge-offs ($mm) | Reported allowance ($mm) |
| 6 | Credit Card | CCB | 138,400 | 1.70 | 0.0374 | 0.8800 | 0.1650 | 0 | None | 4,620 | 8,640 |
| 7 | Residential Mortgage | CCB | 218,600 | 6.50 | 0.0035 | 0.1400 | 0.1400 | 1.80 | HPI | 40 | 820 |
| 8 | Auto | CCB | 64,900 | 2.40 | 0.0104 | 0.4200 | 0.1200 | 0.4000 | None | 410 | 690 |
| 9 | Commercial Real Estate | CIB | 98,200 | 3.80 | 0.0137 | 0.3800 | 0.1500 | 1.60 | CRE | 380 | 2,470 |
| 10 | Commercial & Industrial | CIB | 172,500 | 2.30 | 0.0150 | 0.4100 | 0.1350 | 0 | None | 560 | 2,760 |
| 11 | Other Consumer & Wholesale | AWM/CCB | 49,700 | 2 | 0.0149 | 0.3300 | 0.1000 | 0 | None | 90 | 540 |
| 12 | Total |  | 742,300 |  |  |  |  |  |  | 6,100 | 15,920 |

### Formulas in Segment_Inputs (3)

| Cell | Row label | Column header | Formula | Value |
|---|---|---|---|---|
| C12 | Total | EAD / balance ($mm) | `=SUM(C6:C11)` | 742,300 |
| J12 | Total | FY2025 net charge-offs ($mm) | `=SUM(J6:J11)` | 6,100 |
| K12 | Total | Reported allowance ($mm) | `=SUM(K6:K11)` | 15,920 |

### Cell notes in Segment_Inputs

- K6: Reported in Annual Report Note 6 (Allowance for Credit Losses).
- K7: Reported in Annual Report Note 6 (Allowance for Credit Losses).
- K8: Reported in Annual Report Note 6 (Allowance for Credit Losses).
- K9: Reported in Annual Report Note 6 (Allowance for Credit Losses).
- K10: Reported in Annual Report Note 6 (Allowance for Credit Losses).
- K11: Reported in Annual Report Note 6 (Allowance for Credit Losses).

## Sheet: ECL_Calc

> Scenario-Conditional Lifetime ECL
> One block per scenario; rows = portfolio segments
> SYNTHETIC DOCUMENT FOR A PROOF OF CONCEPT. Meridian Harbor Financial Corp. is a fictional institution. All names, figures and events are invented and do not describe any real company.

| Row | A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|---|
| 5 | Scenario: Upside |  |  |  |  |  |  |
| 6 | Segment | Scenario PD (annual) | Lifetime PD | Collateral price chg | Scenario LGD | EAD ($mm) | Lifetime ECL ($mm) |
| 7 | Credit Card | 0.0337 | 0.0566 | 0 | 0.8800 | 138,400 | 6,894.36 |
| 8 | Residential Mortgage | 0.0032 | 0.0207 | 0.0450 | 0.1287 | 218,600 | 580.96 |
| 9 | Auto | 0.0097 | 0.0230 | 0 | 0.4200 | 64,900 | 627.11 |
| 10 | Commercial Real Estate | 0.0125 | 0.0466 | 0.0300 | 0.3618 | 98,200 | 1,653.82 |
| 11 | Commercial & Industrial | 0.0138 | 0.0314 | 0 | 0.4100 | 172,500 | 2,222.31 |
| 12 | Other Consumer & Wholesale | 0.0140 | 0.0278 | 0 | 0.3300 | 49,700 | 456.21 |
| 13 | Total - Upside |  |  |  |  |  | 12,434.76 |
| 15 | Scenario: Baseline |  |  |  |  |  |  |
| 16 | Segment | Scenario PD (annual) | Lifetime PD | Collateral price chg | Scenario LGD | EAD ($mm) | Lifetime ECL ($mm) |
| 17 | Credit Card | 0.0374 | 0.0627 | 0 | 0.8800 | 138,400 | 7,641.79 |
| 18 | Residential Mortgage | 0.0035 | 0.0225 | 0.0220 | 0.1345 | 218,600 | 662.27 |
| 19 | Auto | 0.0104 | 0.0248 | 0 | 0.4200 | 64,900 | 675.41 |
| 20 | Commercial Real Estate | 0.0137 | 0.0511 | -0.0100 | 0.3861 | 98,200 | 1,936.21 |
| 21 | Commercial & Industrial | 0.0150 | 0.0342 | 0 | 0.4100 | 172,500 | 2,416.26 |
| 22 | Other Consumer & Wholesale | 0.0149 | 0.0296 | 0 | 0.3300 | 49,700 | 485.11 |
| 23 | Total - Baseline |  |  |  |  |  | 13,817.04 |
| 25 | Scenario: Downside |  |  |  |  |  |  |
| 26 | Segment | Scenario PD (annual) | Lifetime PD | Collateral price chg | Scenario LGD | EAD ($mm) | Lifetime ECL ($mm) |
| 27 | Credit Card | 0.0522 | 0.0871 | 0 | 0.8800 | 138,400 | 10,611.39 |
| 28 | Residential Mortgage | 0.0047 | 0.0300 | -0.0850 | 0.1614 | 218,600 | 1,058.80 |
| 29 | Auto | 0.0134 | 0.0318 | 0 | 0.4200 | 64,900 | 868.10 |
| 30 | Commercial Real Estate | 0.0186 | 0.0690 | -0.1400 | 0.4651 | 98,200 | 3,150.43 |
| 31 | Commercial & Industrial | 0.0199 | 0.0451 | 0 | 0.4100 | 172,500 | 3,188.96 |
| 32 | Other Consumer & Wholesale | 0.0185 | 0.0366 | 0 | 0.3300 | 49,700 | 600.45 |
| 33 | Total - Downside |  |  |  |  |  | 19,478.13 |

### Formulas in ECL_Calc (129)

| Cell | Row label | Column header | Formula | Value |
|---|---|---|---|---|
| A7 | Credit Card | Scenario: Upside | `=Segment_Inputs!A6` | Credit Card |
| B7 | Credit Card |  | `=MAX(0,Segment_Inputs!E6*(1+Segment_Inputs!G6*(Scenarios!$C$6-Scenarios!$B$11)*100))` | 0.0337 |
| C7 | Credit Card |  | `=1-(1-B7)^Segment_Inputs!D6` | 0.0566 |
| D7 | Credit Card |  | `=IF(Segment_Inputs!I6="HPI",Scenarios!$E$6,IF(Segment_Inputs!I6="CRE",Scenarios!$F$6,0))` | 0 |
| E7 | Credit Card |  | `=MIN(1,MAX(0,Segment_Inputs!F6*(1-Segment_Inputs!H6*D7)))` | 0.8800 |
| F7 | Credit Card |  | `=Segment_Inputs!C6` | 138,400 |
| G7 | Credit Card |  | `=F7*C7*E7` | 6,894.36 |
| A8 | Residential Mortgage | Scenario: Upside | `=Segment_Inputs!A7` | Residential Mortgage |
| B8 | Residential Mortgage |  | `=MAX(0,Segment_Inputs!E7*(1+Segment_Inputs!G7*(Scenarios!$C$6-Scenarios!$B$11)*100))` | 0.0032 |
| C8 | Residential Mortgage |  | `=1-(1-B8)^Segment_Inputs!D7` | 0.0207 |
| D8 | Residential Mortgage |  | `=IF(Segment_Inputs!I7="HPI",Scenarios!$E$6,IF(Segment_Inputs!I7="CRE",Scenarios!$F$6,0))` | 0.0450 |
| E8 | Residential Mortgage |  | `=MIN(1,MAX(0,Segment_Inputs!F7*(1-Segment_Inputs!H7*D8)))` | 0.1287 |
| F8 | Residential Mortgage |  | `=Segment_Inputs!C7` | 218,600 |
| G8 | Residential Mortgage |  | `=F8*C8*E8` | 580.96 |
| A9 | Auto | Scenario: Upside | `=Segment_Inputs!A8` | Auto |
| B9 | Auto |  | `=MAX(0,Segment_Inputs!E8*(1+Segment_Inputs!G8*(Scenarios!$C$6-Scenarios!$B$11)*100))` | 0.0097 |
| C9 | Auto |  | `=1-(1-B9)^Segment_Inputs!D8` | 0.0230 |
| D9 | Auto |  | `=IF(Segment_Inputs!I8="HPI",Scenarios!$E$6,IF(Segment_Inputs!I8="CRE",Scenarios!$F$6,0))` | 0 |
| E9 | Auto |  | `=MIN(1,MAX(0,Segment_Inputs!F8*(1-Segment_Inputs!H8*D9)))` | 0.4200 |
| F9 | Auto |  | `=Segment_Inputs!C8` | 64,900 |
| G9 | Auto |  | `=F9*C9*E9` | 627.11 |
| A10 | Commercial Real Estate | Scenario: Upside | `=Segment_Inputs!A9` | Commercial Real Estate |
| B10 | Commercial Real Estate |  | `=MAX(0,Segment_Inputs!E9*(1+Segment_Inputs!G9*(Scenarios!$C$6-Scenarios!$B$11)*100))` | 0.0125 |
| C10 | Commercial Real Estate |  | `=1-(1-B10)^Segment_Inputs!D9` | 0.0466 |
| D10 | Commercial Real Estate |  | `=IF(Segment_Inputs!I9="HPI",Scenarios!$E$6,IF(Segment_Inputs!I9="CRE",Scenarios!$F$6,0))` | 0.0300 |
| E10 | Commercial Real Estate |  | `=MIN(1,MAX(0,Segment_Inputs!F9*(1-Segment_Inputs!H9*D10)))` | 0.3618 |
| F10 | Commercial Real Estate |  | `=Segment_Inputs!C9` | 98,200 |
| G10 | Commercial Real Estate |  | `=F10*C10*E10` | 1,653.82 |
| A11 | Commercial & Industrial | Scenario: Upside | `=Segment_Inputs!A10` | Commercial & Industrial |
| B11 | Commercial & Industrial |  | `=MAX(0,Segment_Inputs!E10*(1+Segment_Inputs!G10*(Scenarios!$C$6-Scenarios!$B$11)*100))` | 0.0138 |
| C11 | Commercial & Industrial |  | `=1-(1-B11)^Segment_Inputs!D10` | 0.0314 |
| D11 | Commercial & Industrial |  | `=IF(Segment_Inputs!I10="HPI",Scenarios!$E$6,IF(Segment_Inputs!I10="CRE",Scenarios!$F$6,0))` | 0 |
| E11 | Commercial & Industrial |  | `=MIN(1,MAX(0,Segment_Inputs!F10*(1-Segment_Inputs!H10*D11)))` | 0.4100 |
| F11 | Commercial & Industrial |  | `=Segment_Inputs!C10` | 172,500 |
| G11 | Commercial & Industrial |  | `=F11*C11*E11` | 2,222.31 |
| A12 | Other Consumer & Wholesale | Scenario: Upside | `=Segment_Inputs!A11` | Other Consumer & Wholesale |
| B12 | Other Consumer & Wholesale |  | `=MAX(0,Segment_Inputs!E11*(1+Segment_Inputs!G11*(Scenarios!$C$6-Scenarios!$B$11)*100))` | 0.0140 |
| C12 | Other Consumer & Wholesale |  | `=1-(1-B12)^Segment_Inputs!D11` | 0.0278 |
| D12 | Other Consumer & Wholesale |  | `=IF(Segment_Inputs!I11="HPI",Scenarios!$E$6,IF(Segment_Inputs!I11="CRE",Scenarios!$F$6,0))` | 0 |
| E12 | Other Consumer & Wholesale |  | `=MIN(1,MAX(0,Segment_Inputs!F11*(1-Segment_Inputs!H11*D12)))` | 0.3300 |
| F12 | Other Consumer & Wholesale |  | `=Segment_Inputs!C11` | 49,700 |
| G12 | Other Consumer & Wholesale |  | `=F12*C12*E12` | 456.21 |
| G13 | Total - Upside |  | `=SUM(G7:G12)` | 12,434.76 |
| A17 | Credit Card | Scenario: Upside | `=Segment_Inputs!A6` | Credit Card |
| B17 | Credit Card |  | `=MAX(0,Segment_Inputs!E6*(1+Segment_Inputs!G6*(Scenarios!$C$7-Scenarios!$B$11)*100))` | 0.0374 |
| C17 | Credit Card |  | `=1-(1-B17)^Segment_Inputs!D6` | 0.0627 |
| D17 | Credit Card |  | `=IF(Segment_Inputs!I6="HPI",Scenarios!$E$7,IF(Segment_Inputs!I6="CRE",Scenarios!$F$7,0))` | 0 |
| E17 | Credit Card |  | `=MIN(1,MAX(0,Segment_Inputs!F6*(1-Segment_Inputs!H6*D17)))` | 0.8800 |
| F17 | Credit Card |  | `=Segment_Inputs!C6` | 138,400 |
| G17 | Credit Card |  | `=F17*C17*E17` | 7,641.79 |
| A18 | Residential Mortgage | Scenario: Upside | `=Segment_Inputs!A7` | Residential Mortgage |
| B18 | Residential Mortgage |  | `=MAX(0,Segment_Inputs!E7*(1+Segment_Inputs!G7*(Scenarios!$C$7-Scenarios!$B$11)*100))` | 0.0035 |
| C18 | Residential Mortgage |  | `=1-(1-B18)^Segment_Inputs!D7` | 0.0225 |
| D18 | Residential Mortgage |  | `=IF(Segment_Inputs!I7="HPI",Scenarios!$E$7,IF(Segment_Inputs!I7="CRE",Scenarios!$F$7,0))` | 0.0220 |
| E18 | Residential Mortgage |  | `=MIN(1,MAX(0,Segment_Inputs!F7*(1-Segment_Inputs!H7*D18)))` | 0.1345 |
| F18 | Residential Mortgage |  | `=Segment_Inputs!C7` | 218,600 |
| G18 | Residential Mortgage |  | `=F18*C18*E18` | 662.27 |
| A19 | Auto | Scenario: Upside | `=Segment_Inputs!A8` | Auto |
| B19 | Auto |  | `=MAX(0,Segment_Inputs!E8*(1+Segment_Inputs!G8*(Scenarios!$C$7-Scenarios!$B$11)*100))` | 0.0104 |
| C19 | Auto |  | `=1-(1-B19)^Segment_Inputs!D8` | 0.0248 |
| D19 | Auto |  | `=IF(Segment_Inputs!I8="HPI",Scenarios!$E$7,IF(Segment_Inputs!I8="CRE",Scenarios!$F$7,0))` | 0 |
| E19 | Auto |  | `=MIN(1,MAX(0,Segment_Inputs!F8*(1-Segment_Inputs!H8*D19)))` | 0.4200 |
| F19 | Auto |  | `=Segment_Inputs!C8` | 64,900 |
| G19 | Auto |  | `=F19*C19*E19` | 675.41 |
| A20 | Commercial Real Estate | Scenario: Upside | `=Segment_Inputs!A9` | Commercial Real Estate |
| B20 | Commercial Real Estate |  | `=MAX(0,Segment_Inputs!E9*(1+Segment_Inputs!G9*(Scenarios!$C$7-Scenarios!$B$11)*100))` | 0.0137 |
| C20 | Commercial Real Estate |  | `=1-(1-B20)^Segment_Inputs!D9` | 0.0511 |
| D20 | Commercial Real Estate |  | `=IF(Segment_Inputs!I9="HPI",Scenarios!$E$7,IF(Segment_Inputs!I9="CRE",Scenarios!$F$7,0))` | -0.0100 |
| E20 | Commercial Real Estate |  | `=MIN(1,MAX(0,Segment_Inputs!F9*(1-Segment_Inputs!H9*D20)))` | 0.3861 |
| F20 | Commercial Real Estate |  | `=Segment_Inputs!C9` | 98,200 |
| G20 | Commercial Real Estate |  | `=F20*C20*E20` | 1,936.21 |
| A21 | Commercial & Industrial | Scenario: Upside | `=Segment_Inputs!A10` | Commercial & Industrial |
| B21 | Commercial & Industrial |  | `=MAX(0,Segment_Inputs!E10*(1+Segment_Inputs!G10*(Scenarios!$C$7-Scenarios!$B$11)*100))` | 0.0150 |
| C21 | Commercial & Industrial |  | `=1-(1-B21)^Segment_Inputs!D10` | 0.0342 |
| D21 | Commercial & Industrial |  | `=IF(Segment_Inputs!I10="HPI",Scenarios!$E$7,IF(Segment_Inputs!I10="CRE",Scenarios!$F$7,0))` | 0 |
| E21 | Commercial & Industrial |  | `=MIN(1,MAX(0,Segment_Inputs!F10*(1-Segment_Inputs!H10*D21)))` | 0.4100 |
| F21 | Commercial & Industrial |  | `=Segment_Inputs!C10` | 172,500 |
| G21 | Commercial & Industrial |  | `=F21*C21*E21` | 2,416.26 |
| A22 | Other Consumer & Wholesale | Scenario: Upside | `=Segment_Inputs!A11` | Other Consumer & Wholesale |
| B22 | Other Consumer & Wholesale |  | `=MAX(0,Segment_Inputs!E11*(1+Segment_Inputs!G11*(Scenarios!$C$7-Scenarios!$B$11)*100))` | 0.0149 |
| C22 | Other Consumer & Wholesale |  | `=1-(1-B22)^Segment_Inputs!D11` | 0.0296 |
| D22 | Other Consumer & Wholesale |  | `=IF(Segment_Inputs!I11="HPI",Scenarios!$E$7,IF(Segment_Inputs!I11="CRE",Scenarios!$F$7,0))` | 0 |
| E22 | Other Consumer & Wholesale |  | `=MIN(1,MAX(0,Segment_Inputs!F11*(1-Segment_Inputs!H11*D22)))` | 0.3300 |
| F22 | Other Consumer & Wholesale |  | `=Segment_Inputs!C11` | 49,700 |
| G22 | Other Consumer & Wholesale |  | `=F22*C22*E22` | 485.11 |
| G23 | Total - Baseline |  | `=SUM(G17:G22)` | 13,817.04 |
| A27 | Credit Card | Scenario: Upside | `=Segment_Inputs!A6` | Credit Card |
| B27 | Credit Card |  | `=MAX(0,Segment_Inputs!E6*(1+Segment_Inputs!G6*(Scenarios!$C$8-Scenarios!$B$11)*100))` | 0.0522 |
| C27 | Credit Card |  | `=1-(1-B27)^Segment_Inputs!D6` | 0.0871 |
| D27 | Credit Card |  | `=IF(Segment_Inputs!I6="HPI",Scenarios!$E$8,IF(Segment_Inputs!I6="CRE",Scenarios!$F$8,0))` | 0 |
| E27 | Credit Card |  | `=MIN(1,MAX(0,Segment_Inputs!F6*(1-Segment_Inputs!H6*D27)))` | 0.8800 |
| F27 | Credit Card |  | `=Segment_Inputs!C6` | 138,400 |
| G27 | Credit Card |  | `=F27*C27*E27` | 10,611.39 |
| A28 | Residential Mortgage | Scenario: Upside | `=Segment_Inputs!A7` | Residential Mortgage |
| B28 | Residential Mortgage |  | `=MAX(0,Segment_Inputs!E7*(1+Segment_Inputs!G7*(Scenarios!$C$8-Scenarios!$B$11)*100))` | 0.0047 |
| C28 | Residential Mortgage |  | `=1-(1-B28)^Segment_Inputs!D7` | 0.0300 |
| D28 | Residential Mortgage |  | `=IF(Segment_Inputs!I7="HPI",Scenarios!$E$8,IF(Segment_Inputs!I7="CRE",Scenarios!$F$8,0))` | -0.0850 |
| E28 | Residential Mortgage |  | `=MIN(1,MAX(0,Segment_Inputs!F7*(1-Segment_Inputs!H7*D28)))` | 0.1614 |
| F28 | Residential Mortgage |  | `=Segment_Inputs!C7` | 218,600 |
| G28 | Residential Mortgage |  | `=F28*C28*E28` | 1,058.80 |
| A29 | Auto | Scenario: Upside | `=Segment_Inputs!A8` | Auto |
| B29 | Auto |  | `=MAX(0,Segment_Inputs!E8*(1+Segment_Inputs!G8*(Scenarios!$C$8-Scenarios!$B$11)*100))` | 0.0134 |
| C29 | Auto |  | `=1-(1-B29)^Segment_Inputs!D8` | 0.0318 |
| D29 | Auto |  | `=IF(Segment_Inputs!I8="HPI",Scenarios!$E$8,IF(Segment_Inputs!I8="CRE",Scenarios!$F$8,0))` | 0 |
| E29 | Auto |  | `=MIN(1,MAX(0,Segment_Inputs!F8*(1-Segment_Inputs!H8*D29)))` | 0.4200 |
| F29 | Auto |  | `=Segment_Inputs!C8` | 64,900 |
| G29 | Auto |  | `=F29*C29*E29` | 868.10 |
| A30 | Commercial Real Estate | Scenario: Upside | `=Segment_Inputs!A9` | Commercial Real Estate |
| B30 | Commercial Real Estate |  | `=MAX(0,Segment_Inputs!E9*(1+Segment_Inputs!G9*(Scenarios!$C$8-Scenarios!$B$11)*100))` | 0.0186 |
| C30 | Commercial Real Estate |  | `=1-(1-B30)^Segment_Inputs!D9` | 0.0690 |
| D30 | Commercial Real Estate |  | `=IF(Segment_Inputs!I9="HPI",Scenarios!$E$8,IF(Segment_Inputs!I9="CRE",Scenarios!$F$8,0))` | -0.1400 |
| E30 | Commercial Real Estate |  | `=MIN(1,MAX(0,Segment_Inputs!F9*(1-Segment_Inputs!H9*D30)))` | 0.4651 |
| F30 | Commercial Real Estate |  | `=Segment_Inputs!C9` | 98,200 |
| G30 | Commercial Real Estate |  | `=F30*C30*E30` | 3,150.43 |
| A31 | Commercial & Industrial | Scenario: Upside | `=Segment_Inputs!A10` | Commercial & Industrial |
| B31 | Commercial & Industrial |  | `=MAX(0,Segment_Inputs!E10*(1+Segment_Inputs!G10*(Scenarios!$C$8-Scenarios!$B$11)*100))` | 0.0199 |
| C31 | Commercial & Industrial |  | `=1-(1-B31)^Segment_Inputs!D10` | 0.0451 |
| D31 | Commercial & Industrial |  | `=IF(Segment_Inputs!I10="HPI",Scenarios!$E$8,IF(Segment_Inputs!I10="CRE",Scenarios!$F$8,0))` | 0 |
| E31 | Commercial & Industrial |  | `=MIN(1,MAX(0,Segment_Inputs!F10*(1-Segment_Inputs!H10*D31)))` | 0.4100 |
| F31 | Commercial & Industrial |  | `=Segment_Inputs!C10` | 172,500 |
| G31 | Commercial & Industrial |  | `=F31*C31*E31` | 3,188.96 |
| A32 | Other Consumer & Wholesale | Scenario: Upside | `=Segment_Inputs!A11` | Other Consumer & Wholesale |
| B32 | Other Consumer & Wholesale |  | `=MAX(0,Segment_Inputs!E11*(1+Segment_Inputs!G11*(Scenarios!$C$8-Scenarios!$B$11)*100))` | 0.0185 |
| C32 | Other Consumer & Wholesale |  | `=1-(1-B32)^Segment_Inputs!D11` | 0.0366 |
| D32 | Other Consumer & Wholesale |  | `=IF(Segment_Inputs!I11="HPI",Scenarios!$E$8,IF(Segment_Inputs!I11="CRE",Scenarios!$F$8,0))` | 0 |
| E32 | Other Consumer & Wholesale |  | `=MIN(1,MAX(0,Segment_Inputs!F11*(1-Segment_Inputs!H11*D32)))` | 0.3300 |
| F32 | Other Consumer & Wholesale |  | `=Segment_Inputs!C11` | 49,700 |
| G32 | Other Consumer & Wholesale |  | `=F32*C32*E32` | 600.45 |
| G33 | Total - Downside |  | `=SUM(G27:G32)` | 19,478.13 |

## Sheet: Sensitivity

> Allowance Sensitivity to Scenario Weighting
> Modeled allowance plus the same qualitative overlay
> SYNTHETIC DOCUMENT FOR A PROOF OF CONCEPT. Meridian Harbor Financial Corp. is a fictional institution. All names, figures and events are invented and do not describe any real company.

| Row | A | B | C | D | E |
|---|---|---|---|---|---|
| 5 | Weighting | Modeled ECL ($mm) | Plus overlay ($mm) | Change vs reported ($mm) | Change (%) |
| 6 | 100% Upside | 12,434.76 | 13,115.85 | -2,804.15 | -0.1761 |
| 7 | 100% Baseline | 13,817.04 | 14,498.13 | -1,421.87 | -0.0893 |
| 8 | 100% Downside | 19,478.13 | 20,159.22 | 4,239.22 | 0.2663 |
| 9 | Probability-weighted (reported) | 15,238.91 | 15,920 | 0 | 0 |

### Formulas in Sensitivity (16)

| Cell | Row label | Column header | Formula | Value |
|---|---|---|---|---|
| B6 | 100% Upside | Modeled ECL ($mm) | `=Allowance_Summary!B12` | 12,434.76 |
| C6 | 100% Upside | Plus overlay ($mm) | `=B6+Allowance_Summary!$F$12` | 13,115.85 |
| D6 | 100% Upside | Change vs reported ($mm) | `=C6-Allowance_Summary!$H$12` | -2,804.15 |
| E6 | 100% Upside | Change (%) | `=IF(Allowance_Summary!$H$12=0,0,D6/Allowance_Summary!$H$12)` | -0.1761 |
| B7 | 100% Baseline | Modeled ECL ($mm) | `=Allowance_Summary!C12` | 13,817.04 |
| C7 | 100% Baseline | Plus overlay ($mm) | `=B7+Allowance_Summary!$F$12` | 14,498.13 |
| D7 | 100% Baseline | Change vs reported ($mm) | `=C7-Allowance_Summary!$H$12` | -1,421.87 |
| E7 | 100% Baseline | Change (%) | `=IF(Allowance_Summary!$H$12=0,0,D7/Allowance_Summary!$H$12)` | -0.0893 |
| B8 | 100% Downside | Modeled ECL ($mm) | `=Allowance_Summary!D12` | 19,478.13 |
| C8 | 100% Downside | Plus overlay ($mm) | `=B8+Allowance_Summary!$F$12` | 20,159.22 |
| D8 | 100% Downside | Change vs reported ($mm) | `=C8-Allowance_Summary!$H$12` | 4,239.22 |
| E8 | 100% Downside | Change (%) | `=IF(Allowance_Summary!$H$12=0,0,D8/Allowance_Summary!$H$12)` | 0.2663 |
| B9 | Probability-weighted (reported) | Modeled ECL ($mm) | `=Allowance_Summary!E12` | 15,238.91 |
| C9 | Probability-weighted (reported) | Plus overlay ($mm) | `=B9+Allowance_Summary!$F$12` | 15,920 |
| D9 | Probability-weighted (reported) | Change vs reported ($mm) | `=C9-Allowance_Summary!$H$12` | 0 |
| E9 | Probability-weighted (reported) | Change (%) | `=IF(Allowance_Summary!$H$12=0,0,D9/Allowance_Summary!$H$12)` | 0 |
