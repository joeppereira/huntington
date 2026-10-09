---
type: Person
entity_id: melissa-grant
title: Melissa Grant
description: Engineering Manager for the Enterprise Notification Service (ENS) within Crestline National Bank's Enterprise Notification Platform team; document owner of ENS-INT-3.2 and owner of the ENS-1120 entity-level subscriptions initiative.
tags: [people, enterprise-notification-service, ens, enterprise-notification-platform, engineering-manager, system-ownership, subscriptions]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-49303e801f124d97df9c3ea3
    resource: repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md
  - id: openwiki-source-d637e82ba742e8a4b8f0c799
    resource: repo://sources/estate/ens-int-3.2-enterprise-notification-service-integration-guide.md
  - id: openwiki-source-4452149a3b4502b4c763a559
    resource: repo://sources/estate/jira-export-wt-discovery-2026-10-05.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Summary

Melissa Grant is the Engineering Manager (EM) for the **Enterprise Notification
Service (ENS)**, Crestline National Bank's shared platform for sending
transactional notifications across email, SMS, mobile push (CBO Mobile), and
the CBO in-app inbox. She sits within the Enterprise Notification Platform
team, led by Director Sanjay Iyer, alongside Paul Henderson, who owns the
ENS event-onboarding intake process. Melissa is the named **document owner**
of [ENS-INT-3.2](../documents/ens-int-3.2.md) (the ENS Integration Guide &
Treasury Event Catalog) and the named **owner of ENS-1120**, the planned
initiative to add entity-level subscriptions to ENS.

## Roles and responsibilities

| Role | Scope | Source |
|---|---|---|
| Engineering Manager, Enterprise Notification Service | Reports into the Enterprise Notification Platform group under Director Sanjay Iyer; team contacts also include Paul Henderson (event onboarding) | PTT organization directory |
| Technical owner, system `SYS-ENS` | Enterprise Notification Service is registered as a Tier-2 (business hours + on-call) system; Melissa is its technical owner, with Sanjay Iyer as the accountable business owner | PTT system ownership register |
| Document owner, ENS-INT-3.2 | Owns the published Enterprise Notification Service Integration Guide & Treasury Event Catalog (v3.2), approved by Sanjay Iyer | ENS-INT-3.2 |
| Initiative owner, ENS-1120 | Named owner of the "Entity-level subscriptions (subscribe to a specific `paymentId` / `caseId`)" initiative, status Planned, target 2027-H1 | Jira export WT-discovery |

As EM for ENS, Melissa's team operates the notification platform that other
Payments & Treasury Technology (PTT) teams integrate against — most visibly
CBO Wire Center, which produces the `TRS.WIRE.*` and `TRS.ACH.*` event types
documented in ENS-INT-3.2 — rather than owning any producer-side business
logic herself.

## Document ownership: ENS-INT-3.2

Melissa owns [ENS-INT-3.2](../documents/ens-int-3.2.md), the integration guide
that governs how producer systems onboard new event types and templates with
ENS, documents the current Treasury (TRS) event catalog, and sets the ENS
subscription model, API surface, and content/compliance rules. Key points she
is accountable for as document owner:

- **Subscription model limits.** ENS subscriptions today are scoped per user
  to an event type, with optional `accountId` and amount-threshold filters;
  ENS does not support subscribing to an individual entity (e.g. a specific
  `paymentId`). This gap is called out explicitly in the guide as the reason
  entity-level subscriptions are tracked as a separate future initiative
  (ENS-1120) rather than a configuration change.
- **Onboarding SLA.** New event types follow a five-step process — ServiceNow
  catalog submission, payload/recipient-filter definition, Disclosure Review
  Committee (DRC) template approval, ENS configuration and testing (~12
  engineering hours), and producer UAT/production enablement — against a
  **6-week SLA**, with requests submitted after 2026-11-20 deferred past the
  year-end change freeze.
- **Treasury event catalog.** The guide is the current source of truth for
  which `TRS.WIRE.*` and `TRS.ACH.*` events are live, and explicitly notes
  that no event types yet exist for wire network acceptance, gpi beneficiary
  credit (`ACCC`), wire returns, gpi milestones, or client-action-required
  states on held wires.
- **Content/compliance rules.** Templates covering financial-crimes-related
  states must use FCC-approved copy from POL-FCC-014 Appendix B, and ENS
  content must follow producer-approved status terminology and avoid exposing
  transaction data outside authenticated sessions.

## Initiative ownership: ENS-1120 (entity-level subscriptions)

Melissa is the named owner of **ENS-1120**, a Planned initiative (target
2027-H1) to let a user subscribe to updates about a specific entity, such as
a single `paymentId` or `caseId`, rather than only to an event type with
coarse `accountId`/amount filters. See
[ENS-1120: Entity-Level Subscriptions](../projects/ens-1120-entity-level-subscriptions.md)
for the initiative-level writeup. ENS-1120 is cross-referenced from
ENS-INT-3.2 as the planned resolution to the subscription model's current
entity-level gap, and is listed there as a related document. Until ENS-1120
ships, producers needing to notify a specific, dynamically-determined
audience about updates to a single entity must use the documented
workaround — "producer-resolved recipients," where the producer system
itself maintains the recipient list and sends directly to named users rather
than relying on an ENS subscription.

## Relationships

- **Sanjay Iyer** (Director, Enterprise Notification Platform) — Melissa's
  manager; approver of ENS-INT-3.2 and accountable business owner of
  `SYS-ENS`.
- **Paul Henderson** — owns the ENS event-onboarding intake process
  (ServiceNow catalog item "ENS Event Onboarding") that producer teams submit
  through as the first step of onboarding a new event type under
  ENS-INT-3.2.
- **Producer teams** — teams such as the CBO Wire Center squad (Tom Becker,
  EM) integrate with ENS as event producers, sending `TRS.WIRE.*` and
  `TRS.ACH.*` events through the ENS APIs documented in ENS-INT-3.2; these
  teams depend on Melissa's organization for onboarding new event types and
  for any future entity-level subscription capability delivered by ENS-1120.

## See also

- [Enterprise Notification Service](../systems/enterprise-notification-service.md)
  — system-level page for ENS.
- [ENS-1120: Entity-Level Subscriptions](../projects/ens-1120-entity-level-subscriptions.md)
  — the initiative Melissa owns.
- [ENS-INT-3.2](../documents/ens-int-3.2.md) — the integration guide Melissa
  owns as document owner.
- [Payments & Treasury Technology](../organizations/payments-treasury-technology.md)
  — organization-level page covering the Enterprise Notification Platform
  team and PTT system ownership register.
