---
type: Report
title: 2025 Pillar 3 Regulatory Capital Disclosures
description: Structure, key templates and page markers of the Meridian Harbor Financial Corp. Basel III Pillar 3 report for the year ended December 31, 2025, with its headline capital, RWA, leverage and liquidity figures and the metrics, concepts, models and APIs it ties to.
tags: [pillar-3, basel-iii, regulatory-capital, fy2025, cet1, rwa, leverage, liquidity, irrbb, model-risk, report]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-05T02:29:31.666Z
sources:
  - id: openwiki-source-d7481767c8aa79de795d1f43
    resource: repo://sources/models/capital-planning-model.md
  - id: openwiki-source-9e2090b855b8be2710ba081f
    resource: repo://sources/models/nii-sensitivity-model.md
  - id: openwiki-source-eb14da62fbec45aad876fb64
    resource: repo://sources/reports/mhfc-2025-annual-report.md
  - id: openwiki-source-c13af588d055d118eda543d5
    resource: repo://sources/reports/mhfc-2025-pillar3-disclosures.md
generated: { by: "openwiki/0.7.0", at: "2026-10-05T02:29:31.666Z" }
---

# 2025 Pillar 3 Regulatory Capital Disclosures

The Pillar 3 report of [Meridian Harbor Financial Corp.](../organizations/meridian-harbor-financial-corp.md) (MHFC) covers the fiscal year ended **December 31, 2025** and was published March 2026. It is prepared under 12 CFR 217 Subpart D (§217.61-63) and Subpart E (§217.171-173) (§ cover, `<!-- page 1 -->`). It is a **synthetic proof-of-concept document**: the firm and all figures are fictional (p. 1, p. 22). The source was converted from `raw/reports/MHFC_2025_Pillar3_Disclosures.pdf`; the `<!-- page N -->` markers (22 pages) are used for every citation below. The Contents table on pp. 2-3 did not survive conversion and is empty, so the structure here comes from the requirement-to-section table on p. 4 and the section headings. For the framework itself see [Basel III Pillar 3](../concepts/basel-iii-pillar-3.md).

What distinguishes this report from the [2025 Annual Report](annual-report-2025.md) is that it ties capital, rate-risk and liquidity numbers to named Tier 1 models (`MDL-*`) and Developer Platform APIs (`API-NN`), and states where each disclosure's data came from (§14-15).

## Scope and basis of preparation (§1, p. 4)

- Covers the **consolidated bank holding company**; the principal insured depository institution, Meridian Harbor Bank, N.A., has separate capital requirements and is well capitalized. No impediments to moving funds or capital within the Firm beyond those generally applicable to U.S. bank holding companies.
- MHFC is an **advanced approaches** banking organization, computing RWA under both Standardized and Advanced approaches. The lower of each ratio is used for capital adequacy (the "Collins Floor"), **currently the Standardized approach**.
- The disclosures are **not required to be audited**, but are subject to disclosure controls and Disclosure Committee review, and are described as consistent with FR Y-9C, FFIEC 101 and FR Y-15.

## Structure and page map

