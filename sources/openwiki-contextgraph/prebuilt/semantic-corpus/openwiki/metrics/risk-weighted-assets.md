---
type: FinancialMetric
title: Risk-Weighted Assets
description: Risk-weighted assets (RWA) of Meridian Harbor Financial Corp. (a synthetic, fictional institution) by risk type under the Standardized and Advanced approaches, the 2025 RWA flow, reported 2026 values, and the nine-quarter baseline and severely adverse RWA projections from MDL-CAP-003.
tags: [risk-weighted-assets, rwa, regulatory-capital, basel-iii, capital-planning, stress-testing, financial-metric]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-05T01:46:21.335Z
sources:
  - id: openwiki-source-6017268cd41c9c2877299736
    resource: repo://sources/api_docs/apis/api-16-regulatory-reporting-api.md
  - id: openwiki-source-d7481767c8aa79de795d1f43
    resource: repo://sources/models/capital-planning-model.md
  - id: openwiki-source-eb14da62fbec45aad876fb64
    resource: repo://sources/reports/mhfc-2025-annual-report.md
  - id: openwiki-source-c13af588d055d118eda543d5
    resource: repo://sources/reports/mhfc-2025-pillar3-disclosures.md
  - id: openwiki-source-9da334bbfcfb68cd7514ff33
    resource: repo://sources/reports/mhfc-q2-2026-earnings-supplement.md
generated: { by: "openwiki/0.7.0", at: "2026-10-05T01:46:21.335Z" }
---

# Risk-Weighted Assets

Risk-weighted assets (RWA) are exposures weighted by their riskiness under the Standardized or Advanced approaches ([Annual Report glossary](../../sources/reports/mhfc-2025-annual-report.md)). RWA is the denominator of every risk-based capital ratio, so it is the lever that, together with capital, sets the [CET1 Ratio](cet1-ratio.md). Meridian Harbor Financial Corp. (MHFC) is a fictional institution in a proof-of-concept corpus; all figures are invented. Figures are USD millions unless stated.

Related: [CET1 Ratio](cet1-ratio.md), [Basel III Pillar 3](../concepts/basel-iii-pillar-3.md), [Stress Capital Buffer](../concepts/stress-capital-buffer.md), [Regulatory Reporting API (API-16)](../apis/api-16-regulatory-reporting-api.md).

## Two approaches, one binding

MHFC is an advanced approaches banking organization and computes RWA under both the Standardized and Advanced approaches. The lower of each ratio under the two approaches is used to assess capital adequacy (the "Collins Floor"), and that is currently the Standardized approach ([Pillar 3](../../sources/reports/mhfc-2025-pillar3-disclosures.md)). Consequently the Standardized RWA is the figure used for requirements, the management target and projections; the Advanced RWA is reported alongside. At 31 Dec 2025 the Standardized CET1 ratio was 15.08% against 15.92% under the Advanced approach, because Standardized RWA (652,800) is larger than Advanced RWA (618,300).

The two approaches use different risk-type taxonomies, so their breakdowns are not directly comparable:

- **Standardized** splits RWA by exposure type and includes market risk but no operational-risk component.
- **Advanced** splits RWA into credit risk (including counterparty credit risk and CVA), market risk and operational risk.

## RWA by risk type, 31 Dec 2025

### Standardized (total 652,800)

| Exposure type | RWA | % of total | 8% capital requirement |
|---|---|---|---|
| Wholesale credit risk | 312,400 | 47.9% | 24,992 |
| Retail credit risk | 196,800 | 30.1% | 15,744 |
| Counterparty credit risk (derivatives and SFTs) | 41,600 | 6.4% | 3,328 |
| Securitization exposures | 9,300 | 1.4% | 744 |
| Equity exposures | 6,900 | 1.1% | 552 |
| Other assets | 31,600 | 4.8% | 2,528 |
| Market risk | 54,200 | 8.3% | 4,336 |
| **Total** | **652,800** | 100.0% | 52,224 |

The credit-risk subtotal (everything except market risk) is 598,600, which is the "credit risk" column in the RWA flow statement below.

### Advanced (total 618,300)

| Risk type | RWA | % of total |
|---|---|---|
| Credit risk (incl. CCR and CVA) | 451,500 | 73.0% |
| Market risk | 54,200 | 8.8% |
| Operational risk | 112,600 | 18.2% |

Market risk RWA is identical (54,200) in both approaches. Operational-risk RWA exists only in the Advanced figure; it is computed with a loss distribution approach combining internal and external loss data, scenario analysis and business-environment and internal-control factors.

### What drives each component

