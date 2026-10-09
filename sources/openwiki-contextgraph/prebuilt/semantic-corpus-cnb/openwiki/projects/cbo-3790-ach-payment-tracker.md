---
type: Project
entity_id: CBO-3790
title: "CBO-3790: ACH Payment Tracker"
description: "Done epic (R25.4, 2025-11) that delivered ACH milestone tracking and status notifications in Crestline Business Online by building the reusable <cbo-journey-timeline> component and the Status Projection Service ACH consumer, now the reference pattern for event-driven status features including planned wire tracking."
tags: [cbo, wire-center, ach, status-projection-service, journey-timeline, ens, kafka, adr-pay-019, treasury, epic]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-95e454ddd82fc29fca46b0a9
    resource: repo://sources/estate/arb-pay-reg-2026q3-payments-arb-adr-register-and-minutes.md
  - id: openwiki-source-550c0e3f038aab7950cab477
    resource: repo://sources/estate/cbo-arch-wc-4.1-wire-center-current-state-architecture.md
  - id: openwiki-source-49303e801f124d97df9c3ea3
    resource: repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md
  - id: openwiki-source-d637e82ba742e8a4b8f0c799
    resource: repo://sources/estate/ens-int-3.2-enterprise-notification-service-integration-guide.md
  - id: openwiki-source-4452149a3b4502b4c763a559
    resource: repo://sources/estate/jira-export-wt-discovery-2026-10-05.md
  - id: openwiki-source-3cc45df143c5eec31fe1f9f6
    resource: repo://sources/estate/pir-2024-07-wire-status-lite-pilot-inc-2024-1182-post-implementation-review.md
  - id: openwiki-source-a4ee8b1dfcb7e3cec0a315e4
    resource: repo://sources/estate/pph-api-cat-2026.3-prism-payments-hub-api-and-event-catalog.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

CBO-3790 is a **Done** epic (release R25.4, 2025-11; 89 points; owner Marcus Chen, Product
Owner - CBO Wire Center and Payments & Transfers) that delivered milestone-timeline tracking
and status notifications for ACH payments inside Crestline Business Online (CBO). It shipped
two child stories: a reusable Aurora Design System timeline component
(`<cbo-journey-timeline>`, CBO-3802) and a Kafka-backed read model, the **CBO Status
Projection Service** (SPS) ACH lifecycle consumer (CBO-3815). Both are now cited by
architecture and governance documents as the reusable blueprint for giving any CBO payment
rail — including Fedwire/Swift wires — an event-driven, client-facing status experience
without polling the Prism Payments Hub (PPH).

The epic exists because an earlier attempt at near-real-time wire status, **Wire Status Lite**
(CBO-3120, 2024), caused a production incident (INC-2024-1182) by polling PPH v1 every 30
seconds per visible wire; at month-end volume this exhausted PPH's shared thread pool and
delayed wire release for 47 minutes. The resulting post-implementation review (PIR-2024-07)
led to [ADR-PAY-019](#adr-pay-019-and-the-event-driven-status-pattern) (channel status must be
event-driven, no PPH polling) and an explicit action item to "build a reusable status
projection service in CBO," delivered for ACH by CBO-3790/CBO-3815 in 2025. CBO-3790 is
therefore both a feature delivery (ACH tracking) and the platform investment that resolved the
2024 incident's root cause.

## Child stories

| Key | Summary | Status | Points | Owner |
|---|---|---|---|---|
| CBO-3802 | Aurora DS: reusable `<cbo-journey-timeline>` component | Done (R25.3) | 13 | Lucas Ferreira |
| CBO-3815 | Status Projection Service (SPS) — ACH lifecycle consumer | Done (R25.3) | 21 | Arjun Mehta |

Both child stories closed in R25.3, ahead of the parent epic's R25.4 close, consistent with
component/platform work landing before the epic that assembles it into a client-facing
feature.

## What was built

### `<cbo-journey-timeline>` (CBO-3802)

A rail-agnostic Aurora Design System v4 component that renders a milestone timeline with
terminal-state and error styling. It is explicitly catalogued as a reusable asset in
CBO's current-state architecture precisely because it does not hard-code ACH semantics — any
payment type's ordered milestone list can be rendered with the same component, which is why it
is proposed as the front-end half of a future wire-tracking feature.

### Status Projection Service — ACH consumer (CBO-3815)

SPS implements the event-driven read-model pattern mandated by ADR-PAY-019:

```
pay.ach.lifecycle.v1 (Kafka, EV-PPH-02)
        |
   SPS Kafka consumer
        |
   Postgres read model (CBO Platform-owned)
        |
   GET /cbo/sps/v1  (client-facing status API)
```

- **Producer/topic**: `pay.ach.lifecycle.v1` (EV-PPH-02), published by Prism Payments Hub,
  7-day retention, consumed by CBO SPS for the ACH Tracker use case.
- **Consumer**: a Kafka consumer owned by the CBO Platform & Entitlements team (technical
  owner Arjun Mehta) that projects lifecycle events into a Postgres read model, decoupling CBO
  from PPH's synchronous APIs entirely for status reads.
- **API**: `/cbo/sps/v1` serves the projected status to CBO channel code; this is the only
  interface channel consumers need, keeping SPS swappable behind one contract.
- **Extensibility design**: per the implementing engineer's own characterization, SPS is
  **payment-type agnostic** — adding support for a new rail is "add a topic subscription + a
  mapping module," not a rewrite. Wire support specifically would require (a) a new
  consumer ACL on `pay.wire.lifecycle.v2` and (b) a mapping module from PPH v2
  `lifecycleState` values to CBO client-facing milestones. Neither exists yet.
