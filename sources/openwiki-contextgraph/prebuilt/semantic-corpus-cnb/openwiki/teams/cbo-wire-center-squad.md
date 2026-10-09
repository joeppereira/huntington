---
type: Team
entity_id: cbo-wire-center-squad
title: CBO Wire Center Squad
description: Engineering team within Digital Treasury Channels at Crestline National Bank that owns SYS-CBO (the Wire Center module of Crestline Business Online); its leadership, Jira/Slack engagement routes, PI 27.1 planning factors, and current capacity commitment.
tags: [cbo, wire-center, sys-cbo, digital-treasury-channels, team, engineering-team, jira, slack, ptt, program-increment, planning-factors]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-49303e801f124d97df9c3ea3
    resource: repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

The **CBO Wire Center squad** is the engineering team that builds and
operates the Wire Center module of Crestline Business Online (CBO),
Crestline National Bank's (CNB) commercial digital banking portal for
Treasury Management clients. It is the named owning team and technical
owner of record for **SYS-CBO** in the Payments & Treasury Technology (PTT)
system ownership register, and sits inside the **Digital Treasury Channels**
engineering organization alongside its sibling team, CBO Platform &
Entitlements.
[System ownership register, SYS-CBO](repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L78-L84)

For the system the squad owns, see [CBO Wire Center (SYS-CBO)](../systems/cbo-wire-center.md).
For the organization it reports into, see
[Digital Treasury Channels](../organizations/digital-treasury-channels.md).

## Leadership and structure

The squad is led day-to-day by Engineering Manager **Tom Becker**, with
**Lucas Ferreira** as Tech Lead holding shared technical design authority,
and **Marcus Chen** (Director, Digital Treasury Product) as the Product
Owner who sets prioritization. The squad reports up through Director
**Anjali Deshpande**, who leads Digital Treasury Channels Engineering and is
the accountable engineering leader for both of its teams.
[Engineering team directory](repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L41-L45)

| Role | Person | Notes |
|---|---|---|
| Director (Digital Treasury Channels Engineering) | Anjali Deshpande | Accountable engineering leader; squad reports to her |
| Engineering Manager | Tom Becker | Day-to-day delivery lead; co-technical owner of SYS-CBO |
| Tech Lead | Lucas Ferreira | Shared technical design authority; co-technical owner of SYS-CBO; document owner of CBO-ARCH-WC-4.1 |
| Product Owner | Marcus Chen (Director, Digital Treasury Product) | Business owner of record for SYS-CBO; sets roadmap priorities |

This reflects PTT's general pattern of separating business ownership from
engineering ownership: Chen is organizationally distinct from the squad and
from Deshpande's reporting line, prioritizing work as Product Owner while
Becker and Ferreira own engineering delivery, technical design, and
on-call/support accountability.

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: an unescaped angle bracket inside a label breaks rendering; rephrase the label. -->
```text
graph TD
  GH["Gregory Hall<br/>MD, CIO Payments & Treasury Technology"]
  DO["Danielle Okafor<br/>EVP, Head of Treasury Management Products"]
  MC["Marcus Chen<br/>Director, Digital Treasury Product<br/>(Product Owner)"]
  AD["Anjali Deshpande<br/>Director, Digital Treasury Channels Eng."]
  TB["Tom Becker<br/>EM, CBO Wire Center squad"]
  LF["Lucas Ferreira<br/>Tech Lead, CBO Wire Center squad"]

  GH --> AD
  DO --> MC
  AD --> TB
  TB --- LF
  MC -.->|prioritization| TB
```

## System ownership: SYS-CBO

| Field | Value |
|---|---|
| System ID | SYS-CBO |
| System | Crestline Business Online - Wire Center module |
| Owning team | CBO Wire Center squad |
| Technical owner | Tom Becker / Lucas Ferreira |
| Business owner | Marcus Chen |
| Support tier | T1 (24x7 critical) |

