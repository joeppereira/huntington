---
type: Interface
entity_id: EP-PPH-06
title: PPH Kafka Lifecycle Event Topics
description: "EV-PPH-01 pay.wire.lifecycle.v2 and EV-PPH-02 pay.ach.lifecycle.v1: PRISM Payments Hub's Kafka payment-lifecycle topics, their Avro payload, 7-day retention, Jira-based consumer ACL onboarding, and what is (ISO return reasons since 2026-08) and is not (hold reasons) published."
tags: [pph, kafka, confluent, pay.wire.lifecycle.v2, pay.ach.lifecycle.v1, event-driven, payments, adr-pay-017, adr-pay-019, adr-pay-021, status-projection]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-95e454ddd82fc29fca46b0a9
    resource: repo://sources/estate/arb-pay-reg-2026q3-payments-arb-adr-register-and-minutes.md
  - id: openwiki-source-a4ee8b1dfcb7e3cec0a315e4
    resource: repo://sources/estate/pph-api-cat-2026.3-prism-payments-hub-api-and-event-catalog.md
  - id: openwiki-source-19beabaf3acaad354d39ee1e
    resource: repo://sources/estate/pph-sys-ovw-9.2-prism-payments-hub-system-overview-and-lifecycle-state-model.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

`pay.wire.lifecycle.v2` (catalog ID **EV-PPH-01**) and `pay.ach.lifecycle.v1` (catalog ID
**EV-PPH-02**) are the two Confluent Kafka topics through which **PRISM Payments Hub (PPH)** — the
wire and ACH orchestration platform built on the Volaris Payment Platform — publishes payment
lifecycle state changes. They are the concrete implementation of [ADR-PAY-017](../decisions/adr-pay-017.md)
("Kafka is the integration backbone for payment lifecycle events") for the wire and ACH rails, and
the mandatory integration path required by [ADR-PAY-019](../decisions/adr-pay-019.md) ("channel
status integrations must be event-driven; no polling of PPH"). Any channel or back-office system
that needs payment status is expected to consume these topics into its own read model rather than
calling PPH's synchronous REST APIs repeatedly.

Both topics are documented as EV-PPH-01 / EV-PPH-02 in the PPH API & Event Catalog
(PPH-API-CAT-2026.3), alongside the v1 (deprecated, sunsetting 2027-03-31) and v2 REST APIs that
cover the same payment lifecycle data via request/response.

## Topics at a glance

| ID | Topic | Content | Retention | Consumer onboarding |
|---|---|---|---|---|
| EV-PPH-01 | `pay.wire.lifecycle.v2` | `WireLifecycleEvent` v2.3 (Avro): `paymentId`, `rail`, `fromState`, `toState`, `eventTs`, `identifiers`, `return.isoReason` | 7 days | Classification: Confidential - Client. Consumer ACL requested via PPH Jira; ~3 weeks lead time including schema-registry access |
| EV-PPH-02 | `pay.ach.lifecycle.v1` | ACH lifecycle events | 7 days | Consumed in production by the CBO Status Projection Service (ACH Tracker) |

Both topics are produced exclusively by PPH. `pay.wire.lifecycle.v2` carries an availability target
of 99.95% and a p95 event lag under 2 seconds (T1 support), the same support tier as the PPH v2 REST
API.

## Payload: `WireLifecycleEvent` v2.3 (Avro)

Each event on `pay.wire.lifecycle.v2` represents a single state transition and carries, at minimum:

- `paymentId` — PPH's internal payment key (`pphId`), the same identifier returned by the v2 REST
  API (`GET /pph/v2/payments/{paymentId}`).
- `rail` — `FEDWIRE | SWIFT | BOOK`.
- `fromState` / `toState` — the v2 canonical lifecycle states (`RECEIVED`, `VALIDATING`,
  `SCREENING`, `HELD`, `REPAIR`, `FUNDS_CONTROL`, `WAREHOUSED`, `RELEASED`, `SENT_TO_NETWORK`,
  `NETWORK_ACCEPTED`, `NETWORK_REJECTED`, `COMPLETED`, `CANCELLED`, `RETURNED`) — see the PPH system
  overview's lifecycle state model for the full meaning and typical duration of each state. Unlike
  the legacy v1 status field, which collapses `RELEASED`, `SENT_TO_NETWORK`, `NETWORK_ACCEPTED` and
  `COMPLETED` into a single `PROCESSED` value, v2 events expose the distinct underlying state, so a
  consumer can tell "released for transmission" apart from "acknowledged by the network."
- `eventTs` — the time PPH recorded the transition. For the `NETWORK_ACCEPTED` transition on
  Fedwire, this is PPH's own processing time, not the Federal Reserve's creation timestamp carried
  in the underlying `pacs.002`; the authoritative Fed timestamp exists only on the Fedwire Funds
  Connector's `net.fedwire.ack.v1` topic (see [Fedwire Network Acknowledgment Topics](fedwire-network-ack-topics.md)),
  which PPH consumes internally but does not re-publish verbatim onto the lifecycle topic.
- `identifiers` — correlation identifiers propagated from the v2 payment record, including the
  UETR assigned at release to every outbound wire (per [ADR-PAY-023](../decisions/adr-pay-023.md)),
  IMAD/OMAD, `cboRef` (channel reference), and `endToEndId`.
- `return.isoReason` — the ISO 20022 `pacs.004` return reason code (e.g., `AC04`, `AC01`, `RR05`)
  when the transition is into `RETURNED`.

There is no published Avro schema excerpt for `pay.ach.lifecycle.v1` in the catalog beyond "ACH
lifecycle events"; its consumer (the CBO Status Projection Service's ACH Tracker) is the
authoritative reference for the fields it actually relies on.

## What is, and is not, published

Two deliberate content boundaries shape what these topics can be used for:

- **Return reasons are published, since 2026-08.** `pay.wire.lifecycle.v2` began carrying
  `return.isoReason` — the ISO `pacs.004` return reason code — as of PPH-2266 (2026-08). Before that
  change, a consumer could see that a payment transitioned to `RETURNED` but not why.
- **Hold reasons are never published on PPH topics.** This is not an oversight but an enforced
  invariant under [ADR-PAY-021](../decisions/adr-pay-021.md) ("hold reason details never leave the
  financial-crimes trust boundary"): hold reason codes, descriptions, scores and analyst notes
  remain inside Financial Crimes Trust (FCT) systems.
  Lifecycle events, like the v2 REST API, expose only hold *presence* (a payment is in the `HELD`
  state) and a `holdId`, never the reason. The legacy v1 REST field `holdReasonDesc` — a free-text
  description synchronized from the Hold Management System since 2019 — has no v2 or event
  equivalent and is retained only until the v1 API sunsets (2027-03-31). Any client-facing hold
  explanation must come from a separate, FCC-approved FCT facade that returns a disclosure tier and
  pre-approved copy, not from these Kafka topics.

Settlement-time data is also absent: there is no settlement object on either the v2 REST payload or
the lifecycle events today. Rail-specific settlement status and the authoritative Federal Reserve
acceptance timestamp are tracked as backlog item PPH-2207 (8 points, awaiting a product sponsor),
not scheduled. Intermediary- or beneficiary-bank charges are likewise never known to PPH and so
never appear on these topics.

## Consumer onboarding

Gaining access to `pay.wire.lifecycle.v2` or `pay.ach.lifecycle.v1` requires a **Kafka ACL grant**,
requested via a Jira ticket against the owning team (PPH), plus Confluent **schema-registry access**
for the Avro-encoded wire topic. The catalog's stated lead time is roughly three weeks end to end.
This onboarding cost is a direct, named consequence of ADR-PAY-017/ADR-PAY-019: any new channel
status capability must budget for topic ACL onboarding, a projection/mapping module translating
lifecycle events into channel-facing status, and replay handling for the resulting read model — it
cannot be added as "just another polling call" against PPH.

`pay.wire.lifecycle.v2` is classified **Confidential - Client**, reflecting that payment identifiers
and return reasons are customer data even though hold detail is excluded.

## Consumers today

- **`pay.ach.lifecycle.v1`** is consumed in production by the CBO Status Projection Service's ACH
  Tracker, the reference event-driven read-model pattern (Kafka consumer → Postgres read model →
  REST API) that the Payments Architecture Review Board (ARB) reaffirmed on 2026-09-08 as the
  pattern for client-facing status of **any** payment type.
- **`pay.wire.lifecycle.v2`** has no production channel consumer materializing wire status as of the
  same period: Wire Center (the CBO wire channel) still relies on synchronous PPH v1 status calls
  under ADR-PAY-019's throttled user-initiated-refresh exception, and has not been onboarded to this
  topic. Wire support in the Status Projection Service is tracked as future work requiring a new
  mapping module and a consumer ACL grant onto this topic. IVR wire status and the Wire Room console
  have migrated off v1 (IVR to v2 REST; Wire Room to an internal wire builder), but neither is
  described in the catalog as a lifecycle-event consumer of `pay.wire.lifecycle.v2` itself — their
  migration targets v2 REST, not the event topic.

## Retention and failure/replay implications

Both topics retain only **7 days** of events. This retention window is deliberately short because
the topics are designed to drive near-real-time read models and status propagation, not to serve as
a durable system of record or audit trail. Practical consequences for consumers:

- A new or re-onboarded consumer cannot backfill its read model purely by replaying the topic from
  the beginning once more than 7 days have elapsed; it must reconcile against PPH's own
  state-history API (`GET /pph/v2/payments/{paymentId}/history`, EP-PPH-06) for anything older, since
  that endpoint — not the topic — is the durable source of PPH's processing-time state history.
  Note that EP-PPH-06 timestamps are PPH processing time, the same caveat that applies to `eventTs`
  on the lifecycle events themselves.
- Consumer-side outages or backlogs longer than 7 days risk silently missing transitions, which is
  why any production consumer (such as the Status Projection Service) needs explicit replay/catch-up
  handling as part of its build, not an afterthought.

## Relationship to the v1/v2 REST APIs and other rails

- `pay.wire.lifecycle.v2` is the event-topic counterpart to the v2 REST APIs (EP-PPH-04 through
  EP-PPH-07); both surface the same v2 canonical lifecycle states, the same UETR/IMAD/OMAD
  identifier set, and the same hold-presence-only view, but the topic is push-based and
  short-retention while the REST API is pull-based and backed by PPH's full state history.
- The v1 synchronous status API (`GET /pph/v1/wires/{wireRef}/status`, EP-PPH-01) has no Kafka
  equivalent: it predates the lifecycle topics, exposes the legacy `holdReasonDesc` field that v2
  deliberately drops, and is scheduled to sunset 2027-03-31 alongside the rest of the v1 surface.
- Upstream of PPH, the Federal Reserve's own Fedwire acceptance data (OMAD and Fed creation
  timestamp) flows to PPH over a separate Kafka topic, `net.fedwire.ack.v1`, owned by Payment
  Networks Engineering. PPH consumes that topic to drive its own `NETWORK_ACCEPTED` transition but
  does not pass the Fed's OMAD-bearing acknowledgment through verbatim on
  `pay.wire.lifecycle.v2` — only the derived state transition and PPH's own processing timestamp
  appear there. See [Fedwire Network Acknowledgment Topics](fedwire-network-ack-topics.md) for that
  upstream topic.

## Related decisions and documents

- [ADR-PAY-017: Kafka as the Integration Backbone](../decisions/adr-pay-017.md) — establishes Kafka
  as the mandatory integration backbone that these topics implement.
- [ADR-PAY-019: Event-Driven Channel Status (No Polling)](../decisions/adr-pay-019.md) — the decision
  that makes consuming these topics (rather than polling PPH) mandatory for channel status use
  cases.
- [ADR-PAY-021](../decisions/adr-pay-021.md) (hold reason confidentiality) — governs the hold-reason
  exclusion described above.
- [ADR-PAY-023](../decisions/adr-pay-023.md) (UETR as canonical correlation id) — governs the
  `identifiers.uetr` field carried on `pay.wire.lifecycle.v2`.
- [Fedwire Network Acknowledgment Topics](fedwire-network-ack-topics.md) — the upstream Fedwire
  acknowledgment feed PPH consumes to drive wire lifecycle transitions.
