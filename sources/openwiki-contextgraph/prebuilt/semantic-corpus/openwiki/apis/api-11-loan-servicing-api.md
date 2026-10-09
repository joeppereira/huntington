---
type: API
title: API-11 Loan Servicing API
description: Loan-level and portfolio-level balances, amortization schedules, delinquency, remaining contractual life and repricing terms for consumer and wholesale loans. A critical data service that feeds CECL exposure at default (EAD) and remaining life, and the ALM repricing profile.
tags: [api, loan-servicing, lending-operations, cecl, ead, critical-data-service, alm, repricing]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-05T01:46:21.335Z
sources:
  - id: openwiki-source-00eb967862ea67fd6af69064
    resource: repo://sources/api_docs/apis/api-09-credit-decisioning-api.md
  - id: openwiki-source-6d7547a21ca2bb10a57c90e3
    resource: repo://sources/api_docs/apis/api-11-loan-servicing-api.md
  - id: openwiki-source-65a2ad8de7d532680de82b60
    resource: repo://sources/api_docs/mhfc-developer-platform-api-reference.md
  - id: openwiki-source-b575b40c2132eeef7814e5c4
    resource: repo://sources/models/cecl-allowance-model.md
  - id: openwiki-source-9e2090b855b8be2710ba081f
    resource: repo://sources/models/nii-sensitivity-model.md
generated: { by: "openwiki/0.7.0", at: "2026-10-05T01:46:21.335Z" }
---

# API-11 Loan Servicing API

API-11 is the Meridian Harbor Developer Platform's system of record for loan-level servicing data. It exposes balances, payment schedules, delinquency status, remaining contractual life and repricing terms for consumer and wholesale loans. It also supports payoff quotes and payment posting. Its most consequential use is as a **critical data service**. The [CECL allowance model](../models/cecl-allowance-model.md) (MDL-CR-007) takes its balances (used as EAD) and remaining life from this API, and the NII Sensitivity Model (MDL-ALM-014) takes its repricing profile.

The service is owned by [Lending Platforms Engineering](../teams/lending-platforms-engineering.md).

## At a glance

| Attribute | Value |
| --- | --- |
| API ID / version | API-11, v2.8 |
| Base path | `/loans/v2` |
| Business domain | Lending Operations |
| Owning team | Lending Platforms Engineering |
| Intended consumers | Servicing applications, CECL and ALM models, customer channels |
| Data classification | Confidential - Client Data |
| OAuth scopes | `loans:read`, `loans.payments:write`, `loans.portfolio:read` |
| Rate limit | 900 requests/minute; portfolio snapshots go through an async extract |
| SLO | 99.95% availability |

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/loans/{loanId}` | Loan details: balance, rate, next reset date, maturity, status |
| GET | `/loans/{loanId}/schedule` | Amortization schedule |
| GET | `/portfolio/snapshots/{asOf}` | Month-end portfolio snapshot aggregated by segment and repricing bucket (0-3m, 3-12m, 1-5y, >5y) |
| POST | `/loans/{loanId}/payoff-quotes` | Generate a payoff quote |

The overview text also lists payment posting as a capability. It is the reason for the `loans.payments:write` scope. The endpoint table lists no dedicated payment-posting path, so check the portal contract before depending on it.

The endpoints fall into two groups:

- **Loan-level (servicing).** The `/loans/{loanId}` family serves servicing applications and customer channels. The scope requirements are not mapped per endpoint in the source. `loans:read` is the natural read scope, and `loans.payments:write` is the write scope.
- **Portfolio-level (risk and finance).** `/portfolio/snapshots/{asOf}` is the aggregate view for model consumers. It sits behind the separate `loans.portfolio:read` scope, so risk consumers do not need loan-level read access. That scope-to-endpoint mapping is inferred from the scope names, not stated in the source.

### Portfolio snapshot example

```
GET /loans/v2/portfolio/snapshots/2025-12-31?segment=COMMERCIAL_AND_INDUSTRIAL
```

```json
{
  "segment": "Commercial & Industrial",
  "balance": 172500,
  "units": "USD millions",
  "repricing": { "0-3m": 0.78, "3-12m": 0.08, "1-5y": 0.12, ">5y": 0.02 },
  "delinquency30Plus": 0.0031
}
```

- The payload states its own `units` (USD millions). This is the platform convention for risk and finance APIs.
- `repricing` gives the share of balance in each bucket. The four buckets sum to 1.0.
- The segment's `balance` of 172,500 matches the C&I EAD in the CECL model's `Segment_Inputs` sheet at 2025-12-31. That is the hand-off from this API to the model.

## Role in the data lineage

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: an unescaped angle bracket inside a label breaks rendering; rephrase the label. -->
```text
flowchart LR
  SYS["Servicing systems<br/>(mortgage, auto, card, commercial)"] --> API11["API-11 Loan Servicing API"]
  API09["API-09 Credit Decisioning<br/>(bookings)"] --> API11
  API11 --> CECL["MDL-CR-007 CECL model<br/>(EAD, remaining life)"]
  API11 --> ALM["MDL-ALM-014 NII Sensitivity<br/>(repricing profile)"]
  API11 --> API10["API-10 Credit Risk Scoring"]
  API11 --> API01["API-01 Accounts API"]