SYS-CBO's Tier-1 classification reflects that it gates client-initiated
money movement: domestic (Fedwire) and international (Swift) wire
initiation, templates, dual approval, step-up-authenticated release, the
wire activity list, wire detail, CSV export, and confirmation PDF download.
See [CBO Wire Center (SYS-CBO)](../systems/cbo-wire-center.md) for the
system-level architecture, current-state scope, and known capability gaps
(no milestone tracking, no gpi/international status, no hold explanations,
no client actions on held wires).
[System ownership register, SYS-CBO](repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L78-L84)

The sibling team, **CBO Platform & Entitlements** (EM Nadia Haddad, Tech
Lead Arjun Mehta), owns the shared platform systems Wire Center depends on —
**SYS-CBO-SPS** (CBO Status Projection Service, T2) and **SYS-CES**
(Commercial Entitlements Service, T1) — both also under Marcus Chen's
business ownership.
[System ownership register](repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L85-L86)

## Engagement route

Demand against the squad is raised through **Jira project CBO** and
**Slack channel `#cbo-wire-center`**; intake is prioritized by the Product
Owner (Marcus Chen).
[Engineering team directory](repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L43-L45)
[Engagement routes and planning factors](repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L124-L126)

This is distinct from the sibling team's route: CBO Platform &
Entitlements work is raised in the separate **Jira CBO (Platform)** project
via `#cbo-platform`, with a 2-week triage cycle — teams requesting
dependency work should route to the correct Jira project rather than the
shared "CBO" naming.

## Planning factors (calibrated from the last four PIs)

| Factor | Value |
|---|---|
| Story point sizing | ~6.5 engineering hours per point |
| Velocity | ~42 points/sprint |
| Intake route / lead time | Jira CBO; Product Owner prioritization |
| Capacity note (PI 27.1) | Q4-2026 ~85% committed |

These factors are intended for first-pass sizing of cross-team dependencies
against the squad and are refreshed quarterly alongside the rest of the PTT
organization directory; organizational announcements issued between
refreshes take precedence.
[Engagement routes and planning factors](repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L120-L126)

For comparison, the sibling CBO Platform & Entitlements team uses the same
~6.5 hr/point factor but a lower velocity (~30 pts/sprint) and reports
lower commitment (~70%) for the same period — useful context when a
dependency could be routed to either CBO team.
[Engagement routes and planning factors, CBO Platform row](repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L127)

## Program increment calendar

| PI | Dates | Planning event |
|---|---|---|
| PI 26.4 | 2026-09-07 to 2026-11-27 | Complete |
| PI 27.1 | 2026-12-01 to 2027-03-05 | PI planning 2026-11-17/18; dependency asks due 2026-11-06 |
| PI 27.2 | 2027-03-15 to 2027-06-11 | PI planning 2027-03-02/03 |
[Program increment calendar](repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L140-L146)

With Q4-2026 capacity already ~85% committed, the squad has comparatively
little uncommitted room heading into PI 27.1 planning. This is the planning
backdrop against which currently unscheduled, backlog work competes for a
slot — notably **CBO-4471** (the 34-point epic to migrate `cbo-wire-bff`
off the deprecated PPH v1 Wire Status API before the 2027-03-31 sunset,
owned by Tom Becker), which as of the most recent Jira export had not been
placed into PI 26.4 or draft PI 27.1. See
[CBO-4471: PPH v1 to v2 migration](../projects/cbo-4471-pph-v1-to-v2-migration.md)
for the migration epic itself.

## Governance and escalation

New client-facing integrations to payment systems (including changes that
touch Wire Center's external-facing surfaces) require review by the
**Payments Architecture Review Board (ARB)**, which meets monthly (2nd
Tuesday) with a 10-business-day submission lead time. Client-facing copy,
disclaimers, and notification templates additionally require sign-off from
the **Disclosure Review Committee (DRC)** (bi-weekly, Thursday, 5-business-day
lead time).
[Governance forums](repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L98-L104)
[Governance forums, DRC](repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L114-L118)

Dependency conflicts the squad cannot resolve at the engineering-manager
level escalate first to Director Anjali Deshpande, then to the PTT
Leadership Team, which meets weekly on Mondays. Compliance or policy
interpretation questions are routed to FCC Policy & Advisory or the Privacy
Office rather than decided within the squad.
[Escalation](repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L148-L150)
