---
type: Interface
entity_id: [EP-CBO-01, EP-CBO-02, EP-CBO-03]
title: "CBO Wire BFF API (EP-CBO-01/02/03)"
description: The cbo-wire-bff endpoints behind CBO Wire Center's wire activity list, wire detail, and user-initiated status refresh (EP-CBO-01/02/03) - all GA, all backed synchronously by the deprecated PPH v1 wire APIs, with the refresh endpoint throttled to 1 call per 60 seconds per wire under ADR-PAY-019.
tags: [cbo, wire-center, cbo-wire-bff, ep-cbo-01, ep-cbo-02, ep-cbo-03, wire-status, refresh, pph-v1, adr-pay-019, rest-api]
sources:
  - id: openwiki-source-4452149a3b4502b4c763a559
    resource: repo://sources/estate/jira-export-wt-discovery-2026-10-05.md
owned_by: [openwiki/teams/cbo-wire-center-squad.md]
part_of: openwiki/systems/cbo-wire-center.md
status: live
described_by: [openwiki/documents/jira-export-wt-discovery-2026-10-05.md]
aliases: [up to date, latest data]
---

## Overview

The **CBO Wire BFF API** is the backend-for-frontend surface of
[CBO Wire Center](../systems/cbo-wire-center.md) (`cbo-wire-bff`) that the Wire
Center UI calls for wire activity, wire detail, and status refresh. All three
endpoints are GA, and all three are thin synchronous adapters over the
[deprecated PPH v1 wire APIs](pph-v1-wire-status-api.md) — which is why the
Wire Center squad tracks [CBO-4471](../projects/cbo-4471-pph-v1-to-v2-migration.md)
("Replace /pph/v1 calls in cbo-wire-bff with /pph/v2") ahead of the v1 sunset.

## Endpoint inventory (EP-CBO-01/02/03)

| ID | Method / path | Purpose | Backing call |
|---|---|---|---|
| EP-CBO-01 | `GET /cbo/wire-bff/v1/wires` | Wire activity list | PPH v1 list (EP-PPH-02) |
| EP-CBO-02 | `GET /cbo/wire-bff/v1/wires/{cboRef}` | Wire detail | PPH v1 status (EP-PPH-01) |
| EP-CBO-03 | `POST /cbo/wire-bff/v1/wires/{cboRef}/refresh-status` | User-initiated refresh | PPH v1 status (EP-PPH-01), throttled |

EP-CBO-03 is throttled to **1 refresh per 60 seconds per wire**, the
throttled-refresh exception recorded in [ADR-PAY-019](../decisions/adr-pay-019.md)
after the Wire Status Lite polling incident.

## Known limitations carried from PPH v1

Because the BFF fronts PPH v1, its behavior inherits v1's limits, as recorded in
the Jira backlog export (JIRA-EXP-2026-10-05):

- The activity list is capped at the v1 maximum of **500 rows with no cursor**;
  the rail/status/date-range filters shipped in CBO-4302 are applied
  **client-side** over those results.
- Wire detail shows only the v1 fields: coarse status, IMAD via `fedRef`
  (CBO-4355) — no OMAD and no UETR.
- The "Pending Review" hold-reason tooltip in progress under CBO-4388 is
  populated from the v1 `holdReasonDesc` free-text field.
- The v1 status `PROCESSED` is mapped to the client label "Completed"
  (CBO-4402).

Migration of all three endpoints to PPH v2 is tracked as
[CBO-4471](../projects/cbo-4471-pph-v1-to-v2-migration.md) (34 pts,
unscheduled), which must complete before the v1 sunset on 2027-03-31 tracked in
[PPH-2190](../projects/pph-2190-v1-sunset-migration.md).
