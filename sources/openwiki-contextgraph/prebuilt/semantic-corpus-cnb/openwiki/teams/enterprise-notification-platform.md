---
type: Team
entity_id: enterprise-notification-platform
title: Enterprise Notification Platform
description: Engineering team within Payments & Treasury Technology (PTT) that owns the Enterprise Notification Service (SYS-ENS); led by Director Sanjay Iyer with Melissa Grant (EM) and Paul Henderson (onboarding); runs the 6-week, ~12-engineering-hour ENS event-onboarding SLA for all PTT producer teams.
tags: [team, enterprise-notification-platform, ens, enterprise-notification-service, payments-treasury-technology, system-ownership, event-onboarding, capacity-planning, notifications]
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

## Overview

**Enterprise Notification Platform** is one of seven engineering teams in
Payments & Treasury Technology (PTT) at Crestline National Bank (CNB),
reporting directly to **Gregory Hall** (MD, CIO Payments & Treasury
Technology). It is led by **Sanjay Iyer (Director)**, with **Melissa Grant**
as Engineering Manager and **Paul Henderson** as the named owner of event
onboarding. The team is reachable via Jira project `ENS` and Slack channel
`#ens-onboarding`.
<!-- openwiki: broken internal link [../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L54-L63] heading anchor "L54-L63" does not exist in "../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md". Fix the href or restore the target, then delete this comment. -->
[PTT engineering team directory](../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L54-L63)

Unlike most PTT engineering teams, which own a payment-processing,
screening, or data domain, Enterprise Notification Platform owns a
**horizontal, shared capability** — outbound client notifications across
email, SMS, mobile push (CBO Mobile), and the CBO in-app inbox — that other
PTT producer teams (CBO Wire Center, CBO Status Projection Service, Core
Deposit Platform, and future producers) integrate against rather than
operate themselves. The team does not own payment, account, or case state;
producers remain the system of record for the underlying business event, and
the team's system is a downstream delivery layer only.
[Enterprise Notification Service](../systems/enterprise-notification-service.md)

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: a semicolon inside a label breaks rendering; rephrase the label. -->
```text
graph TD
  GH["Gregory Hall<br/>MD, CIO Payments &amp; Treasury Technology"]
  SI["Sanjay Iyer<br/>Director, Enterprise Notification Platform<br/>Business owner: SYS-ENS"]
  MG["Melissa Grant<br/>EM, Enterprise Notification Service<br/>Technical owner: SYS-ENS<br/>Doc owner: ENS-INT-3.2"]
  PH["Paul Henderson<br/>Owner: ENS Event Onboarding intake"]
  ENS["SYS-ENS<br/>Enterprise Notification Service (T2)"]

  GH --> SI
  SI --> MG
  SI --> PH
  MG -->|technical owner, day-to-day delivery| ENS
  SI -.->|accountable business owner| ENS
```

## System owned: SYS-ENS

| System ID | System | Technical owner | Business owner | Support tier |
|---|---|---|---|---|
| SYS-ENS | [Enterprise Notification Service](../systems/enterprise-notification-service.md) | Melissa Grant | Sanjay Iyer | T2 (business hours + on-call) |

<!-- openwiki: broken internal link [../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L78-L97] heading anchor "L78-L97" does not exist in "../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md". Fix the href or restore the target, then delete this comment. -->
[PTT system ownership register](../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L78-L97)

The PTT system register splits accountability between Melissa Grant as
**technical owner** (day-to-day engineering management of ENS) and Sanjay
Iyer as **business owner** (accountable for scope, capacity commitments, and
roadmap) — the same engineering/business ownership separation pattern used
elsewhere across PTT. ENS is rated **Tier 2** (business hours plus on-call)
rather than the Tier-1 24x7 coverage given to client-facing
payment-processing systems such as CBO Wire Center or PRISM Payments Hub,
reflecting that ENS is a notification-delivery layer rather than a system
that itself blocks a critical payment workflow if degraded.
<!-- openwiki: broken internal link [../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L93-L93] heading anchor "L93-L93" does not exist in "../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md". Fix the href or restore the target, then delete this comment. -->
[PTT system ownership register](../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L93-L93)

