---
type: Team
entity_id: payments-hub-engineering
title: Payments Hub Engineering
description: Engineering team within Payments & Treasury Technology at Crestline National Bank that owns PRISM Payments Hub (SYS-PPH); led by Director Raymond Ortiz, with demand routed through the Payments Platform Demand Board.
tags: [pph, team, payments-hub-engineering, payments-treasury-technology, prism-payments-hub, demand-board, planning-factors, system-ownership]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-49303e801f124d97df9c3ea3
    resource: repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md
  - id: openwiki-source-4452149a3b4502b4c763a559
    resource: repo://sources/estate/jira-export-wt-discovery-2026-10-05.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

**Payments Hub Engineering** is an engineering team within Payments & Treasury Technology (PTT)
at Crestline National Bank (CNB), led by Director **Raymond Ortiz**. The team builds and operates
**PRISM Payments Hub (PPH)** (`SYS-PPH`), CNB's wire orchestration platform (vendor: Volaris
Payment Platform 9.4), which intakes, validates, screens, funds-controls, releases, transmits and
settles outgoing and incoming payments across Fedwire, Swift CBPR+, and internal book-transfer
rails. See [PRISM Payments Hub](../systems/prism-payments-hub.md) for the system's full lifecycle,
processing stages, and API surface.

Payments Hub Engineering is one of several first-line engineering teams reporting toward
**Gregory Hall** (MD, CIO Payments & Treasury Technology), alongside Digital Treasury Channels'
CBO Wire Center squad, CBO Platform & Entitlements, Payment Networks Engineering (PNE), Global
Transaction Services Integration (GTSI), and Financial Crimes Technology (PRSP). The team's
business-side counterpart is **Laura Kim**, Director of Payments Platform Product, who is the
Product Owner of PPH and the Business Data Owner for payment datasets more broadly (including
the Fedwire Funds Connector, the Swift Alliance/gpi Connector, and the payment-data slice of the
Treasury Data & Insights Platform).

This write-up is based on the PTT Organization, System Ownership & Engagement Directory
(**CNB-ORG-PTT-2026-06**, v2026.2, published 2026-06-15); see
[CNB-ORG-PTT-2026-06](../documents/cnb-org-ptt-2026-06.md) for the directory's full content and
refresh cadence.

## Leadership and contacts

| Role | Person |
|---|---|
| Director | Raymond Ortiz |
| Engineering Manager (EM) | Kevin O'Brien |
| Principal Engineer | Sunita Rao |
| Product Owner (business) | Laura Kim (Director, Payments Platform Product) |
| Jira project | PPH |
| Slack channel | `#pph-support` |