- **Credit risk.** Advanced credit RWA depends on internal PD, LGD and EAD parameters. The Pillar 3 report says these are served to capital calculators through the [Credit Risk Scoring API (API-10)](../apis/api-10-credit-risk-scoring-api.md) as through-the-cycle estimates with regulatory floors (the same API exposes separate point-in-time parameters for CECL). Standardized credit RWA uses supervisory risk weights and eligible collateral (cash, Treasuries and agencies, investment-grade debt, main-index equities); at year-end 2025 eligible financial collateral covered 214 billion of exposures, guarantees 18 billion and single-name credit derivatives 31 billion, with collateral values refreshed daily from the [Market Data API (API-12)](../apis/api-12-market-data-api.md).
- **Counterparty credit risk.** Standardized RWA uses SA-CCR; Advanced uses the internal models methodology, with CVA capital under the advanced CVA approach (CVA RWA 26.1 billion). Standardized CCR RWA of 41,600 comprises bilateral OTC derivatives 24,300, cleared OTC 1,100, exchange-traded 600, SFTs 9,800 and CCP default fund contributions 5,800.
- **Securitization.** Risk-weighted with the simplified supervisory formula approach or a 1,250% weight; RWA 9,300 on exposure of 47,114.
- **Equity (banking book).** RWA 6,900 on carrying value of 4,990.
- **Market risk.** Total 54,200 (2024: 52,600): regulatory VaR 11,400, stressed VaR 21,900, incremental risk charge 7,800, comprehensive risk measure 1,300 and standardized specific risk 11,800. Inputs come from the Market Data API and FX Rates API (API-13). Two backtesting exceptions in 2025 kept the regulatory multiplier below the five-exception trigger.

## 2025 RWA movement (Standardized)

| Driver | Credit | Market | Total |
|---|---|---|---|
| RWA at 31 Dec 2024 | 581,300 | 52,600 | 633,900 |
| Loan and commitment growth | 14,200 | - | 14,200 |
| Counterparty exposure (derivatives, SFTs) | 3,100 | - | 3,100 |
| Asset quality and collateral | (1,400) | - | (1,400) |
| Securities portfolio repositioning | 1,700 | - | 1,700 |
| Market risk positions and model updates | - | 1,600 | 1,600 |
| FX and other | (300) | - | (300) |
| **RWA at 31 Dec 2025** | **598,600** | **54,200** | **652,800** |

Standardized RWA rose 18.9 billion (3.0%). Credit growth was concentrated in retail (Card, +9.8 billion) and middle-market wholesale lending (+4.4 billion); the asset-quality offset reflects more eligible collateral on securities-based lending in Asset & Wealth Management; market-risk growth reflects higher stressed VaR in rates trading in the second quarter. Advanced RWA rose 14.2 billion (2.4%, from 604,100), less than Standardized because internal PD and LGD for Card reflect the high credit quality of new originations.

## Reported trajectory

| Date | Standardized RWA | Advanced RWA | Change |
|---|---|---|---|
| 31 Dec 2024 | 633,900 | 604,100 | |
| 31 Dec 2025 | 652,800 | 618,300 | +3.0% / +2.4% |
| 31 Mar 2026 | 661,000 | n/a | |
| 30 Jun 2026 | 668,400 | n/a | +1.1% q/q |

The Q2 2026 supplement attributes the flat 15.1% CET1 ratio to net income being offset by distributions and RWA growth of 1.1% ([Q2 2026 supplement](../../sources/reports/mhfc-q2-2026-earnings-supplement.md)). The 30 Jun 2026 value, delivered by API-16 as locked data, is the projection starting point.

## Where the numbers come from

The [Regulatory Reporting API (API-16)](../apis/api-16-regulatory-reporting-api.md) is the governed, general-ledger-reconciled source for RWA: its `GET /rwa/{asOf}?approach=standardized` endpoint returns RWA by exposure type and approach, and `GET /capital/{asOf}` returns CET1 together with `standardizedRwa` and `cet1Ratio`. Its upstreams are the general ledger, the RWA calculation engines and the FX Rates API; its downstream consumers are the Capital Planning model, FR Y-9C and FFIEC 101 filings, and Pillar 3. Operationally it is restricted to internal consumers (scope `regulatory:read`, 20 requests/minute) with quarter-end data locked by day 25 ([API reference](../../sources/api_docs/apis/api-16-regulatory-reporting-api.md)). Pillar 3 states the disclosures are consistent with the FR Y-9C, FFIEC 101 and FR Y-15 and are not audited but are subject to disclosure controls and Disclosure Committee review.

## Projecting RWA (MDL-CAP-003)

The Capital Planning & Stress Projection Model (MDL-CAP-003, Tier 1, owned by Corporate Treasury - Capital Management, validated by MRGR; last validated 2026-02-27, next due 2027-02-28) projects RWA over nine quarters (Q3 2026 to Q3 2028) from the 30 Jun 2026 actual of 668,400. It is re-run each quarter with updated starting capital, RWA and scenario paths ([model workbook](../../sources/models/capital-planning-model.md)).

