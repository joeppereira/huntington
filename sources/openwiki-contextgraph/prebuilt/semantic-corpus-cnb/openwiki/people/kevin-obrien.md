---
type: Person
entity_id: kevin-obrien
title: Kevin O'Brien
description: Engineering Manager for Payments Hub Engineering and technical owner of SYS-PPH (PRISM Payments Hub); owns the PPH v1 API sunset consumer-migration tracking epic PPH-2190.
tags: [people, engineering-manager, payments-hub-engineering, pph, prism-payments-hub, pph-2190, system-ownership]
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

Kevin O'Brien is the Engineering Manager (EM) for the Payments Hub Engineering team within Payments & Treasury Technology (PTT) at Crestline National Bank. He is listed as technical owner, alongside Principal Engineer Sunita Rao, of [PRISM Payments Hub](../systems/prism-payments-hub.md) (system ID `SYS-PPH`, running Volaris 9.4), the Tier 1 (24x7 critical) payments processing platform owned by Payments Hub Engineering. He reports into Raymond Ortiz (Director, Payments Hub Engineering) and works alongside Laura Kim, Director of Payments Platform Product, who is the business owner for PPH and Business Data Owner for payment datasets.

## Role and reporting line

| Attribute | Value |
|---|---|
| Team | Payments Hub Engineering |
| Title | Engineering Manager (EM) |
| Director | Raymond Ortiz |
| Peer technical contact | Sunita Rao (Principal Engineer) |
| Product Owner / business owner | Laura Kim (Director, Payments Platform Product) |
| Jira project / Slack | PPH / `#pph-support` |

Within the PTT engineering team directory, Payments Hub Engineering is distinct from the Digital Treasury Channels teams (CBO Wire Center squad and CBO Platform & Entitlements) that consume PPH's APIs; Kevin O'Brien is the named engineering-side point of contact for PPH dependency and system-ownership questions raised by those and other consuming teams.

## System ownership: SYS-PPH

Kevin O'Brien is recorded as technical owner of `SYS-PPH` (PRISM Payments Hub, Volaris 9.4) in the PTT system ownership register, which designates the "technical owner" as the accountable engineering manager/lead for a system, as distinct from the "business owner" (accountable product or data owner). SYS-PPH is rated Tier 1, meaning 24x7 critical support.

Payments Hub Engineering's planning factors (from the quarterly PTT directory) size PPH work at roughly 1 story point ≈ 8 engineering hours, reflecting vendor-platform constraints plus regression testing overhead. Demand is routed through the Payments Platform Demand Board (monthly cadence, 6-8 weeks lead time to schedule) rather than direct backlog intake, and the team was reported as ~90% committed for Q4 2026 due to concurrent address-enforcement and FedNow outbound work alongside the v1 sunset effort described below.

## Ownership of PPH-2190: PPH v1 API sunset migration tracking

Kevin O'Brien is the assignee/owner of **PPH-2190** ("PPH v1 API sunset - consumer migration tracking"), an Epic tracked in the PPH Jira project. See [PPH-2190 v1 Sunset Migration](../projects/pph-2190-v1-sunset-migration.md) for the project page.

Key facts about the epic, as owned by Kevin O'Brien:

- **Status / target:** In Progress; hard sunset date 2027-03-31.
- **Driver:** The PPH v1 API adapter is not supported on the upcoming Volaris 9.6 upgrade (planned April 2027), making the sunset non-negotiable on the current timeline.
- **No extensions:** The Payments Architecture Review Board (ARB) confirmed on 2026-09-08 that no extension beyond 2027-03-31 will be granted.
- **Tracked consumer migration status (as of 2026-09-22):**
  - IVR — migrated
  - CRM — in progress
  - `cbo-wire-bff` (CBO Wire Center) — **not started**
- **Escalation activity:** Kevin O'Brien sent a reminder to the CBO Wire Center team (recorded as the third such reminder) on 2026-09-22, chasing the unstarted `cbo-wire-bff` migration.

The unstarted CBO Wire Center consumer migration is tracked downstream as epic **CBO-4471** ("Migrate Wire Center from PPH v1 to PPH v2 APIs," owned by Tom Becker, 34 points, unscheduled as of 2026-08-30), which itself depends on CES account-filter mapping work (CBO-4473, owned by Arjun Mehta) and has not yet been placed into PI 26.4 or the PI 27.1 draft plan. As the epic owner for PPH-2190, Kevin O'Brien is the accountable party for driving this dependency to closure ahead of the 2027-03-31 sunset.

### Related v1/v2 risk context

Two v1-related issues intersect with PPH-2190's scope and are relevant to why the sunset matters beyond API versioning hygiene:

- **FCT-2004** (Risk, Open): PPH v1's `holdReasonDesc` field surfaces free-text Hold Management Service (HMS) content — including fraud/AML risk-codes and analyst notes — to downstream channel consumers (e.g., the CBO wire-hold tooltip feature, CBO-4388). Daniel Kowalski (FCT) raised this to Sunita Rao (PPH) and Tom Becker (CBO); remediation options are to stop the field sync or redact at the API gateway, and the comment thread notes the v1 sunset "may make this moot" once `cbo-wire-bff` moves to v2.
- **CBO-4419** (Bug, Open): A client-facing incident in which a wire status sourced from PPH v1 showed "Completed" and was later returned/rejected (RJCT AC04), linked to regulatory complaint CMP-2026-1189. This illustrates the kind of status-fidelity gap in the v1 API surface that the v2 migration is also expected to help address, since PPH-2190 governs the schedule under which `cbo-wire-bff` can adopt v2 semantics.

## Related pages

- [PRISM Payments Hub](../systems/prism-payments-hub.md) — the system Kevin O'Brien technically owns (SYS-PPH).
- [PPH-2190 v1 Sunset Migration](../projects/pph-2190-v1-sunset-migration.md) — the migration-tracking epic he owns.
