---
type: quickstart
title: Quickstart
description: Task-routing map for the Meridian Harbor Financial Corp. (fictional bank) wiki. Pick a question type, then follow the lineage chain API -> model -> metric -> report to the right folder and page.
tags: [quickstart, routing, data-lineage, navigation, mhfc]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-05T01:46:21.335Z
sources:
  - id: openwiki-source-6017268cd41c9c2877299736
    resource: repo://sources/api_docs/apis/api-16-regulatory-reporting-api.md
  - id: openwiki-source-65a2ad8de7d532680de82b60
    resource: repo://sources/api_docs/mhfc-developer-platform-api-reference.md
  - id: openwiki-source-d7481767c8aa79de795d1f43
    resource: repo://sources/models/capital-planning-model.md
  - id: openwiki-source-b575b40c2132eeef7814e5c4
    resource: repo://sources/models/cecl-allowance-model.md
  - id: openwiki-source-9e2090b855b8be2710ba081f
    resource: repo://sources/models/nii-sensitivity-model.md
  - id: openwiki-source-c13af588d055d118eda543d5
    resource: repo://sources/reports/mhfc-2025-pillar3-disclosures.md
generated: { by: "openwiki/0.7.0", at: "2026-10-05T01:46:21.335Z" }
---

# Quickstart

This wiki documents a fictional bank, Meridian Harbor Financial Corp. (MHFC). The sources are three financial reports, three Excel models and an 18-API Developer Platform reference, not code. Each entity has its own small page, and this page only routes you to them. For the big picture read the [Overview](overview.md).

## The one idea to remember

Reported model numbers trace back through a fixed chain:

**API -> model -> metric -> report**

Each Developer Platform API documents its upstream sources and downstream consumers. Each model workbook lists the API feeds that fill its input cells. The reports' model inventories name the disclosures that use each model. The full joined chain is on [API to Model to Report Lineage](workflows/api-to-model-to-report-lineage.md).

| Model | Consumes | Produces | Disclosed in |
|---|---|---|---|
| [MDL-CR-007 CECL Allowance](models/cecl-allowance-model.md) | [API-10](apis/api-10-credit-risk-scoring-api.md), [API-11](apis/api-11-loan-servicing-api.md), [API-14](apis/api-14-macroeconomic-scenario-api.md) | [Allowance for credit losses](metrics/allowance-for-credit-losses.md) | [Annual Report](reports/annual-report-2025.md), [Q2 2026 Supplement](reports/q2-2026-earnings-supplement.md) |
| [MDL-ALM-014 NII Sensitivity](models/nii-sensitivity-model.md) | [API-11](apis/api-11-loan-servicing-api.md), [API-12](apis/api-12-market-data-api.md), [API-15](apis/api-15-treasury-liquidity-positions-api.md) (plus [API-16](apis/api-16-regulatory-reporting-api.md) for Tier 1 capital) | [Net interest income](metrics/net-interest-income.md) and [EVE](concepts/economic-value-of-equity.md) sensitivity | [Annual Report](reports/annual-report-2025.md), [Pillar 3](reports/pillar3-disclosures-2025.md) |
| [MDL-CAP-003 Capital Planning](models/capital-planning-model.md) | [API-16](apis/api-16-regulatory-reporting-api.md), [API-14](apis/api-14-macroeconomic-scenario-api.md) | [CET1 ratio](metrics/cet1-ratio.md), [RWA](metrics/risk-weighted-assets.md), indicative [stress capital buffer](concepts/stress-capital-buffer.md) | [Annual Report](reports/annual-report-2025.md), [Pillar 3](reports/pillar3-disclosures-2025.md), [Q2 2026 Supplement](reports/q2-2026-earnings-supplement.md) |

Two caveats when tracing a number. The NII model's use of API-16 for Tier 1 capital appears in the workbook and the API page but not in the registered model inventory. The Pillar 3 allowance paragraph names MDL-CR-007 although its inventory does not list Pillar 3 as a downstream disclosure. The [lineage page](workflows/api-to-model-to-report-lineage.md) covers these and other mismatches.

## Route by question type

