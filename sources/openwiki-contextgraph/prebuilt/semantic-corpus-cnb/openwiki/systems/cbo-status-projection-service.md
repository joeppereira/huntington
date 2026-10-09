---
type: System
entity_id: SYS-CBO-SPS
title: CBO Status Projection Service (SPS) (SYS-CBO-SPS)
description: Reusable Kafka-consumer-to-Postgres-read-model system (SYS-CBO-SPS, built under CBO-3815) that is CNB's reference pattern for event-driven, non-polling payment status in Crestline Business Online; today configured for ACH only and not wired to Wire Center's Fedwire/Swift wires.
tags: [sps, cbo, status-projection-service, kafka, postgres, read-model, event-driven, adr-pay-019, ach, wire-center, reference-pattern, cbo-platform]
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
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

The **CBO Status Projection Service** (SPS, system ID `SYS-CBO-SPS`) is the Kafka-consumer-
to-Postgres-read-model system that materializes Prism Payments Hub (PPH) payment-lifecycle
events into a queryable status read model for Crestline Business Online (CBO). It was built
under story **CBO-3815** as the platform half of the **ACH Payment Tracker** epic (CBO-3790,
Done, R25.4/2025-11), alongside the companion front-end component
`<cbo-journey-timeline>` (CBO-3802). SPS exposes its projection to channel code through
`/cbo/sps/v1`; see [SPS Read Model API](../interfaces/sps-read-model-api.md) for the request
and response contract.

SPS exists because Crestline Business Online is forbidden from polling PPH for status. The
2024 "Wire Status Lite" pilot (CBO-3120) refreshed every visible wire's status from PPH's
synchronous v1 API every 30 seconds; at month-end volume this drove ~85 TPS against PPH,
exhausted its API thread pool, and delayed wire release for 47 minutes
([INC-2024-1182](../incidents/inc-2024-1182.md), analyzed in
[PIR-2024-07](../incidents/pir-2024-07.md)). The resulting architecture decision,
[ADR-PAY-019](../decisions/adr-pay-019.md) (accepted 2024-06-11), requires channel status
integrations to consume PPH lifecycle events into a **channel-owned read model** instead of
polling, and names SPS directly as the decision's reference implementation. The Payments
Architecture Review Board (ARB) reaffirmed this on 2026-09-08: SPS is "the reference pattern
for client-facing status of any payment type," not just ACH.

As of the current Wire Center architecture review (CBO-ARCH-WC-4.1, last reviewed
2026-08-20), that generalization has not yet happened in practice: **SPS is configured for
ACH only**. It consumes `pay.ach.lifecycle.v1` and serves the ACH Payment Tracker experience;
it has no subscription to `pay.wire.lifecycle.v2` and no wire mapping module, and
[Wire Center](../systems/cbo-wire-center.md) does not call `/cbo/sps/v1` at all — it still
derives its status labels from synchronous, throttled calls to the deprecated PPH v1 status
API. CBO-ARCH-WC-4.1 §7–§8 and the CBO-3815 Jira record both describe this as a bounded,
well-understood configuration gap (a Kafka ACL plus a mapping module), not a redesign.

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: an unescaped angle bracket inside a label breaks rendering; rephrase the label. -->
```text
flowchart LR
    subgraph PPH["Prism Payments Hub"]
        ACHTopic["pay.ach.lifecycle.v1\n(EV-PPH-02)"]
        WireTopic["pay.wire.lifecycle.v2\n(EV-PPH-01) — not onboarded"]
    end
    subgraph SPS["CBO Status Projection Service (SYS-CBO-SPS)"]
        Consumer["Kafka consumer\n(CBO-3815, ACH only)"]
        Mapper["Mapping module\nlifecycle state -> client milestone"]
        PG[("Postgres read model")]
        API["/cbo/sps/v1"]
    end
    ACHTopic --> Consumer --> Mapper --> PG --> API
    WireTopic -. "needs new ACL\n+ new mapping module" .-> Mapper
    API --> Timeline["<cbo-journey-timeline>\n(ACH Payment Tracker UI)"]
    API -. "not integrated today" .-> WireUI["Wire Center UI\n(still calls PPH v1 sync)"]
    SPS -- "TRS.ACH.STATUS_CHANGED\nTRS.ACH.RETURN_RECEIVED" --> ENS["Enterprise Notification Service"]
```

## Responsibilities and architectural role

