---
type: Team
title: Fraud Strategy Engineering
description: Fraud Strategy Engineering is the team that owns the Fraud Risk Signals API (API-08, v4.0, /fraud/v4) in the Fraud & Financial Crimes domain. This page covers what the team is accountable for, who depends on its API, its upstream data, and the operating commitments it carries.
tags: [team, fraud-strategy-engineering, fraud-financial-crimes, api-08, fraud-scoring, developer-platform]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-05T01:46:21.335Z
sources:
  - id: openwiki-source-171083d8e51f266b1242a132
    resource: repo://sources/api_docs/apis/api-02-transactions-api.md
  - id: openwiki-source-7e11142a8ff791b3ef3acaf9
    resource: repo://sources/api_docs/apis/api-03-payments-initiation-api.md
  - id: openwiki-source-dd711ce9b07a438489c0fd1c
    resource: repo://sources/api_docs/apis/api-04-real-time-payments-api.md
  - id: openwiki-source-2064030e3f1ddd3bc4b386c8
    resource: repo://sources/api_docs/apis/api-05-wire-transfer-api.md
  - id: openwiki-source-c7e3d73581e8777916a14977
    resource: repo://sources/api_docs/apis/api-08-fraud-risk-signals-api.md
  - id: openwiki-source-00eb967862ea67fd6af69064
    resource: repo://sources/api_docs/apis/api-09-credit-decisioning-api.md
  - id: openwiki-source-65a2ad8de7d532680de82b60
    resource: repo://sources/api_docs/mhfc-developer-platform-api-reference.md
  - id: openwiki-source-eb14da62fbec45aad876fb64
    resource: repo://sources/reports/mhfc-2025-annual-report.md
  - id: openwiki-source-c13af588d055d118eda543d5
    resource: repo://sources/reports/mhfc-2025-pillar3-disclosures.md
  - id: openwiki-source-9da334bbfcfb68cd7514ff33
    resource: repo://sources/reports/mhfc-q2-2026-earnings-supplement.md
generated: { by: "openwiki/0.7.0", at: "2026-10-05T01:46:21.335Z" }
---

# Fraud Strategy Engineering

Fraud Strategy Engineering is the owning team for the [API-08 Fraud Risk Signals API](../apis/api-08-fraud-risk-signals-api.md). The Developer Platform catalog lists it as owner of that one API, which belongs to the **Fraud & Financial Crimes** business domain. The sources give no headcount, reporting line, on-call rota, repositories or escalation path for the team. Everything below comes from the API's published reference and from corporate reporting that mentions it. For the platform context, see the [Developer Platform overview](../apis/developer-platform-overview.md).

## What the team is accountable for

The team runs the real-time fraud decision service. A caller submits an event: a card authorization, payment, login or account change. The service returns a fraud score between 0 and 1, a `decision` and a list of reason codes. The API reference says the scores come from gradient-boosted and graph-based models, with average decision latency under 35 ms. Graph features and new reason codes arrived in v4.0 (2025-12).

Published surface, base path `/fraud/v4`:

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `/scores` | Score an event |
| POST | `/feedback` | Report confirmed fraud or a false positive, for model retraining |
| GET | `/reason-codes` | Reference list of reason codes |

The example scoring call sends an `Idempotency-Key` header and a body with `eventType` (for example `rtp_send`), `amount`, `accountId`, `deviceId` and `payee`. The response carries `score`, `decision` (the example shows `approve`) and `reasons` (for example `NEW_PAYEE_LOW_RISK`). The team therefore owns three things: the scoring models, the reason-code vocabulary and the feedback channel that returns outcomes to model retraining. The source does not describe the retraining process, the decision thresholds or the feedback payload.

## Who depends on the team's API

The API is **internal only**. Its intended consumers are Card authorization, Payments, RTP, Wires and Credit Decisioning. The named downstream consumers are:

- [Payments Initiation API (API-03)](../apis/api-03-payments-initiation-api.md)
- [Real-Time Payments API (API-04)](../apis/api-04-real-time-payments-api.md)
- [Wire Transfer API (API-05)](../apis/api-05-wire-transfer-api.md)
- [Credit Decisioning API (API-09)](../apis/api-09-credit-decisioning-api.md), which combines fraud signals with bureau data and behaviour scores. It is owned by [Credit Platforms Engineering](./credit-platforms-engineering.md).
- Operational risk loss data. The Pillar 3 disclosures list this as the downstream use of the real-time fraud scores.

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: an unescaped angle bracket inside a label breaks rendering; rephrase the label. -->
```text
flowchart LR
    TX[Transactions API-02 feature store] --> F[API-08 Fraud Risk Signals<br/>Fraud Strategy Engineering]
    DEV[Device intelligence] --> F
    CON[Consortium fraud data] --> F
    F --> P3[Payments Initiation API-03]
    F --> RTP[Real-Time Payments API-04]
    F --> W[Wire Transfer API-05]
    F --> CD[Credit Decisioning API-09]
    F --> OPR[Operational risk loss data]
```

## Upstream dependencies

The team's models depend on data produced elsewhere:

- The feature store fed by the [Transactions API (API-02)](../apis/api-02-transactions-api.md). API-02 lists "Fraud Strategy" among its intended consumers and the API-08 feature store as a downstream consumer.
- Device intelligence.
- Consortium fraud data.

The sources do not name the owners of device intelligence or consortium data. Changes to the API-02 feature feed can affect model inputs, so the team depends on that feed's stability.

## Operating commitments

| Commitment | Value |
| --- | --- |
| Availability SLO | 99.99% |
| Latency | p99 60 ms; average under 35 ms |
| Rate limit | 50,000 requests/second aggregate, internal callers only |
| OAuth scope | `fraud:score` |
| Data classification | Restricted - Internal |

Operational points to keep in mind:

- **Critical-path position.** The 2025 annual report says real-time fraud scoring is applied to every card authorization, real-time payment and wire. The 2Q26 earnings supplement says each payment is screened by API-08 before release. A degradation affects several money-movement flows at once, which is why the availability and latency targets are tight.
- **Volume.** The 2Q26 earnings supplement reports about 690 million calls per month, up 24% year-on-year, at 99.99% availability. The key consumers listed are authorizations, RTP and wires.
- **Outcomes.** Fraud losses as a percentage of card sales declined to 7.9 basis points in the 2025 annual report. The report presents real-time scoring as one control and does not credit it alone.
- **Undocumented behaviour.** The sources do not say what callers should do on timeout (fail open or closed), which decision values besides `approve` exist, or how the aggregate rate limit is split between callers. The team is the place to confirm these. Consuming teams need to define their own fallback policy.

## Change considerations

- Reason codes are served from `/reason-codes`, and v4.0 added new ones. Consumers should read the list and not hard-code it.
- The API is not registered as an upstream feed of any Tier 1 model in the API-to-model lineage matrix, which has no entries in the API-08 row.
- Changes to scoring behaviour reach the payment and credit flows listed above. Coordinate model or reason-code changes with those consumers, and with the Credit Decisioning API owner in particular, because it uses fraud signals in underwriting.

## Sources

- API-08 reference: `sources/api_docs/apis/api-08-fraud-risk-signals-api.md`
- Consolidated API catalog: `sources/api_docs/mhfc-developer-platform-api-reference.md`
- Corporate reporting: 2025 annual report, 2025 Pillar 3 disclosures, 2Q26 earnings supplement.
