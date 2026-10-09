<!-- source: raw/models/NII_Sensitivity_Model.xlsx | converted by tools/convert_corpus.py -->
# Excel model: NII_Sensitivity_Model.xlsx

This file is a text rendering of an Excel workbook. Each sheet is shown as a value grid, followed by the list of formulas in that sheet (cell, row label, column header, formula, computed value). Blue-font cells in the workbook are inputs; black cells are formulas; green cells link to other sheets.

## Sheet: README


### Net Interest Income Sensitivity Model  (MDL-ALM-014)


### Meridian Harbor Financial Corp. - model documentation sheet

SYNTHETIC DOCUMENT FOR A PROOF OF CONCEPT. Meridian Harbor Financial Corp. is a fictional institution. All names, figures and events are invented and do not describe any real company.
- **Model ID** MDL-ALM-014
- **Model name** Net Interest Income Sensitivity Model
- **Risk tier** Tier 1 (High)
- **Model owner** Corporate Treasury - Asset & Liability Management
- **Independent validator** Model Risk Governance & Review (MRGR)
- **Last validation** 2025-09-18
- **Next validation due** 2026-09-30
- **Purpose** Projects 12-month net interest income under parallel rate shocks and economic value of equity (EVE) sensitivity for IRRBB reporting.
- **Upstream data feeds (APIs)** API-12 Market Data API; API-15 Treasury Liquidity Positions API; API-11 Loan Servicing API
- **Downstream disclosures** Annual Report - Market Risk Management; Pillar 3 - Interest Rate Risk in the Banking Book
- **Units** USD millions unless stated otherwise; rates stored as decimals
- **As-of date** See Assumptions sheet

### Sheets

- **Assumptions** As-of date, policy rate, rate shock grid, repricing timing conventions, risk limits.
- **Balance_Sheet** Rate-sensitive assets and liabilities with balances, yields/costs, repricing profile, deposit betas and modified durations.
- **NII_Projection** Base-case 12-month NII and the change in NII for each parallel shock.
- **EVE** Economic value of equity sensitivity using a modified-duration approximation.
- **Summary** Results versus Board-approved IRRBB limits; feeds Annual Report and Pillar 3.

### How the model works

- **1.** Base NII = sum over assets of balance x yield, minus sum over liabilities of balance x cost.
- **2.** For each shock, every position reprices only for the fraction of the 12-month horizon remaining after its repricing date (bucket midpoint): 0-3m reprices at month 1.5, 3-12m at month 7.5.
- **3.** Asset rates move one-for-one with the shock (asset beta in column L); liability rates move by shock x deposit beta.
- **4.** Change in NII = asset repricing effect - liability repricing effect. Static balance sheet (no growth, no mix shift).
- **5.** EVE change = -(asset value x modified duration - liability value x modified duration) x shock.

### Key inputs

- **1.** Balances and yields from API-15 Treasury Liquidity Positions API (month-end snapshot).
- **2.** Loan repricing profiles from API-11 Loan Servicing API.
- **3.** Yield curve and policy rate from API-12 Market Data API.
- **4.** Deposit betas from the Deposit Behaviour sub-model (annual calibration, MRGR approved).

### Key outputs

- **1.** 12-month NII under +/-100 bp and +/-200 bp parallel shocks.
- **2.** EVE sensitivity as a % of Tier 1 capital.
- **3.** Limit utilisation flags used in ALCO reporting.

### Limits, controls and known limitations

- **1.** Board limit: NII decline no greater than 7.0% of base NII in any parallel shock.
- **2.** Board limit: EVE decline no greater than 15.0% of Tier 1 capital.
- **3.** Limitations: parallel shocks only (no twists), static balance sheet, no rate floors on deposit costs below zero, betas held constant across shock sizes.
- **4.** Compensating control: dynamic balance-sheet simulation run quarterly in the ALM engine.

### Colour legend

- Blue text = hard-coded input / scenario lever
- Black text = formula
- Green text = link to another sheet
- Yellow fill = key assumption

## Sheet: Summary

> IRRBB Summary vs Limits
> Feeds: Annual Report (Market Risk) and Pillar 3 (IRRBB)
> SYNTHETIC DOCUMENT FOR A PROOF OF CONCEPT. Meridian Harbor Financial Corp. is a fictional institution. All names, figures and events are invented and do not describe any real company.

| Row | A | B | C | D | E | F | G | H | I |
|---|---|---|---|---|---|---|---|---|---|
| 5 | Scenario | Shock (bps) | Projected NII ($mm) | Change in NII ($mm) | Change in NII (%) | NII limit status | Change in EVE ($mm) | EVE % of Tier 1 | EVE limit status |
| 6 | Down 200 | -200 | 47,220.02 | -3,016.89 | -0.0601 | Within limit | 2,737.40 | 0.0247 | Within limit |
| 7 | Down 100 | -100 | 48,728.47 | -1,508.44 | -0.0300 | Within limit | 1,368.70 | 0.0124 | Within limit |
| 8 | Base | 0 | 50,236.91 | 0 | 0 | Within limit | 0 | 0 | Within limit |
| 9 | Up 100 | 100 | 51,745.35 | 1,508.44 | 0.0300 | Within limit | -1,368.70 | -0.0124 | Within limit |
| 10 | Up 200 | 200 | 53,253.80 | 3,016.89 | 0.0601 | Within limit | -2,737.40 | -0.0247 | Within limit |

### Formulas in Summary (45)

| Cell | Row label | Column header | Formula | Value |
|---|---|---|---|---|
| A6 | Down 200 | Scenario | `=Assumptions!A17` | Down 200 |
| B6 | Down 200 | Shock (bps) | `=Assumptions!B17` | -200 |
| C6 | Down 200 | Projected NII ($mm) | `=NII_Projection!D24` | 47,220.02 |
| D6 | Down 200 | Change in NII ($mm) | `=NII_Projection!D22` | -3,016.89 |
| E6 | Down 200 | Change in NII (%) | `=NII_Projection!D25` | -0.0601 |
| F6 | Down 200 | NII limit status | `=IF(E6<-Assumptions!$B$11,"BREACH","Within limit")` | Within limit |
| G6 | Down 200 | Change in EVE ($mm) | `=EVE!F22` | 2,737.40 |
| H6 | Down 200 | EVE % of Tier 1 | `=EVE!F24` | 0.0247 |
| I6 | Down 200 | EVE limit status | `=IF(H6<-Assumptions!$B$12,"BREACH","Within limit")` | Within limit |
| A7 | Down 100 | Scenario | `=Assumptions!A18` | Down 100 |
| B7 | Down 100 | Shock (bps) | `=Assumptions!B18` | -100 |
| C7 | Down 100 | Projected NII ($mm) | `=NII_Projection!E24` | 48,728.47 |
| D7 | Down 100 | Change in NII ($mm) | `=NII_Projection!E22` | -1,508.44 |
| E7 | Down 100 | Change in NII (%) | `=NII_Projection!E25` | -0.0300 |
| F7 | Down 100 | NII limit status | `=IF(E7<-Assumptions!$B$11,"BREACH","Within limit")` | Within limit |
| G7 | Down 100 | Change in EVE ($mm) | `=EVE!G22` | 1,368.70 |
| H7 | Down 100 | EVE % of Tier 1 | `=EVE!G24` | 0.0124 |
| I7 | Down 100 | EVE limit status | `=IF(H7<-Assumptions!$B$12,"BREACH","Within limit")` | Within limit |
| A8 | Base | Scenario | `=Assumptions!A19` | Base |
| B8 | Base | Shock (bps) | `=Assumptions!B19` | 0 |
| C8 | Base | Projected NII ($mm) | `=NII_Projection!F24` | 50,236.91 |
| D8 | Base | Change in NII ($mm) | `=NII_Projection!F22` | 0 |
| E8 | Base | Change in NII (%) | `=NII_Projection!F25` | 0 |
| F8 | Base | NII limit status | `=IF(E8<-Assumptions!$B$11,"BREACH","Within limit")` | Within limit |
| G8 | Base | Change in EVE ($mm) | `=EVE!H22` | 0 |
| H8 | Base | EVE % of Tier 1 | `=EVE!H24` | 0 |
| I8 | Base | EVE limit status | `=IF(H8<-Assumptions!$B$12,"BREACH","Within limit")` | Within limit |
| A9 | Up 100 | Scenario | `=Assumptions!A20` | Up 100 |
| B9 | Up 100 | Shock (bps) | `=Assumptions!B20` | 100 |
| C9 | Up 100 | Projected NII ($mm) | `=NII_Projection!G24` | 51,745.35 |
| D9 | Up 100 | Change in NII ($mm) | `=NII_Projection!G22` | 1,508.44 |
| E9 | Up 100 | Change in NII (%) | `=NII_Projection!G25` | 0.0300 |
| F9 | Up 100 | NII limit status | `=IF(E9<-Assumptions!$B$11,"BREACH","Within limit")` | Within limit |
| G9 | Up 100 | Change in EVE ($mm) | `=EVE!I22` | -1,368.70 |
| H9 | Up 100 | EVE % of Tier 1 | `=EVE!I24` | -0.0124 |
| I9 | Up 100 | EVE limit status | `=IF(H9<-Assumptions!$B$12,"BREACH","Within limit")` | Within limit |
| A10 | Up 200 | Scenario | `=Assumptions!A21` | Up 200 |
| B10 | Up 200 | Shock (bps) | `=Assumptions!B21` | 200 |
| C10 | Up 200 | Projected NII ($mm) | `=NII_Projection!H24` | 53,253.80 |
| D10 | Up 200 | Change in NII ($mm) | `=NII_Projection!H22` | 3,016.89 |
| E10 | Up 200 | Change in NII (%) | `=NII_Projection!H25` | 0.0601 |
| F10 | Up 200 | NII limit status | `=IF(E10<-Assumptions!$B$11,"BREACH","Within limit")` | Within limit |
| G10 | Up 200 | Change in EVE ($mm) | `=EVE!J22` | -2,737.40 |
| H10 | Up 200 | EVE % of Tier 1 | `=EVE!J24` | -0.0247 |
| I10 | Up 200 | EVE limit status | `=IF(H10<-Assumptions!$B$12,"BREACH","Within limit")` | Within limit |

