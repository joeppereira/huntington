---
type: Document
entity_id: ENS-INT-3.2
title: "ENS-INT-3.2: Enterprise Notification Service Integration Guide & Treasury Event Catalog"
description: Metadata and scope record for the published integration guide covering how producers register event types and templates with the Enterprise Notification Service (ENS), the subscription model, the Treasury (TRS) event catalog, and content/compliance rules for notifications.
tags: [ens, enterprise-notification-service, integration-document, treasury, notifications, payments, governance, subscriptions]
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
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Summary

**ENS-INT-3.2** ("Enterprise Notification Service - Integration Guide & Treasury Event Catalog") is
the published reference for integrating with the **Enterprise Notification Service (ENS)**, Crestline
National Bank's shared platform for sending transactional notifications across email, SMS, mobile
push (CBO Mobile), and the CBO in-app inbox. It documents how producer systems onboard new event
types, how ENS's subscription model resolves recipients, the current Treasury (TRS) wire/ACH event
catalog, the public APIs, and content/compliance rules for templates. See
[Enterprise Notification Service](../systems/enterprise-notification-service.md) for the system-level
writeup derived from this document.

## Document metadata

| Field | Value |
|---|---|
| Document ID | ENS-INT-3.2 |
| Version / Status | 3.2 / Published |
| Document owner | Melissa Grant, EM — Enterprise Notification Service |
| Approver(s) | Sanjay Iyer (Director, Enterprise Notification Platform) |
| Effective / Last reviewed | Published 2026-07-30 |
| Classification | INTERNAL - CONFIDENTIAL |
| Related documents | CBO-ARCH-WC-4.1; POL-FCC-014; ENS-1120 |

The document carries an **INTERNAL - CONFIDENTIAL** classification and is marked "uncontrolled when
printed," meaning printed or exported copies are not guaranteed to reflect the current approved
revision. Each page footer repeats the document ID, version, and classification banner, consistent
with the Payments & Treasury Technology documentation template used for related architecture and
integration records (e.g. CBO-ARCH-WC-4.1).

## Ownership and approval chain

- **Owner**: Melissa Grant, Engineering Manager for the Enterprise Notification Service, within the
  Enterprise Notification Platform group led by Sanjay Iyer (Director). Paul Henderson owns the
  event-onboarding intake process specifically.
- **Approver**: Sanjay Iyer (Director, Enterprise Notification Platform) signs off on the integration
  guide's content.
- **System-of-record status**: the Enterprise Notification Platform is tracked as system `SYS-ENS`
  (tier T2) in the CNB system ownership directory, with Melissa Grant as engineering owner and Sanjay
  Iyer as director-level accountable owner.

## Related documents

ENS-INT-3.2 cross-references the following documents, which should be treated as its authoritative
dependencies for related policy and roadmap items:

| Related document | Relevance to this document |
|---|---|
| CBO-ARCH-WC-4.1 | Current-state architecture for CBO Wire Center, a consumer of ENS that produces `TRS.WIRE.*` events via this guide's APIs |
| POL-FCC-014 | Financial-crimes compliance policy; its Appendix B supplies FCC-approved copy that financial-crimes-related notification templates must use |
| ENS-1120 | Planned initiative (2027-H1) to add entity-level subscriptions (e.g. subscribing to a specific `paymentId` or `caseId`), called out in this guide as a current subscription-model gap |

## Scope: what this document covers

ENS-INT-3.2 documents the ENS producer/integration surface as it exists today, organized into the
following sections:

1. **Overview** — ENS's role delivering transactional notifications across email, SMS, mobile push,
   and the CBO in-app inbox, resolving recipients from subscriptions and rendering approved templates
   per user channel preference; a capability table giving throughput (300 msg/s sustained, 1,200 msg/s
   burst, with a 120 msg/s quota specifically for the Treasury domain), p95 delivery latency for
   push/in-app (4s), SMS consent/length constraints (TCPA consent flag required; 160-character
   templates), and masking rules (account numbers masked to last 4; no Restricted data in payloads or
   templates).
2. **Onboarding a new event type** — the five-step process from ServiceNow catalog submission through
   Disclosure Review Committee (DRC) template approval, ENS configuration/testing, and producer UAT to
   production enablement, with an end-to-end **6-week SLA** and a year-end change-freeze cutoff for
   requests submitted after 2026-11-20.
3. **Subscription model** — per-user subscriptions scoped to an event type with optional `accountId`
   and amount-threshold filters; the explicit limitation that ENS does not support subscribing to an
   individual entity (e.g. a specific `paymentId`), with entity-level subscriptions tracked as a future
   capability under ENS-1120 (2027-H1); and the "producer-resolved recipients" pattern, where a
   producer sends directly to a named user because it maintains its own recipient list.
4. **Treasury (TRS) event catalog** — the registered wire and ACH event types, their producing
   systems, triggers, and template IDs/subject lines.
5. **APIs** — the three public ENS endpoints producers and subscribers integrate against.
6. **Content rules** — compliance and UX constraints templates must satisfy.

## Treasury (TRS) event catalog

