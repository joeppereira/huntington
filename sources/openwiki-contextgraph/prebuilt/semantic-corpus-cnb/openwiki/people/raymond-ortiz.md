---
type: Person
entity_id: raymond-ortiz
title: Raymond Ortiz
description: Director of Payments Hub Engineering at Crestline National Bank; accountable technical leader for the PRISM Payments Hub (PPH) system and approver of its system overview and API/event catalog documentation.
tags: [people, payments-hub-engineering, pph, payments-treasury-technology, director, system-owner, approver]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-49303e801f124d97df9c3ea3
    resource: repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md
  - id: openwiki-source-a4ee8b1dfcb7e3cec0a315e4
    resource: repo://sources/estate/pph-api-cat-2026.3-prism-payments-hub-api-and-event-catalog.md
  - id: openwiki-source-19beabaf3acaad354d39ee1e
    resource: repo://sources/estate/pph-sys-ovw-9.2-prism-payments-hub-system-overview-and-lifecycle-state-model.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Role and scope

Raymond Ortiz is the **Director of Payments Hub Engineering** within Crestline National Bank's Payments & Treasury Technology (PTT) organization. He leads the engineering team accountable for **PRISM Payments Hub (PPH)**, CNB's wire orchestration platform (vendor product: Volaris Payment Platform 9.4), which receives payment instructions from all channels, performs validation, screening, funds control, release, network transmission and accounting close for outgoing and incoming wires across Fedwire, Swift CBPR+, and book transfer rails ([pph-sys-ovw-9.2](../documents/pph-sys-ovw-9.2.md)).

As Director, Raymond Ortiz sits above the Payments Hub Engineering leads in PPH's reporting line: Kevin O'Brien (Engineering Manager) and Sunita Rao (Principal Engineer) report into his organization, and Laura Kim (Director, Payments Platform Product) is the paired business/product owner for PPH ([cnb-org-ptt-2026-06](../documents/cnb-org-ptt-2026-06.md)).

## Document approval responsibilities

Raymond Ortiz is the named **Director-level approver** on the two primary PPH reference documents:

- **PPH-SYS-OVW-9.2** - "PRISM Payments Hub - System Overview & Wire Lifecycle State Model" - co-approved with Laura Kim (Payments Platform Product); authored/owned day-to-day by Sunita Rao and Kevin O'Brien. This document defines the canonical v2 lifecycle state model (RECEIVED through COMPLETED/CANCELLED/RETURNED), the v1-to-v2 status mapping, rail-specific settlement semantics for NETWORK_ACCEPTED, identifier scoping (pphId, IMAD, OMAD, UETR, EndToEndId), HMS hold integration, and cutoff/operating-window rules ([pph-sys-ovw-9.2](../documents/pph-sys-ovw-9.2.md)).
- **PPH-API-CAT-2026.3** - "PRISM Payments Hub - API & Event Catalog (v1/v2) incl. v1 Deprecation Notice" - co-approved with Kevin O'Brien (EM); owned by Sunita Rao. This catalog documents the deprecated v1 REST endpoints, the v2 API/event surface, and the v1 sunset (2027-03-31, confirmed by the Architecture Review Board with no extensions) ([pph-api-cat-2026.3](../documents/pph-api-cat-2026.3.md)).

Approval by Raymond Ortiz on both documents signals that engineering-level sign-off for PPH's system behavior and its external API/event contracts is concentrated in the Payments Hub Engineering director role, distinct from the business/product approval supplied by Laura Kim.

## Organizational context

Within the PTT engineering directory, Payments Hub Engineering is one of several first-line engineering teams reporting toward Gregory Hall (MD, CIO Payments & Treasury Technology), alongside Digital Treasury Channels (CBO Wire Center), CBO Platform & Entitlements, Payment Networks Engineering (PNE), Global Transaction Services Integration (GTSI), and Financial Crimes Technology (PRSP) ([cnb-org-ptt-2026-06](../documents/cnb-org-ptt-2026-06.md)).

Team contact points for Payments Hub Engineering under Raymond Ortiz's directorship are tracked via the `PPH` Jira project and `#pph-support` Slack channel. The team is the technical owner of record for **SYS-PPH** (PRISM Payments Hub, Volaris 9.4) in the PTT system ownership register, with Laura Kim recorded as business owner and a T1 (24x7 critical) support tier ([cnb-org-ptt-2026-06](../documents/cnb-org-ptt-2026-06.md)).

## Planning and demand

Cross-team work routed to Payments Hub Engineering is sized using a planning factor of roughly 1 story point ≈ 8 engineering hours (reflecting vendor-platform constraints plus regression testing), intake is through the Payments Platform Demand Board with a 6-8 week scheduling lead time, and the team's capacity for PI 27.1 is noted as approximately 90% committed, driven by the November 2026 structured-address enforcement change and the FedNow outbound expansion ([cnb-org-ptt-2026-06](../documents/cnb-org-ptt-2026-06.md)). As director, Raymond Ortiz's organization is the point of escalation for engineering-manager-level dependency conflicts involving Payments Hub Engineering before they are raised further to the PTT Leadership Team ([cnb-org-ptt-2026-06](../documents/cnb-org-ptt-2026-06.md)).

## Related pages

- [Payments Hub Engineering (team)](../teams/payments-hub-engineering.md)
