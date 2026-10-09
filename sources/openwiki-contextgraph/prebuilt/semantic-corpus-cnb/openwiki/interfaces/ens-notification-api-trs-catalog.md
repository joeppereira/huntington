---
type: Interface
entity_id: EP-ENS-01..03
title: "ENS Notification API & TRS Event Catalog"
description: "Describes the Enterprise Notification Service (ENS) v3 notification/subscription APIs (EP-ENS-01..03) and the current Treasury (TRS) wire/ACH event catalog, including the explicit list of wire-lifecycle notifications (network acceptance, gpi ACCC, returns, held-wire client action) that do not yet exist."
tags: [ens, notifications, trs, wire, ach, event-catalog, api, treasury, gpi]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-550c0e3f038aab7950cab477
    resource: repo://sources/estate/cbo-arch-wc-4.1-wire-center-current-state-architecture.md
  - id: openwiki-source-d637e82ba742e8a4b8f0c799
    resource: repo://sources/estate/ens-int-3.2-enterprise-notification-service-integration-guide.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

The Enterprise Notification Service (ENS) is the shared platform that sends transactional
notifications across email, SMS, mobile push (CBO Mobile) and the CBO in-app inbox. Producer
systems emit a registered **event type**; ENS resolves recipients from **subscriptions**,
renders an approved **template**, and delivers the message per the user's channel
preferences. Within the Treasury (TRS) domain, the only current producers of wire/ACH
notifications are the CBO Wire Center backend (`cbo-wire-bff`), the CBO Status Projection
Service (SPS), and CDP (incoming wire posting).

ENS enforces domain-level throughput quotas (TRS domain: 120 msgs/s of a 300 msgs/s
sustained / 1,200 msgs/s burst platform capacity), a 4 s p95 delivery latency target for
push/in-app, account-number masking to last 4 digits, and a prohibition on Restricted data in
any payload or template. SMS delivery additionally requires a TCPA consent flag on the CBO
user profile and is limited to 160-character templates.

## Notification and subscription APIs (EP-ENS-01..03)

| ID | Endpoint | Purpose |
|---|---|---|
| EP-ENS-01 | `POST /ens/v3/notifications` | Send an event (must be a registered event type with an approved template) |
| EP-ENS-02 | `POST /ens/v3/subscriptions` | Create a subscription (`eventType` + `accountId` filter) |
| EP-ENS-03 | `GET /ens/v3/event-types?domain=TRS` | Read the TRS event-type catalog |

`cbo-wire-bff` is the only Wire Center integration that calls ENS, and it does so
synchronously over `POST /ens/v3/notifications` (EP-ENS-01) to produce the `TRS.WIRE.*`
events described below.

### Subscription model

Subscriptions are created per user for an **event type**, with optional filters on
`accountId` and amount thresholds. ENS does **not** support subscribing to an individual
entity (for example, one specific `paymentId`); entity-level subscriptions are planned under
[ENS-1120](../projects/ens-1120-entity-level-subscriptions.md) (targeted 2027-H1). Until that
ships, producers that need to notify a specific, pre-resolved recipient for a transactional
event send directly to a named user — the "producer-resolved recipients" pattern — rather
than relying on ENS subscription matching.

### Onboarding a new event type

Registering a new TRS event type is a multi-step, multi-team process with a published
**6-week SLA** from complete submission to production, including bi-weekly Disclosure Review
Committee (DRC) review of templates:

1. Submit the ServiceNow catalog item "ENS Event Onboarding."
2. Define the payload schema and recipient-resolution (subscription filter) logic.
3. Draft templates per channel and submit them to the DRC.
4. ENS engineering configures and tests the new event type (~12 engineering hours).
5. Producer performs integration testing in UAT, then production enablement.

Requests submitted after 2026-11-20 are scheduled after the year-end change freeze, which is
a practical constraint on closing any of the catalog gaps below before year end.

### Content rules

- Templates covering financial-crimes-related states must use FCC-approved copy; see
  [POL-FCC-014](../policies/pol-fcc-014.md), Appendix B.
- Status wording in templates must match the producer's approved status terminology (for
  Wire Center, the CBO client-facing labels, not raw PPH v1 status values).
- Templates and links must not expose transaction data outside an authenticated session.

## TRS event catalog (wire and ACH)

The table below is the current Treasury event catalog as published in ENS-INT-3.2 §4. It is
the authoritative list of every wire/ACH event type ENS can deliver today.

| Event type | Producer | Trigger | Template (subject line) | Status |
|---|---|---|---|---|
| `TRS.WIRE.APPROVAL_REQUIRED` | CBO | Wire awaiting approver | TPL-WIRE-APR-01 "Wire awaiting your approval" | Live |
| `TRS.WIRE.RELEASED` | CBO | PPH v1 status → `PROCESSED` | TPL-WIRE-REL-02 "Wire completed: {amount} to {beneficiary}" | Live |
| `TRS.WIRE.REJECTED` | CBO | PPH v1 status → `REJECTED` | TPL-WIRE-REJ-01 "Wire rejected" | Live |
| `TRS.WIRE.INCOMING_POSTED` | CDP | Incoming wire posted to DDA | TPL-WIRE-IN-03 "Incoming wire received" | Live |
| `TRS.ACH.STATUS_CHANGED` | CBO SPS | ACH lifecycle milestone | TPL-ACH-STS-01 | Live (2025-11) |
| `TRS.ACH.RETURN_RECEIVED` | CBO SPS | ACH return | TPL-ACH-RET-01 | Live (2025-11) |

