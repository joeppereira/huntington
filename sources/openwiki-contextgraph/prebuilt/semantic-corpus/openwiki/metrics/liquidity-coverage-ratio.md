---
type: FinancialMetric
title: Liquidity Coverage Ratio
description: Meridian Harbor's Liquidity Coverage Ratio (LCR) is the stock of high-quality liquid assets (HQLA) divided by 30-day stressed net cash outflows. This page gives the reported levels (116% in Q4 2025, 115% in Q2 2026), the HQLA and outflow build-up, the 110% risk-appetite floor, and how API-15 feeds the calculation.
tags: [lcr, hqla, liquidity, basel-iii, risk-appetite, treasury, financial-metric]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-05T01:46:21.335Z
sources:
  - id: openwiki-source-eb14da62fbec45aad876fb64
    resource: repo://sources/reports/mhfc-2025-annual-report.md
  - id: openwiki-source-c13af588d055d118eda543d5
    resource: repo://sources/reports/mhfc-2025-pillar3-disclosures.md
  - id: openwiki-source-9da334bbfcfb68cd7514ff33
    resource: repo://sources/reports/mhfc-q2-2026-earnings-supplement.md
generated: { by: "openwiki/0.7.0", at: "2026-10-05T01:46:21.335Z" }
---

# Liquidity Coverage Ratio (LCR)

## Definition

The annual report glossary defines the LCR as HQLA divided by net cash outflows over a 30-day stress period. HQLA is the stock of high-quality liquid assets eligible for the ratio ([Annual Report 2025, glossary](../../sources/reports/mhfc-2025-annual-report.md)). Meridian Harbor reports an **average** LCR, calculated as a quarterly average rather than a point-in-time figure. The reported figures are:

- Q4 2025 average: 116%.
- Q2 2026 average: 115%.

Treasury/CIO is the Corporate segment function that manages the Firm's liquidity (see [Corporate](../organizations/corporate.md)). Treasury/CIO is responsible for liquidity risk management. The Liquidity Risk Oversight function within the Chief Risk Office provides independent oversight.

The companion structural measure is the [Net Stable Funding Ratio](net-stable-funding-ratio.md). The LCR covers short-term resilience and the NSFR covers one-year structural funding. Both are disclosed in the Pillar 3 liquidity section ([Pillar 3 Disclosures 2025](../reports/pillar3-disclosures-2025.md)).

## Reported levels

| Period | Average LCR | Average HQLA ($m) | Source |
|---|---|---|---|
| Q4 2024 | 113% | 274,500 | Annual report liquidity metrics |
| Q4 2025 | 116% | 286,000 | Annual report; Pillar 3 §12.1 |
| 1Q26 | 117% | not given | Q2 2026 earnings supplement |
| 2Q26 | 115% | 292,300 | Q2 2026 earnings supplement |

The LCR rose 3 points over 2025 (113% to 116%). It fell 2 points from 1Q26 to 2Q26 (117% to 115%). The earnings supplement summarises 2Q26 as an average LCR of 115% alongside a Standardized CET1 ratio of 15.1% and a supplementary leverage ratio of 6.1%.

Average HQLA grew in both periods, from 286,000 to 292,300 ($m) between Q4 2025 and 2Q26. The ratio still fell, because weighted net outflows grew faster, from 246,550 to 254,200 ($m).

## How the ratio is built

The Pillar 3 and earnings tables show the numerator and denominator in two steps. Outflows are weighted by run-off assumptions and inflows are netted against them.

| Component ($m, weighted) | Q4 2025 | 2Q26 |
|---|---|---|
| **HQLA** | 286,000 | 292,300 |
| Retail (and small business) funding outflows | 40,900 (unweighted 652,300) | 41,800 (unweighted 668,900) |
| Unsecured wholesale funding outflows | 168,900 (unweighted 415,700) | 171,400 (unweighted 421,300) |
| Secured wholesale funding / derivative outflows | 36,800 | 38,600 |
| Additional requirements (derivatives, commitments) | 122,200 | 131,900 (commitments and other) |
| Other outflows | 13,600 | not shown separately |
| **Total cash outflows** | 382,400 | 383,700 |
| Total cash inflows | (135,850) | (129,500) |
| **Net cash outflows** | 246,550 | 254,200 |
| **LCR** | 116% | 115% |

The tables are internally consistent. Q4 2025 inflows combine secured lending inflows of 74,300 and inflows from fully performing exposures of 61,550. Net outflows are total outflows minus total inflows (382,400 − 135,850 = 246,550). HQLA of 286,000 divided by 246,550 gives about 116%. For 2Q26, 292,300 divided by 254,200 gives about 115%.