SPS has one responsibility: turn PPH's asynchronous payment-lifecycle Kafka events into a
read model a channel backend-for-frontend (BFF) can query cheaply, repeatedly, and without
ever calling PPH synchronously. It sits strictly downstream of PPH and upstream of channel
UI and notifications:

- **Upstream** — PPH is the sole producer of the lifecycle topics SPS consumes. SPS never
  calls PPH's REST APIs as part of its own pipeline; it only consumes Kafka events.
- **Downstream (reads)** — `/cbo/sps/v1` is called by CBO channel BFF code to drive the
  `<cbo-journey-timeline>` milestone component. Today that is exclusively the ACH Payment
  Tracker; no Wire Center screen queries this API.
- **Downstream (notifications)** — SPS is itself an Enterprise Notification Service (ENS)
  producer, sending `TRS.ACH.STATUS_CHANGED` and `TRS.ACH.RETURN_RECEIVED` via
  `POST /ens/v3/notifications`. See
  [ENS Notification API & TRS Event Catalog](../interfaces/ens-notification-api-trs-catalog.md).

**Ownership**: SPS is owned by the **CBO Platform & Entitlements** team (technical owner
Arjun Mehta, business owner Marcus Chen), distinct from the CBO Wire Center squad (Tom
Becker / Lucas Ferreira) that owns Wire Center itself. It runs at **T2** support (business
hours + on-call), one tier below Wire Center's T1. Any future wire-tracking work is
therefore necessarily a cross-team build between these two teams, not a Wire-Center-only
change.

## Mechanism: the Kafka-consumer-to-Postgres pipeline

The pipeline has three stages, all currently instantiated only for the ACH rail:

1. **Kafka consumption.** SPS subscribes to a per-payment-type lifecycle topic — today only
   `pay.ach.lifecycle.v1` (catalog ID EV-PPH-02). Like its wire counterpart
   `pay.wire.lifecycle.v2` (EV-PPH-01), the topic retains only 7 days of events, so the
   consumer must implement replay/catch-up handling for any processing gap rather than
   assume it can rebuild state from topic start. See
   [PPH Kafka Lifecycle Event Topics](../interfaces/pph-lifecycle-event-topics.md) for
   retention, payload, and onboarding details.
2. **Mapping to client milestones.** A per-payment-type **mapping module** translates raw
   rail lifecycle states into the client-facing milestones the journey timeline displays.
   This mapping layer is SPS's designed extension point: the implementing engineer
   describes SPS as "payment-type agnostic" — onboarding a new rail means adding a topic
   subscription and a mapping module, not changing the consumer or storage layer.
3. **Postgres materialization and serving.** Mapped per-payment milestone state is upserted
   into a Postgres read model keyed by payment identifier, which `/cbo/sps/v1` serves to
   callers. This read-your-writes-from-Postgres design is what lets the channel BFF query
   status on every page render or list refresh without that traffic ever reaching PPH.

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

## Extension model: adding a new payment type

SPS was explicitly designed so that onboarding a new payment type is additive, not a
rewrite. Adding wire support — the scenario the ARB and Wire Center architecture document
both call out as the immediate candidate — requires two concrete, independent pieces of
work, neither of which is scheduled as of the 2026-10-05 backlog snapshot:

1. **A Kafka consumer ACL on `pay.wire.lifecycle.v2`.** SPS has no existing grant on this
   topic. Per the PPH event catalog, a consumer ACL is requested via a Jira ticket against
   the PPH team and takes roughly three weeks end to end, including Confluent
   schema-registry access for the Avro-encoded `WireLifecycleEvent` v2.3 payload.
2. **A new mapping module** translating wire's v2 `lifecycleState` values (`RECEIVED`,
   `VALIDATING`, `SCREENING`, `HELD`, `REPAIR`, `FUNDS_CONTROL`, `WAREHOUSED`, `RELEASED`,
   `SENT_TO_NETWORK`, `NETWORK_ACCEPTED`, `NETWORK_REJECTED`, `COMPLETED`, `CANCELLED`,
   `RETURNED`) into client-facing milestones. This is new engineering, not a reuse of the
   ACH mapping, because the two rails' state machines differ. Only the Postgres storage
   layer, the `/cbo/sps/v1` API shape, and the `<cbo-journey-timeline>` UI component
   (CBO-3802, already rail-agnostic) are expected to be reusable as-is.

Even once built, a wire mapping module would inherit constraints that already apply to the
underlying topic:

