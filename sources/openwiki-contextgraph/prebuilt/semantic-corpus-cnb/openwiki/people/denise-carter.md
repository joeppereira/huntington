---
type: Person
entity_id: denise-carter
title: Denise Carter
description: Accountable leader for Payment Operations at Crestline National Bank; named approver of the Wire Status Lite post-implementation review (PIR-2024-07) and business owner of the registered EUA-TRS-0007 corridor completion dashboard.
tags: [people, payment-operations, payments-treasury-technology, accountable-leader, pir-2024-07, end-user-analytic, model-risk-management]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-49303e801f124d97df9c3ea3
    resource: repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md
  - id: openwiki-source-661f09048ce207829077c40d
    resource: repo://sources/estate/mrm-pol-02-v7.0-model-risk-management-policy-extract.md
  - id: openwiki-source-3cc45df143c5eec31fe1f9f6
    resource: repo://sources/estate/pir-2024-07-wire-status-lite-pilot-inc-2024-1182-post-implementation-review.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

Denise Carter is the **accountable leader for Payment Operations**, a
first-line business function that sits alongside (but outside) the
Payments & Treasury Technology (PTT) engineering organization at Crestline
National Bank (CNB). She is named in the PTT Organization, System Ownership
& Engagement Directory as the accountable owner of the Payment Operations
partner function, is one of three named approvers of **PIR-2024-07** (the
post-implementation review of the Wire Status Lite pilot and incident
INC-2024-1182), and is the registered business owner of
**EUA-TRS-0007**, the "ops corridor completion dashboard" End-User Analytic
(EUA) in the Model Risk Management inventory.

## Role and scope

Payment Operations is listed in the PTT directory's partner-functions table
as a first/second-line function distinct from the engineering teams it
depends on: Carter is its accountable leader, with Luis Ramirez (Wire
Investigations) and Tanya Brooks (Wire Room) named as the contacts for
product and design reviews that touch her organization.
Payment Operations' planning factor for engineering engagement is
~40 hours per new client-facing workflow for building standard operating
procedures (SOPs), routed through an Ops Readiness Review required four
weeks before go-live — meaning any new or changed client-facing payments
workflow must clear Payment Operations' readiness process, with Carter's
organization as the accountable reviewer, before launch.

Payment Operations Tech, a technology team distinct from Carter's own
first-line organization, owns the **Investigations Workbench**
(`SYS-IWB`, Tier 2 — business hours plus on-call support) in the system
ownership register, with Luis Ramirez as its named business owner; this
system is adjacent to, but not directly owned by, Carter. Carter's own
named ownership in the directory and related governance records is of the
Payment Operations function itself, its Ops Readiness Review gate, and the
EUA-TRS-0007 dashboard described below.

## Approval authority

### PIR-2024-07 (Wire Status Lite post-implementation review)

Carter is one of three named approvers — alongside **Anjali Deshpande**
(Director, Digital Treasury Channels Engineering) and **Raymond Ortiz**
(Director, Payments Hub Engineering) — of **PIR-2024-07**, the
post-implementation review of the **Wire Status Lite** pilot (CBO-3120) and
the resulting incident **INC-2024-1182**. The pilot auto-refreshed wire
status in Crestline Business Online (CBO) by polling the PRISM Payments Hub
(PPH) v1 status API from the browser every 30 seconds for 60 clients
between January and May 2024. On 2024-05-31 (month-end), combined pilot and
production refresh traffic drove roughly 85 TPS against the v1 status API,
exhausting its thread pool and delaying wire release for 47 minutes — 1,240
wires delayed, 312 released after the 6:00 p.m. ET Fedwire customer cutoff,
and 14 clients compensated $41,800 in interest claims. The pilot was
terminated and its epic closed.

Carter's sign-off closes the review across the three accountable leadership
areas it touched: Wire Center engineering (Deshpande), Payments Hub
engineering (Ortiz), and Payment Operations (Carter). Her approval is
particularly significant because two of the review's findings land squarely
in her function's domain rather than engineering's:

- **Treasury Support could not explain held wires to clients** without
  Financial Crimes Compliance (FCC) guidance — a client-facing operations
  gap, not a technology defect.
