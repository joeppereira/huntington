---
type: Person
entity_id: lucas-ferreira
title: Lucas Ferreira
description: Tech Lead for the CBO Wire Center squad at Crestline National Bank; document owner of the Wire Center current-state architecture (CBO-ARCH-WC-4.1) and assignee of the international wire status visibility (gpi) discovery spike CBO-4480.
tags: [people, tech-lead, cbo, wire-center, digital-treasury-channels, architecture-document, gpi, payments-treasury-technology]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-550c0e3f038aab7950cab477
    resource: repo://sources/estate/cbo-arch-wc-4.1-wire-center-current-state-architecture.md
  - id: openwiki-source-49303e801f124d97df9c3ea3
    resource: repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md
  - id: openwiki-source-4452149a3b4502b4c763a559
    resource: repo://sources/estate/jira-export-wt-discovery-2026-10-05.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Role and reporting line

Lucas Ferreira is the **Tech Lead for the CBO Wire Center squad**, part of
Digital Treasury Channels Engineering within Payments & Treasury Technology
(PTT) at Crestline National Bank (CNB). The squad is led day-to-day by
Engineering Manager Tom Becker, with Marcus Chen as Product Owner, and
reports up through Director Anjali Deshpande; Ferreira holds technical
design authority for the squad's systems alongside Becker's delivery
management role.
[Engineering team directory](repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L41-L45)

In the Payments & Treasury Technology system ownership register, Ferreira
is listed as co-technical-owner (with Tom Becker) of **SYS-CBO**, the
Crestline Business Online Wire Center module — a Tier-1, 24x7-critical
system, reflecting that it gates client-initiated money movement. Marcus
Chen is the system's business owner.
[System ownership register, SYS-CBO](repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L78-L84)

See [CBO Wire Center](../systems/cbo-wire-center.md) for the system-level
writeup and [Digital Treasury Channels](../organizations/digital-treasury-channels.md)
for the organization's full structure.

## Document owner: CBO-ARCH-WC-4.1