| If you are asking about... | Go to | Start with |
|---|---|---|
| A reported number or ratio (NII, CET1, LCR, NCOs, VaR, ...) | `metrics/` | [Net interest income](metrics/net-interest-income.md), [CET1 ratio](metrics/cet1-ratio.md), [Allowance for credit losses](metrics/allowance-for-credit-losses.md), [Net income and EPS](metrics/net-income-and-eps.md), [Net charge-offs](metrics/net-charge-offs.md), [LCR](metrics/liquidity-coverage-ratio.md), [NSFR](metrics/net-stable-funding-ratio.md), [SLR](metrics/supplementary-leverage-ratio.md), [RWA](metrics/risk-weighted-assets.md), [VaR](metrics/value-at-risk.md) |
| How a figure is calculated, its inputs and sheets | `models/` and `models/components/` | [CECL model](models/cecl-allowance-model.md), [NII model](models/nii-sensitivity-model.md), [Capital model](models/capital-planning-model.md); steps such as [Lifetime PD](models/components/cecl-lifetime-pd.md), [LGD and EAD](models/components/cecl-lgd-and-ead.md), [Scenario weighting](models/components/cecl-scenario-weighting.md), [Qualitative overlay](models/components/cecl-qualitative-overlay.md), [Repricing and deposit betas](models/components/nii-repricing-and-deposit-betas.md), [Rate shock projection](models/components/nii-rate-shock-projection.md), [EVE modified duration](models/components/eve-modified-duration.md), [Baseline projection](models/components/capital-baseline-projection.md), [Stress projection](models/components/capital-stress-projection.md), [Indicative SCB](models/components/indicative-stress-capital-buffer.md) |
| An API's scopes, endpoints, owner, consumers, SLOs | `apis/` | [Developer Platform overview](apis/developer-platform-overview.md) indexes all 18 APIs; risk and finance APIs are API-10 to API-16 (for example [API-14 Macroeconomic Scenario](apis/api-14-macroeconomic-scenario-api.md), [API-16 Regulatory Reporting](apis/api-16-regulatory-reporting-api.md)) |
| Macro or rate assumptions behind a result | `scenarios/` | [Macro Scenarios MSC-2025Q4](scenarios/macro-scenarios-msc-2025q4.md), [Internal Severely Adverse](scenarios/internal-severely-adverse.md), [Parallel Rate Shocks](scenarios/parallel-rate-shocks.md) |
| What a regulatory or risk term means | `concepts/` | [CECL](concepts/cecl.md), [IRRBB](concepts/irrbb.md), [EVE](concepts/economic-value-of-equity.md), [Stress Capital Buffer](concepts/stress-capital-buffer.md), [G-SIB Surcharge](concepts/gsib-surcharge.md), [Basel III Pillar 3](concepts/basel-iii-pillar-3.md), [BCBS 239](concepts/bcbs-239.md), [Model Risk (SR 11-7)](concepts/model-risk-sr-11-7.md) |
| Where a figure is disclosed, and in which section | `reports/` | [2025 Annual Report](reports/annual-report-2025.md), [2025 Pillar 3 Disclosures](reports/pillar3-disclosures-2025.md), [Q2 2026 Earnings Supplement](reports/q2-2026-earnings-supplement.md) |
| Who owns or validates a model or API | `teams/` | [Developer Platform Engineering](teams/developer-platform-engineering.md), [Model Risk Governance & Review](teams/model-risk-governance-review.md), [Corporate Treasury - ALM](teams/corporate-treasury-alm.md), [Corporate Treasury - Capital Management](teams/corporate-treasury-capital-management.md), [Allowance Methodology](teams/consumer-wholesale-credit-risk-allowance-methodology.md), [Risk Analytics Engineering](teams/risk-analytics-engineering.md); the other API-owning teams are in `teams/` |
| Which executive leads a function | `people/` | [CEO](people/chief-executive-officer.md), [CFO](people/chief-financial-officer.md), [CRO](people/chief-risk-officer.md), [CTO](people/chief-technology-officer.md), [Treasurer](people/treasurer.md) |
| Which business segment a result belongs to | `organizations/` | [Meridian Harbor Financial Corp.](organizations/meridian-harbor-financial-corp.md), [Consumer & Community Banking](organizations/consumer-community-banking.md), [Commercial & Investment Bank](organizations/commercial-investment-bank.md), [Asset & Wealth Management](organizations/asset-wealth-management.md), [Corporate (Treasury/CIO)](organizations/corporate.md) |
| End-to-end process walkthroughs | `workflows/` | [Lineage](workflows/api-to-model-to-report-lineage.md), [CECL allowance calculation](workflows/cecl-allowance-calculation-flow.md), [Capital and rate sensitivity](workflows/capital-and-rate-sensitivity-flow.md) |

## Worked routes for common questions

- **Which APIs feed the CECL model?** Open [CECL Allowance Model](models/cecl-allowance-model.md); it consumes API-10, API-11 and API-14. The flow is in [CECL Allowance Calculation Flow](workflows/cecl-allowance-calculation-flow.md).
- **How is the allowance calculated?** Scenario PD, then LGD and EAD, then ECL by scenario, then probability weighting, then a management overlay. Read [CECL Allowance Calculation Flow](workflows/cecl-allowance-calculation-flow.md), then [Allowance for Credit Losses](metrics/allowance-for-credit-losses.md).
- **What happens to NII if rates fall 200 bp?** Read [Capital Projection and Rate Sensitivity Flows](workflows/capital-and-rate-sensitivity-flow.md), then [Parallel Rate Shocks](scenarios/parallel-rate-shocks.md) and [NII Rate Shock Projection](models/components/nii-rate-shock-projection.md).
- **What drove Q2 2026 net income?** Start at [Net Income and EPS](metrics/net-income-and-eps.md) and the [Q2 2026 Earnings Supplement](reports/q2-2026-earnings-supplement.md).
- **Where does a capital or RWA actual come from?** Capital and RWA actuals come from [API-16](apis/api-16-regulatory-reporting-api.md), not from a model. Projections and the indicative buffer come from [Capital Planning Model](models/capital-planning-model.md).
- **Who validates the models, and what is the governance?** [MRGR](teams/model-risk-governance-review.md) validates independently; see [Model Risk (SR 11-7)](concepts/model-risk-sr-11-7.md). API-10 to API-16 are BCBS 239 critical data services, and a breaking change to one triggers a model change review.

## How to trace a reported number

1. Find the figure on a [report](reports/annual-report-2025.md) page or in its model inventory.
2. Follow the model ID to its [model page](models/cecl-allowance-model.md) for the sheet and input cell.
3. Open the API named in the cell's source note and check its Data lineage, owner and timing commitments.
4. Check the [scenario](scenarios/macro-scenarios-msc-2025q4.md) set used. Scenario set names differ between sources (MSC-2025Q4 for the CECL workbook, SA-2025-INT in Pillar 3), so confirm which set a run used before comparing results.

Model inputs are copied into workbook cells at run time, so lineage describes a refresh procedure and not a live link.

## Related

- [Overview](overview.md)
- [API to Model to Report Lineage](workflows/api-to-model-to-report-lineage.md)
- [Developer Platform API Reference Overview](apis/developer-platform-overview.md)
