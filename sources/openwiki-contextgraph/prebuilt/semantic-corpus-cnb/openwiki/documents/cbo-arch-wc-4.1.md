---
type: Document
entity_id: CBO-ARCH-WC-4.1
title: "CBO-ARCH-WC-4.1: Wire Center Current-State Architecture"
description: Metadata and scope record for the approved current-state architecture document covering Crestline Business Online's Wire Center module — its integrations, status model, and known constraints.
tags: [cbo, wire-center, architecture-document, payments, treasury, wire-transfer, governance]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-550c0e3f038aab7950cab477
    resource: repo://sources/estate/cbo-arch-wc-4.1-wire-center-current-state-architecture.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Summary

**CBO-ARCH-WC-4.1** ("Crestline Business Online - Wire Center: Current-State Architecture") is the
governing architecture document for the **Wire Center** module of Crestline Business Online (CBO),
CNB's commercial digital banking portal for Treasury Management clients. It records the
existing (as-built) wire capabilities, integrations, status model, and known constraints for the
module — it is explicitly a current-state description, not a target-state or roadmap document. See
[CBO Wire Center](../systems/cbo-wire-center.md) for the system-level writeup derived from this
document.

## Document metadata

| Field | Value |
|---|---|
| Document ID | CBO-ARCH-WC-4.1 |
| Version / Status | 4.1 / Approved |
| Document owner | Lucas Ferreira, Tech Lead — CBO Wire Center |
| Approver(s) | Anjali Deshpande (Director, Digital Treasury Channels Eng.); Nikhil Bose (Chief Architect) |
| Effective / Last reviewed | Last reviewed 2026-08-20 |
| Classification | INTERNAL - CONFIDENTIAL |
| Related documents | PPH-API-CAT-2026.3; ENS-INT-3.2; ADR-PAY-019; PIR-2024-07; SEC-STD-22 |

The document carries an **INTERNAL - CONFIDENTIAL** classification and is marked "uncontrolled when
printed," meaning printed or exported copies are not guaranteed to reflect the current approved
revision — the authoritative version is the one held in the source document system of record. Each
page footer repeats the document ID, version, and classification banner, consistent with the
Payments & Treasury Technology documentation template used for this and related architecture
records.

## Ownership and approval chain

- **Owner**: Lucas Ferreira, Tech Lead for CBO Wire Center, is accountable for keeping the document
  accurate as the module evolves.
- **Approvers**: Anjali Deshpande (Director, Digital Treasury Channels Engineering) and Nikhil Bose
  (Chief Architect) sign off on the content, giving it standing as an approved architecture record
  rather than a draft or proposal.
- **Review cadence**: the document is periodically re-reviewed; the 4.1 revision reflects a review
  completed 2026-08-20.

## Related documents

CBO-ARCH-WC-4.1 cross-references the following documents, which should be treated as its
authoritative dependencies for related subsystems and decisions:

| Related document | Relevance to this document |
|---|---|
| PPH-API-CAT-2026.3 | API catalog for Payment Processing Hub (PPH), the upstream wire-processing system Wire Center integrates with (v1 APIs) |
| ENS-INT-3.2 | Integration reference for the Event Notification Service (ENS), used by Wire Center to produce `TRS.WIRE.*` notification events |
| ADR-PAY-019 | Architecture decision record prohibiting Wire Center from polling PPH for wire status (driven by incident INC-2024-1182); establishes the user-initiated, throttled refresh model described in this document |
| PIR-2024-07 | Post-incident review informing the no-polling constraint and related operational guardrails |
| SEC-STD-22 | Digital Channel External Sharing & Step-Up Standard; governs step-up authentication and any future external-sharing capability for wire data |

## Scope: what this document covers

CBO-ARCH-WC-4.1 documents the Wire Center module as it exists today, organized into the following
sections:

1. **Overview and usage** — describes Wire Center's purpose (domestic Fedwire and international
   Swift wire initiation, templates, dual approval, release with step-up authentication, activity
   list, wire detail, CSV export, confirmation PDF) and captures a trailing-90-day usage snapshot
   (client entitlement counts, active users, wire volumes, page views, refresh-click volume, and
   CBO's share of CNB's total outgoing wire volume).
2. **Logical architecture** — a component/integration diagram showing the Wire Center micro-frontend,
   the `cbo-wire-bff` backend-for-frontend, and the downstream services it calls (CES entitlements,
   CBO Auth step-up, PPH v1 wire APIs, ENS notifications), plus an explicit list of systems and APIs
   *not* currently used (PPH v2, gpi data, Status Projection Service for wires, HMS APIs, TDIP
   Insights API) and an integration inventory table of every consumer/endpoint pairing.
3. **Status model and client-facing labels** — the mapping from PPH v1 wire statuses to CBO-facing
   labels, visual treatment, and the release version each label was introduced in, including the
   R26.1 rename of "Processed" to "Completed."
4. **Identifiers stored by Wire Center** — which identifiers (cboRef, pphId, IMAD, OMAD, UETR) are
   persisted, displayed-only, or unavailable in the current (PPH v1) integration.
5. **Notifications produced by Wire Center** — the `TRS.WIRE.*` event types, their triggers,
   templates, and notification channels.
6. **Security and entitlements** — the CES entitlement types that gate Wire Center actions, the
   step-up and dual-approval requirements for wire release, and the explicit statement that external
   sharing of client transaction data is unsupported absent an InfoSec design review and Privacy
   Impact Assessment.
7. **Constraints and known limitations** — the no-polling constraint, the PPH v1 sunset date and its
   migration dependency, the lack of international (gpi) tracking in the client-facing product, the
   500-row activity-list ceiling, and the ACH-only scope of the existing Status Projection Service.
8. **Reusable assets** — components and services from adjacent initiatives (the `<cbo-journey-timeline>`
   UI component, the Status Projection Service, step-up authentication, and the ENS producer library)
   that are identified as candidates for reuse in future Wire Center work.

## Why this document exists

The document's explicit framing — current-state architecture, constraints, and reusable assets —
signals that it is intended as the baseline inventory from which future Wire Center work (e.g.
closing the gpi/milestone-tracking gap, migrating off PPH v1, or extending the Status Projection
Service to wires) is scoped. Several of its constraint statements function as binding guardrails for
any such future work:

- No PPH status polling is permitted; new status capabilities must be event-driven (per ADR-PAY-019).
- PPH v1 is scheduled to sunset 2027-03-31, making the v1→v2 migration (tracked as CBO-4471, with a
  dependency on CBO-4473) a forcing function for the module's integration layer.
- Any capability to externally share client transaction data requires an InfoSec design review under
  SEC-STD-22 and a Privacy Impact Assessment before implementation.

## Relationship to other wiki pages

- [CBO Wire Center](../systems/cbo-wire-center.md) — the system page describing the Wire Center
  module's architecture, integrations, and status model in detail, derived from this document.

## Source

This page is derived from the converted source document
[`cbo-arch-wc-4.1-wire-center-current-state-architecture.md`](../../sources/estate/cbo-arch-wc-4.1-wire-center-current-state-architecture.md),
itself converted from the original PDF `CBO-ARCH-WC-4.1_Wire_Center_Current-State_Architecture.pdf`.
</content>