Ferreira is the named **document owner** of **CBO-ARCH-WC-4.1**,
"Crestline Business Online - Wire Center: Current-State Architecture,"
version 4.1 (status Approved, last reviewed 2026-08-20). The document
describes Wire Center's existing domestic (Fedwire) and international
(Swift) wire capabilities — initiation, templates, dual approval,
step-up-gated release, activity list, wire detail, CSV export and
confirmation PDF — and explicitly scopes out milestone tracking,
international (gpi) status, hold explanations and client actions on held
wires as *not currently provided*. It is approved by Anjali Deshpande
(Director, Digital Treasury Channels Engineering) and Nikhil Bose (Chief
Architect), with Ferreira accountable as owner for keeping it accurate as
the module evolves.
[Document header](repo://sources/estate/cbo-arch-wc-4.1-wire-center-current-state-architecture.md#L11-L26)

As document owner, Ferreira's CBO-ARCH-WC-4.1 is the authoritative
current-state reference for several constraints that bound his own and
the squad's backlog, including:

- **No status polling** — per ADR-PAY-019 (adopted after incident
  INC-2024-1182), Wire Center must not poll PPH for status; only a
  user-initiated, throttled refresh (1 per 60 s per wire) is permitted,
  and any new status capability must be event-driven.
- **PPH v1 sunset 2027-03-31** — migration to PPH v2 is tracked as the
  unscheduled epic CBO-4471, blocked on CES account-filter mapping work
  (CBO-4473).
- **No international (gpi) tracking** — gpi status is visible only to
  Payment Operations in the Investigations Workbench, a gap directly
  addressed by Ferreira's own discovery spike CBO-4480 (below).
- **Status Projection Service (SPS) is ACH-only** — extending it to wires
  would require a new mapping module and a consumer ACL on
  `pay.wire.lifecycle.v2`.

[Constraints and known limitations](repo://sources/estate/cbo-arch-wc-4.1-wire-center-current-state-architecture.md#L125-L144)

See [CBO-ARCH-WC-4.1](../documents/cbo-arch-wc-4.1.md) for the full
document-level summary.

## Delivered work: reusable `<cbo-journey-timeline>` component (CBO-3802)

Ferreira delivered **CBO-3802**, "Aurora DS: reusable `<cbo-journey-timeline>`
component" (13 points, Done, release R25.3), a child story of the ACH
Payment Tracker epic (CBO-3790, owned by Marcus Chen). The component is a
rail-agnostic Aurora Design System v4 milestone timeline, including
terminal/error-state styling, and is listed in CBO-ARCH-WC-4.1's reusable
assets inventory as a candidate building block for any future Wire Center
milestone-tracking feature — relevant to the gap CBO-4480 is scoping.
[CBO-3802](repo://sources/estate/jira-export-wt-discovery-2026-10-05.md#L30)
[Reusable assets](repo://sources/estate/cbo-arch-wc-4.1-wire-center-current-state-architecture.md#L145-L153)

## Current work: international wire status visibility spike (CBO-4480)

Ferreira is the assignee of **CBO-4480**, "International wire status
visibility (gpi) for clients" — a 3-point discovery spike, status To Do,
unscheduled in the backlog as of the 2026-10-05 Jira export. The spike's
stated problem is that gpi (Swift Global Payments Innovation) status for
international wires is today visible only to Payment Operations, inside
the Investigations Workbench (IWB) — never surfaced to Wire Center clients
— and its description directs Ferreira to contact Payment Networks
Engineering (Raj Malhotra) about API options.
[CBO-4480](repo://sources/estate/jira-export-wt-discovery-2026-10-05.md#L39)
[CBO-4480 description and comment](repo://sources/estate/jira-export-wt-discovery-2026-10-05.md#L115-L121)

In a 2026-05-14 comment on the ticket, Ferreira recorded that gpi status
"lives only in Ops IWB" and that he would reach out to Raj Malhotra in
Payment Networks Engineering (PNE) about an API. As of the later 2026-10-05
Jira export, no linked follow-up API work existed yet; the closest related
item is **GTSI-0107**, "gpi Tracker Real-Time Service (GTRS)" — a
change-feed-based internal API initiative owned by Elena Vasquez (Director,
Global Transaction Services Integration), planned for discovery in
2027-Q2 and build in 2027-Q3/Q4, not funded for 2026. Vasquez's comment on
that initiative notes interest in early channel requirements to shape its
discovery, which positions CBO-4480's findings as a potential input to
GTRS scoping rather than something Ferreira can resolve unilaterally within
PNE's current gpi integration (the Swift gpi Tracker API contract,
quota 250k calls/month, renewing 2027-01-31).
[CBO-4480 comment](repo://sources/estate/jira-export-wt-discovery-2026-10-05.md#L121)
[GTSI-0107](repo://sources/estate/jira-export-wt-discovery-2026-10-05.md#L58)
[GTSI-0107 detail](repo://sources/estate/jira-export-wt-discovery-2026-10-05.md#L169-L175)
[GTSI-0115, Swift gpi Tracker API contract](repo://sources/estate/jira-export-wt-discovery-2026-10-05.md#L60)

The spike also sits alongside a live client-impact issue that strengthens
its business case: **CBO-4419**, an open bug reporting that an
international wire displayed the client label "Completed" and then was
returned/rejected by the beneficiary bank the next day (linked complaint
CMP-2026-1189, a EUR 412,600 wire where the client had already released
goods based on the "Completed" status). Because Wire Center has no gpi or
milestone visibility for international wires today, clients have no way to
see intermediate states between release and the terminal PPH status label
— the exact gap CBO-4480 is scoped to investigate.
[CBO-4419](repo://sources/estate/jira-export-wt-discovery-2026-10-05.md#L99-L105)

## Relationships

- **Anjali Deshpande** — Director, Digital Treasury Channels Engineering;
  Ferreira's organizational leader and a co-approver (with Nikhil Bose) of
  CBO-ARCH-WC-4.1.
- **Tom Becker** — Engineering Manager, CBO Wire Center squad; delivery
  counterpart to Ferreira's technical leadership and co-technical-owner of
  SYS-CBO; also document owner of PIR-2024-07, the post-incident review
  behind ADR-PAY-019.
- **Marcus Chen** — Director, Digital Treasury Product; Product Owner for
  Wire Center, sets roadmap priority for Ferreira's squad (including
  CBO-4480's priority against other backlog items).
- **Nikhil Bose** — Chief Architect, Payments & Treasury; co-approver of
  CBO-ARCH-WC-4.1.
- **Raj Malhotra** — Director, Payment Networks Engineering (PNE); contact
  named in CBO-4480 for gpi API options.
- **Arjun Mehta** — Tech Lead, SPS and CES on CBO Platform & Entitlements;
  owner of the Status Projection Service extension pattern that any future
  Wire Center milestone-tracking feature (potentially informed by CBO-4480)
  would need to follow.

## Related pages

- [CBO Wire Center](../systems/cbo-wire-center.md)
- [Digital Treasury Channels](../organizations/digital-treasury-channels.md)
- [CBO-ARCH-WC-4.1](../documents/cbo-arch-wc-4.1.md)
- [JIRA-EXP-2026-10-05](../documents/jira-export-wt-discovery-2026-10-05.md)
- [Anjali Deshpande](anjali-deshpande.md)