| Section | Content | Page marker |
|---|---|---|
| Cover, Contents | Title, March 2026 publication, synthetic disclaimer; empty contents table | 1-3 |
| 1 Introduction and Scope; requirement-to-section table | Scope, approaches, audit status | 4 |
| 2 Risk Management Framework | Three lines of defense, CRO, risk appetite table, committees | 4-5 |
| 3 Capital Structure | Common equity to CET1 reconciliation, capital instruments | 6 |
| 4 Capital Adequacy (4.1 RWA, 4.1a RWA flow, 4.1b CCyB, 4.2 ratios/buffers) | Standardized and Advanced RWA, RWA movement, buffers | 7-9 |
| 5 Leverage | Total leverage exposure, SLR | 10 |
| 6 Credit Risk (6.1-6.5) | Exposure by type/geography/maturity/industry, equities, PD bands, allowance, CRM | 10-12 |
| 7 Counterparty Credit Risk; 8 Securitization | CCR EAD/RWA, derivatives, CVA; securitization RWA | 13 |
| 9 Market Risk; 10 Operational Risk | Market RWA components, VaR, backtesting; operational loss and RWA | 14-15 |
| 11 IRRBB | NII and EVE sensitivity, assumptions, limitations | 16 |
| 12 Liquidity (12.1 LCR, 12.2 NSFR) | Q4 2025 average LCR and NSFR build-ups | 17 |
| 13 Capital Planning and Stress Testing | MDL-CAP-003, internal scenario, CCAR 2025, reverse stress tests | 18 |
| 14 Model Risk Management and Model Inventory | Three Tier 1 model cards and validation findings | 19-20 |
| 15 Risk Data Aggregation and API Data Lineage | API-to-model-to-disclosure map | 21 |
| 16 Remuneration and Risk Alignment; Glossary | MRT compensation, deferral and clawback; terms | 22 |

The p. 4 table maps Pillar 3 requirements to sections: scope (§1), capital structure (§3), capital adequacy (§4), buffers (§4.2), leverage (§5), credit risk (§6), CCR (§7), securitization (§8), market risk (§9), operational risk (§10), IRRBB (§11), liquidity (§12), stress testing (§13) and model risk/data governance (§14-15).

## Key templates and headline figures

All figures are as of **December 31, 2025** unless stated (Q4 2025 average for liquidity).

### Capital structure (§3, p. 6)

| Item ($mm) | Dec 31, 2025 |
|---|---|
| Common stockholders' equity | 116,240 |
| Common Equity Tier 1 capital | 98,450 |
| Tier 1 capital | 110,620 |
| Total capital (Standardized) | 128,900 |

CET1 reconciles from common equity by deducting goodwill (14,210), other intangibles (2,150), NOL/credit-carryforward DTAs (1,380), pension net assets (1,240) and other adjustments (2,230), and adding back cash-flow-hedge AOCI losses (3,420). Tier 1 adds 12,500 of qualifying preferred (less 330 of deductions); Total capital adds 11,900 of subordinated debt and 6,380 of qualifying allowance. CET1 capital rose $5.3 billion in 2025: net income $25.0 billion, less common dividends $6.1 billion, repurchases $11.0 billion, preferred dividends $1.1 billion and other movements including AOCI. The instruments table (p. 6) lists 1,388.8 million common shares, Series AA/CC/DD/EE preferred (AT1; 2.5/3.0/4.0/3.0 billion) and subordinated notes due 2033-2045 (11,900; Tier 2).

### Ratios and buffers (§4.2, p. 9)

| Ratio | Standardized | Advanced | Requirement | Well-capitalized |
|---|---|---|---|---|
| CET1 | 15.08% | 15.92% | 10.2% | n/a |
| Tier 1 | 16.95% | 17.89% | 11.7% | 6.0% |
| Total capital | 19.75% | 20.54% | 13.7% | 10.0% |

The Standardized conservation buffer requirement is the stress capital buffer (3.2%) plus the G-SIB surcharge (2.5%) plus the CCyB (currently 0%), i.e. 5.7%. The actual Standardized buffer was **10.58%**, so no distribution or discretionary bonus limits applied; eligible retained income was $23.9 billion (p. 9). The CCyB table (§4.1b, p. 8) shows a 0.00% U.S. rate and a firm-specific non-U.S. weighted contribution of 0.108%, shown for transparency and Advanced computations. See [Stress Capital Buffer](../concepts/stress-capital-buffer.md) and [G-SIB Surcharge](../concepts/gsib-surcharge.md).

### Risk-weighted assets (§4.1, §4.1a, p. 7-8)

| Standardized RWA ($mm) | RWA | % |
|---|---|---|
| Wholesale credit | 312,400 | 47.9% |
| Retail credit | 196,800 | 30.1% |
| Counterparty credit | 41,600 | 6.4% |
| Securitization | 9,300 | 1.4% |
| Equity | 6,900 | 1.1% |
| Other assets | 31,600 | 4.8% |
| Market risk | 54,200 | 8.3% |
| **Total Standardized** | **652,800** | 100.0% (capital at 8%: 52,224) |