| Event type | Producer | Trigger | Template (subject line) | Status |
|---|---|---|---|---|
| `TRS.WIRE.APPROVAL_REQUIRED` | CBO | Wire awaiting approver | TPL-WIRE-APR-01 "Wire awaiting your approval" | Live |
| `TRS.WIRE.RELEASED` | CBO | PPH v1 status → `PROCESSED` | TPL-WIRE-REL-02 "Wire completed: {amount} to {beneficiary}" | Live |
| `TRS.WIRE.REJECTED` | CBO | PPH v1 status → `REJECTED` | TPL-WIRE-REJ-01 "Wire rejected" | Live |
| `TRS.WIRE.INCOMING_POSTED` | CDP | Incoming wire posted to DDA | TPL-WIRE-IN-03 "Incoming wire received" | Live |
| `TRS.ACH.STATUS_CHANGED` | CBO SPS | ACH lifecycle milestone | TPL-ACH-STS-01 | Live (2025-11) |
| `TRS.ACH.RETURN_RECEIVED` | CBO SPS | ACH return | TPL-ACH-RET-01 | Live (2025-11) |

The wire events are produced by CBO (via the `cbo-wire-bff` backend-for-frontend, per
CBO-ARCH-WC-4.1), using PPH v1 wire status transitions as triggers for `RELEASED` and `REJECTED`; the
ACH events are produced by the CBO Status Projection Service (SPS). The catalog explicitly notes a
coverage gap: **no event types are registered** for wire network acceptance, beneficiary credit
(gpi `ACCC`), wire returns, gpi milestones, or client-action-required states on held wires — i.e. the
international/gpi tracking data available upstream does not yet flow through ENS as client-facing
notifications.

## APIs

| ID | Endpoint | Purpose |
|---|---|---|
| EP-ENS-01 | `POST /ens/v3/notifications` | Send an event (must use a registered event type and an approved template) |
| EP-ENS-02 | `POST /ens/v3/subscriptions` | Create a subscription (`eventType` + `accountId` filter) |
| EP-ENS-03 | `GET /ens/v3/event-types?domain=TRS` | Retrieve the event-type catalog for a domain |

Per CBO-ARCH-WC-4.1, CBO integrates with ENS through a reusable "ENS producer library" shipped in
`cbo-commons 3.x`, which wraps templated sends and masking helpers over these APIs rather than having
each producer call the endpoints directly.

## Onboarding workflow and SLA

```
1. Submit ServiceNow catalog item "ENS Event Onboarding" (owner: Paul Henderson)
2. Define payload schema and recipient resolution (subscription filters)
3. Draft templates per channel -> submit to Disclosure Review Committee (DRC, bi-weekly)
4. ENS configuration and test (~12 ENS engineering hours per event type)
5. Producer integration testing in UAT -> production enablement
```

The guide commits to a **6-week SLA** from complete submission to production, inclusive of DRC
review. Requests submitted after **2026-11-20** are deferred past the year-end change freeze, which
is a scheduling constraint producers must account for when planning new-event-type launches near
year end.

## Content and compliance rules

- Templates covering financial-crimes-related states must use FCC-approved copy, per **POL-FCC-014
  Appendix B** — this routes certain templates through compliance review in addition to the DRC.
- Status wording in templates must follow the producing system's own approved status terminology
  (e.g. CBO's client-facing wire status labels), rather than ENS inventing its own phrasing.
- Templates and links must not expose transaction data outside of authenticated sessions — ENS
  notifications (email/SMS) are not permitted to carry direct links to unauthenticated detail pages.
- Masking rules from the overview section (account numbers to last 4, no Restricted data in payloads
  or templates) apply uniformly across all channels, including SMS and push, where payload size and
  exposure risk are higher.

## Why this document exists

ENS-INT-3.2 functions as the authoritative producer-facing contract for any team building or
extending notifications on top of ENS, and as the single current source for "what Treasury
notifications exist today." Two points in the document function as binding constraints for future
integration work:

- **No entity-level subscriptions today.** Any feature requiring a user to subscribe to updates about
  a single payment, case, or similar entity cannot be built on today's subscription model; it depends
  on ENS-1120, which is only planned for 2027-H1. Producer-resolved recipients are the documented
  workaround where the producer itself tracks the audience.
- **TRS catalog gaps are explicit, not implicit.** The absence of registered events for gpi
  milestones, beneficiary credit, wire returns, and held-wire client actions is called out directly,
  making it clear that closing these gaps requires new ENS event-type onboarding (with its 6-week SLA
  and DRC review) rather than a configuration change to an existing event.

## Relationship to other wiki pages

- [Enterprise Notification Service](../systems/enterprise-notification-service.md) — the system-level
  page describing ENS's architecture and integrations, derived in part from this document.
- [CBO-ARCH-WC-4.1](cbo-arch-wc-4.1.md) — Wire Center's current-state architecture document, which
  depends on this guide for the `TRS.WIRE.*` events it produces through the ENS producer library.

## Source

This page is derived from the converted source document
[`ens-int-3.2-enterprise-notification-service-integration-guide.md`](../../sources/estate/ens-int-3.2-enterprise-notification-service-integration-guide.md),
itself converted from the original PDF
`ENS-INT-3.2_Enterprise_Notification_Service_Integration_Guide.pdf`.
</content>
