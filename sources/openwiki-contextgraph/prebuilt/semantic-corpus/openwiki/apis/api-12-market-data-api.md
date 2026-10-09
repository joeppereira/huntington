---
type: API
title: API-12 Market Data API
description: Critical data service (v5.1, /market-data/v5) publishing prices, yield curves, credit spreads and volatility surfaces; golden source for VaR, fair value and the policy rate and curves feeding the NII Sensitivity Model (MDL-ALM-014).
tags: [api, market-data, critical-data-service, yield-curves, nii-model, bcbs-239, markets-treasury]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-05T01:46:21.335Z
sources:
  - id: openwiki-source-3692caf122b70c59f03bd5c1
    resource: repo://sources/api_docs/apis/api-12-market-data-api.md
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

# API-12 Market Data API

API-12 is the Meridian Harbor Developer Platform's REST service for market data. It publishes end-of-day and intraday prices, yield curves (SOFR, Treasury), credit spreads and volatility surfaces, sourced from licensed vendors and internal marks. It is the golden source for VaR, fair value and the policy rate used in ALM models. The owning team is [Market Data Services](../teams/market-data-services.md). Its most prominent model consumer is the [NII Sensitivity Model](../models/nii-sensitivity-model.md) (MDL-ALM-014), which takes its yield curve and policy rate from this API.

## Profile

| Attribute | Value |
| --- | --- |
| API ID / version | API-12, v5.1 |
| Base path | `/market-data/v5` |
| Business domain | Markets & Treasury |
| Owner | Market Data Services |
| Intended consumers | Trading, risk, valuation control, Treasury/CIO models |
| Data classification | Internal - Licensed Data |
| OAuth scopes | `marketdata:read`, `marketdata.curves:read` |
| Rate limit | 5,000 requests/minute; streaming via WebSocket |
| SLO | 99.99% availability; EOD snapshot by 19:00 ET |

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/curves/{curveId}` | Yield curve points for a date (e.g. `USD-SOFR`, `UST`) |
| GET | `/series/{seriesId}` | Time series, e.g. `POLICY.FEDFUNDS.UB` |
| GET | `/prices` | Instrument prices for a list of identifiers |
| GET | `/vol-surfaces/{surfaceId}` | Implied volatility surface |

All endpoints are read-only. Intraday data can also be streamed over WebSocket (added in v5.1).

### Example: policy rate

```
GET /market-data/v5/series/POLICY.FEDFUNDS.UB?date=2025-12-31
```

```json
{
  "seriesId": "POLICY.FEDFUNDS.UB",
  "date": "2025-12-31",
  "value": 0.0375,
  "source": "official"
}
```

Values are decimals (0.0375 = 3.75%). The `source` field indicates the provenance of the value (here `official`).

## Data lineage

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: an unescaped angle bracket inside a label breaks rendering; rephrase the label. -->
```text
flowchart LR
  V[Licensed market data vendors] --> API[API-12 Market Data API]
  M[Internal trader marks<br/>validated by Valuation Control] --> API
  API --> NII[MDL-ALM-014 NII Sensitivity Model<br/>policy rate, curves]
  API --> VAR[VaR engine]
  API --> FV[Fair value - Note 13]
  API --> COL[Collateral valuation]
```

- **Upstream:** licensed vendor feeds and internal trader marks. Internal trader marks are validated by Valuation Control.
- **Downstream:** the NII Sensitivity Model, the VaR engine, fair value reporting (Note 13) and collateral valuation. Pillar 3 disclosures describe collateral values being refreshed daily from this API and market-risk model inputs (prices, curves, volatility surfaces) being sourced from it and from API-13 (FX Rates).

## Role in the NII model

MDL-ALM-014 is registered in the platform's API-to-model lineage matrix with API-12 as an upstream feed (alongside API-15 Treasury Liquidity Positions and API-11 Loan Servicing). The model uses API-12 for two inputs:

1. **Yield curve** for the rate scenarios applied to the balance sheet.
2. **Policy rate**, read from series `POLICY.FEDFUNDS.UB` (fed funds upper bound). The model's Assumptions sheet records 0.0375 for the 2025-12-31 as-of date, matching the example response above.

Because the model's as-of date is a month-end snapshot, requests made for model runs should pin an explicit `date` parameter rather than rely on the latest value, so that results are reproducible and the policy rate matches the balance snapshot.

## Governance and operations

- **Critical data element.** The Annual Report states API-12 (with API-13) is designated a critical data element under the BCBS 239 program. Critical data services carry named data owners, documented data-quality rules and enhanced change management, and are registered in the model inventory, so a breaking change automatically triggers a model change review by Model Risk Governance & Review (MRGR). Any change to curve identifiers, series IDs or units therefore has model-validation implications for MDL-ALM-014.
- **Escalation.** API-12 is on the list of critical data services escalated to the Data and Technology Risk Committee, 24x7 during quarter close.
- **Authentication.** Platform-wide OAuth 2.0: client-credentials with mutual TLS for server-to-server callers; access tokens are JWTs valid for 15 minutes; least-privilege scopes enforced. Curve access is covered by `marketdata.curves:read`; other reads by `marketdata:read`.
- **Rate limiting.** Per client and per API; clients receive `X-RateLimit-Limit`, `X-RateLimit-Remaining` and, on HTTP 429, `Retry-After`. Bulk consumers should use `/prices` with identifier lists or the WebSocket stream rather than many single calls.
- **Errors.** Standard platform error envelope (`400 invalid_request`, `401 unauthorized`, `403 insufficient_scope`, `404 not_found`, `429 rate_limited`, `500 internal_error`, `503 service_unavailable`).
- **Licensing.** Data is classified "Internal - Licensed Data", so redistribution beyond intended internal consumers is restricted by vendor terms.
- **Versioning.** Major version is in the path (`/v5`); minor versions are additive. A major version stays supported at least 12 months after its successor reaches general availability.
- **Usage.** The Q2 2026 earnings supplement reports about 310 million calls per month (+11% YoY) and 99.99% availability, with trading, the NII model and fair value as key consumers.

## Failure considerations

If the API is unavailable or the EOD snapshot (due by 19:00 ET) is late, downstream valuation (VaR, fair value, collateral) and the NII model lack current curves and policy rate. Callers should treat 429/503 with backoff per `Retry-After` and must not silently substitute stale rates in model runs.

## Changelog

- **v5.1 (2026-03):** WebSocket streaming.
- **v5.0 (2025-05):** SOFR curve family.
5):** SOFR curve family.
