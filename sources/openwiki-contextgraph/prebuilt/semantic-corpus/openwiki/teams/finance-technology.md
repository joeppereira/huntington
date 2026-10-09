---
type: Team
title: Finance Technology
description: Finance Technology is the engineering team that owns the Regulatory Reporting API (API-16, v1.8, /regulatory/v1), the governed source of regulatory capital, RWA, leverage exposure and report line items. This page covers its accountabilities, commitments, consumers and operating constraints.
tags: [team, finance-technology, api-16, regulatory-reporting, critical-data-service, bcbs-239, developer-platform]
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
  - id: openwiki-source-9e2090b855b8be2710ba081f
    resource: repo://sources/models/nii-sensitivity-model.md
  - id: openwiki-source-c13af588d055d118eda543d5
    resource: repo://sources/reports/mhfc-2025-pillar3-disclosures.md
  - id: openwiki-source-9da334bbfcfb68cd7514ff33
    resource: repo://sources/reports/mhfc-q2-2026-earnings-supplement.md
generated: { by: "openwiki/0.7.0", at: "2026-10-05T01:46:21.335Z" }
---

# Finance Technology

Finance Technology is the owning team for the [API-16 Regulatory Reporting API](../apis/api-16-regulatory-reporting-api.md). In the [Developer Platform](../apis/developer-platform-overview.md) catalog it owns exactly one API, in the **Finance & Regulatory** business domain. The sources describe nothing else about the team. They give no headcount, reporting line, repositories or on-call rota, so this page covers only what the team's single API implies.

## What the team is accountable for

API-16 delivers governed regulatory capital, risk-weighted assets (RWA), leverage exposure and report line items for FR Y-9C, FFIEC 101 and FR Y-15. The figures are reconciled to the general ledger at legal-entity level. The API is the golden source for Pillar 3 disclosures. The team's job is therefore to keep one authoritative, reconciled, quarter-locked data set that finance, capital and disclosure processes all read.

Four read-only endpoints are documented under `/regulatory/v1`:

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/capital/{asOf}` | CET1, Tier 1, Total capital and deductions |
| GET | `/rwa/{asOf}?approach=standardized` | RWA by exposure type and approach |
| GET | `/leverage/{asOf}` | Total leverage exposure components and SLR |
| GET | `/reports/{reportId}/{asOf}` | Line items for a regulatory report schedule |

All four take an `asOf` reporting date. The example response for `/capital/2026-06-30` carries `cet1` 101,200 and `standardizedRwa` 668,400, both in `USD millions`, along with `cet1Ratio` 0.1514 and `status: "locked"`. The `status` field in that example shows a data-lock state is surfaced to callers. Only the `standardized` value of the `approach` parameter is documented. No write endpoints exist, and the single OAuth scope is `regulatory:read`.

## Commitments the team carries

| Commitment | Value |
| --- | --- |
| Current version | v1.8, with the major version in the path (`/regulatory/v1`) |
| Data classification | Restricted - Internal |
| OAuth scope | `regulatory:read` |
| Rate limit | 20 requests/minute |
| Availability SLO | 99.9% |
| Data-lock SLO | Quarter-end data locked by day 25 |

The Q2 2026 earnings supplement reports about 0.4 million calls per month (up 3% year on year) at 99.90% availability. That exactly meets the SLO target, so there is no headroom. Volume is tiny next to customer-facing APIs, which fits an API with a handful of internal batch-style consumers and a 20 requests/minute limit.

### Platform and governance obligations

- **Internal-only exposure.** API-16 is listed among the restricted risk and finance APIs (API-10, API-14, API-15, API-16) served from the internal host `https://internal.api.mhfc.example`, which is reachable on the private network only. Intended consumers are Regulatory Reporting, Capital Management and the Disclosure Committee.
- **Critical data service.** APIs that feed Tier 1 models or regulatory disclosures are classified as critical data services under the Firm's [BCBS 239](../concepts/bcbs-239.md) program. They need named data owners, documented data-quality rules, enhanced change management and model-inventory registration. Any breaking change triggers a model change review by Model Risk Governance & Review (MRGR). A breaking change to API-16 therefore has a review process attached because it feeds the [Capital Planning & Stress Projection Model](../models/capital-planning-model.md).
- **Escalation.** Critical data services, including API-16, escalate through the Data and Technology Risk Committee, with 24x7 coverage during quarter close.
- **Data-quality reporting.** Data-quality exceptions on critical data elements are reported monthly to the Data and Technology Risk Committee. The 2025 Pillar 3 disclosures state that no exception materially affected reported capital ratios that year.
- **Platform-wide rules** apply: OAuth 2.0 with 15-minute JWTs, mutual TLS for server clients, 429 with `Retry-After` on rate-limit breaches, the standard error object, and additive-only minor versions (see [Developer Platform Engineering](developer-platform-engineering.md) for the platform owner).

