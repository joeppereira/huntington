---
type: Interface
entity_id: EP-PPH-01
title: CBO Status Projection Service (SPS) Read Model API
description: "/cbo/sps/v1, the Kafka-consumer-to-Postgres read-model API behind CNB's reference event-driven channel status pattern (ADR-PAY-019); today configured for ACH only (pay.ach.lifecycle.v1), with wire support requiring a new mapping module and a consumer ACL on pay.wire.lifecycle.v2."
tags: [sps, cbo, status-projection-service, read-model, kafka, postgres, pay.ach.lifecycle.v1, pay.wire.lifecycle.v2, adr-pay-019, event-driven, ach, wire-center]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-550c0e3f038aab7950cab477
    resource: repo://sources/estate/cbo-arch-wc-4.1-wire-center-current-state-architecture.md
  - id: openwiki-source-49303e801f124d97df9c3ea3
    resource: repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md
  - id: openwiki-source-d637e82ba742e8a4b8f0c799
    resource: repo://sources/estate/ens-int-3.2-enterprise-notification-service-integration-guide.md
  - id: openwiki-source-4452149a3b4502b4c763a559
    resource: repo://sources/estate/jira-export-wt-discovery-2026-10-05.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

The CBO Status Projection Service (SPS, internal system ID `SYS-CBO-SPS`, built under
story CBO-3815) exposes `/cbo/sps/v1`, a channel-facing REST read model backed by a
Kafka-consumer-to-Postgres materialization pipeline. It is the concrete reference
implementation of [ADR-PAY-019](../decisions/adr-pay-019.md)'s requirement that channel
status integrations consume Prism Payments Hub (PPH) lifecycle events into a
channel-owned read model rather than poll PPH's synchronous status APIs — a requirement
the Payments Architecture Review Board (ARB) reaffirmed on 2026-09-08 as the pattern for
client-facing status of **any** payment type, not just the ACH rail it was originally
built for.

As of the current CBO-ARCH-WC-4.1 architecture review (last reviewed 2026-08-20), SPS is
**configured for ACH only**: it consumes `pay.ach.lifecycle.v1` and drives the ACH
Payment Tracker experience (CBO-3790) in Crestline Business Online (CBO). [Wire
Center](../systems/cbo-wire-center.md) does not use SPS today — it still calls PPH v1
synchronously — and `/cbo/sps/v1` has no wire payment type configured. Both the Wire
Center architecture document and the SPS implementation story (CBO-3815) are explicit
that this is a configuration gap, not an architectural one: the service was built to be
payment-type agnostic, and adding wire support is described as a bounded, well-understood
unit of work (a new mapping module plus a Kafka consumer ACL), not a redesign.

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: an unescaped angle bracket inside a label breaks rendering; rephrase the label. -->
```text
flowchart LR
    subgraph PPH["Prism Payments Hub (PPH)"]
        ACHTopic["pay.ach.lifecycle.v1\n(EV-PPH-02, 7-day retention)"]
        WireTopic["pay.wire.lifecycle.v2\n(EV-PPH-01, 7-day retention)\nNOT onboarded"]
    end
    subgraph SPS["CBO Status Projection Service (SYS-CBO-SPS)"]
        Consumer["Kafka consumer\n(ACH Tracker, CBO-3815)"]
        Mapper["Mapping module\nlifecycle state -> client milestone"]
        PG[("Postgres read model")]
        API["/cbo/sps/v1 REST API"]
    end
    ACHTopic --> Consumer
    WireTopic -. "requires new ACL + mapping module\n(not built)" .-> Mapper
    Consumer --> Mapper --> PG --> API
    API --> Timeline["<cbo-journey-timeline> component\n(ACH Payment Tracker, CBO-3790)"]
    API -. "not wired up today" .-> WireUI["Wire Center detail/list UI\n(still calls PPH v1 sync)"]
```

## Responsibilities and architectural role

SPS owns a single responsibility: materializing payment-lifecycle Kafka events into a
Postgres read model that a channel BFF can query cheaply and repeatedly, so that no
channel UI needs to call PPH synchronously for routine status display. This directly
closes the gap that caused [INC-2024-1182](../incidents/inc-2024-1182.md): the "Wire
Status Lite" pilot (CBO-3120) drove ~85 TPS of synchronous polling against PPH v1's
status endpoint at month-end, exhausting its thread pool and delaying wire release for 47
minutes. ADR-PAY-019 was adopted in direct response, and SPS is named in the ADR as *the*
reference implementation of its decision.