- **37% of surveyed pilot users believed "Processed" meant the beneficiary
  had received the funds**, a status-terminology misunderstanding that
  front-line operations staff have to field from clients.

The review's remaining open action — validating client-facing status
terminology with FCC and Legal before any future tracking feature ships —
is carried forward to CBO Product, but it is exactly the kind of
client-communication risk that Payment Operations surfaced and that
Carter's approval endorsed as a documented, still-open gap rather than a
closed one.

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: an unescaped angle bracket inside a label breaks rendering; rephrase the label. -->
```text
graph TD
  AD["Anjali Deshpande<br/>Director, Digital Treasury Channels Eng."]
  RO["Raymond Ortiz<br/>Director, Payments Hub Engineering"]
  DC["Denise Carter<br/>Accountable leader, Payment Operations"]
  PIR["PIR-2024-07<br/>Wire Status Lite PIR / INC-2024-1182"]

  AD -->|approver| PIR
  RO -->|approver| PIR
  DC -->|approver| PIR
```

See [PIR-2024-07 (document record)](../documents/pir-2024-07.md) and the
[PIR-2024-07 incident review](../incidents/pir-2024-07.md) for the full
narrative, root causes, and remediation tracking.

## EUA-TRS-0007: ops corridor completion dashboard

Carter is the named business owner, with attestation responsibility, of
**EUA-TRS-0007**, the "ops corridor completion dashboard," registered in
the Model Risk Management (MRM) inventory in 2026-05. Under
**MRM-POL-02** (v7.0), an End-User Analytic (EUA) is a simple descriptive
calculation — counts, medians, percentages over historical data — with no
forward-looking estimation; EUAs are registered in Archer with
business-owner attestation and do not receive independent validation,
unlike Tier 1–3 models. As business owner, Carter is accountable for:

- attesting that the dashboard's calculations remain within the registered,
  descriptive-only EUA scope (no forward-looking estimation or
  client-facing predictive claims), since crossing into forward-looking
  territory would reclassify it as at least a Tier 2 "customer-facing
  estimate," which cannot be shown to clients before independent
  validation and Disclosure Review Committee-approved disclaimers are in
  place;
- keeping the dashboard's registration current in Archer, MRM's system of
  record for tiering and validation status; and
- using the dashboard as the owner of record for the corridor-completion
  operational metric it reports, which is distinct from — and does not
  substitute for — any client-facing wire status feature such as the
  terminated Wire Status Lite pilot.

EUA registration plus attestation is a lighter-weight process than
model validation: the PTT directory's planning factors estimate EUA
registration at roughly 16 hours of Model Risk Management effort, against
160–240 validator hours for a Tier 2 customer-facing estimate. This
places EUA-TRS-0007 firmly on the internal-operational side of that
boundary: it supports Payment Operations' own visibility into corridor
completion rather than any claim communicated to clients.

See [MRM-POL-02 (document record)](../documents/mrm-pol-02.md) for the
policy's full tiering model and inventory extract.

## Relationships

- **Luis Ramirez** — Wire Investigations contact for Payment Operations
  design/product reviews, and named business owner of the Investigations
  Workbench (`SYS-IWB`).
- **Tanya Brooks** — Wire Room contact for Payment Operations design/product
  reviews.
- **Anjali Deshpande** and **Raymond Ortiz** — co-approvers of PIR-2024-07,
  representing Digital Treasury Channels Engineering and Payments Hub
  Engineering respectively.
- **Jonathan Price** — Head of Model Risk Management; second-line owner of
  MRM-POL-02 and the model inventory in which EUA-TRS-0007 is registered.
- **Sophie Laurent** — Validation Lead, Treasury & Operations models; the
  named MRM contact for Payment Operations' Treasury/Operations-adjacent
  model and EUA registrations.

## Related pages

- [Payment Operations](../teams/payment-operations.md)
- [PIR-2024-07 (document record)](../documents/pir-2024-07.md)
- [PIR-2024-07 incident review](../incidents/pir-2024-07.md)
- [MRM-POL-02 (document record)](../documents/mrm-pol-02.md)
- [CNB-ORG-PTT-2026-06 (document record)](../documents/cnb-org-ptt-2026-06.md)
- [Payments & Treasury Technology](../organizations/payments-treasury-technology.md)
