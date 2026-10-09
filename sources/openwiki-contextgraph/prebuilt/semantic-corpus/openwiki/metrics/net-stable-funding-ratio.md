---
type: FinancialMetric
title: Net Stable Funding Ratio
description: Meridian Harbor's Net Stable Funding Ratio (NSFR) is available stable funding divided by required stable funding. It was 128% in Q4 2025 (126% in 2024). This page gives the ASF and RSF build-up, how it relates to the LCR, its data lineage through API-15, and what the sources do not disclose.
tags: [nsfr, liquidity, funding, basel-iii, pillar-3, treasury, financial-metric]
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

# Net Stable Funding Ratio (NSFR)

## Definition

The annual report glossary defines the NSFR as **available stable funding (ASF) divided by required stable funding (RSF)** ([Annual Report 2025, glossary](../../sources/reports/mhfc-2025-annual-report.md)). The Pillar 3 glossary uses the same ASF / RSF terms for the NSFR calculation ([Pillar 3 Disclosures 2025](../../sources/reports/mhfc-2025-pillar3-disclosures.md)). A ratio above 100% means stable funding exceeds the stable funding the asset and off-balance-sheet profile requires.

The NSFR is the structural companion to the [Liquidity Coverage Ratio](liquidity-coverage-ratio.md). The LCR tests whether high-quality liquid assets cover 30 days of stressed net outflows. The NSFR looks at whether the balance sheet's funding is sufficiently long-term and stable relative to its assets. Both are disclosed in Section 12 of the Pillar 3 report ([Pillar 3 Disclosures 2025](../reports/pillar3-disclosures-2025.md)).

## Reported levels

| Period | NSFR | Source |
|---|---|---|
| Year-end 2024 | 126% | Annual report liquidity metrics |
| Q4 2025 (average, Pillar 3) / 2025 (annual report) | 128% | Annual report; Pillar 3 §12.2 |

The ratio rose 2 points over 2025. The Q2 2026 earnings supplement does not report an NSFR, so no more recent figure is available in the sources. The Pillar 3 table is labelled "Q4 2025 average". The annual report liquidity table shows the same 128% under "2025" without an averaging label. Treat the two as the same disclosed figure.

## How the ratio is built

Pillar 3 §12.2 gives weighted amounts ($ millions, Q4 2025 average):

| Component | Weighted amount |
|---|---|
| ASF: regulatory capital and long-term debt | 214,600 |
| ASF: retail and small business deposits | 598,400 |
| ASF: wholesale funding and other | 269,000 |
| **Total ASF** | **1,082,000** |
| RSF: loans and securities | 671,800 |
| RSF: HQLA, derivatives and other assets | 142,700 |
| RSF: off-balance-sheet | 30,800 |
| **Total RSF** | **845,300** |
| **NSFR** | **128%** |

The table is internally consistent:

- ASF components sum to 1,082,000 and RSF components to 845,300.
- 1,082,000 / 845,300 is about 128.0%.
- The implied surplus of ASF over RSF is about 236,700 ($ millions).

What the composition shows:

- Retail and small business deposits are the largest ASF component, about 55% of total ASF (598,400 / 1,082,000). This fits the annual report's statement that deposits are the primary funding source, with about 66% from consumer and small-business clients.
- Regulatory capital and long-term debt supply about 20% of ASF. Long-term debt outstanding was $86.7 billion, with a weighted-average remaining maturity of 6.8 years.
- Loans and securities are about 79% of total RSF (671,800 / 845,300). The loan book is therefore the main driver of required stable funding.
- Only weighted amounts are disclosed. Unlike the LCR table, the NSFR table gives no unweighted balances or maturity buckets, so the applied ASF and RSF factors cannot be recomputed from the sources.

## Risk appetite and limits

The Pillar 3 risk appetite table lists LCR (average) at ≥ 110% as the liquidity ratio limit. It carries **no NSFR limit or threshold**. The framework's other liquidity parameter is that liquidity sources must exceed stressed outflows over a 90-day horizon. The annual report states this held in every material legal entity at December 31, 2025 ([Pillar 3 Disclosures 2025](../../sources/reports/mhfc-2025-pillar3-disclosures.md); [Annual Report 2025](../../sources/reports/mhfc-2025-annual-report.md)). The sources do not state an internal NSFR target or the regulatory minimum.

## Data lineage and ownership

- Treasury/CIO, in the Corporate segment, is responsible for liquidity risk management. The Liquidity Risk Oversight function in the Chief Risk Office provides independent oversight.
- Liquidity positions across all legal entities are aggregated daily through the [Treasury Liquidity Positions API (API-15)](../apis/api-15-treasury-liquidity-positions-api.md). Pillar 3 says it provides legal-entity-level views of HQLA, encumbrance and contractual cash flows to the liquidity stress testing engine, the **LCR and NSFR calculators**, and the asset-liability management models.
- The Pillar 3 data-lineage table lists API-15 against MDL-ALM-014, MDL-CAP-003 and "LCR/NSFR", and cites Sections 11 and 12 ([Pillar 3 Disclosures 2025](../../sources/reports/mhfc-2025-pillar3-disclosures.md)).

## Interpretation notes

- A 128% ratio is a reported average-period disclosure, not a regulatory-limit headroom calculation. Headroom cannot be stated without the applicable minimum, which the sources do not give.
- The NSFR and LCR moved in the same direction in 2025: NSFR 126% to 128%, LCR 113% to 116%.
- The loan-to-deposit ratio was 73% in both 2024 and 2025. This is consistent with a deposit-funded balance sheet and a stable NSFR.
- Other disclosures for the same year: unencumbered marketable securities of $318.0 billion (2024: $305.0 billion).

## Sources

- [Pillar 3 Disclosures 2025, §12.2 and risk appetite](../../sources/reports/mhfc-2025-pillar3-disclosures.md)
- [Annual Report 2025, Liquidity Risk Management and glossary](../../sources/reports/mhfc-2025-annual-report.md)
- [Q2 2026 Earnings Supplement](../../sources/reports/mhfc-q2-2026-earnings-supplement.md) (no NSFR reported)
