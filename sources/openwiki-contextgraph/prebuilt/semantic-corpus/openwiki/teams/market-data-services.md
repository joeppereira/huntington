---
type: Team
title: Market Data Services
description: The team that owns the Market Data API (API-12) and the FX Rates API (API-13) in the Markets & Treasury domain; covers its two services, downstream dependents, governance obligations and operating expectations.
tags: [team, market-data, fx, markets-and-treasury, critical-data-elements, bcbs-239, ownership]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-05T01:46:21.335Z
sources:
  - id: openwiki-source-3692caf122b70c59f03bd5c1
    resource: repo://sources/api_docs/apis/api-12-market-data-api.md
  - id: openwiki-source-cc9b094c5510fbe3941b7a83
    resource: repo://sources/api_docs/apis/api-13-fx-rates-api.md
  - id: openwiki-source-65a2ad8de7d532680de82b60
    resource: repo://sources/api_docs/mhfc-developer-platform-api-reference.md
  - id: openwiki-source-9e2090b855b8be2710ba081f
    resource: repo://sources/models/nii-sensitivity-model.md
  - id: openwiki-source-eb14da62fbec45aad876fb64
    resource: repo://sources/reports/mhfc-2025-annual-report.md
  - id: openwiki-source-c13af588d055d118eda543d5
    resource: repo://sources/reports/mhfc-2025-pillar3-disclosures.md
  - id: openwiki-source-9da334bbfcfb68cd7514ff33
    resource: repo://sources/reports/mhfc-q2-2026-earnings-supplement.md
generated: { by: "openwiki/0.7.0", at: "2026-10-05T01:46:21.335Z" }
---

# Market Data Services

Market Data Services is the owning team, in the Markets & Treasury business domain, for the two reference-data APIs of the Meridian Harbor Developer Platform:

| API | Version | Base path | What it serves |
| --- | --- | --- | --- |
| [API-12 Market Data API](../apis/api-12-market-data-api.md) | v5.1 | `/market-data/v5` | Prices, yield curves, credit spreads, volatility surfaces, policy-rate series |
| [API-13 FX Rates API](../apis/api-13-fx-rates-api.md) | v2.4 | `/fx/v2` | Spot, end-of-day and forward-described FX rates, plus executable client quotes |

The platform overview lists this team as owning exactly these two APIs (see [Developer Platform Overview](../apis/developer-platform-overview.md)). The sources describe no other team attributes (headcount, on-call roster, contacts), so this page documents ownership, what the team's services feed, and the obligations that follow from that.

## Responsibilities

- **Publish licensed and internal market data.** API-12 combines licensed vendor feeds with internal trader marks. The internal marks are validated by Valuation Control. API-13 draws on the FX trading desk pricing engine and licensed vendors. Both are classified "Internal - Licensed Data", so the team's services carry vendor redistribution limits.
- **Act as golden source.** API-12 is the golden source for VaR, fair value and the policy rate used in ALM models. API-13 supplies the FX rates used to value trading positions and convert non-USD exposures.
- **Meet the service-level commitments.** Both APIs target 99.99% availability. API-12 also commits to an end-of-day snapshot by 19:00 ET. API-13 commits to a quote validity of 60 seconds and does not document an EOD publication time.
- **Run as critical data elements.** The annual report and Pillar 3 disclosures designate both feeds as critical data elements under the BCBS 239 program. Pillar 3 says their inputs are validated independently by the Valuation Control Group.

## How the two services fit together

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: an unescaped angle bracket inside a label breaks rendering; rephrase the label. -->
```text
flowchart LR
  vendors[Licensed vendors] --> API12[API-12 Market Data API]
  marks[Internal trader marks<br/>validated by Valuation Control] --> API12
  vendors --> API13[API-13 FX Rates API]
  desk[FX trading desk pricing engine] --> API13
  API12 --> NII[MDL-ALM-014 NII Sensitivity Model]
  API12 --> VAR[VaR engine]
  API12 --> FV[Fair value - Note 13]
  API12 --> COL[Collateral valuation]
  API13 --> VAR
  API13 --> WIRE[API-05 Wire Transfer]
  API13 --> REG[API-16 Regulatory Reporting<br/>currency conversion]
```