Advanced RWA totals **618,300** ($mm): credit incl. CCR/CVA 451,500 (73.0%), market 54,200 (8.8%), operational 112,600 (18.2%). Because Standardized RWA is larger, the Standardized CET1 ratio (98,450 / 652,800 = 15.08%) is lower than the Advanced (15.92%) and binds. Standardized RWA rose from 633,900 to 652,800 (+$18.9 billion): loan and commitment growth +14,200 (Card and C&I; Card retail +9.8 billion, middle-market wholesale +4.4 billion), counterparty +3,100, asset quality/collateral (1,400), securities repositioning +1,700, market risk +1,600, FX/other (300) (p. 8). Advanced RWA rose $14.2 billion, more slowly because Card PD/LGD from [API-10](../apis/api-10-credit-risk-scoring-api.md) reflects high-quality new originations (p. 7). See [Risk-Weighted Assets](../metrics/risk-weighted-assets.md) and [CET1 Ratio](../metrics/cet1-ratio.md).

### Leverage (§5, p. 10)

Total leverage exposure was **$1,812,000mm** (on-balance-sheet 1,418,560, less 19,000 of adjustments, derivatives 98,600, SFTs 142,500, off-balance-sheet 171,340). With Tier 1 capital of 110,620 the **SLR was 6.10%** against an effective G-SIB requirement of 5.0% (3.0% minimum + 2.0% enhanced buffer); the Tier 1 leverage ratio was 7.91% (minimum 4.0%). See [Supplementary Leverage Ratio](../metrics/supplementary-leverage-ratio.md).

### Liquidity (§12, p. 17)

Q4 2025 averages: HQLA 286,000 over total net cash outflows 246,550 (outflows 382,400, inflows 135,850) gives an **LCR of 116%**; available stable funding 1,082,000 over required stable funding 845,300 gives an **NSFR of 128%**. Both are computed from positions aggregated daily through [API-15](../apis/api-15-treasury-liquidity-positions-api.md). See [Liquidity Coverage Ratio](../metrics/liquidity-coverage-ratio.md) and [Net Stable Funding Ratio](../metrics/net-stable-funding-ratio.md).

### Risk appetite (§2, p. 5)

Board limits and 2025 outcomes, all "Within": Standardized CET1 >= 13.0% (15.08%); internal severely adverse minimum CET1 >= 10.2% (12.6%); SLR >= 5.5% (6.1%); average LCR >= 110% (116%); NII decline under -200 bp <= 7.0% (6.0%); EVE decline under +200 bp <= 15.0% of Tier 1 (2.5%); Card net charge-off rate <= 4.5% (3.42%); single-name wholesale exposure <= 10% of Tier 1 (4.8%). The CRO reports to the CEO and Board Risk Committee within a three-lines-of-defense model (p. 4).

### Other risk templates

- **Credit (§6, pp. 10-12):** total credit exposure $1,589.1 billion (loans $742.3 billion); wholesale exposure $1,214.1 billion, 74% investment grade; PD-band table (Advanced) with wholesale EAD $854.2 billion (avg PD 1.21%) and retail EAD $471.0 billion (2.09%). The allowance is **15,920** ($mm) under CECL via [MDL-CR-007](../models/cecl-allowance-model.md) with $681 million of qualitative overlays; 6,380 qualifies as Tier 2 (p. 12). Regulatory PD/LGD are through-the-cycle while CECL uses point-in-time parameters, served from separate API-10 endpoints. 2025 NCOs were 6,100; nonaccrual 5,150 (p. 12). See [Allowance for Credit Losses](../metrics/allowance-for-credit-losses.md) and [CECL](../concepts/cecl.md).
- **Counterparty credit and securitization (§7-8, p. 13):** CCR EAD 147,600 and Standardized RWA 41,600; Advanced CVA RWA $26.1 billion; additional collateral on downgrade about $2.1 billion (one notch) and $4.6 billion (two notches). Securitization exposure 47,114 with RWA 9,300.
- **Market risk (§9, p. 14):** market risk RWA 54,200 (52,600 at Dec 31, 2024); total regulatory VaR (10-day, 99%) average 160, period-end 149 ($mm); **2 backtesting exceptions**, below the five that would lift the multiplier above 3.0. See [Value at Risk](../metrics/value-at-risk.md).
- **Operational risk (§10, pp. 14-15):** operational risk RWA $112.6 billion (loss distribution approach); 2025 losses $1.4 billion (41% clients/products/business practices, 28% external fraud, 17% execution/delivery).
- **Remuneration (§16, p. 22):** deferral of at least 40% (60% for the Operating Committee) over three to five years; 1.1% of eligible employees had pay reduced for risk, control or conduct.