```

- **Upstream.** The underlying loan servicing systems (mortgage, auto, card, commercial) and new bookings from the Credit Decisioning API (API-09). API-09 itself lists API-11 as a downstream consumer "on booking", so a decisioned loan becomes a serviced loan here.
- **Downstream.** The CECL model (EAD and remaining life), the NII Sensitivity Model (repricing profile), the Credit Risk Scoring API (API-10) and the Accounts API (API-01).

### How CECL uses it

In the CECL model, scenario ECL = EAD x lifetime PD x scenario LGD. Lifetime PD is `1 - (1 - scenario PD) ^ remaining life`. API-11 supplies two of the inputs: the segment balance, used as EAD, and the remaining life in years. See [CECL LGD and EAD](../models/components/cecl-lgd-and-ead.md) for how the model uses them.

The FY2025 segment inputs fed from this feed are:

| Segment | EAD ($mm) | Remaining life (yrs) |
| --- | --- | --- |
| Credit Card | 138,400 | 1.70 |
| Residential Mortgage | 218,600 | 6.50 |
| Auto | 64,900 | 2.40 |
| Commercial Real Estate | 98,200 | 3.80 |
| Commercial & Industrial | 172,500 | 2.30 |
| Other Consumer & Wholesale | 49,700 | 2.00 |
| **Total** | **742,300** | |

Remaining life enters the lifetime PD exponent, so an error in this field shifts the allowance. A change to the balance changes the allowance one-for-one. The `remaining-life` field was added in v2.6 (2025-06) for CECL.

### How ALM uses it

The NII Sensitivity Model applies each position's repricing for the part of the 12-month horizon that remains after its repricing date. The repricing-bucket snapshot, added in v2.8 (2026-02) "for ALM", supplies the loan asset side of that profile.

## Governance and operations

- **Critical data service.** APIs that feed Tier 1 models or regulatory disclosures are classified under the Firm's BCBS 239 program. They carry named data owners, documented data-quality rules and enhanced change management, and they are registered in the model inventory. A breaking change automatically triggers a model change review by Model Risk Governance & Review (MRGR). Treat any change to balance, remaining-life, repricing-bucket or delinquency semantics as potentially breaking for CECL and ALM.
- **Versioning.** The major version is in the path (`/loans/v2`). Minor versions are additive and backward compatible. A major version is supported for at least 12 months after its successor reaches GA, and deprecation is signalled by the `Sunset` header.
- **Escalation.** API-11 is one of the critical data services (API-10, 11, 12, 14, 15, 16) escalated through the Data and Technology Risk Committee, 24x7 during quarter close.
- **Auth and errors.** The platform-wide OAuth 2.0 rules apply: 15-minute JWTs, mTLS for server-to-server clients and least-privilege scopes. Errors use the standard `{error:{code,message,requestId}}` envelope (401, 403 `insufficient_scope`, 404, 429 with `Retry-After`, and so on). POSTs that create resources, such as payoff quotes and payment posting, need an `Idempotency-Key`, which is retained for 24 hours.
- **Rate limits and bulk data.** The 900 requests/minute limit is for interactive use. Bulk portfolio snapshots are meant to use the async extract, not loops over `/loans/{loanId}`. The source is not explicit about how the extract relates to the synchronous `GET /portfolio/snapshots/{asOf}` endpoint.
- **Data sensitivity.** The data is classified Confidential - Client Data. Loan-level responses are client data, while aggregated snapshots carry segment totals.
- **Environment note.** The platform reference lists only API-10, 14, 15 and 16 as private-network-only on the internal risk and finance host. API-11 is not in that list.

## Change history

| Version | Date | Change |
| --- | --- | --- |
| v2.6 | 2025-06 | Remaining-life field for CECL |
| v2.8 | 2026-02 | Repricing-bucket snapshot for ALM |

## Related

- [CECL Allowance Model](../models/cecl-allowance-model.md)
- [CECL LGD and EAD](../models/components/cecl-lgd-and-ead.md)
- [Lending Platforms Engineering](../teams/lending-platforms-engineering.md)

## Source scope

This page is based on the API reference entry for API-11, the platform-wide conventions in the Developer Platform API Reference, and the CECL model documentation sheet. No implementation code or tests are available in this corpus. Per-endpoint behavior beyond the table above is not documented.