## Sheet: Assumptions

> Assumptions
> All rates as decimals; shocks in basis points
> SYNTHETIC DOCUMENT FOR A PROOF OF CONCEPT. Meridian Harbor Financial Corp. is a fictional institution. All names, figures and events are invented and do not describe any real company.

| Row | A | B | C |
|---|---|---|---|
| 5 | Assumption | Value | Source / note |
| 6 | As-of date | 2025-12-31 | Month-end snapshot used for the FY2025 Annual Report. |
| 7 | Policy rate (fed funds upper bound) | 0.0375 | Source: API-12 Market Data API, series POLICY.FEDFUNDS.UB |
| 8 | Projection horizon (months) | 12 | Standard IRRBB earnings horizon. |
| 9 | Repricing month - bucket 0-3m (midpoint) | 1.50 | Convention: midpoint of bucket. |
| 10 | Repricing month - bucket 3-12m (midpoint) | 7.50 | Convention: midpoint of bucket. |
| 11 | NII limit (max decline, % of base) | 0.0700 | Board Risk Committee limit, approved 2025-03. |
| 12 | EVE limit (max decline, % of Tier 1) | 0.1500 | Board Risk Committee limit, approved 2025-03. |
| 13 | Tier 1 capital ($mm) | 110,620 | Source: API-16 Regulatory Reporting API, YE2025. |
| 16 | Scenario | Shock (bps) |  |
| 17 | Down 200 | -200 |  |
| 18 | Down 100 | -100 |  |
| 19 | Base | 0 |  |
| 20 | Up 100 | 100 |  |
| 21 | Up 200 | 200 |  |

## Sheet: Balance_Sheet

> Rate-Sensitive Balance Sheet
> Balances $mm at 2025-12-31; repricing shares sum to 100% per row
> SYNTHETIC DOCUMENT FOR A PROOF OF CONCEPT. Meridian Harbor Financial Corp. is a fictional institution. All names, figures and events are invented and do not describe any real company.

| Row | A | B | C | D | E | F | G | H | I | J | K | L | M |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 | Line | Side | Balance ($mm) | Yield / cost | Reprice 0-3m | Reprice 3-12m | Reprice 1-5y | Reprice >5y | Share check | Annual interest ($mm) | Mod. duration (yrs) | Rate beta | Feed |
| 6 | Deposits with banks & fed funds sold | Asset | 246,900 | 0.0372 | 1 | 0 | 0 | 0 | OK | 9,184.68 | 0.1000 | 1 | API-15 |
| 7 | Investment securities (AFS + HTM) | Asset | 170,900 | 0.0386 | 0.1200 | 0.1000 | 0.3800 | 0.4000 | OK | 6,596.74 | 4.60 | 1 | API-15 |
| 8 | Trading assets (interest-earning) | Asset | 98,400 | 0.0410 | 0.3500 | 0.2500 | 0.2500 | 0.1500 | OK | 4,034.40 | 2.10 | 1 | API-15 |
| 9 | Credit card loans | Asset | 138,400 | 0.1650 | 0.6200 | 0.0800 | 0.3000 | 0 | OK | 22,836 | 0.9000 | 1 | API-11 |
| 10 | Residential mortgage loans | Asset | 218,600 | 0.0428 | 0.0500 | 0.0700 | 0.2800 | 0.6000 | OK | 9,356.08 | 5.80 | 1 | API-11 |
| 11 | Auto loans | Asset | 64,900 | 0.0655 | 0.0600 | 0.2400 | 0.7000 | 0 | OK | 4,250.95 | 1.70 | 1 | API-11 |
| 12 | Commercial real estate loans | Asset | 98,200 | 0.0640 | 0.5500 | 0.1000 | 0.3000 | 0.0500 | OK | 6,284.80 | 1.60 | 1 | API-11 |
| 13 | Commercial & industrial loans | Asset | 172,500 | 0.0640 | 0.7800 | 0.0800 | 0.1200 | 0.0200 | OK | 11,040 | 0.6000 | 1 | API-11 |
| 14 | Other consumer & wholesale loans | Asset | 49,700 | 0.0590 | 0.5000 | 0.1500 | 0.3000 | 0.0500 | OK | 2,932.30 | 1.40 | 1 | API-11 |
| 15 | Consumer interest-bearing deposits | Liability | 402,000 | 0.0205 | 0.7000 | 0.3000 | 0 | 0 | OK | 8,241 | 2.80 | 0.4500 | API-15 |
| 16 | Wholesale interest-bearing deposits | Liability | 338,400 | 0.0315 | 0.8500 | 0.1500 | 0 | 0 | OK | 10,659.60 | 0.6000 | 0.7500 | API-15 |
| 17 | Noninterest-bearing deposits | Liability | 272,000 | 0 | 0 | 0 | 0.4000 | 0.6000 | OK | 0 | 3.50 | 0 | API-15 |
| 18 | Repo & short-term borrowings | Liability | 81,000 | 0.0395 | 1 | 0 | 0 | 0 | OK | 3,199.50 | 0.1000 | 1 | API-15 |
| 19 | Long-term debt | Liability | 86,700 | 0.0482 | 0.3000 | 0.1000 | 0.3500 | 0.2500 | OK | 4,178.94 | 4.90 | 1 | API-15 |
| 21 | Total rate-sensitive assets |  | 1,258,500 |  |  |  |  |  |  | 76,515.95 |  |  |  |
| 22 | Total rate-sensitive liabilities |  | 1,180,100 |  |  |  |  |  |  | 26,279.04 |  |  |  |
| 23 | Base-case annual net interest income |  |  |  |  |  |  |  |  | 50,236.91 |  |  |  |

### Formulas in Balance_Sheet (33)

