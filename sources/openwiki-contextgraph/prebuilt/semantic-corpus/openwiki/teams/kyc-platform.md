---
type: Team
title: Know-Your-Customer Platform
description: The Know-Your-Customer Platform team owns the Customer Identity & KYC API (API-07, v1.9, /kyc/v1) in the Client Onboarding domain. This page covers what the team is accountable for, who depends on its API, and the commitments it carries.
tags: [team, kyc-platform, client-onboarding, api-07, identity-verification, aml, pii, developer-platform]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-05T01:46:21.335Z
sources:
  - id: openwiki-source-dd711ce9b07a438489c0fd1c
    resource: repo://sources/api_docs/apis/api-04-real-time-payments-api.md
  - id: openwiki-source-01f8f4581a996f4e990cf168
    resource: repo://sources/api_docs/apis/api-06-card-management-api.md
  - id: openwiki-source-02937dfc348e02c68c1fd975
    resource: repo://sources/api_docs/apis/api-07-customer-identity-kyc-api.md
  - id: openwiki-source-00eb967862ea67fd6af69064
    resource: repo://sources/api_docs/apis/api-09-credit-decisioning-api.md
  - id: openwiki-source-65a2ad8de7d532680de82b60
    resource: repo://sources/api_docs/mhfc-developer-platform-api-reference.md
generated: { by: "openwiki/0.7.0", at: "2026-10-05T01:46:21.335Z" }
---

# Know-Your-Customer Platform

The Know-Your-Customer (KYC) Platform team is the owning team for the [API-07 Customer Identity & KYC API](../apis/api-07-customer-identity-kyc-api.md). In the [Developer Platform](../apis/developer-platform-overview.md) catalog it owns exactly one API, and that API belongs to the **Client Onboarding** business domain. The sources describe no other responsibilities for the team. They give no headcount, reporting line, on-call process, repositories or contacts.

## What the team is accountable for

The team runs the capability that decides whether a customer or entity can be trusted enough to open accounts and transact. The API's stated scope is identity verification, customer due diligence and beneficial-ownership checks. It returns a KYC status and an AML risk rating, and other systems use those results to gate account opening and payment limits.

Only three endpoints are documented under `/kyc/v1`:

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `/verifications` | Start an individual or entity verification |
| GET | `/verifications/{id}` | Fetch the result (`verified`, `review` or `rejected`) with reason codes |
| GET | `/customers/{customerId}/risk-rating` | Fetch the current AML risk rating (`low`, `medium` or `high`) |

Two outputs matter to consumers. The verification status is the outcome of a single verification. The risk rating is a customer-level property that is read separately. The example verification response carries both, along with the list of checks performed (`id`, `sanctions`, `pep`).

## Commitments the team carries

| Commitment | Value |
| --- | --- |
| Current version | v1.9, with the major version in the path (`/kyc/v1`) |
| Data classification | Restricted - PII |
| OAuth scopes | `kyc:verify`, `kyc:read` |
| Rate limit | 200 requests/minute per client |
| SLO | 99.9% availability; p95 latency 1.2 s for verification |

### Security posture

- **PII handling is the central concern.** The API is classified Restricted - PII. The documented request refers to the identity document through an opaque `documentToken` (for example `doc_44ab`) and does not carry raw document data.
- **Scope separation.** `kyc:verify` and `kyc:read` are separate scopes, which suggests that the right to start verifications can be granted separately from read access. The source does not map scopes to endpoints, so that mapping is an inference.
- **Platform-wide rules** apply. These are OAuth 2.0 (client credentials with mutual TLS for servers, authorization code with PKCE for customer-facing apps), an `Idempotency-Key` header on POSTs, 429 responses on rate-limit breaches, and standard error objects. The documented verification request sends an `Idempotency-Key`.

## Consumers and integration boundaries

Intended consumers are **onboarding applications**, **Payments** and **Card Services**. The team's API is a shared dependency of several domains, so a change in its behavior or availability has an effect beyond Client Onboarding.

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: an unescaped angle bracket inside a label breaks rendering; rephrase the label. -->
```text
flowchart LR
    V[Identity verification vendors] --> K[API-07 Customer Identity and KYC<br/>owned by KYC Platform]
    S[Sanctions and PEP lists] --> K
    R[Corporate registries] --> K
    K --> AO[Accounts opening]
    K --> RTP[Real-Time Payments API API-04 limits]
    K --> CARD[Card Management API API-06]
```

- **Upstream:** identity verification vendors, sanctions and PEP lists, and corporate registries. The vendor and list sources line up with the `id`, `sanctions` and `pep` checks. Registries are the likely source for entity and beneficial-ownership checks, although the source does not say so.
- **Downstream:** account opening, the [Real-Time Payments API](../apis/api-04-real-time-payments-api.md) (API-04) limits, and the [Card Management API](../apis/api-06-card-management-api.md) (API-06). The API-04, API-06 and API-09 lineage tables each list API-07 as an upstream source. The source does not say how those consumers use KYC data in detail, for example whether it gates card issuance.
- **Not on the lineage:** API-07 is not registered as an upstream feed of any Tier 1 model in the API-to-model matrix, so it is not described as a critical data service in the sources.

## Change history owned by the team

- **v1.9 (2026-01):** added beneficial-ownership checks for entities. This is the only changelog entry in the source.

Platform convention says minor versions are additive and a major version change moves the path, so a breaking change would mean a new `/kyc/v2` base path.

## Operating notes and open questions

- Verification latency includes vendor round trips. The `review` status implies that some results are not immediate, so consumers should be ready to poll `GET /verifications/{id}`. The source does not document asynchronous behavior or webhooks for status changes.
- The 200 requests/minute limit is low for bulk onboarding, so batch jobs need throttling.
- Consumers that gate on KYC have no documented fallback for the case where the API is unavailable against its 99.9% SLO.
- The sources do not document the entity request schema, the reason-code catalogue, the risk-rating methodology or its recalculation schedule, error cases specific to KYC, or transitions out of `review`.
- Team contacts, escalation paths and runbooks are not in the source corpus. Do not assume them from this page. For general production incidents, the platform lists an API operations hotline.
