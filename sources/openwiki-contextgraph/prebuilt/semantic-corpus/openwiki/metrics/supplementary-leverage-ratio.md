---
type: FinancialMetric
title: Supplementary Leverage Ratio
description: Definition, exposure build-up, regulatory requirement (5.0%), internal 5.5% risk-appetite limit and reported levels (6.1% at 2024, 2025 and 2Q26) of the supplementary leverage ratio (SLR) for Meridian Harbor Financial Corp.
tags: [supplementary-leverage-ratio, slr, leverage, regulatory-capital, financial-metric]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-05T01:46:21.335Z
sources:
  - id: openwiki-source-6017268cd41c9c2877299736
    resource: repo://sources/api_docs/apis/api-16-regulatory-reporting-api.md
  - id: openwiki-source-eb14da62fbec45aad876fb64
    resource: repo://sources/reports/mhfc-2025-annual-report.md
  - id: openwiki-source-c13af588d055d118eda543d5
    resource: repo://sources/reports/mhfc-2025-pillar3-disclosures.md
  - id: openwiki-source-9da334bbfcfb68cd7514ff33
    resource: repo://sources/reports/mhfc-q2-2026-earnings-supplement.md
generated: { by: "openwiki/0.7.0", at: "2026-10-05T01:46:21.335Z" }
---

# Supplementary Leverage Ratio

The supplementary leverage ratio (SLR) is Tier 1 capital divided by total leverage exposure. Total leverage exposure includes on-balance-sheet assets and certain off-balance-sheet exposures ([Pillar 3 Disclosures](../../sources/reports/mhfc-2025-pillar3-disclosures.md), Section 5; [Annual Report](../../sources/reports/mhfc-2025-annual-report.md) glossary). For Meridian Harbor Financial Corp. (MHFC, a fictional institution in this corpus) the SLR is a risk-insensitive backstop to the risk-based [CET1 Ratio](cet1-ratio.md): it ignores risk weights, so it constrains balance-sheet size rather than asset mix. Amounts are USD millions unless noted.

Related: [Pillar 3 Disclosures 2025](../reports/pillar3-disclosures-2025.md), [CET1 Ratio](cet1-ratio.md).

## Reported levels

| Date | Tier 1 capital | Total leverage exposure | SLR |
|---|---|---|---|
| 31 Dec 2024 | 105,840 | 1,741,000 | 6.1% (+2 bps over the year to 2025) |
| 31 Dec 2025 | 110,620 | 1,812,000 | 6.10% |
| 30 Jun 2026 | not disclosed in the supplement | not disclosed | 6.1% |

- The SLR was 6.1% at both year-end 2024 and year-end 2025, a +2 bps change. Tier 1 capital grew 4.5% and total leverage exposure grew 4.1%, so the ratio barely moved ([Annual Report](../../sources/reports/mhfc-2025-annual-report.md)).
- At 2Q26 the Q2 2026 earnings supplement reports 6.1%, unchanged on a rounded basis from 1Q26 (6.1%) with a -3 bps quarterly change ([Q2 2026 supplement](../../sources/reports/mhfc-q2-2026-earnings-supplement.md)). The supplement does not give the 2Q26 Tier 1 capital or exposure, so the drivers of that small decline are not itemised.
- The companion Tier 1 leverage ratio (Tier 1 capital over average on-balance-sheet assets) was 7.91% at year-end 2025 (7.9% in both 2025 and 2024). It is a different measure: its denominator excludes off-balance-sheet and derivative/SFT add-ons, which is why it is higher than the SLR.

## Exposure build-up (31 Dec 2025)

| Component | Amount |
|---|---|
| On-balance-sheet assets | 1,418,560 |
| Less: Tier 1 capital deductions and other adjustments | (19,000) |
| Derivative exposures (replacement cost + PFE) | 98,600 |
| Securities financing transaction exposures | 142,500 |
| Off-balance-sheet exposures (after credit conversion factors) | 171,340 |
| **Total leverage exposure** | **1,812,000** |
| Tier 1 capital | 110,620 |
| **SLR** | **6.10%** |

The components sum to the reported exposure. The on-balance-sheet line equals reported total assets of 1,418,560. Roughly 78% of exposure is balance-sheet assets net of deductions; the remaining ~22% comes from derivatives, securities financing and off-balance-sheet commitments ([Pillar 3](../../sources/reports/mhfc-2025-pillar3-disclosures.md)).

## Requirement versus limit

Two thresholds apply, and they should not be conflated:

| Threshold | Level | Source nature |
|---|---|---|
| Minimum SLR | 3.0% | Regulatory |
| Enhanced SLR buffer (G-SIB) | 2.0% | Regulatory |
| **Effective regulatory requirement** | **5.0%** | Regulatory (3.0% + 2.0%) |
| Risk appetite limit | >= 5.5% | Internal, Board-approved |
| Tier 1 leverage ratio minimum | 4.0% | Regulatory (separate measure) |

The Pillar 3 report states that MHFC, as a G-SIB, is subject to a 3.0% minimum plus a 2.0% enhanced buffer, for an effective requirement of 5.0%. The Board-approved risk appetite table sets an internal SLR limit of at least 5.5%, with status "Within" at 6.1% for 31 Dec 2025. The internal limit sits 50 bps above the regulatory requirement, so a breach of management's limit would occur before any regulatory shortfall.

Headroom, derived from the year-end 2025 figures (not stated in the reports):

- Against 5.0%: Tier 1 capital needed on 1,812,000 of exposure is about 90,600, leaving roughly 20,000 of excess Tier 1 capital.
- Against 5.5%: needed Tier 1 is about 99,660, leaving roughly 10,960 of excess.
- Holding Tier 1 capital constant, exposure could rise to about 2.01 trillion before reaching 5.5%, around 11% above the year-end level.

## Relationship to other metrics

- **CET1 ratio.** The CET1 requirement of 10.2% and management target of 13.0% are risk-based and drive capital planning (see [CET1 Ratio](cet1-ratio.md)). The SLR is reported next to it in the annual report and earnings summary but has no separate projection in the sources reviewed. Capital distributions that reduce CET1 also reduce Tier 1 capital and therefore the SLR numerator, so buybacks (3,000 in 2Q26; 11.0 billion in 2025) weigh on both.
- **Other risk appetite metrics.** SLR is one of eight Board-approved appetite metrics alongside CET1 (13.0% baseline, 10.2% stressed), average LCR (>= 110%), NII and EVE sensitivities, card net charge-off rate and single-name concentration; all were within limits at year-end 2025.

## Data lineage

Leverage exposure components and the SLR are published by the Regulatory Reporting API (API-16) through its `GET /leverage/{asOf}` endpoint ("Total leverage exposure components and SLR"). API-16 is the governed golden source for Pillar 3 and is reconciled to the general ledger at legal-entity level, also feeding FR Y-9C, FFIEC 101 and FR Y-15 line items ([API-16 reference](../../sources/api_docs/apis/api-16-regulatory-reporting-api.md)). The Pillar 3 report lists API-16 as the source for its capital, RWA and leverage sections (Sections 3, 4, 5, 13).

## Caveats

- The reports round the SLR to one decimal (6.1%) in headline tables; only Pillar 3 gives 6.10%. Reading the unchanged 6.1% across 2024, 2025 and 2Q26 as "no movement" is approximate; the disclosed bps changes (+2, -3) show small movements.
- The sources reviewed give no SLR projections, stress-scenario SLR or management SLR target, only the 5.5% limit.
- No source states the regulatory reason for the 5.0% versus 5.5% difference beyond the internal buffer; treat 5.5% as management policy.
