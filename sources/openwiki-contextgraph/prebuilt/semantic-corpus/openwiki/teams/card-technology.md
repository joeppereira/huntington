---
type: Team
title: Card Technology
description: Card Technology is the engineering team that owns the Card Management API (API-06, v2.6, /cards/v2) in the Card Services domain of the Developer Platform. This page covers what the team is accountable for, who depends on its API, and which operating commitments it carries.
tags: [team, card-technology, card-services, api-06, pci, tokenization, developer-platform]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-05T01:46:21.335Z
sources:
  - id: openwiki-source-01f8f4581a996f4e990cf168
    resource: repo://sources/api_docs/apis/api-06-card-management-api.md
  - id: openwiki-source-02937dfc348e02c68c1fd975
    resource: repo://sources/api_docs/apis/api-07-customer-identity-kyc-api.md
  - id: openwiki-source-ae1673926013dfe069091a87
    resource: repo://sources/api_docs/apis/api-18-webhooks-event-notifications-api.md
  - id: openwiki-source-65a2ad8de7d532680de82b60
    resource: repo://sources/api_docs/mhfc-developer-platform-api-reference.md
  - id: openwiki-source-9da334bbfcfb68cd7514ff33
    resource: repo://sources/reports/mhfc-q2-2026-earnings-supplement.md
generated: { by: "openwiki/0.7.0", at: "2026-10-05T01:46:21.335Z" }
---

# Card Technology

Card Technology is the owning team for the [API-06 Card Management API](../apis/api-06-card-management-api.md). In the [Developer Platform](../apis/developer-platform-overview.md) ownership table it owns exactly one API, and that API belongs to the **Card Services** business domain. The sources describe no other responsibilities for the team. They give no headcount, reporting line, on-call process or repositories.

## What the team is accountable for

The team owns the card lifecycle surface that the Developer Platform exposes to mobile and partner clients. The API's stated scope is issuance, activation, lock/unlock, spend controls, digital wallet provisioning and replacement, for both debit and credit cards. Only four endpoints are documented under `/cards/v2`:

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/cards/{cardToken}` | Card status, product and expiry, all tokenized |
| POST | `/cards/{cardToken}/lock` | Temporarily lock a card |
| PUT | `/cards/{cardToken}/controls` | Set merchant-category, geography and amount controls |
| POST | `/cards/{cardToken}/wallet-provisioning` | Provision a card to a digital wallet |

Because the sources document no endpoints for issuance, activation, unlock or replacement, treat those operations as outside the published surface for now. See the [API page](../apis/api-06-card-management-api.md) for the gaps in detail.

## Commitments the team carries

| Commitment | Value |
| --- | --- |
| Current version | v2.6, with the major version in the path (`/cards/v2`) |
| Data classification | Restricted - PCI |
| OAuth scopes | `cards:read`, `cards:write`, `cards.controls:write` |
| Rate limit | 800 requests/minute per client |
| SLO | 99.97% availability; p95 latency 220 ms |

The Q2 2026 earnings supplement reports about 260 million calls per month for API-06, up 15% year on year, at 99.97% availability. That figure matches the SLO target, so the team has little headroom against it.

### Security posture

- **Tokenization is the central invariant.** PAN data is tokenized and raw card numbers are never returned. Clients identify cards only by an opaque `cardToken` (for example `tok_card_83jd`). The API therefore exposes only a tokenized view of card data held by the card processing platform. Any change that returned a PAN would break this contract and the Restricted - PCI classification.
- **Scope separation.** `cards.controls:write` is a distinct scope from `cards:write`, so spend-limit authority can be granted separately from other write operations. The source does not map scopes to endpoints, so that mapping is an inference.
- **Platform-wide rules** apply. These are OAuth 2.0 (client credentials with mutual TLS for servers, authorization code with PKCE for customer-facing apps), `Idempotency-Key` on POSTs, 429 responses on rate-limit breaches, and standard error objects.

## Consumers and integration boundaries

Intended consumers are the **mobile app** and **fintech and co-brand partners**. Co-brand partner scopes arrived in v2.5 (2025-08), so the team supports partner access as well as first-party use.

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: an unescaped angle bracket inside a label breaks rendering; rephrase the label. -->
```text
flowchart LR
    CPP[Card processing platform] --> API06[API-06 Card Management<br/>owned by Card Technology]
    KYC[API-07 Customer Identity & KYC] --> API06
    API06 --> AUTH[Card authorization system]
    API06 --> WAL[Digital wallets]
    API06 --> EVT[API-18 Webhooks & Event Notifications]
    EVT --> CLIENTS[Client systems]
```

- **Upstream:** the card processing platform and the [Customer Identity & KYC API](../apis/api-07-customer-identity-kyc-api.md) (API-07). The KYC API lists the Card Management API among its downstream consumers. The sources do not say how KYC data is used, for example whether it gates issuance.
- **Downstream:** the card authorization system, digital wallets, and the Webhooks & Event Notifications API (API-18). Spend controls set through API-06 are consumed by the card authorization system, and wallet provisioning feeds digital wallets. The API-18 lineage lists API-06 as an upstream event source, which is how card events reach client systems.
- **Adjacent services:** the [Fraud Risk Signals API](../apis/api-08-fraud-risk-signals-api.md) (API-08) is used by the card authorization system and scores card authorizations. The FX Rates API (API-13) lists card cross-border pricing as a consumer. Neither is documented as part of API-06's own lineage, so they are context only.

## Change history owned by the team

- **v2.6 (2026-04):** geography controls (`allowedCountries`).
- **v2.5 (2025-08):** co-brand partner scopes.

Platform convention says minor versions are additive and a major version change moves the path, so a breaking change would mean a new `/cards/v3` base path.

## Operating notes and open questions

- The documented sample is labelled as a lock call, but its body and response match the controls operation. Check the real contract before relying on the lock request or response shape.
- `controlsVersion` appears to increase as controls change. The source does not say it supports optimistic concurrency.
- The sources do not document the card status vocabulary beyond `active`, card-specific error cases, wallet provisioning fields or supported wallets, or whether control changes apply immediately at authorization.
- Team contacts, escalation paths and runbooks are not in the source corpus. Do not assume them from this page.