SPS sits downstream of PPH and upstream of the channel-facing UI and notification layer:

- **Upstream**: PPH publishes payment lifecycle state transitions onto per-rail Kafka
  topics. SPS is a consumer of those topics, never a producer, and never calls PPH
  synchronously as part of its own pipeline.
- **Downstream (read path)**: `/cbo/sps/v1` is called by the CBO channel BFF layer to
  render the `<cbo-journey-timeline>` component (a reusable Aurora DS v4 asset built
  originally for the ACH Payment Tracker, CBO-3802) and to drive status-change
  notifications.
- **Downstream (notifications)**: SPS itself produces `TRS.ACH.STATUS_CHANGED` and
  `TRS.ACH.RETURN_RECEIVED` events to the Enterprise Notification Service (ENS) via `POST
  /ens/v3/notifications`, in addition to serving the read API — it is a notification
  producer as well as a read-model service for the ACH rail it already supports.

Ownership: SPS is owned by **CBO Platform** (technical and business ownership per the PTT
system ownership register, `SYS-CBO-SPS`), distinct from the CBO Wire Center squad that
owns Wire Center itself (`SYS-CBO`). It carries **T2** (business-hours + on-call) support,
one tier below Wire Center's T1.

## The Kafka-consumer-to-Postgres pattern

The pipeline has three stages, all currently instantiated only for ACH:

1. **Kafka consumption.** SPS subscribes to a payment-lifecycle Kafka topic — today,
   `pay.ach.lifecycle.v1` (catalog ID EV-PPH-02) — and consumes lifecycle events as they
   are published by PPH. Like its wire counterpart `pay.wire.lifecycle.v2`, this topic
   retains only 7 days of events, so SPS's consumer must handle replay/catch-up logic for
   any gap in processing rather than assuming it can always rebuild state from the
   beginning of the topic. See [PPH Kafka Lifecycle Event
   Topics](pph-lifecycle-event-topics.md) for the topic's retention and replay
   implications in detail.
2. **Mapping to client milestones.** A per-payment-type **mapping module** translates the
   rail's raw lifecycle states into the client-facing milestones shown in the journey
   timeline. This mapping layer is the extension point the service was explicitly
   designed around: CBO-3815's implementation notes describe SPS as "payment-type
   agnostic," onboarding a new rail by adding a topic subscription plus a mapping module,
   not by changing the consumer or storage layer.
3. **Postgres materialization and serving.** The mapped, per-payment milestone state is
   written to a Postgres read model, which `/cbo/sps/v1` serves to callers. This
   read-your-writes-from-Postgres design is what lets the channel BFF query status
   repeatedly (e.g., on every page render or list refresh) without that traffic ever
   reaching PPH — the entire point of the pattern under ADR-PAY-019.

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: an unescaped angle bracket inside a label breaks rendering; rephrase the label. -->
```text
sequenceDiagram
    participant PPH as PPH (ACH engine)
    participant Topic as pay.ach.lifecycle.v1
    participant SPS as SPS consumer + mapper
    participant PG as Postgres read model
    participant BFF as CBO channel BFF
    participant ENS as ENS

    PPH->>Topic: publish lifecycle event (fromState -> toState)
    Topic->>SPS: consume event
    SPS->>SPS: map lifecycle state -> client milestone
    SPS->>PG: upsert read-model row (keyed by payment id)
    SPS->>ENS: POST /ens/v3/notifications (TRS.ACH.STATUS_CHANGED / RETURN_RECEIVED)
    BFF->>SPS: GET /cbo/sps/v1/... (status/timeline query)
    SPS->>PG: read current projection
    SPS-->>BFF: milestone timeline response
```

## What adding wire support requires

Both CBO-ARCH-WC-4.1 §7/§8 and the CBO-3815 Jira record converge on the same two-part
gap, stated by the SPS implementer (Arjun Mehta) directly: *"Wire would need ACL on
`pay.wire.lifecycle.v2` and a mapping from v2 lifecycleState to client milestones."*
Concretely:

1. **A Kafka consumer ACL on `pay.wire.lifecycle.v2` (EV-PPH-01).** SPS has no existing
   grant on this topic. Per the PPH API & Event Catalog, obtaining a consumer ACL is
   requested via a Jira ticket against the PPH team and takes roughly three weeks end to
   end, including Confluent schema-registry access for the Avro-encoded payload
   (`WireLifecycleEvent` v2.3). This is the same onboarding path and lead time any new
   consumer of that topic must budget for, not a special case for SPS.
2. **A new mapping module** translating the wire rail's v2 `lifecycleState` values
   (`RECEIVED`, `VALIDATING`, `SCREENING`, `HELD`, `REPAIR`, `FUNDS_CONTROL`,
   `WAREHOUSED`, `RELEASED`, `SENT_TO_NETWORK`, `NETWORK_ACCEPTED`, `NETWORK_REJECTED`,
   `COMPLETED`, `CANCELLED`, `RETURNED` — see [Wire Lifecycle State
   Model](../concepts/wire-lifecycle-state-model.md)) into whatever client-facing
   milestones a wire journey timeline would show. This is new work, not a reuse of the
   ACH mapping, because the two rails' underlying state machines differ; only the
   Postgres storage layer, the `/cbo/sps/v1` API shape, and the `<cbo-journey-timeline>`
   UI component are expected to be reusable as-is.

Neither piece is scheduled: CBO-ARCH-WC-4.1 lists SPS wire support as a "reusable asset"
with a known extension path, not a committed backlog item, and the Jira export shows no
story under the CBO or PPH projects actively building the wire mapping module or
requesting the `pay.wire.lifecycle.v2` ACL for SPS specifically — the work is referenced
only in CBO-3815's closing comment and the architecture document's constraints section.
Any attempt to add wire support would additionally inherit the broader lifecycle-topic
constraints already documented for `pay.wire.lifecycle.v2`: hold reasons are never
published on the topic (per [ADR-PAY-021](../decisions/adr-pay-021.md)), so a wire-rail
SPS projection could show hold *presence* but not a hold reason, matching what Wire
Center already cannot show today without a separate FCC-approved facade; and ISO return
reasons (`return.isoReason`, e.g. `AC04`) have only been published since 2026-08
(PPH-2266), so a wire mapping module built before that date would have needed rework to
surface returns correctly.

## Relationship to Wire Center's current status model

Wire Center's own status display is unrelated to SPS today: it derives its client-facing
labels (Draft, Pending Approval, Approved, Submitted, In Process, Pending Review,
Completed, Rejected, Cancelled, Returned) directly from synchronous calls to the
deprecated PPH v1 status API (`GET /pph/v1/wires/{ref}/status`, EP-PPH-01), cached 60
seconds and throttled to one user-initiated refresh per 60 seconds per wire under
ADR-PAY-019's polling exception. That label set, and the known production incident where
a wire showed "Completed" and then was returned a day later
([CMP-2026-1189](../incidents/cmp-2026-1189.md)), stem from PPH v1's coarse `PROCESSED`
status, not from any SPS/mapping-module decision — because SPS has no wire mapping
module, it plays no role in that incident or in Wire Center's current status semantics at
all. Onboarding wire to SPS (rather than, for example, having Wire Center call PPH v2
REST directly) would be one way to simultaneously satisfy ADR-PAY-019 for any new wire
milestone-tracking feature and expose the finer-grained v2 lifecycle states that v1
collapses, but no decision to do so has been made as of the current architecture review.

## Related

- [ADR-PAY-019: Event-Driven Channel Status (No Polling)](../decisions/adr-pay-019.md) —
  the decision SPS implements, and the record of the incident that motivated it.
- [PPH Kafka Lifecycle Event Topics](pph-lifecycle-event-topics.md) — `pay.ach.lifecycle.v1`
  (consumed today) and `pay.wire.lifecycle.v2` (would need to be consumed to add wire
  support), including retention, payload, and onboarding details.
- [Wire Lifecycle State Model](../concepts/wire-lifecycle-state-model.md) — the v2
  lifecycle states a wire mapping module would need to translate into client milestones.
- [ENS Notification API & TRS Event Catalog](ens-notification-api-trs-catalog.md) — the
  `TRS.ACH.STATUS_CHANGED` / `TRS.ACH.RETURN_RECEIVED` events SPS produces today, and the
  explicit absence of any equivalent wire-lifecycle event types.