## IRRBB (§11, p. 16)

The NII measure comes from [MDL-ALM-014](../models/nii-sensitivity-model.md), a Tier 1 model validated by MRGR in September 2025. It applies instantaneous parallel shocks of +/-100 and +/-200 bp to the Dec 31, 2025 balance sheet (static, no growth), with deposit betas of 0.45 consumer, 0.75 wholesale and 0.00 non-interest-bearing, and EVE approximated by modified duration (3.5 years for non-interest-bearing deposits, 2.8 years for consumer interest-bearing).

| Scenario | 12-month NII ($mm) | % base NII | EVE ($mm) | EVE % Tier 1 |
|---|---|---|---|---|
| Down 200 bp | (3,017) | (6.0%) | 2,737 | 2.5% |
| Down 100 bp | (1,508) | (3.0%) | 1,369 | 1.2% |
| Up 100 bp | 1,508 | 3.0% | (1,369) | (1.2%) |
| Up 200 bp | 3,017 | 6.0% | (2,737) | (2.5%) |

Base-case 12-month NII is $50,237 million. The report lists limitations (no non-parallel moves, basis risk, mortgage prepayment optionality, deposit-beta convexity) covered by quarterly dynamic simulation reviewed by ALCO. See [IRRBB](../concepts/irrbb.md), [Economic Value of Equity](../concepts/economic-value-of-equity.md) and [Parallel Rate Shocks](../scenarios/parallel-rate-shocks.md).

## Capital planning and stress testing (§13, p. 18)

[MDL-CAP-003](../models/capital-planning-model.md) projects CET1, RWA and ratios over nine quarters, combining PPNR, provisions and trading/counterparty losses with planned capital actions. Starting positions come from [API-16](../apis/api-16-regulatory-reporting-api.md) and scenarios (set SA-2025-INT) from [API-14](../apis/api-14-macroeconomic-scenario-api.md). Under stress, buybacks are suspended and dividends held flat. The internal severely adverse scenario (peak unemployment 10.2%, real GDP -6.4%, equities -41%, house prices -28%, CRE prices -35%) is described in [Internal Severely Adverse](../scenarios/internal-severely-adverse.md). In the 2025 CCAR cycle the Fed's projected minimum CET1 was **12.1%** (stress capital buffer 3.2%) versus the Firm's own **12.6%**. Projection outputs are deliberately not reproduced, since they refresh quarterly and are published in earnings materials. Reverse stress tests examined a cyber event on payment systems with a severe recession and sustained negative policy rates.

## Models, APIs and data lineage (§14-15, pp. 19-21)

Tier 1 models are tiered under an [SR 11-7](../concepts/model-risk-sr-11-7.md)-aligned policy with annual independent validation by [MRGR](../teams/model-risk-governance-review.md), quarterly monitoring and annual owner attestation. Each upstream API is registered as a critical data source, so a breaking schema or logic change automatically opens a model change review (p. 19).