The VaR engine is the one shared consumer. Market-risk model inputs (prices, curves, volatility surfaces) come from API-12, and FX rates come from API-13. The APIs do not call each other in the sources; their link is the common vendor input and the shared consumers.

## Downstream dependents

| Consumer | Uses | Source API |
| --- | --- | --- |
| [NII Sensitivity Model](../models/nii-sensitivity-model.md) (MDL-ALM-014) | Yield curve and policy rate (`POLICY.FEDFUNDS.UB`, 0.0375 as of 2025-12-31) | API-12 |
| VaR engine | Prices, curves, volatility surfaces, FX rates | API-12, API-13 |
| Fair value (Note 13) and collateral valuation | Prices (collateral values refreshed daily) | API-12 |
| Wire Transfer API (API-05) | Currency conversion for cross-currency wires | API-13 |
| Regulatory Reporting API (API-16) | Currency conversion | API-13 |

Among the Tier 1 models, only MDL-ALM-014 registers one of these APIs as an upstream feed: API-12. API-13 is not registered as an upstream feed of any Tier 1 model in the lineage matrix.

## Change and governance implications

Because API-12 and API-13 are critical data elements, changes by this team carry more weight than a normal API revision.

- **Model impact.** The sources say critical data services are registered in the model inventory, so a breaking change triggers a model change review by Model Risk Governance & Review. Changes to curve identifiers, series IDs or units in API-12 are therefore validation events for MDL-ALM-014, which reads a named series and a curve.
- **Versioning.** The major version is in the path and minor versions are additive. A major version stays supported at least 12 months after its successor reaches general availability. Recent changes: API-12 v5.0 (2025-05) added the SOFR curve family and v5.1 (2026-03) added WebSocket streaming. API-13 v2.4 (2025-11) added the EOD reference endpoint for finance.
- **Escalation.** The platform reference lists API-12 among the critical data services escalated to the Data and Technology Risk Committee, with 24x7 coverage during quarter close. API-13 is not in that list (API-10, 11, 12, 14, 15, 16), even though it is also designated a critical data element. The sources do not explain the difference.
- **Data-quality oversight.** The Data and Technology Risk Committee oversees critical data elements, API change management and BCBS 239 compliance.

## Operating expectations for consumers

- API-12 permits 5,000 requests/minute and API-13 permits 3,000. Clients should batch: use `/prices` identifier lists or the API-12 WebSocket stream, and put several pairs in one API-13 `pairs` list.
- For reproducible month-end model runs, pin an explicit `date` on API-12 calls. For reporting-date FX figures, use `/rates/eod/{date}` rather than spot.
- API-13 quotes expire after 60 seconds. Consumers should request them close to execution.
- On `429` or `503`, back off per `Retry-After`. Do not silently substitute stale rates in model or valuation runs.
- Authentication is the platform-wide OAuth 2.0 with scopes: `marketdata:read` and `marketdata.curves:read` for API-12; `fx:read` and `fx.quotes:write` for API-13.

## Usage and scale

The Q2 2026 earnings supplement reports API-12 at about 310 million calls per month, up 11% year over year, with 99.99% availability. Trading, the NII model and fair value are its key consumers. The sources give no comparable figure for API-13.

## Documented gaps

- API-13's overview mentions forward rates, but v2.4 lists no forward endpoint.
- API-13 has no documented request schema for `POST /quotes`, no error model and no scope-to-endpoint mapping.
- No source describes the team's internal structure, on-call process or release process.

## Related pages

- [API-12 Market Data API](../apis/api-12-market-data-api.md)
- [API-13 FX Rates API](../apis/api-13-fx-rates-api.md)
- [Developer Platform Overview](../apis/developer-platform-overview.md)
- [NII Sensitivity Model](../models/nii-sensitivity-model.md)
