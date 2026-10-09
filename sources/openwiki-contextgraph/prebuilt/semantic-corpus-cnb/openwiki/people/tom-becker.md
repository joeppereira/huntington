---
type: Person
entity_id: tom-becker
title: Tom Becker
description: Engineering Manager for the CBO Wire Center squad at Crestline National Bank; co-technical owner of SYS-CBO, author of the PIR-2024-07 post-implementation review, owner of the open CBO-4419 "Completed" status complaint bug, and owner of the unscheduled PPH v1-to-v2 migration epic CBO-4471.
tags: [people, engineering-manager, cbo, wire-center, digital-treasury-channels, pir-2024-07, cbo-4471, pph-v2-migration, wire-status-lite, ptt]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-49303e801f124d97df9c3ea3
    resource: repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md
  - id: openwiki-source-4452149a3b4502b4c763a559
    resource: repo://sources/estate/jira-export-wt-discovery-2026-10-05.md
  - id: openwiki-source-3cc45df143c5eec31fe1f9f6
    resource: repo://sources/estate/pir-2024-07-wire-status-lite-pilot-inc-2024-1182-post-implementation-review.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Role and reporting line

Tom Becker is the **Engineering Manager (EM) for the CBO Wire Center squad**,
part of Digital Treasury Channels Engineering within Payments & Treasury
Technology (PTT) at Crestline National Bank (CNB). He leads the squad's
day-to-day delivery alongside **Lucas Ferreira** (Tech Lead, shared technical
design authority) and **Marcus Chen** (Product Owner), and the squad reports
up through Director **Anjali Deshpande**.
[Engineering team directory](repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L41-L45)

In the PTT system ownership register, Becker is listed as co-**technical
owner** (with Lucas Ferreira) of **SYS-CBO**, the Crestline Business Online –
Wire Center module — a Tier-1 (24x7-critical) system, reflecting that it
gates client-initiated money movement. Marcus Chen is the system's business
owner.
[System ownership register, SYS-CBO](repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L78-L84)

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: an unescaped angle bracket inside a label breaks rendering; rephrase the label. -->
```text
graph TD
  AD["Anjali Deshpande<br/>Director, Digital Treasury Channels Eng."]
  TB["Tom Becker<br/>EM, CBO Wire Center squad<br/>Technical owner: SYS-CBO"]
  LF["Lucas Ferreira<br/>Tech Lead (co-technical owner: SYS-CBO)"]
  MC["Marcus Chen<br/>Product Owner / business owner"]

  AD --> TB
  TB --- LF
  MC -.->|prioritization| TB
```

See [CBO Wire Center squad](../teams/cbo-wire-center-squad.md) for the
team-level writeup and
[Digital Treasury Channels](../organizations/digital-treasury-channels.md)
for the organization's full structure.

## Author: PIR-2024-07 (Wire Status Lite pilot post-implementation review)