**Mechanism.** RWA is deliberately simple: `RWA(t) = RWA(t-1) x (1 + quarterly growth)`. The model projects **total Standardized RWA only**; it does not project individual risk types, and it is not driven by loan-level or exposure-level calculations. The growth rate is an input: a flat 1.0% per quarter in the baseline (from the balance-sheet plan) and a scenario-specific path under severely adverse. The Pillar 3 report describes the stress path as reflecting increased draws on commitments and higher counterparty exposure early in the scenario. The CET1 ratio is then capital divided by projected RWA, returning 0 if RWA is 0.

| Quarter | Baseline growth | Baseline RWA | Stress growth | Stress RWA |
|---|---|---|---|---|
| Q2 2026 (actual) | | 668,400 | | 668,400 |
| Q3 2026 | 1.0% | 675,084 | +2.2% | 683,105 |
| Q4 2026 | 1.0% | 681,835 | +1.5% | 693,351 |
| Q1 2027 | 1.0% | 688,653 | +0.8% | 698,898 |
| Q2 2027 | 1.0% | 695,540 | +0.4% | 701,694 |
| Q3 2027 | 1.0% | 702,495 | 0.0% | 701,694 |
| Q4 2027 | 1.0% | 709,520 | -0.2% | 700,290 |
| Q1 2028 | 1.0% | 716,615 | -0.4% | 697,489 |
| Q2 2028 | 1.0% | 723,781 | -0.4% | 694,699 |
| Q3 2028 | 1.0% | 731,019 | -0.4% | 691,920 |

Reading the result: baseline RWA compounds to about 9.4% above the start (+62,619 by Q3 2028), whereas under stress RWA peaks at 701,694 (about 5.0% above start) in Q2-Q3 2027 and then declines to 691,920. In the stress case the denominator rises while CET1 capital falls, so RWA growth contributes to the trough of 12.90% in Q3 2027; the later RWA contraction helps recovery to 13.63%. In the baseline, capital growth outpaces the 1.0% RWA growth, lifting the ratio to 16.15%.

### How RWA feeds the model outputs

- **CET1 ratio and headroom.** Dollar headroom = CET1 capital minus (target or requirement) x RWA, so each unit of RWA consumes 13.0% of capital against the management target and 10.2% against the regulatory requirement. Under stress, headroom versus the 13.0% target is negative in Q2 2027 through Q4 2027 (the worst is -713 in Q3 2027), while headroom versus the 10.2% requirement stays positive throughout (minimum 18,934).
- **Indicative SCB.** The SCB add-on divides four quarters of planned dividends by *starting* RWA (668,400): 0.94%. Added to the 2.24% peak-to-trough decline this gives an indicative SCB of 3.18% (floored at 2.5%). See [Stress Capital Buffer](../concepts/stress-capital-buffer.md).
- **Excess capital.** Baseline excess CET1 over the 13.0% target at Q3 2028 is about 22,995, computed on 731,019 of projected RWA. The Q2 2026 supplement presents this as approximately 23.0 billion of capacity for organic growth, distributions or acquisitions.

## Invariants, limits and caveats

- **Single growth driver.** Because projected RWA is a pure growth-rate roll-forward, changing the baseline growth input moves the ratio mechanically; there is no feedback from distributions, credit quality or mix to RWA. Risk-type composition (credit, CCR, market) is not forecast.
- **Stress losses and RWA are independent inputs.** Stress losses are top-down inputs from the enterprise stress testing program and the RWA path is a separate scenario input, so consistency between them is a modeling-governance matter, not enforced by the workbook.
- **Standardized only.** The model starts from Standardized RWA and so does not reproduce the Advanced approach or the Collins Floor comparison; it relies on Standardized being the binding approach.
- **Simplifications.** The model does not capture AOCI volatility or deferred-tax-asset threshold deductions (these affect capital, not RWA).
- **Start-value dependency.** Starting RWA is read from API-16 (FR Y-9C / FFIEC 101 extract); a change to the API's schema or business logic opens a model change review, because upstream APIs are registered as critical data sources in the model inventory ([Pillar 3](../../sources/reports/mhfc-2025-pillar3-disclosures.md)). Pillar 3 does not reproduce projection outputs because they refresh quarterly; the latest are published in the quarterly earnings materials.
- **Unit and rate conventions.** Values are USD millions and growth rates are stored as decimals.

## Key figures at a glance

| Measure | Value |
|---|---|
| Standardized RWA, 31 Dec 2025 | 652,800 |
| Advanced RWA, 31 Dec 2025 | 618,300 |
| Standardized RWA, 30 Jun 2026 | 668,400 |
| Largest Standardized component | Wholesale credit, 47.9% |
| Baseline RWA at Q3 2028 | 731,019 |
| Stress RWA peak | 701,694 (Q2-Q3 2027) |
| Stress RWA at Q3 2028 | 691,920 |