- **No hold reasons.** Under [ADR-PAY-021](../decisions/adr-pay-021.md), hold reason codes,
  descriptions, scores and analyst notes never leave Financial Crimes Trust (FCT) systems.
  `pay.wire.lifecycle.v2` carries only hold *presence* and a `holdId`, so a wire SPS
  projection could show that a wire is held but not why — matching what Wire Center already
  cannot show today without a separate FCC-approved facade.
- **ISO return reasons only since 2026-08.** `pay.wire.lifecycle.v2` began carrying
  `return.isoReason` (the `pacs.004` return reason code) only after PPH-2266 shipped in
  2026-08; a mapping module built earlier would have needed rework to surface returns
  correctly.

No Jira story in the current backlog snapshot is actively requesting the
`pay.wire.lifecycle.v2` ACL or building the wire mapping module; the work is referenced only
in CBO-3815's closing engineering comment and in the Wire Center architecture document's
constraints and reusable-assets sections, not as a committed, pointed backlog item.

## Relationship to Wire Center's current status handling

Wire Center's status display today is entirely independent of SPS: it derives client-facing
labels (Draft, Pending Approval, Approved, Submitted, In Process, Pending Review, Completed,
Rejected, Cancelled, Returned) from synchronous, 60-second-cached, once-per-60-seconds
user-initiated-refresh calls to the deprecated PPH v1 status API, under the throttled-refresh
exception ADR-PAY-019 allows. Because no wire mapping module exists, SPS plays no role in
Wire Center's current status semantics or in the incident where a wire displayed "Completed"
and was returned by the beneficiary bank the next day
([CMP-2026-1189](../incidents/cmp-2026-1189.md)) — that incident traces to PPH v1's coarse
`PROCESSED` status collapsing multiple distinct lifecycle states, not to any SPS decision.
Onboarding wire to SPS would be one way to simultaneously satisfy ADR-PAY-019 for a future
wire milestone-tracking feature and expose the finer-grained v2 lifecycle states that v1
collapses, but no such decision has been made.

SPS is also unrelated to international (Swift gpi) wire status: gpi tracking data is visible
only to Payment Operations in the Investigations Workbench today, a gap tracked separately as
spike CBO-4480, with no SPS or Kafka-topic dependency identified yet.

## Configuration and operations summary

| Aspect | Current state |
|---|---|
| Payment types configured | ACH only (`pay.ach.lifecycle.v1`, EV-PPH-02) |
| Wire support | Not configured; needs ACL on `pay.wire.lifecycle.v2` (EV-PPH-01) + new mapping module |
| Serving API | `/cbo/sps/v1` (see [SPS Read Model API](../interfaces/sps-read-model-api.md)) |
| State store | Postgres read model, keyed by payment identifier |
| Notification output | `TRS.ACH.STATUS_CHANGED`, `TRS.ACH.RETURN_RECEIVED` via ENS |
| Owning team | CBO Platform & Entitlements (tech owner Arjun Mehta, business owner Marcus Chen) |
| Support tier | T2 (business hours + on-call) |
| Built under | CBO-3815 (Done, R25.3), child of CBO-3790 (ACH Payment Tracker, Done, R25.4) |
| Governing decision | [ADR-PAY-019](../decisions/adr-pay-019.md); reaffirmed as cross-rail reference pattern by ARB 2026-09-08 |

## Related

- [SPS Read Model API](../interfaces/sps-read-model-api.md) — the `/cbo/sps/v1` contract SPS
  exposes to channel BFFs.
- [CBO-3790: ACH Payment Tracker](../projects/cbo-3790-ach-payment-tracker.md) — the epic
  under which SPS (CBO-3815) and `<cbo-journey-timeline>` (CBO-3802) were built.
- [ADR-PAY-019: Event-Driven Channel Status (No Polling)](../decisions/adr-pay-019.md) — the
  decision SPS implements, and the incident record behind it.
- [PPH Kafka Lifecycle Event Topics](../interfaces/pph-lifecycle-event-topics.md) —
  `pay.ach.lifecycle.v1` (consumed today) and `pay.wire.lifecycle.v2` (would need onboarding
  for wire support).
- [ADR-PAY-021: Hold Reason Confidentiality](../decisions/adr-pay-021.md) — the invariant
  limiting what any future wire mapping module could surface about holds.
- [ENS Notification API & TRS Event Catalog](../interfaces/ens-notification-api-trs-catalog.md)
  — the `TRS.ACH.STATUS_CHANGED` / `TRS.ACH.RETURN_RECEIVED` events SPS produces.