- **Notifications**: SPS is also the producer of two live ENS event types —
  `TRS.ACH.STATUS_CHANGED` (ACH lifecycle milestone) and `TRS.ACH.RETURN_RECEIVED` (ACH
  return) — both live since 2025-11, delivered via templates `TPL-ACH-STS-01` and
  `TPL-ACH-RET-01`. See [ENS Notification API & TRS Event Catalog](../interfaces/ens-notification-api-trs-catalog.md)
  for the full TRS catalog and ENS's delivery mechanics.

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: an unescaped angle bracket inside a label breaks rendering; rephrase the label. -->
```text
flowchart LR
    PPH["Prism Payments Hub"] -- "pay.ach.lifecycle.v1\n(EV-PPH-02, Kafka)" --> SPSConsumer["SPS Kafka consumer\n(CBO Platform)"]
    SPSConsumer --> PG[("Postgres read model")]
    PG --> API["GET /cbo/sps/v1"]
    API --> Timeline["<cbo-journey-timeline>\n(Aurora DS, CBO-3802)"]
    SPSConsumer -- "milestone / return events" --> ENS["ENS v3\nPOST /ens/v3/notifications"]
    ENS --> Notif["TRS.ACH.STATUS_CHANGED\nTRS.ACH.RETURN_RECEIVED"]
```

ACH status flows from PPH's lifecycle topic through the SPS read model to both the CBO UI
(via `<cbo-journey-timeline>`) and ENS notifications; no synchronous PPH call is on this path.

## ADR-PAY-019 and the event-driven status pattern

ADR-PAY-019 ("Channel status integrations must be event-driven; no polling of PPH," accepted
2024-06-11, applies to all channels) decided that channels must obtain payment status by
consuming lifecycle events into a channel-owned read model — explicitly naming the
CBO Status Projection Service pattern — with synchronous status calls limited to
user-initiated, throttled refresh. CBO-3815 is the ADR's reference implementation. The
Payments Architecture Review Board (ARB) reaffirmed this at its 2026-09-08 session: "SPS
[is] the reference pattern for client-facing status of any payment type" (minute owner Arjun
Mehta), explicitly generalizing beyond ACH.

## Why this is the blueprint for wire tracking

CBO's Wire Center currently integrates only with PPH v1 REST APIs
(`EP-PPH-01`/`02`/`03`) and is documented as **not** using SPS, `pay.wire.lifecycle.v2`, PPH
v2, gpi data, or HMS APIs. This leaves Wire Center unable to offer milestone tracking, gpi
status, hold-reason detail, or returns notifications, and structurally unable to close those
gaps by polling, because ADR-PAY-019 forbids it (Wire Center's only PPH read is a 60-second
cached, 1-per-60-seconds-throttled user-initiated refresh). The current-state architecture
document for Wire Center lists both CBO-3790 deliverables under "reusable assets":

| Asset | Origin | Reuse notes |
|---|---|---|
| `<cbo-journey-timeline>` component (Aurora DS v4) | CBO-3802 (ACH Payment Tracker) | Rail-agnostic milestone timeline, incl. terminal/error styling |
| Status Projection Service (SPS) | CBO-3815 | Kafka consumer → Postgres read model → `/cbo/sps/v1`; add payment types by config + mapping module |

Closing the wire-tracking gap therefore does not require inventing a new architecture pattern;
it requires: a consumer ACL grant on `pay.wire.lifecycle.v2`, a new SPS mapping module from
PPH v2 `lifecycleState` to CBO wire milestones, and reuse of the existing
`<cbo-journey-timeline>` component on the front end. New ENS event types (for example, wire
network acceptance or gpi beneficiary-credit confirmation) would still need to go through
ENS's roughly 6-week event-onboarding SLA — see
[ENS Notification API & TRS Event Catalog](../interfaces/ens-notification-api-trs-catalog.md)
for that process and for the full list of wire-lifecycle notifications that do not exist yet.
No wire-tracking epic has been scheduled as of the 2026-10-05 backlog snapshot; PPH v1→v2
migration for Wire Center (CBO-4471, 34 points) is itself unscheduled and blocked on
CBO-4473 (CES account-filter mapping for PPH v2 search).

## Ownership and operations

| System | Owning team | Technical owner | Business owner | Support tier |
|---|---|---|---|---|
| CBO Status Projection Service (SYS-CBO-SPS) | CBO Platform & Entitlements | Arjun Mehta | Marcus Chen | T2 |

SPS is owned by the CBO Platform & Entitlements team (engineering manager Nadia Haddad), a
different team from the CBO Wire Center squad (Tom Becker / Lucas Ferreira) that would need to
integrate with it for any future wire-tracking work — meaning wire tracking would be a
cross-team build, not a Wire Center-only change. `<cbo-journey-timeline>` is owned by Aurora
Design System tooling under the CBO Wire Center squad's design lead, Lucas Ferreira.

## Related pages

- [ENS Notification API & TRS Event Catalog](../interfaces/ens-notification-api-trs-catalog.md) — the live `TRS.ACH.STATUS_CHANGED` / `TRS.ACH.RETURN_RECEIVED` events produced by SPS, and the explicit list of wire-lifecycle notifications that do not yet exist.
- [CBO Status Projection Service](../systems/cbo-status-projection-service.md) — system-level detail on the SPS consumer, read model, and API.