## Data flow and integration boundaries

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: an unescaped angle bracket inside a label breaks rendering; rephrase the label. -->
```text
flowchart LR
    GL[General ledger] --> API16
    RWA[RWA calculation engines] --> API16
    FX[API-13 FX Rates] --> API16
    API16[API-16 Regulatory Reporting<br/>owned by Finance Technology]
    API16 --> CAP[MDL-CAP-003 Capital Planning model]
    API16 --> FILINGS[FR Y-9C and FFIEC 101 filings]
    API16 --> P3[Pillar 3 disclosures]
    API16 --> NII[NII model Tier 1 capital input]
```

- **Upstream:** the general ledger, the RWA calculation engines and the [FX Rates API](../apis/api-13-fx-rates-api.md) (API-13). The FX Rates API lists API-16 currency conversion as a downstream use, which suggests non-USD exposures are converted before they reach reported figures.
- **Downstream:**
  - The [Capital Planning & Stress Projection Model](../models/capital-planning-model.md) (MDL-CAP-003, owned by [Corporate Treasury - Capital Management](corporate-treasury-capital-management.md)) takes its starting CET1 and RWA from API-16. The Q2 2026 values are 101,200 and 668,400 USD millions.
  - The FR Y-9C and FFIEC 101 filings are prepared from API-16 data. Ratios in the earnings supplement are "estimated and subject to finalization" in the FR Y-9C.
  - [Pillar 3 disclosures](../reports/pillar3-disclosures-2025.md) use API-16 as the golden source.
  - The [NII Sensitivity Model](../models/nii-sensitivity-model.md) uses API-16 Tier 1 capital as an input, for example year-end 2025 Tier 1 of 110,620.

Because the same governed data feeds the model, the filings and the disclosures, Finance Technology is where figures for capital planning and for external reporting are kept consistent. The 2025 Pillar 3 report says API-16 "delivers the same governed data used to prepare these disclosures and the FR Y-9C".

## Lifecycle and change history

The data follows the quarterly reporting cycle. Quarter-end data is locked by day 25, and responses carry a `status` such as `locked`. The sources do not describe the other status values, so treat them as undocumented.

| Version | Date | Change |
| --- | --- | --- |
| v1.8 | 2026-03 | GL reconciliation status flag |
| v1.7 | 2025-09 | Strategic platform migration |

In 2025 the Firm completed the API's migration to the strategic data platform and introduced automated reconciliation of API-16 outputs to the general ledger at legal-entity level. The v1.8 flag exposes that reconciliation state to consumers. The sources do not name the flag's field or its values, so the response schema should be checked before relying on it.

## Operational notes and risks

- **No headroom on availability.** Measured availability equals the SLO. A quarter-close incident would hit the Capital Management, Regulatory Reporting and Disclosure Committee workflows together, which is why escalation is 24x7 during close.
- **Low rate limit.** 20 requests/minute per client is suited to scheduled extracts. Consumers should cache locked quarter-end data and not poll.
- **Locked versus unlocked data.** Before day 25 of quarter close, figures may not be final. Downstream models should check `status` and the GL reconciliation flag before treating a pull as an official starting point.
- **Breaking changes are expensive.** A breaking change triggers MRGR model change review for dependent Tier 1 models. Prefer additive minor versions, and keep a major version for at least 12 months after its successor reaches general availability.
- **Gaps in the sources.** No endpoint pagination detail, error cases specific to API-16, reconciliation tolerances, legal-entity parameters or test strategy are documented. The reconciliation is described as legal-entity level, but none of the four endpoints shows a legal-entity parameter.

## Related pages

- [API-16 Regulatory Reporting API](../apis/api-16-regulatory-reporting-api.md)
- [Capital Planning & Stress Projection Model](../models/capital-planning-model.md)
- [CET1 ratio](../metrics/cet1-ratio.md), [Risk-weighted assets](../metrics/risk-weighted-assets.md) and [Supplementary leverage ratio](../metrics/supplementary-leverage-ratio.md)
- [Basel III Pillar 3](../concepts/basel-iii-pillar-3.md)
- [BCBS 239](../concepts/bcbs-239.md)
