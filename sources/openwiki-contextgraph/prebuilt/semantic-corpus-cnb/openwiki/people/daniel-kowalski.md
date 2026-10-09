---
type: Person
entity_id: daniel-kowalski
title: Daniel Kowalski
description: Tech Lead for the PRSP Hold Management Service (HMS) at Crestline National Bank; owns design document PRSP-HMS-3.4 and raised the open data-leakage risk FCT-2004 concerning PPH v1 holdReasonDesc.
tags: [person, tech-lead, hold-management-service, prsp, financial-crimes-technology, fct-2004, prsp-hms-3.4]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-49303e801f124d97df9c3ea3
    resource: repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md
  - id: openwiki-source-4452149a3b4502b4c763a559
    resource: repo://sources/estate/jira-export-wt-discovery-2026-10-05.md
  - id: openwiki-source-08ac07f04b390aa09d5edc51
    resource: repo://sources/estate/prsp-hms-3.4-hold-management-service-design-and-reason-taxonomy-restricted.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

Daniel Kowalski is the Tech Lead for the **Hold Management Service (HMS)** within Financial Crimes Technology (FCT), part of the Payment Risk & Screening Platform (PRSP) organization at Crestline National Bank. He reports into the FCT - PRSP team led by Victor Petrov (Director), alongside Grace Mensah (Engineering Manager).

## Roles and responsibilities

- **Tech Lead, Hold Management Service** — Daniel is the named technical owner of `SYS-PRSP-HMS` (PRSP - Hold Management Service), sharing accountability with Grace Mensah (EM); the business owner is Rebecca Stone (FIU).
- **Document owner, PRSP-HMS-3.4** — Daniel co-owns (with Grace Mensah) the *Hold Management Service: Design & Hold Reason Taxonomy* document, which defines the HMS hold lifecycle, the hold reason code (HRC) taxonomy and disclosure tiers, data handling rules, interfaces, and controls. The document was approved by Victor Petrov (Director, FCT) and reviewed by Jordan Ellis (FCC Policy & Advisory); it was last reviewed 2026-06-24.
- **Risk owner, FCT-2004** — Daniel raised and is assignee of the open Jira risk **FCT-2004**, "PPH v1 `holdReasonDesc` exposes HMS free-text to channel consumers."
- **Backlog owner, FCT-1893** — Daniel is the assignee of **FCT-1893**, "Client-Safe Hold Status Facade" (`GET /prsp/hms/v1/holds/{holdId}/client-view`), a 21-point story deprioritized in 2025-Q3 by Grace Mensah pending a funded client-facing hold experience.

## FCT-2004: holdReasonDesc leakage risk

FCT-2004 is the central issue associated with Daniel. It documents that the legacy HMS-to-PRISM Payments Hub (PPH) v1 description sync populates PPH's `holdReasonDesc` field directly from the HMS hold `description`, which may embed restricted HRC mnemonics and analyst notes (e.g. `FRAUD_MODEL_HIGH sc=9xx L1 queue`, `SANCTIONS_REVIEW name match 0.91 L2`). Per PRSP-HMS-3.4, this sync predates ADR-PAY-021 and remains active only for v1 backward compatibility until the PPH v1 API sunset (2027-03-31); the document explicitly flags FCT-2004 as open.

Daniel's risk writeup states that consumers must not display this text and proposes two remediation options: stop the sync, or redact the field at the API gateway. In a 2026-05-27 comment he recorded that he raised the issue to PPH (Sunita Rao) and to CBO Wire Center (Tom Becker), that a remediation decision is still pending, and that the v1 sunset may ultimately make the fix moot by retiring the field's consumer path entirely.

The risk materialized operationally before remediation: CBO-4388 ("Show hold reason tooltip on 'Pending Review' wires"), a Wire Center story aimed at reducing "why is my wire pending" support calls, populates a client-facing tooltip directly from `holdReasonDesc` (truncated at 120 characters). UAT samples captured in that story include restricted-tier HRC content such as `FRAUD_MODEL_HIGH sc=9xx L1 queue` and `SANCTIONS_REVIEW name match 0.91 L2` — exactly the kind of restricted free text FCT-2004 warns against exposing. That feature shipped to `release/26.21` behind the `WC_HOLD_TOOLTIP` flag (default on, targeted for production 2026-10-22), ahead of any FCT-2004 remediation.

## FCT-1893: Client-Safe Hold Status Facade

As the assignee of FCT-1893, Daniel scoped a 21-point story to add a client-safe HMS endpoint, `GET /prsp/hms/v1/holds/{holdId}/client-view`, that would return only the POL-FCC-014 disclosure tier, an approved copy key, and permitted client actions — explicitly never the HRC code or analyst notes. The story was deprioritized in 2025-Q3 because no channel consumer had committed to building against it, and per PRSP-HMS-3.4 no client-facing HMS interface or client attestation endpoint currently exists. This leaves `holdReasonDesc` passthrough as the only channel-accessible source of hold context until either FCT-1893 is refunded or FCT-2004 is remediated.

## Related pages

- [Hold Management Service](../systems/hold-management-service.md)