Becker is the named **document owner and author** of **PIR-2024-07**,
"Post-Implementation Review: Wire Status Lite Pilot and Incident
INC-2024-1182" (v1.1, Final, 2024-07-15), facilitated by Enterprise
Architecture and approved by Anjali Deshpande, Raymond Ortiz, and Denise
Carter.
[PIR-2024-07 header](repo://sources/estate/pir-2024-07-wire-status-lite-pilot-inc-2024-1182-post-implementation-review.md#L15-L22)

The PIR closed out **Wire Status Lite** (epic **CBO-3120**, 55 points,
assigned to Becker), a pilot that auto-refreshed wire status for 60 CBO
clients from January to May 2024 by polling the PRISM Payments Hub (PPH) v1
status API every 30 seconds per visible wire. On **2024-05-31** (month-end),
combined pilot polling and normal production wire-release refreshes drove
~85 TPS against the shared, synchronous v1 API, exhausting its thread pool
and delaying wire release for 47 minutes (**INC-2024-1182**). The pilot was
terminated and CBO-3120 was closed as "Won't Do."
[CBO-3120 / PIR summary](repo://sources/estate/pir-2024-07-wire-status-lite-pilot-inc-2024-1182-post-implementation-review.md#L24-L26)
[CBO-3120 Jira record](repo://sources/estate/jira-export-wt-discovery-2026-10-05.md#L28)

As author, Becker's PIR documents the quantified impact (1,240 wires
delayed, 312 released after the 6:00 p.m. ET Fedwire customer cutoff, 14
clients compensated $41,800 in interest claims, no regulatory notification
required), three root causes (unthrottled polling against a shared
synchronous API, no month-end capacity testing, and status semantics never
validated with Compliance/Legal before client exposure), and four follow-up
actions.
[Impact table](repo://sources/estate/pir-2024-07-wire-status-lite-pilot-inc-2024-1182-post-implementation-review.md#L28-L35)
[Root causes](repo://sources/estate/pir-2024-07-wire-status-lite-pilot-inc-2024-1182-post-implementation-review.md#L45-L51)

Three of the four actions were completed in 2024–2025 (PPH v1 status API
rate-limited to 20 TPS shared; the event-driven status pattern became
**ADR-PAY-019**; CBO Platform delivered a reusable Status Projection Service
for ACH in 2025 as CBO-3815). The fourth action — **validate client-facing
status terminology with FCC and Legal before any future tracking feature** —
remains **open, carried forward**, and is the action directly implicated
when the later "Completed" mislabeling produced complaint **CMP-2026-1189**.
[Actions table](repo://sources/estate/pir-2024-07-wire-status-lite-pilot-inc-2024-1182-post-implementation-review.md#L53-L60)

See [PIR-2024-07](../incidents/pir-2024-07.md) for the full narrative and
[documents/pir-2024-07.md](../documents/pir-2024-07.md) for document-level
metadata.

## Open bug: "Completed" status complaint (CBO-4419)

Becker is the assignee of **CBO-4419**, "Client complaint: wire showed
'Completed' then returned/rejected" — an `Open`, unscheduled (Backlog) bug
linked to complaint **CMP-2026-1189**. An international wire for Halvorsen
Industrial Supply (EUR 412,600) was shown "Completed" in CBO on 2026-09-16;
the beneficiary bank rejected it the next day (RJCT, ISO return reason
AC04), and funds were returned to CNB on 2026-09-21 — after the client had
already released goods in reliance on the "Completed" status. Root cause was
still TBD as of the 2026-10-05 Jira export.
[CBO-4419](repo://sources/estate/jira-export-wt-discovery-2026-10-05.md#L99-L106)

This bug is the direct, current-day recurrence of the status-terminology
risk Becker's own PIR-2024-07 flagged as unresolved two years earlier,
tying his authorship of that review to his present-day ownership of its
consequence.

## Owner: CBO-4471 — PPH v1-to-v2 migration epic

Becker is the owner of **CBO-4471**, "Migrate Wire Center from PPH v1 to PPH
v2 APIs" — an Epic sized at **34 points**, status **Backlog (unscheduled)**,
with a hard target of completing **before the 2027-03-31 PPH v1 sunset**.
The work replaces `/pph/v1` calls in `cbo-wire-bff` with `/pph/v2`, and is
tracked as a consumer line item under the platform-side sunset epic
**PPH-2190** (owned by Kevin O'Brien), which as of 2026-09-22 recorded
`cbo-wire-bff` as the one sunset consumer that had **not started** migrating
(versus IVR, migrated, and CRM, in progress).
[CBO-4471](repo://sources/estate/jira-export-wt-discovery-2026-10-05.md#L107-L113)
[PPH-2190](repo://sources/estate/jira-export-wt-discovery-2026-10-05.md#L137-L141)

The epic **blocks nothing** but **depends on CBO-4473** (CES: account-filter
mapping for PPH v2 search by `clientId` + entitled accounts, owned by Arjun
Mehta, also unscheduled in Backlog). In an 2026-08-30 comment, Becker noted
the 34-point sizing assumes reuse of the existing list/detail UI and
excludes any new tracking features, and that the epic was not yet placed in
PI 26.4 or the PI 27.1 draft — i.e., as of the 2026-10-05 export, the migration
had no committed delivery date against the fixed 2027-03-31 sunset deadline.
[CBO-4473 dependency and sizing comment](repo://sources/estate/jira-export-wt-discovery-2026-10-05.md#L109-L113)
[CBO-4473](repo://sources/estate/jira-export-wt-discovery-2026-10-05.md#L38)

The migration is also where another open platform risk converges on
Becker's backlog: **FCT-2004** records that PPH v1's `holdReasonDesc` field
exposes free-text Hold Management Service (HMS) analyst notes to channel
consumers, and that this was raised to both Sunita Rao (PPH) and Becker
(CBO) with no remediation decision yet made — noting the v1 sunset, which
CBO-4471 delivers, "may make this moot."
[FCT-2004](repo://sources/estate/jira-export-wt-discovery-2026-10-05.md#L165-L167)

See [CBO-4471 (PPH v1→v2 migration)](../projects/cbo-4471-pph-v1-to-v2-migration.md)
for the project-level writeup.

## Planning context

Demand for the CBO Wire Center squad Becker manages is sized in PTT's
quarterly planning directory at roughly **1 story point ≈ 6.5 engineering
hours**, with observed velocity of **~42 points/sprint** and PI 27.1 capacity
tracked at **~85% committed** — a constraint relevant to when the
unscheduled, 34-point CBO-4471 epic can realistically be slotted against the
fixed PPH v1 sunset deadline.
[Planning factors](repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L124-L126)
