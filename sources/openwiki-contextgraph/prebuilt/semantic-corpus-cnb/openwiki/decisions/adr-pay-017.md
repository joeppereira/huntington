---
type: Decision
entity_id: ADR-PAY-017
title: "ADR-PAY-017: Kafka as the Integration Backbone"
description: Accepted 2023-11-07 architecture decision making Kafka (Confluent) the mandatory integration backbone for payment lifecycle events across all payment systems at Crestline National Bank.
tags: [adr, kafka, confluent, payments, integration-backbone, event-driven, pph, payments-arb]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-95e454ddd82fc29fca46b0a9
    resource: repo://sources/estate/arb-pay-reg-2026q3-payments-arb-adr-register-and-minutes.md
  - id: openwiki-source-550c0e3f038aab7950cab477
    resource: repo://sources/estate/cbo-arch-wc-4.1-wire-center-current-state-architecture.md
  - id: openwiki-source-4452149a3b4502b4c763a559
    resource: repo://sources/estate/jira-export-wt-discovery-2026-10-05.md
  - id: openwiki-source-a4ee8b1dfcb7e3cec0a315e4
    resource: repo://sources/estate/pph-api-cat-2026.3-prism-payments-hub-api-and-event-catalog.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Status

**Accepted** — 2023-11-07. Applies to **all payment systems**. Tracked as the first entry in the Payments Architecture Review Board (ARB) ADR register and remains in force as of the 2026-Q3 register extract.

## Context

Before this decision, payment systems integrated with each other and with downstream consumers (channels, operations tooling, data platforms) largely through point-to-point and polling-based mechanisms. As payment volumes and the number of consuming systems grew, this created tight coupling between producers and consumers of payment state and made it difficult to add new consumers without renegotiating integration contracts system by system.

ADR-PAY-017 establishes Kafka, run on the Confluent platform, as the shared integration backbone for publishing and consuming **payment lifecycle events** — the state transitions a payment goes through from receipt to a terminal outcome (processed, rejected, cancelled, returned, etc.). It predates, and is foundational to, several later ARB decisions that assume an event backbone already exists (see [Relationship to later ADRs](#relationship-to-later-adrs)).

## Decision

- Kafka (Confluent) is the integration backbone for payment lifecycle events, applicable to **all payment systems**, not just a single rail or product.
- Payment systems must publish lifecycle state changes as events on Kafka topics rather than requiring consumers to poll source-of-truth APIs for status.
- New payment-event integrations are expected to be built as Kafka producers/consumers rather than bespoke point-to-point feeds.

The decision is enforced in practice by PRISM Payments Hub (PPH), the system of record for payment lifecycle state, which publishes lifecycle events onto Confluent Kafka topics rather than exposing only a request/response API. See [PPH Kafka Lifecycle Event Topics](../interfaces/pph-lifecycle-event-topics.md) for the concrete topic catalog (`pay.wire.lifecycle.v2`, `pay.ach.lifecycle.v1`), payload schemas, retention, and consumer onboarding process that implement this ADR for the wire and ACH rails.

## Consequences

- Consumers that need payment status (channel back-ends, status projection services, operations tooling) are expected to build Kafka-consumer-based read models rather than calling source APIs synchronously and repeatedly. The reference pattern for this is the Status Projection Service (SPS): `Kafka consumer -> Postgres read model -> REST API`, reused across payment types via a configuration and mapping module.
- Onboarding a new consumer to a payment-lifecycle topic requires a Kafka ACL grant (requested via Jira against the owning team, e.g. PPH) and, where Avro schemas are used, schema-registry access — a lead time of roughly three weeks in the PPH case.
- Because events are the backbone, event payload design decisions (what fields are included, what is retained, what is withheld for confidentiality) become architecturally significant control points. For example, hold reason detail is deliberately excluded from PPH lifecycle events to preserve the financial-crimes trust boundary (ADR-PAY-021), while ISO return-reason codes were later added to `pay.wire.lifecycle.v2` (2026-08) because they were judged safe and useful to publish.
- Event retention is short (days, not months) by design, which means lifecycle events are suited to driving real-time/near-real-time read models and status propagation, not as a long-term system of record or audit trail; systems needing durable history must read it from the owning system's API (e.g., PPH's state-history endpoint) rather than from the topic.

## Relationship to later ADRs

ADR-PAY-017's backbone is the precondition several subsequent Payments ARB decisions build on:

- **ADR-PAY-019** (2024-06-11, event-driven channel status) turns the "events exist" capability established here into a hard requirement: channels must consume lifecycle events into a channel-owned read model and must not poll PPH for status, following the peak-load degradation seen in INC-2024-1182.
- **ADR-PAY-021** (2025-04-08, hold reason confidentiality) constrains what the Kafka backbone is allowed to carry: hold reason codes, descriptions, scores, and analyst notes must never appear on payment lifecycle events (or v2 APIs); only hold presence and a `holdId` may be exposed.
- **ADR-PAY-023** (2025-09-09, UETR as correlation id) relies on the same v2 APIs and lifecycle events as the channel for propagating the UETR correlation identifier to consumers that need to correlate with SWIFT gpi data.

## Scope and known gaps

- The decision applies to **all payment systems**, but rollout across rails is uneven in practice: ACH lifecycle events (`pay.ach.lifecycle.v1`) are consumed in production by the Status Projection Service, while wire lifecycle event consumption for client-facing channel status required separate, later funding and build work (see ADR-PAY-019 and the Wire Center current-state architecture).
- Settlement-time data (authoritative Fedwire/ACH network acceptance and settlement status) is not yet available on payment lifecycle topics; ingesting Fed acceptance/OMAD data into analytical platforms is tracked as unscheduled backlog work pending both a Kafka ACL grant and a business sponsor.
- Real-time SWIFT gpi tracking data has not been approved for exposure to channels directly from its source snapshot; the ARB's 2026-09-08 minutes reaffirm that any such exposure would need to go through a reviewed, quota-isolated read-only service rather than direct backbone access, underscoring that "backbone" status does not imply unrestricted publication of every available payment data source.

## Governance

ADR-PAY-017 was approved by the Payments Architecture Review Board, the forum responsible for architecture decisions binding on channel, payments, and data teams. See [Payments Architecture Review Board (ARB) / Enterprise Architecture](../teams/payments-arb-enterprise-architecture.md) for the board's charter, membership, and decision cadence. It is recorded as entry ADR-PAY-017 in the Payments ARB's ADR register, alongside ADR-PAY-019, ADR-PAY-021, ADR-PAY-023, and ADR-PAY-026.