| Cell | Row label | Column header | Formula | Value |
|---|---|---|---|---|
| I6 | Deposits with banks & fed funds sold | Share check | `=IF(ABS(SUM(E6:H6)-1)<0.0001,"OK","CHECK")` | OK |
| J6 | Deposits with banks & fed funds sold | Annual interest ($mm) | `=C6*D6` | 9,184.68 |
| I7 | Investment securities (AFS + HTM) | Share check | `=IF(ABS(SUM(E7:H7)-1)<0.0001,"OK","CHECK")` | OK |
| J7 | Investment securities (AFS + HTM) | Annual interest ($mm) | `=C7*D7` | 6,596.74 |
| I8 | Trading assets (interest-earning) | Share check | `=IF(ABS(SUM(E8:H8)-1)<0.0001,"OK","CHECK")` | OK |
| J8 | Trading assets (interest-earning) | Annual interest ($mm) | `=C8*D8` | 4,034.40 |
| I9 | Credit card loans | Share check | `=IF(ABS(SUM(E9:H9)-1)<0.0001,"OK","CHECK")` | OK |
| J9 | Credit card loans | Annual interest ($mm) | `=C9*D9` | 22,836 |
| I10 | Residential mortgage loans | Share check | `=IF(ABS(SUM(E10:H10)-1)<0.0001,"OK","CHECK")` | OK |
| J10 | Residential mortgage loans | Annual interest ($mm) | `=C10*D10` | 9,356.08 |
| I11 | Auto loans | Share check | `=IF(ABS(SUM(E11:H11)-1)<0.0001,"OK","CHECK")` | OK |
| J11 | Auto loans | Annual interest ($mm) | `=C11*D11` | 4,250.95 |
| I12 | Commercial real estate loans | Share check | `=IF(ABS(SUM(E12:H12)-1)<0.0001,"OK","CHECK")` | OK |
| J12 | Commercial real estate loans | Annual interest ($mm) | `=C12*D12` | 6,284.80 |
| I13 | Commercial & industrial loans | Share check | `=IF(ABS(SUM(E13:H13)-1)<0.0001,"OK","CHECK")` | OK |
| J13 | Commercial & industrial loans | Annual interest ($mm) | `=C13*D13` | 11,040 |
| I14 | Other consumer & wholesale loans | Share check | `=IF(ABS(SUM(E14:H14)-1)<0.0001,"OK","CHECK")` | OK |
| J14 | Other consumer & wholesale loans | Annual interest ($mm) | `=C14*D14` | 2,932.30 |
| I15 | Consumer interest-bearing deposits | Share check | `=IF(ABS(SUM(E15:H15)-1)<0.0001,"OK","CHECK")` | OK |
| J15 | Consumer interest-bearing deposits | Annual interest ($mm) | `=C15*D15` | 8,241 |
| I16 | Wholesale interest-bearing deposits | Share check | `=IF(ABS(SUM(E16:H16)-1)<0.0001,"OK","CHECK")` | OK |
| J16 | Wholesale interest-bearing deposits | Annual interest ($mm) | `=C16*D16` | 10,659.60 |
| I17 | Noninterest-bearing deposits | Share check | `=IF(ABS(SUM(E17:H17)-1)<0.0001,"OK","CHECK")` | OK |
| J17 | Noninterest-bearing deposits | Annual interest ($mm) | `=C17*D17` | 0 |
| I18 | Repo & short-term borrowings | Share check | `=IF(ABS(SUM(E18:H18)-1)<0.0001,"OK","CHECK")` | OK |
| J18 | Repo & short-term borrowings | Annual interest ($mm) | `=C18*D18` | 3,199.50 |
| I19 | Long-term debt | Share check | `=IF(ABS(SUM(E19:H19)-1)<0.0001,"OK","CHECK")` | OK |
| J19 | Long-term debt | Annual interest ($mm) | `=C19*D19` | 4,178.94 |
| C21 | Total rate-sensitive assets | Balance ($mm) | `=SUMIFS(C6:C19,B6:B19,"Asset")` | 1,258,500 |
| J21 | Total rate-sensitive assets | Annual interest ($mm) | `=SUMIFS(J6:J19,B6:B19,"Asset")` | 76,515.95 |
| C22 | Total rate-sensitive liabilities | Balance ($mm) | `=SUMIFS(C6:C19,B6:B19,"Liability")` | 1,180,100 |
| J22 | Total rate-sensitive liabilities | Annual interest ($mm) | `=SUMIFS(J6:J19,B6:B19,"Liability")` | 26,279.04 |
| J23 | Base-case annual net interest income | Annual interest ($mm) | `=J21-J22` | 50,236.91 |

### Cell notes in Balance_Sheet

- L15: Deposit beta from Deposit Behaviour sub-model (2025 calibration).
- L16: Deposit beta from Deposit Behaviour sub-model (2025 calibration).
- L17: Deposit beta from Deposit Behaviour sub-model (2025 calibration).
- L18: Deposit beta from Deposit Behaviour sub-model (2025 calibration).
- L19: Deposit beta from Deposit Behaviour sub-model (2025 calibration).

## Sheet: NII_Projection

> 12-Month NII Projection by Parallel Shock
> Effect = balance x shock x beta x (share 0-3m x (H-1.5)/H + share 3-12m x (H-7.5)/H)
> SYNTHETIC DOCUMENT FOR A PROOF OF CONCEPT. Meridian Harbor Financial Corp. is a fictional institution. All names, figures and events are invented and do not describe any real company.

| Row | A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|---|
| 5 | Line | Side | Repricing factor | Down 200 | Down 100 | Base | Up 100 | Up 200 |
| 6 | Shock (bps) |  |  | -200 | -100 | 0 | 100 | 200 |
| 7 | Deposits with banks & fed funds sold | Asset | 0.8750 | -4,320.75 | -2,160.38 | 0 | 2,160.38 | 4,320.75 |
| 8 | Investment securities (AFS + HTM) | Asset | 0.1425 | -487.06 | -243.53 | 0 | 243.53 | 487.06 |
| 9 | Trading assets (interest-earning) | Asset | 0.4000 | -787.20 | -393.60 | 0 | 393.60 | 787.20 |
| 10 | Credit card loans | Asset | 0.5725 | -1,584.68 | -792.34 | 0 | 792.34 | 1,584.68 |
| 11 | Residential mortgage loans | Asset | 0.0700 | -306.04 | -153.02 | 0 | 153.02 | 306.04 |
| 12 | Auto loans | Asset | 0.1425 | -184.97 | -92.48 | 0 | 92.48 | 184.97 |
| 13 | Commercial real estate loans | Asset | 0.5188 | -1,018.83 | -509.41 | 0 | 509.41 | 1,018.83 |
| 14 | Commercial & industrial loans | Asset | 0.7125 | -2,458.12 | -1,229.06 | 0 | 1,229.06 | 2,458.12 |
| 15 | Other consumer & wholesale loans | Asset | 0.4938 | -490.79 | -245.39 | 0 | 245.39 | 490.79 |
| 16 | Consumer interest-bearing deposits | Liability | 0.7250 | 2,623.05 | 1,311.53 | 0 | -1,311.53 | -2,623.05 |
| 17 | Wholesale interest-bearing deposits | Liability | 0.8000 | 4,060.80 | 2,030.40 | 0 | -2,030.40 | -4,060.80 |
| 18 | Noninterest-bearing deposits | Liability | 0 | 0 | 0 | 0 | 0 | 0 |
| 19 | Repo & short-term borrowings | Liability | 0.8750 | 1,417.50 | 708.75 | 0 | -708.75 | -1,417.50 |
| 20 | Long-term debt | Liability | 0.3000 | 520.20 | 260.10 | 0 | -260.10 | -520.20 |
| 22 | Change in NII ($mm) |  |  | -3,016.89 | -1,508.44 | 0 | 1,508.44 | 3,016.89 |
| 23 | Base-case NII ($mm) |  |  | 50,236.91 | 50,236.91 | 50,236.91 | 50,236.91 | 50,236.91 |
| 24 | Projected NII ($mm) |  |  | 47,220.02 | 48,728.47 | 50,236.91 | 51,745.35 | 53,253.80 |
| 25 | Change in NII (%) |  |  | -0.0601 | -0.0300 | 0 | 0.0300 | 0.0601 |

### Formulas in NII_Projection (137)