### Explicit catalog gaps

ENS-INT-3.2 §4 states this gap list verbatim: **no event types are registered for wire
network acceptance, beneficiary credit (gpi ACCC), wire returns, gpi milestones, or client
action required on held wires.**

These gaps are not independent platform limitations — they trace directly to Wire Center's
current-state architecture (CBO-ARCH-WC-4.1):

- Wire Center consumes only **PPH v1** (`EP-PPH-01`/`02`/`03`), which exposes a coarse status
  set (`RECEIVED`, `PENDING`, `HELD`, `PROCESSED`, `REJECTED`, `CANCELLED`, `RETURNED`) and no
  UETR, OMAD, or gpi milestone data. There is no `RETURNED`-triggered notification event
  today even though PPH v1 surfaces a `RETURNED` status, and there is no event for
  network-acceptance milestones because PPH v1 does not expose one.
- gpi status for international wires is visible only to Payment Operations in the
  Investigations Workbench; it is not wired into any CBO or ENS flow, which is why no
  `TRS.WIRE.*` event exists for gpi ACCC (beneficiary credit confirmation) or other gpi
  milestones.
- Held wires display only the generic client-facing label "Pending Review" with static text
  ("This wire is being reviewed."); Wire Center has no hold-reason data and no client-action
  workflow, so there is no corresponding "action required on held wire" notification to send.
- `pay.wire.lifecycle.v2` and the Status Projection Service's wire support (SPS today is
  configured for ACH only) are both unused by Wire Center, so neither can yet drive new
  event-driven wire notifications.

Per ADR-PAY-019, Wire Center is prohibited from polling PPH for status (only user-initiated,
throttled refresh is allowed), so closing any of these gaps requires new event-driven
plumbing — either a PPH v2 migration, a wire-capable SPS mapping module and `pay.wire.lifecycle.v2`
consumer ACL, or both — rather than a client-side polling workaround.

## Wire Center as an ENS producer

Wire Center (`cbo-wire-bff`) currently produces exactly three of the six live TRS event
types, all driven off PPH v1 status transitions:

| Event type | Trigger | Template | Channels |
|---|---|---|---|
| `TRS.WIRE.APPROVAL_REQUIRED` | Wire awaiting approver | TPL-WIRE-APR-01 | email, push, in-app |
| `TRS.WIRE.RELEASED` | PPH v1 status transitions to `PROCESSED` | TPL-WIRE-REL-02 | email, push, in-app, SMS (opt-in) |
| `TRS.WIRE.REJECTED` | PPH v1 status `REJECTED` | TPL-WIRE-REJ-01 | email, push, in-app |

`TRS.WIRE.INCOMING_POSTED` is produced by CDP, not Wire Center, and the two `TRS.ACH.*`
events are produced by CBO SPS, not Wire Center — Wire Center has no ACH involvement.

```mermaid
sequenceDiagram
    participant Wire as cbo-wire-bff
    participant PPH as PPH v1
    participant ENS as ENS v3
    participant User as CBO user

    Wire->>PPH: POST /pph/v1/wires (submit)
    PPH-->>Wire: pphId
    Wire->>ENS: POST /ens/v3/notifications (TRS.WIRE.APPROVAL_REQUIRED)
    ENS-->>User: email / push / in-app

    Note over Wire,PPH: User-initiated refresh only; no status polling (ADR-PAY-019)
    Wire->>PPH: GET /pph/v1/wires/{ref}/status
    PPH-->>Wire: status = PROCESSED or REJECTED
    Wire->>ENS: POST /ens/v3/notifications (TRS.WIRE.RELEASED or TRS.WIRE.REJECTED)
    ENS-->>User: email / push / in-app / SMS
```

Notification flow from Wire Center submission through PPH v1 status refresh to ENS delivery; no event-driven path exists yet for network acceptance, gpi ACCC, returns, or held-wire client action.

Because every Wire Center notification is anchored to a PPH v1 status value, and PPH v1 has
no field for network acceptance, gpi milestones, or hold reasons, Wire Center cannot emit the
missing event types without either a data source change (PPH v2, gpi feed) or a new
consumer path (SPS wire mapping + `pay.wire.lifecycle.v2`). This is the same constraint noted
in the gap analysis above, viewed from the producer side.

## Related pages

- [Enterprise Notification Service](../systems/enterprise-notification-service.md) — system-level ENS architecture and operations.
- [ENS-1120: Entity-Level Subscriptions](../projects/ens-1120-entity-level-subscriptions.md) — planned subscription model work referenced above.
- [POL-FCC-014](../policies/pol-fcc-014.md) — FCC-approved copy requirements for financial-crimes-related templates.