Two disclosure differences matter when comparing periods:

- The 2Q26 supplement splits HQLA into Level 1 (cash, central bank reserves, Treasuries) at 221,900 and Level 2A and 2B at 70,400, which sum to 292,300. The Pillar 3 Q4 2025 table shows only the HQLA total.
- Row labels are grouped differently between the two tables. In 2Q26 the derivative outflows are merged with secured funding, and commitments are merged with "other". The line items are therefore not strictly like-for-like.

The retail outflow rate in the Q4 2025 table is about 6.3% (40,900 / 652,300). The unsecured wholesale rate is about 40.6% (168,900 / 415,700). Wholesale funding is a much larger driver of stressed outflows than retail funding.

## Risk appetite and limits

The Board-approved risk appetite framework carries an LCR (average) floor of **≥ 110%**. At December 31, 2025 the reported 116% was "Within" the limit, a 6-point cushion. At 2Q26 the 115% is 5 points above the same floor. The framework refers to this threshold when it applies the 110% floor. The 2Q26 supplement does not restate the limit.

The framework also requires liquidity sources to exceed stressed outflows over a **90-day** horizon. This is the Firm's internal stress test and it is distinct from the 30-day regulatory LCR window. It assumes the loss of unsecured wholesale funding, accelerated deposit outflows, collateral calls from a three-notch downgrade, and draws on committed facilities. At December 31, 2025, liquidity sources exceeded stressed outflows in every material legal entity ([Annual Report 2025](../../sources/reports/mhfc-2025-annual-report.md)).

## Data lineage: API-15

The [Treasury Liquidity Positions API (API-15)](../apis/api-15-treasury-liquidity-positions-api.md) is the data source for the numerator and the cash-flow projections. Its documented behaviour is:

- Positions across all legal entities are aggregated daily. The API publishes intraday and end-of-day cash, collateral and HQLA positions.
- Pillar 3 describes the feed as legal-entity-level views of HQLA, encumbrance and contractual cash flows. These go to the liquidity stress testing engine, the **LCR and NSFR calculators**, and the asset-liability management models.
- The Q2 2026 supplement says HQLA and cash flow projections are compiled daily from API-15.
- API-15 also supplies balance-sheet positions to the NII Sensitivity Model (MDL-ALM-014) and liquidity constraints to the Capital Planning & Stress Projection Model (MDL-CAP-003).
- The annual report classifies API-15 as a critical data service. Critical data services get enhanced change management and data-quality controls, because they feed Tier 1 models and regulatory reports.

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: an unescaped angle bracket inside a label breaks rendering; rephrase the label. -->
```text
flowchart LR
  GL[General ledger, payments, custody, deposits] --> API15[API-15 Treasury Liquidity Positions]
  API15 --> LCRCALC[LCR and NSFR calculators]
  API15 --> STRESS[Liquidity stress testing engine]
  API15 --> ALM[ALM models: MDL-ALM-014, MDL-CAP-003]
  LCRCALC --> P3[Pillar 3 section 12 and earnings supplement]
  LCRCALC --> RAF[Risk appetite monitoring: LCR >= 110%]
```

## Interpretation notes

- HQLA is an average of the quarter, not a period-end amount, so the average LCR may differ from period-end liquidity.
- Total liquidity is wider than HQLA. The Firm also holds unencumbered marketable securities ($318.0 billion at year-end 2025, versus $305.0 billion in 2024). At 2Q26 it cited about $560 billion of total liquidity resources, including unencumbered securities and borrowing capacity at the Federal Home Loan Banks and the Federal Reserve discount window. That figure should not be confused with HQLA.
- Related ratios at year-end 2025: NSFR 128% (126% in 2024) and loan-to-deposit 73% (unchanged).
- About 66% of deposits come from consumer and small-business clients, and an estimated 58% of total deposits are insured or fully collateralized.
- Liquidity models fall under the Model Risk Policy aligned with SR 11-7 ([Basel III Pillar 3](../concepts/basel-iii-pillar-3.md) covers the disclosure framework).

## Sources

- [Pillar 3 Disclosures 2025, §12.1 and risk appetite](../../sources/reports/mhfc-2025-pillar3-disclosures.md)
- [Annual Report 2025, Liquidity Risk Management](../../sources/reports/mhfc-2025-annual-report.md)
- [Q2 2026 Earnings Supplement, LCR detail](../../sources/reports/mhfc-q2-2026-earnings-supplement.md)