| Cell | Row label | Column header | Formula | Value |
|---|---|---|---|---|
| D6 | Shock (bps) | Down 200 | `=Assumptions!B17` | -200 |
| E6 | Shock (bps) | Down 100 | `=Assumptions!B18` | -100 |
| F6 | Shock (bps) | Base | `=Assumptions!B19` | 0 |
| G6 | Shock (bps) | Up 100 | `=Assumptions!B20` | 100 |
| H6 | Shock (bps) | Up 200 | `=Assumptions!B21` | 200 |
| A7 | Deposits with banks & fed funds sold | Line | `=Balance_Sheet!A6` | Deposits with banks & fed funds sold |
| B7 | Deposits with banks & fed funds sold | Side | `=Balance_Sheet!B6` | Asset |
| C7 | Deposits with banks & fed funds sold | Repricing factor | `=Balance_Sheet!E6*(Assumptions!$B$8-Assumptions!$B$9)/Assumptions!$B$8+Balance_Sheet!F6*(Assumptions!$B$8-Assumptions!$B$10)/Assumptions!$B$8` | 0.8750 |
| D7 | Deposits with banks & fed funds sold | Down 200 | `=IF(B7="Asset",1,-1)*Balance_Sheet!C6*Balance_Sheet!L6*$C7*D$6/10000` | -4,320.75 |
| E7 | Deposits with banks & fed funds sold | Down 100 | `=IF(B7="Asset",1,-1)*Balance_Sheet!C6*Balance_Sheet!L6*$C7*E$6/10000` | -2,160.38 |
| F7 | Deposits with banks & fed funds sold | Base | `=IF(B7="Asset",1,-1)*Balance_Sheet!C6*Balance_Sheet!L6*$C7*F$6/10000` | 0 |
| G7 | Deposits with banks & fed funds sold | Up 100 | `=IF(B7="Asset",1,-1)*Balance_Sheet!C6*Balance_Sheet!L6*$C7*G$6/10000` | 2,160.38 |
| H7 | Deposits with banks & fed funds sold | Up 200 | `=IF(B7="Asset",1,-1)*Balance_Sheet!C6*Balance_Sheet!L6*$C7*H$6/10000` | 4,320.75 |
| A8 | Investment securities (AFS + HTM) | Line | `=Balance_Sheet!A7` | Investment securities (AFS + HTM) |
| B8 | Investment securities (AFS + HTM) | Side | `=Balance_Sheet!B7` | Asset |
| C8 | Investment securities (AFS + HTM) | Repricing factor | `=Balance_Sheet!E7*(Assumptions!$B$8-Assumptions!$B$9)/Assumptions!$B$8+Balance_Sheet!F7*(Assumptions!$B$8-Assumptions!$B$10)/Assumptions!$B$8` | 0.1425 |
| D8 | Investment securities (AFS + HTM) | Down 200 | `=IF(B8="Asset",1,-1)*Balance_Sheet!C7*Balance_Sheet!L7*$C8*D$6/10000` | -487.06 |
| E8 | Investment securities (AFS + HTM) | Down 100 | `=IF(B8="Asset",1,-1)*Balance_Sheet!C7*Balance_Sheet!L7*$C8*E$6/10000` | -243.53 |
| F8 | Investment securities (AFS + HTM) | Base | `=IF(B8="Asset",1,-1)*Balance_Sheet!C7*Balance_Sheet!L7*$C8*F$6/10000` | 0 |
| G8 | Investment securities (AFS + HTM) | Up 100 | `=IF(B8="Asset",1,-1)*Balance_Sheet!C7*Balance_Sheet!L7*$C8*G$6/10000` | 243.53 |
| H8 | Investment securities (AFS + HTM) | Up 200 | `=IF(B8="Asset",1,-1)*Balance_Sheet!C7*Balance_Sheet!L7*$C8*H$6/10000` | 487.06 |
| A9 | Trading assets (interest-earning) | Line | `=Balance_Sheet!A8` | Trading assets (interest-earning) |
| B9 | Trading assets (interest-earning) | Side | `=Balance_Sheet!B8` | Asset |
| C9 | Trading assets (interest-earning) | Repricing factor | `=Balance_Sheet!E8*(Assumptions!$B$8-Assumptions!$B$9)/Assumptions!$B$8+Balance_Sheet!F8*(Assumptions!$B$8-Assumptions!$B$10)/Assumptions!$B$8` | 0.4000 |
| D9 | Trading assets (interest-earning) | Down 200 | `=IF(B9="Asset",1,-1)*Balance_Sheet!C8*Balance_Sheet!L8*$C9*D$6/10000` | -787.20 |
| E9 | Trading assets (interest-earning) | Down 100 | `=IF(B9="Asset",1,-1)*Balance_Sheet!C8*Balance_Sheet!L8*$C9*E$6/10000` | -393.60 |
| F9 | Trading assets (interest-earning) | Base | `=IF(B9="Asset",1,-1)*Balance_Sheet!C8*Balance_Sheet!L8*$C9*F$6/10000` | 0 |
| G9 | Trading assets (interest-earning) | Up 100 | `=IF(B9="Asset",1,-1)*Balance_Sheet!C8*Balance_Sheet!L8*$C9*G$6/10000` | 393.60 |
| H9 | Trading assets (interest-earning) | Up 200 | `=IF(B9="Asset",1,-1)*Balance_Sheet!C8*Balance_Sheet!L8*$C9*H$6/10000` | 787.20 |
| A10 | Credit card loans | Line | `=Balance_Sheet!A9` | Credit card loans |
| B10 | Credit card loans | Side | `=Balance_Sheet!B9` | Asset |
| C10 | Credit card loans | Repricing factor | `=Balance_Sheet!E9*(Assumptions!$B$8-Assumptions!$B$9)/Assumptions!$B$8+Balance_Sheet!F9*(Assumptions!$B$8-Assumptions!$B$10)/Assumptions!$B$8` | 0.5725 |
| D10 | Credit card loans | Down 200 | `=IF(B10="Asset",1,-1)*Balance_Sheet!C9*Balance_Sheet!L9*$C10*D$6/10000` | -1,584.68 |
| E10 | Credit card loans | Down 100 | `=IF(B10="Asset",1,-1)*Balance_Sheet!C9*Balance_Sheet!L9*$C10*E$6/10000` | -792.34 |
| F10 | Credit card loans | Base | `=IF(B10="Asset",1,-1)*Balance_Sheet!C9*Balance_Sheet!L9*$C10*F$6/10000` | 0 |
| G10 | Credit card loans | Up 100 | `=IF(B10="Asset",1,-1)*Balance_Sheet!C9*Balance_Sheet!L9*$C10*G$6/10000` | 792.34 |
| H10 | Credit card loans | Up 200 | `=IF(B10="Asset",1,-1)*Balance_Sheet!C9*Balance_Sheet!L9*$C10*H$6/10000` | 1,584.68 |
| A11 | Residential mortgage loans | Line | `=Balance_Sheet!A10` | Residential mortgage loans |
| B11 | Residential mortgage loans | Side | `=Balance_Sheet!B10` | Asset |
| C11 | Residential mortgage loans | Repricing factor | `=Balance_Sheet!E10*(Assumptions!$B$8-Assumptions!$B$9)/Assumptions!$B$8+Balance_Sheet!F10*(Assumptions!$B$8-Assumptions!$B$10)/Assumptions!$B$8` | 0.0700 |
| D11 | Residential mortgage loans | Down 200 | `=IF(B11="Asset",1,-1)*Balance_Sheet!C10*Balance_Sheet!L10*$C11*D$6/10000` | -306.04 |
| E11 | Residential mortgage loans | Down 100 | `=IF(B11="Asset",1,-1)*Balance_Sheet!C10*Balance_Sheet!L10*$C11*E$6/10000` | -153.02 |
| F11 | Residential mortgage loans | Base | `=IF(B11="Asset",1,-1)*Balance_Sheet!C10*Balance_Sheet!L10*$C11*F$6/10000` | 0 |
| G11 | Residential mortgage loans | Up 100 | `=IF(B11="Asset",1,-1)*Balance_Sheet!C10*Balance_Sheet!L10*$C11*G$6/10000` | 153.02 |
| H11 | Residential mortgage loans | Up 200 | `=IF(B11="Asset",1,-1)*Balance_Sheet!C10*Balance_Sheet!L10*$C11*H$6/10000` | 306.04 |
| A12 | Auto loans | Line | `=Balance_Sheet!A11` | Auto loans |
| B12 | Auto loans | Side | `=Balance_Sheet!B11` | Asset |
| C12 | Auto loans | Repricing factor | `=Balance_Sheet!E11*(Assumptions!$B$8-Assumptions!$B$9)/Assumptions!$B$8+Balance_Sheet!F11*(Assumptions!$B$8-Assumptions!$B$10)/Assumptions!$B$8` | 0.1425 |
| D12 | Auto loans | Down 200 | `=IF(B12="Asset",1,-1)*Balance_Sheet!C11*Balance_Sheet!L11*$C12*D$6/10000` | -184.97 |
| E12 | Auto loans | Down 100 | `=IF(B12="Asset",1,-1)*Balance_Sheet!C11*Balance_Sheet!L11*$C12*E$6/10000` | -92.48 |
| F12 | Auto loans | Base | `=IF(B12="Asset",1,-1)*Balance_Sheet!C11*Balance_Sheet!L11*$C12*F$6/10000` | 0 |
| G12 | Auto loans | Up 100 | `=IF(B12="Asset",1,-1)*Balance_Sheet!C11*Balance_Sheet!L11*$C12*G$6/10000` | 92.48 |
| H12 | Auto loans | Up 200 | `=IF(B12="Asset",1,-1)*Balance_Sheet!C11*Balance_Sheet!L11*$C12*H$6/10000` | 184.97 |
| A13 | Commercial real estate loans | Line | `=Balance_Sheet!A12` | Commercial real estate loans |
| B13 | Commercial real estate loans | Side | `=Balance_Sheet!B12` | Asset |
| C13 | Commercial real estate loans | Repricing factor | `=Balance_Sheet!E12*(Assumptions!$B$8-Assumptions!$B$9)/Assumptions!$B$8+Balance_Sheet!F12*(Assumptions!$B$8-Assumptions!$B$10)/Assumptions!$B$8` | 0.5188 |
| D13 | Commercial real estate loans | Down 200 | `=IF(B13="Asset",1,-1)*Balance_Sheet!C12*Balance_Sheet!L12*$C13*D$6/10000` | -1,018.83 |
| E13 | Commercial real estate loans | Down 100 | `=IF(B13="Asset",1,-1)*Balance_Sheet!C12*Balance_Sheet!L12*$C13*E$6/10000` | -509.41 |
| F13 | Commercial real estate loans | Base | `=IF(B13="Asset",1,-1)*Balance_Sheet!C12*Balance_Sheet!L12*$C13*F$6/10000` | 0 |
| G13 | Commercial real estate loans | Up 100 | `=IF(B13="Asset",1,-1)*Balance_Sheet!C12*Balance_Sheet!L12*$C13*G$6/10000` | 509.41 |
| H13 | Commercial real estate loans | Up 200 | `=IF(B13="Asset",1,-1)*Balance_Sheet!C12*Balance_Sheet!L12*$C13*H$6/10000` | 1,018.83 |
| A14 | Commercial & industrial loans | Line | `=Balance_Sheet!A13` | Commercial & industrial loans |
| B14 | Commercial & industrial loans | Side | `=Balance_Sheet!B13` | Asset |
| C14 | Commercial & industrial loans | Repricing factor | `=Balance_Sheet!E13*(Assumptions!$B$8-Assumptions!$B$9)/Assumptions!$B$8+Balance_Sheet!F13*(Assumptions!$B$8-Assumptions!$B$10)/Assumptions!$B$8` | 0.7125 |
| D14 | Commercial & industrial loans | Down 200 | `=IF(B14="Asset",1,-1)*Balance_Sheet!C13*Balance_Sheet!L13*$C14*D$6/10000` | -2,458.12 |
| E14 | Commercial & industrial loans | Down 100 | `=IF(B14="Asset",1,-1)*Balance_Sheet!C13*Balance_Sheet!L13*$C14*E$6/10000` | -1,229.06 |
| F14 | Commercial & industrial loans | Base | `=IF(B14="Asset",1,-1)*Balance_Sheet!C13*Balance_Sheet!L13*$C14*F$6/10000` | 0 |
| G14 | Commercial & industrial loans | Up 100 | `=IF(B14="Asset",1,-1)*Balance_Sheet!C13*Balance_Sheet!L13*$C14*G$6/10000` | 1,229.06 |
| H14 | Commercial & industrial loans | Up 200 | `=IF(B14="Asset",1,-1)*Balance_Sheet!C13*Balance_Sheet!L13*$C14*H$6/10000` | 2,458.12 |
| A15 | Other consumer & wholesale loans | Line | `=Balance_Sheet!A14` | Other consumer & wholesale loans |
| B15 | Other consumer & wholesale loans | Side | `=Balance_Sheet!B14` | Asset |
| C15 | Other consumer & wholesale loans | Repricing factor | `=Balance_Sheet!E14*(Assumptions!$B$8-Assumptions!$B$9)/Assumptions!$B$8+Balance_Sheet!F14*(Assumptions!$B$8-Assumptions!$B$10)/Assumptions!$B$8` | 0.4938 |
| D15 | Other consumer & wholesale loans | Down 200 | `=IF(B15="Asset",1,-1)*Balance_Sheet!C14*Balance_Sheet!L14*$C15*D$6/10000` | -490.79 |
| E15 | Other consumer & wholesale loans | Down 100 | `=IF(B15="Asset",1,-1)*Balance_Sheet!C14*Balance_Sheet!L14*$C15*E$6/10000` | -245.39 |
| F15 | Other consumer & wholesale loans | Base | `=IF(B15="Asset",1,-1)*Balance_Sheet!C14*Balance_Sheet!L14*$C15*F$6/10000` | 0 |
| G15 | Other consumer & wholesale loans | Up 100 | `=IF(B15="Asset",1,-1)*Balance_Sheet!C14*Balance_Sheet!L14*$C15*G$6/10000` | 245.39 |
| H15 | Other consumer & wholesale loans | Up 200 | `=IF(B15="Asset",1,-1)*Balance_Sheet!C14*Balance_Sheet!L14*$C15*H$6/10000` | 490.79 |
| A16 | Consumer interest-bearing deposits | Line | `=Balance_Sheet!A15` | Consumer interest-bearing deposits |
| B16 | Consumer interest-bearing deposits | Side | `=Balance_Sheet!B15` | Liability |
| C16 | Consumer interest-bearing deposits | Repricing factor | `=Balance_Sheet!E15*(Assumptions!$B$8-Assumptions!$B$9)/Assumptions!$B$8+Balance_Sheet!F15*(Assumptions!$B$8-Assumptions!$B$10)/Assumptions!$B$8` | 0.7250 |
| D16 | Consumer interest-bearing deposits | Down 200 | `=IF(B16="Asset",1,-1)*Balance_Sheet!C15*Balance_Sheet!L15*$C16*D$6/10000` | 2,623.05 |
| E16 | Consumer interest-bearing deposits | Down 100 | `=IF(B16="Asset",1,-1)*Balance_Sheet!C15*Balance_Sheet!L15*$C16*E$6/10000` | 1,311.53 |
| F16 | Consumer interest-bearing deposits | Base | `=IF(B16="Asset",1,-1)*Balance_Sheet!C15*Balance_Sheet!L15*$C16*F$6/10000` | 0 |
| G16 | Consumer interest-bearing deposits | Up 100 | `=IF(B16="Asset",1,-1)*Balance_Sheet!C15*Balance_Sheet!L15*$C16*G$6/10000` | -1,311.53 |
| H16 | Consumer interest-bearing deposits | Up 200 | `=IF(B16="Asset",1,-1)*Balance_Sheet!C15*Balance_Sheet!L15*$C16*H$6/10000` | -2,623.05 |
| A17 | Wholesale interest-bearing deposits | Line | `=Balance_Sheet!A16` | Wholesale interest-bearing deposits |
| B17 | Wholesale interest-bearing deposits | Side | `=Balance_Sheet!B16` | Liability |
| C17 | Wholesale interest-bearing deposits | Repricing factor | `=Balance_Sheet!E16*(Assumptions!$B$8-Assumptions!$B$9)/Assumptions!$B$8+Balance_Sheet!F16*(Assumptions!$B$8-Assumptions!$B$10)/Assumptions!$B$8` | 0.8000 |
| D17 | Wholesale interest-bearing deposits | Down 200 | `=IF(B17="Asset",1,-1)*Balance_Sheet!C16*Balance_Sheet!L16*$C17*D$6/10000` | 4,060.80 |
| E17 | Wholesale interest-bearing deposits | Down 100 | `=IF(B17="Asset",1,-1)*Balance_Sheet!C16*Balance_Sheet!L16*$C17*E$6/10000` | 2,030.40 |
| F17 | Wholesale interest-bearing deposits | Base | `=IF(B17="Asset",1,-1)*Balance_Sheet!C16*Balance_Sheet!L16*$C17*F$6/10000` | 0 |
| G17 | Wholesale interest-bearing deposits | Up 100 | `=IF(B17="Asset",1,-1)*Balance_Sheet!C16*Balance_Sheet!L16*$C17*G$6/10000` | -2,030.40 |
| H17 | Wholesale interest-bearing deposits | Up 200 | `=IF(B17="Asset",1,-1)*Balance_Sheet!C16*Balance_Sheet!L16*$C17*H$6/10000` | -4,060.80 |
| A18 | Noninterest-bearing deposits | Line | `=Balance_Sheet!A17` | Noninterest-bearing deposits |
| B18 | Noninterest-bearing deposits | Side | `=Balance_Sheet!B17` | Liability |
| C18 | Noninterest-bearing deposits | Repricing factor | `=Balance_Sheet!E17*(Assumptions!$B$8-Assumptions!$B$9)/Assumptions!$B$8+Balance_Sheet!F17*(Assumptions!$B$8-Assumptions!$B$10)/Assumptions!$B$8` | 0 |
| D18 | Noninterest-bearing deposits | Down 200 | `=IF(B18="Asset",1,-1)*Balance_Sheet!C17*Balance_Sheet!L17*$C18*D$6/10000` | 0 |
| E18 | Noninterest-bearing deposits | Down 100 | `=IF(B18="Asset",1,-1)*Balance_Sheet!C17*Balance_Sheet!L17*$C18*E$6/10000` | 0 |
| F18 | Noninterest-bearing deposits | Base | `=IF(B18="Asset",1,-1)*Balance_Sheet!C17*Balance_Sheet!L17*$C18*F$6/10000` | 0 |
| G18 | Noninterest-bearing deposits | Up 100 | `=IF(B18="Asset",1,-1)*Balance_Sheet!C17*Balance_Sheet!L17*$C18*G$6/10000` | 0 |
| H18 | Noninterest-bearing deposits | Up 200 | `=IF(B18="Asset",1,-1)*Balance_Sheet!C17*Balance_Sheet!L17*$C18*H$6/10000` | 0 |
| A19 | Repo & short-term borrowings | Line | `=Balance_Sheet!A18` | Repo & short-term borrowings |
| B19 | Repo & short-term borrowings | Side | `=Balance_Sheet!B18` | Liability |
| C19 | Repo & short-term borrowings | Repricing factor | `=Balance_Sheet!E18*(Assumptions!$B$8-Assumptions!$B$9)/Assumptions!$B$8+Balance_Sheet!F18*(Assumptions!$B$8-Assumptions!$B$10)/Assumptions!$B$8` | 0.8750 |
| D19 | Repo & short-term borrowings | Down 200 | `=IF(B19="Asset",1,-1)*Balance_Sheet!C18*Balance_Sheet!L18*$C19*D$6/10000` | 1,417.50 |
| E19 | Repo & short-term borrowings | Down 100 | `=IF(B19="Asset",1,-1)*Balance_Sheet!C18*Balance_Sheet!L18*$C19*E$6/10000` | 708.75 |
| F19 | Repo & short-term borrowings | Base | `=IF(B19="Asset",1,-1)*Balance_Sheet!C18*Balance_Sheet!L18*$C19*F$6/10000` | 0 |
| G19 | Repo & short-term borrowings | Up 100 | `=IF(B19="Asset",1,-1)*Balance_Sheet!C18*Balance_Sheet!L18*$C19*G$6/10000` | -708.75 |
| H19 | Repo & short-term borrowings | Up 200 | `=IF(B19="Asset",1,-1)*Balance_Sheet!C18*Balance_Sheet!L18*$C19*H$6/10000` | -1,417.50 |
| A20 | Long-term debt | Line | `=Balance_Sheet!A19` | Long-term debt |
| B20 | Long-term debt | Side | `=Balance_Sheet!B19` | Liability |
| C20 | Long-term debt | Repricing factor | `=Balance_Sheet!E19*(Assumptions!$B$8-Assumptions!$B$9)/Assumptions!$B$8+Balance_Sheet!F19*(Assumptions!$B$8-Assumptions!$B$10)/Assumptions!$B$8` | 0.3000 |
| D20 | Long-term debt | Down 200 | `=IF(B20="Asset",1,-1)*Balance_Sheet!C19*Balance_Sheet!L19*$C20*D$6/10000` | 520.20 |
| E20 | Long-term debt | Down 100 | `=IF(B20="Asset",1,-1)*Balance_Sheet!C19*Balance_Sheet!L19*$C20*E$6/10000` | 260.10 |
| F20 | Long-term debt | Base | `=IF(B20="Asset",1,-1)*Balance_Sheet!C19*Balance_Sheet!L19*$C20*F$6/10000` | 0 |
| G20 | Long-term debt | Up 100 | `=IF(B20="Asset",1,-1)*Balance_Sheet!C19*Balance_Sheet!L19*$C20*G$6/10000` | -260.10 |
| H20 | Long-term debt | Up 200 | `=IF(B20="Asset",1,-1)*Balance_Sheet!C19*Balance_Sheet!L19*$C20*H$6/10000` | -520.20 |
| D22 | Change in NII ($mm) | Down 200 | `=SUM(D7:D20)` | -3,016.89 |
| E22 | Change in NII ($mm) | Down 100 | `=SUM(E7:E20)` | -1,508.44 |
| F22 | Change in NII ($mm) | Base | `=SUM(F7:F20)` | 0 |
| G22 | Change in NII ($mm) | Up 100 | `=SUM(G7:G20)` | 1,508.44 |
| H22 | Change in NII ($mm) | Up 200 | `=SUM(H7:H20)` | 3,016.89 |
| D23 | Base-case NII ($mm) | Down 200 | `=Balance_Sheet!$J$23` | 50,236.91 |
| E23 | Base-case NII ($mm) | Down 100 | `=Balance_Sheet!$J$23` | 50,236.91 |
| F23 | Base-case NII ($mm) | Base | `=Balance_Sheet!$J$23` | 50,236.91 |
| G23 | Base-case NII ($mm) | Up 100 | `=Balance_Sheet!$J$23` | 50,236.91 |
| H23 | Base-case NII ($mm) | Up 200 | `=Balance_Sheet!$J$23` | 50,236.91 |
| D24 | Projected NII ($mm) | Down 200 | `=D23+D22` | 47,220.02 |
| E24 | Projected NII ($mm) | Down 100 | `=E23+E22` | 48,728.47 |
| F24 | Projected NII ($mm) | Base | `=F23+F22` | 50,236.91 |
| G24 | Projected NII ($mm) | Up 100 | `=G23+G22` | 51,745.35 |
| H24 | Projected NII ($mm) | Up 200 | `=H23+H22` | 53,253.80 |
| D25 | Change in NII (%) | Down 200 | `=IF(D23=0,0,D22/D23)` | -0.0601 |
| E25 | Change in NII (%) | Down 100 | `=IF(E23=0,0,E22/E23)` | -0.0300 |
| F25 | Change in NII (%) | Base | `=IF(F23=0,0,F22/F23)` | 0 |
| G25 | Change in NII (%) | Up 100 | `=IF(G23=0,0,G22/G23)` | 0.0300 |
| H25 | Change in NII (%) | Up 200 | `=IF(H23=0,0,H22/H23)` | 0.0601 |