The team is also accountable for the published platform capacity and
compliance limits ENS operates under: 300 msgs/s sustained throughput
(1,200 msgs/s burst, with a 120 msgs/s quota carved out for the Treasury/TRS
domain), a 4-second p95 delivery latency target for push and in-app
notifications, SMS gated on a TCPA consent flag with a 160-character
template limit, and masking of account numbers to the last 4 digits with no
Restricted-tier data permitted in any payload or template.
<!-- openwiki: broken internal link [../../sources/estate/ens-int-3.2-enterprise-notification-service-integration-guide.md#L28-L34] heading anchor "L28-L34" does not exist in "../../sources/estate/ens-int-3.2-enterprise-notification-service-integration-guide.md". Fix the href or restore the target, then delete this comment. -->
[ENS-INT-3.2](../../sources/estate/ens-int-3.2-enterprise-notification-service-integration-guide.md#L28-L34)

## Document ownership: ENS-INT-3.2

The team owns and approves [ENS-INT-3.2](../documents/ens-int-3.2.md)
("Enterprise Notification Service - Integration Guide & Treasury Event
Catalog," v3.2, published 2026-07-30) — Melissa Grant is the named document
owner, Sanjay Iyer the named approver. This document is the authoritative
reference other PTT teams use to integrate with ENS: it defines the
event-onboarding process and SLA, the subscription model and its current
entity-level gap, the live Treasury (TRS) wire/ACH event catalog, the public
API surface, and content/compliance rules for notification templates.
<!-- openwiki: broken internal link [../../sources/estate/ens-int-3.2-enterprise-notification-service-integration-guide.md#L15-L22] heading anchor "L15-L22" does not exist in "../../sources/estate/ens-int-3.2-enterprise-notification-service-integration-guide.md". Fix the href or restore the target, then delete this comment. -->
[ENS-INT-3.2](../../sources/estate/ens-int-3.2-enterprise-notification-service-integration-guide.md#L15-L22)

## Event onboarding: process, SLA, and capacity

Registering a new event type with ENS — for any PTT producer, any domain —
is a fixed five-step process the team operates and is sized against a
published **6-week SLA** from complete submission to production:

1. Submit the ServiceNow catalog item **"ENS Event Onboarding"** (catalog
   owner: Paul Henderson).
2. Define the payload schema and recipient-resolution logic (subscription
   filters).
3. Draft templates per channel and submit them to the **Disclosure Review
   Committee (DRC)**, which reviews bi-weekly.
4. ENS configuration and test — approximately **12 ENS engineering hours**
   per event type.
5. Producer integration testing in UAT, followed by production enablement.

<!-- openwiki: broken internal link [../../sources/estate/ens-int-3.2-enterprise-notification-service-integration-guide.md#L35-L47] heading anchor "L35-L47" does not exist in "../../sources/estate/ens-int-3.2-enterprise-notification-service-integration-guide.md". Fix the href or restore the target, then delete this comment. -->
[ENS-INT-3.2](../../sources/estate/ens-int-3.2-enterprise-notification-service-integration-guide.md#L35-L47)

Per the PTT engagement directory, the team's standard planning factor for
cross-team sizing is **~12 ENS engineering hours per new event type**,
routed through the ServiceNow **"ENS Event Onboarding"** catalog item with a
**6-week SLA** — notably a ServiceNow-intake pattern rather than the
Jira-ticket intake most other PTT engineering teams use for cross-team
dependency work. Requests submitted after **2026-11-20** are scheduled after
the year-end change freeze. As of PI 27.1, the directory records the team's
forward capacity note as **"per-entity subscriptions 2027-H1"**, reflecting
that the planned ENS-1120 initiative is the team's major committed body of
work for that period rather than a specific percentage-committed figure.
<!-- openwiki: broken internal link [../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L120-L132] heading anchor "L120-L132" does not exist in "../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md". Fix the href or restore the target, then delete this comment. -->
[Engagement routes and planning factors](../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L120-L132)

Two factors bound this pipeline for any team planning dependent work:

- **DRC cadence is a hard gate.** Because the Disclosure Review Committee
  meets only bi-weekly, a template needing a second review cycle adds
  roughly two weeks beyond the nominal SLA, independent of how quickly ENS
  engineering and the producer otherwise move.
- **Year-end change freeze.** Any event-type request not already in
  onboarding before 2026-11-20 is deferred past the freeze, which is a
  planning constraint for producer teams targeting year-end delivery.

## Subscription model limits and ENS-1120

The team's current subscription model is scoped **per user, per event
type**, with optional `accountId` and amount-threshold filters; it does not
support subscribing to an individual entity (for example, a specific
`paymentId`). Producers that need to reach a specific, pre-resolved
recipient use the documented **"producer-resolved recipients"** workaround —
sending directly to a named user via `POST /ens/v3/notifications` rather
than relying on subscription matching. Closing this gap is tracked as a
separate, planned initiative, **[ENS-1120](../projects/ens-1120-entity-level-subscriptions.md)**
(entity-level subscriptions, target 2027-H1), owned by Melissa Grant, rather
than as a configuration change to the current model.
<!-- openwiki: broken internal link [../../sources/estate/ens-int-3.2-enterprise-notification-service-integration-guide.md#L49-L51] heading anchor "L49-L51" does not exist in "../../sources/estate/ens-int-3.2-enterprise-notification-service-integration-guide.md". Fix the href or restore the target, then delete this comment. -->
[ENS-INT-3.2](../../sources/estate/ens-int-3.2-enterprise-notification-service-integration-guide.md#L49-L51)

## Engagement route and governance

Cross-team dependency work is raised via the Jira project `ENS` and
discussed in Slack channel `#ens-onboarding`; new event-type registration
specifically goes through the ServiceNow "ENS Event Onboarding" catalog item
rather than Jira. Any onboarding that includes new or changed client-facing
templates must additionally clear the bi-weekly **Disclosure Review
Committee (DRC)**, chaired per the Legal - Treasury & Payments partner
function (Patricia Moore), with a 5-business-day submission lead time; and
templates covering financial-crimes-related states must use FCC-approved
copy per POL-FCC-014 Appendix B before DRC will approve them.
<!-- openwiki: broken internal link [../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L100-L118] heading anchor "L100-L118" does not exist in "../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md". Fix the href or restore the target, then delete this comment. -->
[Governance forums](../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L100-L118)

New client-facing integrations that touch payment systems more broadly may
also require review at the monthly **Payments Architecture Review Board
(ARB)** (2nd Tuesday, 10 business days' submission lead time), since ARB
governs new client-facing integrations to payment systems bank-wide,
although the ENS event-onboarding pipeline itself is the primary gate for
notification-specific changes.
<!-- openwiki: broken internal link [../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L98-L104] heading anchor "L98-L104" does not exist in "../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md". Fix the href or restore the target, then delete this comment. -->
[Governance forums](../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L98-L104)

## Escalation

Dependency conflicts that cannot be resolved between Sanjay Iyer's team and
a peer engineering manager escalate first to the respective Directors, then,
if still unresolved, to the PTT Leadership Team, which meets weekly on
Mondays. Compliance or policy interpretation questions (for example,
disputes over FCC-approved template copy) route instead to FCC Policy &
Advisory (Jordan Ellis) or the Privacy Office (Ethan Brooks) and are not
decided within the engineering escalation chain.
<!-- openwiki: broken internal link [../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L148-L150] heading anchor "L148-L150" does not exist in "../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md". Fix the href or restore the target, then delete this comment. -->
[Escalation](../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L148-L150)

## Relationships

- **[Sanjay Iyer](../people/sanjay-iyer.md)** — Director; accountable
  business owner of `SYS-ENS` and named approver of ENS-INT-3.2.
- **[Melissa Grant](../people/melissa-grant.md)** — Engineering Manager;
  technical owner of `SYS-ENS`, document owner of ENS-INT-3.2, and named
  owner of the ENS-1120 entity-level-subscriptions initiative.
- **Paul Henderson** — owns the "ENS Event Onboarding" ServiceNow catalog
  item, the mandatory first step of event onboarding for every producer
  team.
- **Producer teams** — the CBO Wire Center squad, CBO Status Projection
  Service, and Core Deposit Platform are the current live producers
  (`TRS.WIRE.*`, `TRS.ACH.*`); any PTT team needing a new notification type
  must engage this team through the onboarding process and SLA described
  above.
- **Disclosure Review Committee (DRC)** — reviews and approves client-facing
  notification templates drafted during onboarding step 3.

## Related pages

- [Enterprise Notification Service](../systems/enterprise-notification-service.md) — the system this team owns; full architecture, API surface, and TRS catalog gaps.
- [Sanjay Iyer](../people/sanjay-iyer.md) and [Melissa Grant](../people/melissa-grant.md) — team leadership.
- [ENS-INT-3.2](../documents/ens-int-3.2.md) — the integration guide and event catalog the team owns.
- [ENS-1120: Entity-Level Subscriptions](../projects/ens-1120-entity-level-subscriptions.md) — the team's major planned (2027-H1) initiative.
- [Payments & Treasury Technology](../organizations/payments-treasury-technology.md) — the parent organization.
