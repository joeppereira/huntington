---
type: Person
entity_id: sanjay-iyer
title: Sanjay Iyer
description: Director of the Enterprise Notification Platform team within Payments & Treasury Technology; accountable business owner of the Enterprise Notification Service (SYS-ENS) and approver of the ENS-INT-3.2 integration guide.
tags: [sanjay-iyer, enterprise-notification-platform, enterprise-notification-service, ens, director, system-ownership, ens-int-3.2, payments-treasury-technology]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-49303e801f124d97df9c3ea3
    resource: repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md
  - id: openwiki-source-d637e82ba742e8a4b8f0c799
    resource: repo://sources/estate/ens-int-3.2-enterprise-notification-service-integration-guide.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Summary

Sanjay Iyer is the **Director of the Enterprise Notification Platform**
team within Payments & Treasury Technology (PTT) at Crestline National
Bank. He leads the group that builds and runs the **Enterprise
Notification Service (ENS)** — the shared platform that delivers
transactional notifications across email, SMS, mobile push (CBO Mobile),
and the CBO in-app inbox. In the PTT system ownership register Sanjay is
recorded as the accountable **business owner** of `SYS-ENS`, and he is the
named **approver** of [ENS-INT-3.2](../documents/ens-int-3.2.md), the
published Enterprise Notification Service Integration Guide & Treasury
Event Catalog.

## Roles and responsibilities

| Role | Scope | Source |
|---|---|---|
| Director, Enterprise Notification Platform | Leads the ENS engineering team, reporting directly into Gregory Hall (MD, CIO Payments & Treasury Technology), alongside six other PTT engineering teams | PTT organization directory |
| Business owner, system `SYS-ENS` | Accountable business owner of record for the Enterprise Notification Service, a Tier-2 system (business hours + on-call support) | PTT system ownership register |
| Approver, ENS-INT-3.2 | Signs off on the published Enterprise Notification Service Integration Guide & Treasury Event Catalog (v3.2), the authoritative reference for event onboarding, the subscription model, the Treasury (TRS) event catalog, APIs, and content rules | ENS-INT-3.2 |

Sanjay's organization is one of seven engineering teams reporting to
Gregory Hall across PTT (alongside CBO Wire Center, CBO Platform &
Entitlements, Payments Hub Engineering, Payment Networks Engineering,
Global Transaction Services Integration, Financial Crimes Technology, and
Treasury Data & Analytics). Unlike most of those teams, which own
payment-processing or compliance systems, the Enterprise Notification
Platform owns a horizontal, shared capability — outbound client
notifications — that other PTT producer teams integrate against rather
than operate themselves.

## Team: Enterprise Notification Platform

Sanjay's direct reports/key contacts, per the PTT organization directory,
are:

- **Melissa Grant** — Engineering Manager, Enterprise Notification
  Service; document owner of ENS-INT-3.2 and named owner of the ENS-1120
  entity-level-subscriptions initiative.
- **Paul Henderson** — owns onboarding; specifically the ServiceNow
  catalog item "ENS Event Onboarding," the mandatory first step for any
  producer registering a new event type with ENS.

The team is reachable via the Jira project `ENS` and the Slack channel
`#ens-onboarding`. See
[Enterprise Notification Platform](../teams/enterprise-notification-platform.md)
for the team-level writeup.

## Accountable owner of SYS-ENS

The PTT system ownership register lists the Enterprise Notification
Service (`SYS-ENS`) with Melissa Grant as **technical owner** and Sanjay
Iyer as **business owner**, at support **Tier 2** (business hours plus
on-call, as opposed to the Tier-1 24x7 coverage given to client-facing
payment-processing systems such as CBO Wire Center or PRISM Payments
Hub). As business owner, Sanjay is the accountable leader for ENS's
scope, capacity commitments, and roadmap, distinct from Melissa Grant's
day-to-day engineering-management accountability for the service.

ENS's published capabilities, which Sanjay's organization is accountable
for delivering, include:

- Sustained throughput of 300 msgs/s (1,200 msgs/s burst), with a 120
  msgs/s quota carved out specifically for the Treasury (TRS) domain.
- A 4-second p95 delivery latency target for push and in-app
  notifications.
- SMS delivery gated on a TCPA consent flag from the CBO user profile,
  with a 160-character template limit.