## Sheet: EVE

> Economic Value of Equity Sensitivity
> dEVE ~= -(sum asset PV x duration - sum liability PV x duration) x shock
> SYNTHETIC DOCUMENT FOR A PROOF OF CONCEPT. Meridian Harbor Financial Corp. is a fictional institution. All names, figures and events are invented and do not describe any real company.

| Row | A | B | C | D | E | F | G | H | I | J |
|---|---|---|---|---|---|---|---|---|---|---|
| 5 | Line | Side | Balance ($mm) | Mod. duration | Dollar duration ($mm per 100 bp) | Down 200 | Down 100 | Base | Up 100 | Up 200 |
| 6 | Shock (bps) |  |  |  |  | -200 | -100 | 0 | 100 | 200 |
| 7 | Deposits with banks & fed funds sold | Asset | 246,900 | 0.1000 | 246.90 | 493.80 | 246.90 | 0 | -246.90 | -493.80 |
| 8 | Investment securities (AFS + HTM) | Asset | 170,900 | 4.60 | 7,861.40 | 15,722.80 | 7,861.40 | 0 | -7,861.40 | -15,722.80 |
| 9 | Trading assets (interest-earning) | Asset | 98,400 | 2.10 | 2,066.40 | 4,132.80 | 2,066.40 | 0 | -2,066.40 | -4,132.80 |
| 10 | Credit card loans | Asset | 138,400 | 0.9000 | 1,245.60 | 2,491.20 | 1,245.60 | 0 | -1,245.60 | -2,491.20 |
| 11 | Residential mortgage loans | Asset | 218,600 | 5.80 | 12,678.80 | 25,357.60 | 12,678.80 | 0 | -12,678.80 | -25,357.60 |
| 12 | Auto loans | Asset | 64,900 | 1.70 | 1,103.30 | 2,206.60 | 1,103.30 | 0 | -1,103.30 | -2,206.60 |
| 13 | Commercial real estate loans | Asset | 98,200 | 1.60 | 1,571.20 | 3,142.40 | 1,571.20 | 0 | -1,571.20 | -3,142.40 |
| 14 | Commercial & industrial loans | Asset | 172,500 | 0.6000 | 1,035 | 2,070 | 1,035 | 0 | -1,035 | -2,070 |
| 15 | Other consumer & wholesale loans | Asset | 49,700 | 1.40 | 695.80 | 1,391.60 | 695.80 | 0 | -695.80 | -1,391.60 |
| 16 | Consumer interest-bearing deposits | Liability | 402,000 | 2.80 | -11,256 | -22,512 | -11,256 | 0 | 11,256 | 22,512 |
| 17 | Wholesale interest-bearing deposits | Liability | 338,400 | 0.6000 | -2,030.40 | -4,060.80 | -2,030.40 | 0 | 2,030.40 | 4,060.80 |
| 18 | Noninterest-bearing deposits | Liability | 272,000 | 3.50 | -9,520 | -19,040 | -9,520 | 0 | 9,520 | 19,040 |
| 19 | Repo & short-term borrowings | Liability | 81,000 | 0.1000 | -81 | -162 | -81 | 0 | 81 | 162 |
| 20 | Long-term debt | Liability | 86,700 | 4.90 | -4,248.30 | -8,496.60 | -4,248.30 | 0 | 4,248.30 | 8,496.60 |
| 22 | Change in EVE ($mm) |  |  |  |  | 2,737.40 | 1,368.70 | 0 | -1,368.70 | -2,737.40 |
| 23 | Tier 1 capital ($mm) |  |  |  |  | 110,620 | 110,620 | 110,620 | 110,620 | 110,620 |
| 24 | Change in EVE (% of Tier 1) |  |  |  |  | 0.0247 | 0.0124 | 0 | -0.0124 | -0.0247 |

