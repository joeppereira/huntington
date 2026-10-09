---
type: Person
entity_id: tanya-brooks
title: Tanya Brooks
description: Wire Room contact within Payment Operations, the first-line function that manually releases held or repair-queued wires and partners with Payments & Treasury Technology engineering teams.
tags: [people, payment-operations, wire-room, payments, contact-directory]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-49303e801f124d97df9c3ea3
    resource: repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md
  - id: openwiki-source-4452149a3b4502b4c763a559
    resource: repo://sources/estate/jira-export-wt-discovery-2026-10-05.md
  - id: openwiki-source-a4ee8b1dfcb7e3cec0a315e4
    resource: repo://sources/estate/pph-api-cat-2026.3-prism-payments-hub-api-and-event-catalog.md
  - id: openwiki-source-19beabaf3acaad354d39ee1e
    resource: repo://sources/estate/pph-sys-ovw-9.2-prism-payments-hub-system-overview-and-lifecycle-state-model.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

Tanya Brooks is the named **Wire Room** contact for **Payment Operations**, Crestline National Bank's first-line operational function for wire processing. She is listed alongside Luis Ramirez (the **Wire Investigations** contact) as one of the two product/design-review contacts for Payment Operations in the PTT organization directory, under function owner Denise Carter.

| Attribute | Value |
|---|---|
| Function | Payment Operations (first-line partner function, not a PTT engineering team) |
| Specialty | Wire Room |
| Function owner (accountable) | Denise Carter |
| Peer contact | Luis Ramirez - Wire Investigations |

## Role of the Wire Room

The Wire Room is the operational desk that performs manual intervention on wire payments that cannot complete straight-through in [PRISM Payments Hub (PPH)](../teams/payment-operations.md), CNB's wire orchestration platform. Two mechanisms route work to the Wire Room:

- **REPAIR lifecycle state** - PPH's canonical v2 lifecycle model includes a `REPAIR` state meaning "wire routed to the Wire Room repair queue," with a typical duration of minutes to hours. This state is shown to legacy v1 API consumers as the generic `PENDING` status, so client-facing channels (e.g., CBO Wire Center) cannot distinguish a repair-queue item from ordinary processing without reading the v2 `stateHistory`.
- **High-value/high-risk hold release** - When the Hold Management Service (HMS) raises certain holds, release still requires Wire Room sign-off even where digital self-service exists. For duplicate-suspect holds (HRC-01), Financial Crimes Technology's 2026 pilot allows client self-attestation with step-up authentication, but **wires over $5,000,000 still require Wire Room release** regardless of attestation outcome (CTRL-PAY-031, updated 2026-06-10). No digital release path exists for that threshold.

## Tooling

The legacy "Wire Room console" used by Payment Operations Tech was migrated onto the **Investigations Workbench (IWB)** in 2025; IWB is the current system of record Wire Room staff use to view and action held, repair-queued, and investigation-flagged wires, including gpi tracking status that is not otherwise exposed to channels or clients.

## Engagement and planning factors

Payment Operations is engaged as a first-line partner function rather than a PTT engineering team, so it does not carry a Jira/Slack intake route like the engineering squads. Cross-team engagement guidance lists:

- **Planning factor**: ~40 engineering/ops hours per new client-facing workflow (SOPs) that touches Payment Operations.
- **Intake route**: Ops Readiness Review, required 4 weeks before go-live for any change affecting Wire Room or related Payment Operations workflows.

Teams building features that change wire hold behavior, repair-queue triggers, or hold-release UX (e.g., CBO Wire Center's hold-reason tooltip work, or any future self-service release flow) should route readiness review through Payment Operations in time to engage the Wire Room ahead of launch.

## Related contacts and escalation

- **Luis Ramirez** - Wire Investigations contact, Payment Operations (handles investigative casework rather than routine release).
- **Denise Carter** - accountable owner of the Payment Operations function.
- Compliance or hold-policy interpretation questions (e.g., whether a hold can be released, or attestation eligibility) are not decided by engineering or Wire Room staff directly; they route to FCC Policy & Advisory (Jordan Ellis) per the standard PTT escalation path.

## Related pages

- [Payment Operations](../teams/payment-operations.md)
