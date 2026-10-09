---
type: Person
entity_id: kim-nguyen
title: Kim Nguyen
description: Accountable leader for the Commercial Service Center, the first-line Treasury support function that owns client-facing scripts and training and provides frontline feedback on Wire Center client experience.
tags: [person, commercial-service-center, treasury-support, ptt, first-line-partner, wire-center]
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

Kim Nguyen is the accountable leader for the **Commercial Service Center**, listed as a first-line partner function in the Payments & Treasury Technology (PTT) organization directory. The Commercial Service Center is accountable for Treasury Support scripts and training used by phone agents who field client calls about Crestline Business Online (CBO) wires and other treasury products. See [Commercial Service Center](../teams/commercial-service-center.md) for team-level detail.

## Role and scope

- Accountable function: Commercial Service Center, under the "Partner functions (first and second line)" section of the PTT organization directory, with "Treasury Support scripts and training" as the stated area of contact for product/design reviews.
- Planning factor: engagement with the Commercial Service Center for a new client-facing workflow is estimated at roughly 24 hours of scripts/training work, through a readiness checklist due three weeks before go-live.
- The Commercial Service Center is not an engineering team in the PTT directory; it is a downstream consumer and feedback source for engineering teams such as the CBO Wire Center squad, and it does not appear in the system ownership register (Section 4) or the engineering team directory (Section 3) of the PTT directory.

## Engagement in Wire Center work

Kim Nguyen's visible activity in the PTT backlog centers on the client-facing behavior of the CBO Wire Center module (`SYS-CBO`), which the Commercial Service Center's phone agents must explain to clients:

- **CBO-4388 - "Show hold reason tooltip on 'Pending Review' wires."** This story, requested via Commercial Service Center feedback as a call-deflection measure, populates a tooltip from the PPH v1 field `holdReasonDesc` (truncated at 120 characters, with a fallback of "Under review") so clients can see why a wire is pending without calling support. After the fix merged to `release/26.21` behind the `WC_HOLD_TOOLTIP` feature flag (default ON, targeting production 2026-10-22), Kim Nguyen commented that the change "should reduce 'why is my wire pending' calls" - the explicit link between this engineering change and the Commercial Service Center's call volume.
- **CBO-4419 - "Client complaint: wire showed 'Completed' then returned/rejected."** Kim Nguyen added the operational detail behind this open bug: an international wire to Halvorsen Industrial Supply (EUR 412,600) displayed status "Completed" on 2026-09-16 10:42 ET, but the beneficiary bank rejected it the next day (RJCT AC04) and funds were returned 2026-09-21; the client had already released goods on 2026-09-16 in reliance on the "Completed" status. Kim Nguyen linked this to complaint record `CMP-2026-1189`, which is open pending regulatory complaint review.

Both comments illustrate the Commercial Service Center's role as the feedback loop between client-facing wire status semantics in CBO Wire Center / PRISM Payments Hub (PPH) and the engineering backlog: mis-stated or opaque status labels (e.g., "Completed" before settlement finality, or an unexplained "Pending Review" hold) drive support call volume and complaints, and fixes to those labels are expected to reduce both.

## Relationships

- **CBO Wire Center squad** (leader Anjali Deshpande; PO Marcus Chen) - owns `SYS-CBO`, the system whose status and hold-reason display drives the call volume and complaints Kim Nguyen reports on.
- **Financial Crimes Technology (FCT)** - owns the Hold Management Service (`SYS-PRSP-HMS`) that originates the hold reasons surfaced (via PPH) in the CBO-4388 tooltip; a related security finding (FCT-2004) flags that the same PPH v1 field, `holdReasonDesc`, can leak internal hold-category/analyst-note text to channel consumers, which is a risk directly adjacent to the feature Kim Nguyen praised for reducing calls.
- **Payments Operations** (Denise Carter) - the other first-line partner function alongside the Commercial Service Center, handling wire investigations and the Wire Room rather than general client support scripts/training.
- **Disclosure Review Committee (DRC)** - approves client-facing copy, disclaimers, and notification templates; relevant to any scripts or status labels (e.g., "Completed", hold tooltips) the Commercial Service Center uses with clients.

## Related reading

- [Commercial Service Center](../teams/commercial-service-center.md)