### Formulas in EVE (160)

| Cell | Row label | Column header | Formula | Value |
|---|---|---|---|---|
| F6 | Shock (bps) | Down 200 | `=Assumptions!B17` | -200 |
| G6 | Shock (bps) | Down 100 | `=Assumptions!B18` | -100 |
| H6 | Shock (bps) | Base | `=Assumptions!B19` | 0 |
| I6 | Shock (bps) | Up 100 | `=Assumptions!B20` | 100 |
| J6 | Shock (bps) | Up 200 | `=Assumptions!B21` | 200 |
| A7 | Deposits with banks & fed funds sold | Line | `=Balance_Sheet!A6` | Deposits with banks & fed funds sold |
| B7 | Deposits with banks & fed funds sold | Side | `=Balance_Sheet!B6` | Asset |
| C7 | Deposits with banks & fed funds sold | Balance ($mm) | `=Balance_Sheet!C6` | 246,900 |
| D7 | Deposits with banks & fed funds sold | Mod. duration | `=Balance_Sheet!K6` | 0.1000 |
| E7 | Deposits with banks & fed funds sold | Dollar duration ($mm per 100 bp) | `=IF(B7="Asset",1,-1)*C7*D7/100` | 246.90 |
| F7 | Deposits with banks & fed funds sold | Down 200 | `=-$E7*F$6/100` | 493.80 |
| G7 | Deposits with banks & fed funds sold | Down 100 | `=-$E7*G$6/100` | 246.90 |
| H7 | Deposits with banks & fed funds sold | Base | `=-$E7*H$6/100` | 0 |
| I7 | Deposits with banks & fed funds sold | Up 100 | `=-$E7*I$6/100` | -246.90 |
| J7 | Deposits with banks & fed funds sold | Up 200 | `=-$E7*J$6/100` | -493.80 |
| A8 | Investment securities (AFS + HTM) | Line | `=Balance_Sheet!A7` | Investment securities (AFS + HTM) |
| B8 | Investment securities (AFS + HTM) | Side | `=Balance_Sheet!B7` | Asset |
| C8 | Investment securities (AFS + HTM) | Balance ($mm) | `=Balance_Sheet!C7` | 170,900 |
| D8 | Investment securities (AFS + HTM) | Mod. duration | `=Balance_Sheet!K7` | 4.60 |
| E8 | Investment securities (AFS + HTM) | Dollar duration ($mm per 100 bp) | `=IF(B8="Asset",1,-1)*C8*D8/100` | 7,861.40 |
| F8 | Investment securities (AFS + HTM) | Down 200 | `=-$E8*F$6/100` | 15,722.80 |
| G8 | Investment securities (AFS + HTM) | Down 100 | `=-$E8*G$6/100` | 7,861.40 |
| H8 | Investment securities (AFS + HTM) | Base | `=-$E8*H$6/100` | 0 |
| I8 | Investment securities (AFS + HTM) | Up 100 | `=-$E8*I$6/100` | -7,861.40 |
| J8 | Investment securities (AFS + HTM) | Up 200 | `=-$E8*J$6/100` | -15,722.80 |
| A9 | Trading assets (interest-earning) | Line | `=Balance_Sheet!A8` | Trading assets (interest-earning) |
| B9 | Trading assets (interest-earning) | Side | `=Balance_Sheet!B8` | Asset |
| C9 | Trading assets (interest-earning) | Balance ($mm) | `=Balance_Sheet!C8` | 98,400 |
| D9 | Trading assets (interest-earning) | Mod. duration | `=Balance_Sheet!K8` | 2.10 |
| E9 | Trading assets (interest-earning) | Dollar duration ($mm per 100 bp) | `=IF(B9="Asset",1,-1)*C9*D9/100` | 2,066.40 |
| F9 | Trading assets (interest-earning) | Down 200 | `=-$E9*F$6/100` | 4,132.80 |
| G9 | Trading assets (interest-earning) | Down 100 | `=-$E9*G$6/100` | 2,066.40 |
| H9 | Trading assets (interest-earning) | Base | `=-$E9*H$6/100` | 0 |
| I9 | Trading assets (interest-earning) | Up 100 | `=-$E9*I$6/100` | -2,066.40 |
| J9 | Trading assets (interest-earning) | Up 200 | `=-$E9*J$6/100` | -4,132.80 |
| A10 | Credit card loans | Line | `=Balance_Sheet!A9` | Credit card loans |
| B10 | Credit card loans | Side | `=Balance_Sheet!B9` | Asset |
| C10 | Credit card loans | Balance ($mm) | `=Balance_Sheet!C9` | 138,400 |
| D10 | Credit card loans | Mod. duration | `=Balance_Sheet!K9` | 0.9000 |
| E10 | Credit card loans | Dollar duration ($mm per 100 bp) | `=IF(B10="Asset",1,-1)*C10*D10/100` | 1,245.60 |
| F10 | Credit card loans | Down 200 | `=-$E10*F$6/100` | 2,491.20 |
| G10 | Credit card loans | Down 100 | `=-$E10*G$6/100` | 1,245.60 |
| H10 | Credit card loans | Base | `=-$E10*H$6/100` | 0 |
| I10 | Credit card loans | Up 100 | `=-$E10*I$6/100` | -1,245.60 |
| J10 | Credit card loans | Up 200 | `=-$E10*J$6/100` | -2,491.20 |
| A11 | Residential mortgage loans | Line | `=Balance_Sheet!A10` | Residential mortgage loans |
| B11 | Residential mortgage loans | Side | `=Balance_Sheet!B10` | Asset |
| C11 | Residential mortgage loans | Balance ($mm) | `=Balance_Sheet!C10` | 218,600 |
| D11 | Residential mortgage loans | Mod. duration | `=Balance_Sheet!K10` | 5.80 |
| E11 | Residential mortgage loans | Dollar duration ($mm per 100 bp) | `=IF(B11="Asset",1,-1)*C11*D11/100` | 12,678.80 |
| F11 | Residential mortgage loans | Down 200 | `=-$E11*F$6/100` | 25,357.60 |
| G11 | Residential mortgage loans | Down 100 | `=-$E11*G$6/100` | 12,678.80 |
| H11 | Residential mortgage loans | Base | `=-$E11*H$6/100` | 0 |
| I11 | Residential mortgage loans | Up 100 | `=-$E11*I$6/100` | -12,678.80 |
| J11 | Residential mortgage loans | Up 200 | `=-$E11*J$6/100` | -25,357.60 |
| A12 | Auto loans | Line | `=Balance_Sheet!A11` | Auto loans |
| B12 | Auto loans | Side | `=Balance_Sheet!B11` | Asset |
| C12 | Auto loans | Balance ($mm) | `=Balance_Sheet!C11` | 64,900 |
| D12 | Auto loans | Mod. duration | `=Balance_Sheet!K11` | 1.70 |
| E12 | Auto loans | Dollar duration ($mm per 100 bp) | `=IF(B12="Asset",1,-1)*C12*D12/100` | 1,103.30 |
| F12 | Auto loans | Down 200 | `=-$E12*F$6/100` | 2,206.60 |
| G12 | Auto loans | Down 100 | `=-$E12*G$6/100` | 1,103.30 |
| H12 | Auto loans | Base | `=-$E12*H$6/100` | 0 |
| I12 | Auto loans | Up 100 | `=-$E12*I$6/100` | -1,103.30 |
| J12 | Auto loans | Up 200 | `=-$E12*J$6/100` | -2,206.60 |
| A13 | Commercial real estate loans | Line | `=Balance_Sheet!A12` | Commercial real estate loans |
| B13 | Commercial real estate loans | Side | `=Balance_Sheet!B12` | Asset |
| C13 | Commercial real estate loans | Balance ($mm) | `=Balance_Sheet!C12` | 98,200 |
| D13 | Commercial real estate loans | Mod. duration | `=Balance_Sheet!K12` | 1.60 |
| E13 | Commercial real estate loans | Dollar duration ($mm per 100 bp) | `=IF(B13="Asset",1,-1)*C13*D13/100` | 1,571.20 |
| F13 | Commercial real estate loans | Down 200 | `=-$E13*F$6/100` | 3,142.40 |
| G13 | Commercial real estate loans | Down 100 | `=-$E13*G$6/100` | 1,571.20 |
| H13 | Commercial real estate loans | Base | `=-$E13*H$6/100` | 0 |
| I13 | Commercial real estate loans | Up 100 | `=-$E13*I$6/100` | -1,571.20 |
| J13 | Commercial real estate loans | Up 200 | `=-$E13*J$6/100` | -3,142.40 |
| A14 | Commercial & industrial loans | Line | `=Balance_Sheet!A13` | Commercial & industrial loans |
| B14 | Commercial & industrial loans | Side | `=Balance_Sheet!B13` | Asset |
| C14 | Commercial & industrial loans | Balance ($mm) | `=Balance_Sheet!C13` | 172,500 |
| D14 | Commercial & industrial loans | Mod. duration | `=Balance_Sheet!K13` | 0.6000 |
| E14 | Commercial & industrial loans | Dollar duration ($mm per 100 bp) | `=IF(B14="Asset",1,-1)*C14*D14/100` | 1,035 |
| F14 | Commercial & industrial loans | Down 200 | `=-$E14*F$6/100` | 2,070 |
| G14 | Commercial & industrial loans | Down 100 | `=-$E14*G$6/100` | 1,035 |
| H14 | Commercial & industrial loans | Base | `=-$E14*H$6/100` | 0 |
| I14 | Commercial & industrial loans | Up 100 | `=-$E14*I$6/100` | -1,035 |
| J14 | Commercial & industrial loans | Up 200 | `=-$E14*J$6/100` | -2,070 |
| A15 | Other consumer & wholesale loans | Line | `=Balance_Sheet!A14` | Other consumer & wholesale loans |
| B15 | Other consumer & wholesale loans | Side | `=Balance_Sheet!B14` | Asset |
| C15 | Other consumer & wholesale loans | Balance ($mm) | `=Balance_Sheet!C14` | 49,700 |
| D15 | Other consumer & wholesale loans | Mod. duration | `=Balance_Sheet!K14` | 1.40 |
| E15 | Other consumer & wholesale loans | Dollar duration ($mm per 100 bp) | `=IF(B15="Asset",1,-1)*C15*D15/100` | 695.80 |
| F15 | Other consumer & wholesale loans | Down 200 | `=-$E15*F$6/100` | 1,391.60 |
| G15 | Other consumer & wholesale loans | Down 100 | `=-$E15*G$6/100` | 695.80 |
| H15 | Other consumer & wholesale loans | Base | `=-$E15*H$6/100` | 0 |
| I15 | Other consumer & wholesale loans | Up 100 | `=-$E15*I$6/100` | -695.80 |
| J15 | Other consumer & wholesale loans | Up 200 | `=-$E15*J$6/100` | -1,391.60 |
| A16 | Consumer interest-bearing deposits | Line | `=Balance_Sheet!A15` | Consumer interest-bearing deposits |
| B16 | Consumer interest-bearing deposits | Side | `=Balance_Sheet!B15` | Liability |
| C16 | Consumer interest-bearing deposits | Balance ($mm) | `=Balance_Sheet!C15` | 402,000 |
| D16 | Consumer interest-bearing deposits | Mod. duration | `=Balance_Sheet!K15` | 2.80 |
| E16 | Consumer interest-bearing deposits | Dollar duration ($mm per 100 bp) | `=IF(B16="Asset",1,-1)*C16*D16/100` | -11,256 |
| F16 | Consumer interest-bearing deposits | Down 200 | `=-$E16*F$6/100` | -22,512 |
| G16 | Consumer interest-bearing deposits | Down 100 | `=-$E16*G$6/100` | -11,256 |
| H16 | Consumer interest-bearing deposits | Base | `=-$E16*H$6/100` | 0 |
| I16 | Consumer interest-bearing deposits | Up 100 | `=-$E16*I$6/100` | 11,256 |
| J16 | Consumer interest-bearing deposits | Up 200 | `=-$E16*J$6/100` | 22,512 |
| A17 | Wholesale interest-bearing deposits | Line | `=Balance_Sheet!A16` | Wholesale interest-bearing deposits |
| B17 | Wholesale interest-bearing deposits | Side | `=Balance_Sheet!B16` | Liability |
| C17 | Wholesale interest-bearing deposits | Balance ($mm) | `=Balance_Sheet!C16` | 338,400 |
| D17 | Wholesale interest-bearing deposits | Mod. duration | `=Balance_Sheet!K16` | 0.6000 |
| E17 | Wholesale interest-bearing deposits | Dollar duration ($mm per 100 bp) | `=IF(B17="Asset",1,-1)*C17*D17/100` | -2,030.40 |
| F17 | Wholesale interest-bearing deposits | Down 200 | `=-$E17*F$6/100` | -4,060.80 |
| G17 | Wholesale interest-bearing deposits | Down 100 | `=-$E17*G$6/100` | -2,030.40 |
| H17 | Wholesale interest-bearing deposits | Base | `=-$E17*H$6/100` | 0 |
| I17 | Wholesale interest-bearing deposits | Up 100 | `=-$E17*I$6/100` | 2,030.40 |
| J17 | Wholesale interest-bearing deposits | Up 200 | `=-$E17*J$6/100` | 4,060.80 |
| A18 | Noninterest-bearing deposits | Line | `=Balance_Sheet!A17` | Noninterest-bearing deposits |
| B18 | Noninterest-bearing deposits | Side | `=Balance_Sheet!B17` | Liability |
| C18 | Noninterest-bearing deposits | Balance ($mm) | `=Balance_Sheet!C17` | 272,000 |
| D18 | Noninterest-bearing deposits | Mod. duration | `=Balance_Sheet!K17` | 3.50 |
| E18 | Noninterest-bearing deposits | Dollar duration ($mm per 100 bp) | `=IF(B18="Asset",1,-1)*C18*D18/100` | -9,520 |
| F18 | Noninterest-bearing deposits | Down 200 | `=-$E18*F$6/100` | -19,040 |
| G18 | Noninterest-bearing deposits | Down 100 | `=-$E18*G$6/100` | -9,520 |
| H18 | Noninterest-bearing deposits | Base | `=-$E18*H$6/100` | 0 |
| I18 | Noninterest-bearing deposits | Up 100 | `=-$E18*I$6/100` | 9,520 |
| J18 | Noninterest-bearing deposits | Up 200 | `=-$E18*J$6/100` | 19,040 |
| A19 | Repo & short-term borrowings | Line | `=Balance_Sheet!A18` | Repo & short-term borrowings |
| B19 | Repo & short-term borrowings | Side | `=Balance_Sheet!B18` | Liability |
| C19 | Repo & short-term borrowings | Balance ($mm) | `=Balance_Sheet!C18` | 81,000 |
| D19 | Repo & short-term borrowings | Mod. duration | `=Balance_Sheet!K18` | 0.1000 |
| E19 | Repo & short-term borrowings | Dollar duration ($mm per 100 bp) | `=IF(B19="Asset",1,-1)*C19*D19/100` | -81 |
| F19 | Repo & short-term borrowings | Down 200 | `=-$E19*F$6/100` | -162 |
| G19 | Repo & short-term borrowings | Down 100 | `=-$E19*G$6/100` | -81 |
| H19 | Repo & short-term borrowings | Base | `=-$E19*H$6/100` | 0 |
| I19 | Repo & short-term borrowings | Up 100 | `=-$E19*I$6/100` | 81 |
| J19 | Repo & short-term borrowings | Up 200 | `=-$E19*J$6/100` | 162 |
| A20 | Long-term debt | Line | `=Balance_Sheet!A19` | Long-term debt |
| B20 | Long-term debt | Side | `=Balance_Sheet!B19` | Liability |
| C20 | Long-term debt | Balance ($mm) | `=Balance_Sheet!C19` | 86,700 |
| D20 | Long-term debt | Mod. duration | `=Balance_Sheet!K19` | 4.90 |
| E20 | Long-term debt | Dollar duration ($mm per 100 bp) | `=IF(B20="Asset",1,-1)*C20*D20/100` | -4,248.30 |
| F20 | Long-term debt | Down 200 | `=-$E20*F$6/100` | -8,496.60 |
| G20 | Long-term debt | Down 100 | `=-$E20*G$6/100` | -4,248.30 |
| H20 | Long-term debt | Base | `=-$E20*H$6/100` | 0 |
| I20 | Long-term debt | Up 100 | `=-$E20*I$6/100` | 4,248.30 |
| J20 | Long-term debt | Up 200 | `=-$E20*J$6/100` | 8,496.60 |
| F22 | Change in EVE ($mm) | Down 200 | `=SUM(F7:F20)` | 2,737.40 |
| G22 | Change in EVE ($mm) | Down 100 | `=SUM(G7:G20)` | 1,368.70 |
| H22 | Change in EVE ($mm) | Base | `=SUM(H7:H20)` | 0 |
| I22 | Change in EVE ($mm) | Up 100 | `=SUM(I7:I20)` | -1,368.70 |
| J22 | Change in EVE ($mm) | Up 200 | `=SUM(J7:J20)` | -2,737.40 |
| F23 | Tier 1 capital ($mm) | Down 200 | `=Assumptions!$B$13` | 110,620 |
| G23 | Tier 1 capital ($mm) | Down 100 | `=Assumptions!$B$13` | 110,620 |
| H23 | Tier 1 capital ($mm) | Base | `=Assumptions!$B$13` | 110,620 |
| I23 | Tier 1 capital ($mm) | Up 100 | `=Assumptions!$B$13` | 110,620 |
| J23 | Tier 1 capital ($mm) | Up 200 | `=Assumptions!$B$13` | 110,620 |
| F24 | Change in EVE (% of Tier 1) | Down 200 | `=IF(F23=0,0,F22/F23)` | 0.0247 |
| G24 | Change in EVE (% of Tier 1) | Down 100 | `=IF(G23=0,0,G22/G23)` | 0.0124 |
| H24 | Change in EVE (% of Tier 1) | Base | `=IF(H23=0,0,H22/H23)` | 0 |
| I24 | Change in EVE (% of Tier 1) | Up 100 | `=IF(I23=0,0,I22/I23)` | -0.0124 |
| J24 | Change in EVE (% of Tier 1) | Up 200 | `=IF(J23=0,0,J22/J23)` | -0.0247 |
