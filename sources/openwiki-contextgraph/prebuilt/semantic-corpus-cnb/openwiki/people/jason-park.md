---
type: Person
entity_id: [P-JPARK, jason-park]
title: Jason Park
description: Software Engineer II on the CBO Wire Center squad at Crestline National Bank; owner of the Wire Center stories for activity-list filters (CBO-4302), IMAD display (CBO-4355), the in-progress hold-reason tooltip (CBO-4388), the PROCESSED-to-'Completed' label mapping (CBO-4402), and the remitter-name notification backlog item (CBO-4495).
tags: [people, software-engineer, cbo, wire-center, digital-treasury-channels, jira, cbo-4388, cbo-4402]
sources:
  - id: openwiki-source-4452149a3b4502b4c763a559
    resource: repo://sources/estate/jira-export-wt-discovery-2026-10-05.md
relates_to: [openwiki/documents/jira-export-wt-discovery-2026-10-05.md, openwiki/systems/cbo-wire-center.md, openwiki/interfaces/pph-v1-wire-status-api.md]
---

## Role and team

Jason Park is a **Software Engineer II on the CBO Wire Center squad**, the
Digital Treasury Channels team that builds the Wire Center module of
[Crestline Business Online](../systems/cbo-wire-center.md). The squad is led by
Engineering Manager Tom Becker, with Lucas Ferreira as Tech Lead and Marcus
Chen as Product Owner.

## Jira ownership (WT-discovery export, 2026-10-05)

The Wire Center backlog export
[JIRA-EXP-2026-10-05](../documents/jira-export-wt-discovery-2026-10-05.md)
lists Park as assignee/owner of the squad's client-facing wire status stories:

| Key | Summary | Status |
|---|---|---|
| CBO-4302 | Wire activity list - filters by rail, status, date range (client-side over PPH v1 list results) | Done (R26.3) |
| CBO-4355 | Wire detail - display Fed reference (IMAD) from PPH v1 `fedRef` | Done (R26.4) |
| CBO-4388 | Show hold reason tooltip on 'Pending Review' wires, populated from PPH v1 `holdReasonDesc` | In Progress (Sprint 26.20) |
| CBO-4402 | Map PPH v1 status `PROCESSED` to client label 'Completed' | Done (R26.1) |
| CBO-4495 | Incoming wire notification - include remitter name | Backlog |

Per his 2026-10-01 comment on CBO-4388 in the export, the tooltip change is
merged to `release/26.21` behind feature flag `WC_HOLD_TOOLTIP` (default ON),
targeting production on 2026-10-22. All of this work sits on top of the
[deprecated PPH v1 wire status API](../interfaces/pph-v1-wire-status-api.md).