| Model | Last validation / next due | Upstream APIs | Pillar 3 disclosure |
|---|---|---|---|
| MDL-ALM-014 NII Sensitivity | 2025-09-18 / 2026-09-30 | API-12, API-15, API-11 | §11 IRRBB |
| MDL-CR-007 CECL | 2025-11-04 / 2026-11-30 | API-10, API-11, API-14 | §6 allowance (also Annual Report Note 6) |
| MDL-CAP-003 Capital Planning | 2026-02-27 / 2027-02-28 | API-16, API-14, API-15 | §13 |

Validation findings (p. 20): MDL-CR-007 had one medium finding (no explicit unfunded-commitments model, remediated by interim overlay) and one low; MDL-ALM-014 had a medium finding that deposit betas are constant across shock sizes (compensated by quarterly dynamic simulation); MDL-CAP-003 had nothing above low.

The §15 table (p. 21) maps API-08 through API-16 to models and sections, e.g. API-16 to MDL-CAP-003, FR Y-9C and Pillar 3 §3, 4, 5, 13; API-15 to §11-12; API-10 to §4 and §6; API-12/13 to §9. In 2025 the Firm migrated API-16 and API-14 to the strategic data platform and added automated API-16-to-general-ledger reconciliation at legal-entity level; no data-quality exception materially affected reported capital ratios. Governance follows [BCBS 239](../concepts/bcbs-239.md); see also [API-to-Model-to-Report Lineage](../workflows/api-to-model-to-report-lineage.md).

## Agreement with models and other reports

- **MDL-ALM-014:** the NII workbook's Summary sheet shows Down 200 bp change in NII of -3,016.89 ($mm), -6.01%, EVE +2,737.40 (2.47% of Tier 1), and base NII 50,236.91, matching the rounded §11 table (-3,017; 6.0%; 2,737; 2.5%).
- **MDL-CAP-003:** the workbook's starting point is **Q2 2026 actuals** (starting CET1 ratio 15.14%), not year-end 2025, so it does not reproduce the Pillar 3 year-end figures; the report itself defers projections to quarterly materials. Both share the API-16 / API-14 sourcing.
- **Annual Report:** reports Standardized CET1 of 15.1% (the rounded 15.08%) and Q4 average LCR of 116%, consistent with this report.

## Relationships

- discloses: [CET1 ratio](../metrics/cet1-ratio.md), [risk-weighted assets](../metrics/risk-weighted-assets.md), [supplementary leverage ratio](../metrics/supplementary-leverage-ratio.md), [liquidity coverage ratio](../metrics/liquidity-coverage-ratio.md), [net stable funding ratio](../metrics/net-stable-funding-ratio.md), [allowance for credit losses](../metrics/allowance-for-credit-losses.md), [value at risk](../metrics/value-at-risk.md).
- discloses: [IRRBB](../concepts/irrbb.md) results from [MDL-ALM-014](../models/nii-sensitivity-model.md), capital planning results from [MDL-CAP-003](../models/capital-planning-model.md), and the allowance from [MDL-CR-007](../models/cecl-allowance-model.md).
- applies: [Basel III Pillar 3](../concepts/basel-iii-pillar-3.md), [G-SIB surcharge](../concepts/gsib-surcharge.md), [stress capital buffer](../concepts/stress-capital-buffer.md), [BCBS 239](../concepts/bcbs-239.md).
- derived-from: [API-16 Regulatory Reporting API](../apis/api-16-regulatory-reporting-api.md) (capital, RWA, leverage), [API-15 Treasury Liquidity Positions API](../apis/api-15-treasury-liquidity-positions-api.md) (liquidity), plus [API-10](../apis/api-10-credit-risk-scoring-api.md), [API-11](../apis/api-11-loan-servicing-api.md), [API-12](../apis/api-12-market-data-api.md), [API-13](../apis/api-13-fx-rates-api.md) and [API-14](../apis/api-14-macroeconomic-scenario-api.md) per the §15 lineage table.
- related: [2025 Annual Report](annual-report-2025.md), which discloses the same models in its Capital Risk Management and Market Risk Management sections.