Kevin O'Brien and Sunita Rao jointly hold the "technical owner" role for `SYS-PPH` in the PTT
system ownership register (the directory's accountable engineering manager/lead role, distinct
from the "business owner" role held by Laura Kim). Both report into Raymond Ortiz. See
[Raymond Ortiz](../people/raymond-ortiz.md), [Kevin O'Brien](../people/kevin-obrien.md), and
[Sunita Rao](../people/sunita-rao.md) for role-specific detail, including document-approval and
API-design responsibilities that sit alongside this organizational structure.

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: a semicolon inside a label breaks rendering; rephrase the label. -->
```text
flowchart TD
  GH["Gregory Hall<br/>MD, CIO Payments & Treasury Technology"] --> RO["Raymond Ortiz<br/>Director, Payments Hub Engineering"]
  RO --> KO["Kevin O'Brien<br/>EM"]
  RO --> SR["Sunita Rao<br/>Principal Engineer"]
  KO --> PPH["PRISM Payments Hub<br/>SYS-PPH (Tier 1)"]
  SR --> PPH
  LK["Laura Kim<br/>Director, Payments Platform Product<br/>Business Owner"] -.-> PPH
  Requester["Other PTT teams<br/>(e.g. CBO Wire Center, PNE)"] -->|demand| PPDB["Payments Platform Demand Board<br/>monthly; 6-8 wks to schedule"]
  PPDB --> RO
```
*Payments Hub Engineering's reporting line, system ownership of SYS-PPH, and the demand-board
intake route for cross-team roadmap requests.*

## System ownership: SYS-PPH

Payments Hub Engineering is the owning team of record for **SYS-PPH** (PRISM Payments Hub,
Volaris 9.4) in the PTT system ownership register, rated **Tier 1** (24x7 critical support).
Kevin O'Brien and Sunita Rao are recorded as technical owners; Laura Kim is recorded as business
owner. PPH sits at the center of CNB's payments estate, coordinating with the Payment Risk &
Screening Platform (PRSP) and its Hold Management Service for sanctions/fraud screening and
holds, the Core Deposit Platform for funds control, and the Payment Network Gateway (Fedwire
Funds Connector or Swift Alliance/gpi Connector) for network transmission — each of those
integration points is owned by a separate PTT team, making Payments Hub Engineering a hub of
cross-team dependency within the payments estate rather than a self-contained system owner. See
[PRISM Payments Hub](../systems/prism-payments-hub.md) for the lifecycle state model, processing
stages, and these integration boundaries in detail.

The team is also the named owner/approver of the two primary PPH reference documents:
**PPH-SYS-OVW-9.2** ("System Overview & Wire Lifecycle State Model," authored day-to-day by
Sunita Rao and Kevin O'Brien, approved by Raymond Ortiz and Laura Kim) and **PPH-API-CAT-2026.3**
("API & Event Catalog (v1/v2) incl. v1 Deprecation Notice," owned by Sunita Rao, approved by
Kevin O'Brien and Raymond Ortiz).

## Planning factors and the demand-board intake route

PTT's quarterly directory records Payments Hub Engineering's cross-team engagement model
separately from other PTT engineering teams, reflecting that PPH is a vendor platform (Volaris)
rather than an in-house codebase with normal sprint-based backlog intake:

| Attribute | Value |
|---|---|
| Planning factor | ~1 story point ≈ 8 engineering hours (vendor platform + regression testing) |
| Intake route | Payments Platform Demand Board |
| Lead time | 6-8 weeks to schedule |
| PI 27.1 capacity note | ~90% committed (driven by November 2026 structured-address enforcement and FedNow outbound work) |

Unlike teams such as CBO Wire Center squad, CBO Platform & Entitlements, or Payment Networks
Engineering — which take demand directly into their own Jira projects (CBO, CBO Platform, PNG)
under sprint-based triage — new engineering demand against PPH's roadmap is **not** raised
directly in the PPH Jira project. It must instead be raised through the **Payments Platform
Demand Board**, a monthly governance forum that prioritizes the PPH roadmap (next session noted
as 2026-10-21 in the directory), with requests due by prior month-end and a 6-8 week lead time to
scheduling. This routing reflects both the vendor-platform constraint (changes typically require
vendor-release coordination plus regression testing, reflected in the heavier ~8-hour-per-point
planning factor) and PPH's T1 criticality, which concentrates roadmap prioritization in a single
forum rather than distributing it across requesting teams' own backlogs.

At the time of the directory's 2026-06-15 publication, Payments Hub Engineering's capacity for
Program Increment 27.1 (2026-12-01 to 2027-03-05) was reported as roughly 90% committed — higher
than any other PTT engineering team in the directory (compare PNE and GTSI at ~80%/~75%) — driven
by two concurrent initiatives: mandatory structured-address enforcement for Swift CBPR+ and
Fedwire (effective November 2026) and FedNow outbound expansion. This high committed capacity is
a planning signal that new cross-team asks routed to the Payments Platform Demand Board should
expect to compete with that existing committed work when scheduling PI 27.1 dependencies
(dependency asks for PI 27.1 were due 2026-11-06, ahead of PI planning on 2026-11-17/18).

## Dependency and escalation path

Dependency conflicts that cannot be resolved between engineering managers escalate to the
respective Directors — for Payments Hub Engineering, Raymond Ortiz — and from there, if still
unresolved, to the PTT Leadership Team, which meets weekly on Mondays. Compliance or policy
interpretation questions (for example, screening or hold-related changes affecting PPH's
integration with the Hold Management Service) are routed instead to Financial Crimes Compliance
(FCC) Policy & Advisory or the Privacy Office, and are explicitly not decided by engineering teams
including Payments Hub Engineering.

Because PPH integrates with multiple other PTT- and second-line-owned systems, Payments Hub
Engineering's planning also intersects with other forums beyond the Payments Platform Demand
Board: the **Payments Architecture Review Board (ARB)** (monthly, 2nd Tuesday, 10 business days'
submission lead time) is required for any new client-facing integration to payment systems such
as PPH, and the **FCT Change Advisory** (bi-weekly) requires FCC sign-off for hold/screening
changes that touch PPH's HMS integration.

## Known cross-team dependency: PPH v1 API sunset

Payments Hub Engineering owns the mandatory sunset of PPH's v1 REST API surface (hard date
**2027-03-31**, confirmed by the Payments ARB on 2026-09-08 with no extensions, driven by the v1
adapter's lack of support on the upcoming Volaris 9.6 upgrade). This is tracked as Epic
**PPH-2190**, owned by Kevin O'Brien, and depends on migration work in consuming teams —
notably the CBO Wire Center squad's `cbo-wire-bff` migration (epic CBO-4471), which as of
2026-09-22 had not started despite repeated reminders. This illustrates the kind of cross-team
dependency that the Payments Platform Demand Board and the Director-to-Director escalation path
exist to manage: Payments Hub Engineering sets and enforces the sunset timeline, but closing the
dependency requires scheduled engineering capacity in other teams' own backlogs.

## Related pages

- [PRISM Payments Hub](../systems/prism-payments-hub.md) — the Tier 1 system the team builds and
  operates.
- [Raymond Ortiz](../people/raymond-ortiz.md) — Director, Payments Hub Engineering.
- [Kevin O'Brien](../people/kevin-obrien.md) — Engineering Manager; technical co-owner of SYS-PPH;
  owner of the PPH-2190 v1 sunset migration epic.
- [Sunita Rao](../people/sunita-rao.md) — Principal Engineer; technical co-owner of SYS-PPH;
  designer of record for the PPH v1 and v2 APIs.
- [CNB-ORG-PTT-2026-06](../documents/cnb-org-ptt-2026-06.md) — the quarterly directory this page
  is derived from.