- Masking of account numbers to the last 4 digits and a prohibition on
  Restricted data in any notification payload or template.

## Approver of ENS-INT-3.2

Sanjay is the named approver of
[ENS-INT-3.2](../documents/ens-int-3.2.md) ("Enterprise Notification
Service - Integration Guide & Treasury Event Catalog," v3.2, published
2026-07-30, owned by Melissa Grant). As approver, he is accountable for
the content producer teams rely on to integrate with ENS, including:

- **Event onboarding.** The five-step process — ServiceNow catalog
  submission (via Paul Henderson's intake item), payload/recipient-filter
  definition, Disclosure Review Committee (DRC) template approval, ENS
  configuration/testing (~12 engineering hours), and producer UAT/
  production enablement — against a published **6-week SLA**. Requests
  submitted after 2026-11-20 are deferred past the year-end change
  freeze.
- **The subscription model and its current gap.** Subscriptions are
  created per user for an event type, with optional `accountId` and
  amount-threshold filters; ENS does not support subscribing to an
  individual entity (e.g., a specific `paymentId`). Entity-level
  subscriptions are tracked as a separate, planned initiative
  (**ENS-1120**, targeted 2027-H1) rather than addressed as a
  configuration change to the current guide.
- **The Treasury (TRS) event catalog.** Live event types
  (`TRS.WIRE.APPROVAL_REQUIRED`, `TRS.WIRE.RELEASED`,
  `TRS.WIRE.REJECTED`, `TRS.WIRE.INCOMING_POSTED`,
  `TRS.ACH.STATUS_CHANGED`, `TRS.ACH.RETURN_RECEIVED`), produced by CBO,
  CBO SPS, and CDP. The guide explicitly notes no event types yet exist
  for wire network acceptance, gpi beneficiary credit (`ACCC`), wire
  returns, gpi milestones, or client-action-required states on held
  wires — a gap his organization is accountable for closing via the
  onboarding process it governs.
- **The public API surface** (`POST /ens/v3/notifications`,
  `POST /ens/v3/subscriptions`, `GET /ens/v3/event-types?domain=TRS`) and
  **content rules**: financial-crimes-related templates must use
  FCC-approved copy from POL-FCC-014 Appendix B, status wording must
  follow the producing system's approved terminology, and no links may
  expose transaction data outside authenticated sessions.

See [ENS Notification API & TRS Event Catalog](../interfaces/ens-notification-api-trs-catalog.md)
for the interface-level detail behind this document.

## Engagement and planning factors

The PTT engagement directory records a standard planning factor for work
routed to Sanjay's team: **~12 ENS engineering hours per new event
type**, requested through the ServiceNow "ENS Event Onboarding" catalog
item with a **6-week SLA**. As of PI 27.1, the directory notes the team's
capacity context as "per-entity subscriptions 2027-H1," reflecting that
ENS-1120 is the team's major forward-looking commitment. Any producer
team planning to add a new notification type should size that work using
this factor and submit through the onboarding catalog item rather than
through Sanjay's team's Jira project directly.

## Relationships

- **Gregory Hall** (MD, CIO Payments & Treasury Technology) — Sanjay's
  manager; Sanjay's team is one of seven PTT engineering teams reporting
  to Gregory Hall.
- **Melissa Grant** — Engineering Manager, Enterprise Notification
  Service, reporting to Sanjay; document owner of ENS-INT-3.2 and
  technical owner of `SYS-ENS`.
- **Paul Henderson** — owns the ENS event-onboarding intake process on
  Sanjay's team.
- **Producer teams** (CBO Wire Center squad, CBO Platform &
  Entitlements/SPS, CDP, and future producers) — integrate with ENS as
  event producers and depend on Sanjay's team's onboarding SLA and
  capacity for registering new event types.
- **Disclosure Review Committee (DRC)** — reviews and approves
  client-facing notification templates as part of the onboarding flow
  Sanjay's organization operates.

## See also

- [ENS-INT-3.2: Enterprise Notification Service Integration Guide & Treasury Event Catalog](../documents/ens-int-3.2.md)
- [ENS Notification API & TRS Event Catalog](../interfaces/ens-notification-api-trs-catalog.md)
- [Payments & Treasury Technology](../organizations/payments-treasury-technology.md)
- [Melissa Grant](melissa-grant.md)
- [Paul Henderson](paul-henderson.md)
