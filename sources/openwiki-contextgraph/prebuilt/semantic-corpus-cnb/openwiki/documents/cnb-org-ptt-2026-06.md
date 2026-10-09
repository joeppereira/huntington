---
type: Document
entity_id: CNB-ORG-PTT-2026-06
title: "CNB-ORG-PTT-2026-06: PTT Organization, System Ownership & Engagement Directory"
description: Metadata record for the quarterly-refreshed directory of leadership, engineering teams, system ownership, governance forums, and engagement/planning factors across Payments & Treasury Technology (PTT) and its first- and second-line partners.
tags: [ptt, payments, treasury, organization, system-ownership, governance, engagement-directory, planning-factors]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-49303e801f124d97df9c3ea3
    resource: repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Summary

**CNB-ORG-PTT-2026-06** ("Payments & Treasury Technology - Organization, System Ownership &
Engagement Directory") is the reference directory for who owns what across the Payments business
unit, how to engage each team, and the planning factors used to size cross-team work. It is
published by the PTT Business Management Office (BMO) and refreshed on a quarterly cadence,
covering leadership, the engineering team directory, first- and second-line partner functions, a
system ownership register, governance forums, engagement routes/planning factors, and the program
increment (PI) calendar for Payments & Treasury Technology (PTT). See
[Payments & Treasury Technology](../organizations/payments-treasury-technology.md) for the
organization-level writeup derived from this document.

## Document metadata

| Field | Value |
|---|---|
| Document ID | CNB-ORG-PTT-2026-06 |
| Version / Status | 2026.2 / Published (quarterly refresh) |
| Document owner | PTT Business Management Office (BMO) |
| Approver(s) | Gregory Hall, MD - CIO Payments & Treasury Technology |
| Effective / Last reviewed | Published 2026-06-15; next refresh 2026-12 (Q4) |
| Classification | INTERNAL - CONFIDENTIAL |
| Related documents | CBO-ARCH-WC-4.1; PPH-SYS-OVW-9.2; PNG-TDD-6.0; PRSP-HMS-3.4; ENS-INT-3.2; TDIP-CAT-2026.2 |

The document carries an **INTERNAL - CONFIDENTIAL** classification and is marked "uncontrolled when
printed," meaning exported or printed copies are not guaranteed to reflect the current approved
revision. Each page footer repeats the document ID, version (v2026.2), and classification banner.

## Purpose and intended use

The directory is the reference for system ownership, accountable leaders, and engagement routes
within PTT and its first- and second-line partners. Product and engineering teams are expected to
use it to:

- identify owners for cross-team dependencies,
- raise demand through the correct intake route for each team or function, and
- apply the planning factors in Section 6 of the source document when sizing cross-team work.

Because the directory is refreshed only quarterly, the document explicitly states that
organizational announcements issued between refreshes **take precedence** over its contents — it is
a baseline, not a live system of record for org changes.

## Ownership and approval chain

- **Owner**: the PTT Business Management Office (BMO) is accountable for keeping the directory
  accurate and for running the quarterly refresh cycle.
- **Approver**: Gregory Hall, MD and CIO of Payments & Treasury Technology, signs off on the
  published content, giving it standing as the authoritative org/ownership reference for PTT rather
  than an informal team roster.
- **Review cadence**: version 2026.2 was published 2026-06-15, with the next scheduled refresh in
  2026-12 (Q4). The quarterly cadence means ownership and contact data can lag real-world
  reorganizations by up to one quarter, mitigated by the precedence rule above.

## Scope: what the directory covers

1. **Leadership** — accountable leaders and their scope across PTT and its 1st/2nd-line partners,
   including the CIO, business owners for Treasury Management (TM) products, product owners for
   CBO Wire Center and PRISM Payments Hub (PPH), the Chief Architect (chair of the Payments
   Architecture Review Board), and 2nd-line owners for financial-crimes policy, model risk, and
   privacy.
2. **Engineering team directory** (as of 2026-06-15) — for each engineering team (CBO Wire Center
   squad, CBO Platform & Entitlements, Payments Hub Engineering, Payment Networks Engineering (PNE),
   Global Transaction Services Integration (GTSI), Financial Crimes Technology (FCT/PRSP), Enterprise
   Notification Platform, Treasury Data & Analytics/TDIP): the team leader, key contacts (engineering
   managers, tech leads, product owners), and the Jira project / Slack channel used to reach them.
3. **Partner functions (1st/2nd line)** — accountable leaders and review contacts for Financial
   Crimes Compliance (FCC), Model Risk Management (MRM), Payment Operations, Commercial Service
   Center, Legal (Treasury & Payments), Information Security (Digital Channels), Privacy Office &
   Data Governance, and Deposits Data Ownership.
4. **System ownership register** — for each system, its owning engineering team, technical owner
   (accountable EM/lead), business owner (accountable product/data owner), and support tier
   (T1 = 24x7 critical, T2 = business hours + on-call, T3 = business hours).
5. **Governance forums** — cadence, submission lead time, and notes for the Payments Architecture
   Review Board (ARB), Payments Platform Demand Board, FCT Change Advisory, Disclosure Review
   Committee (DRC), MRM Model Inventory & Validation, and Privacy Impact Assessment (PIA) process.
6. **Engagement routes and planning factors** — per-team intake routes, lead times, first-pass
   sizing factors (e.g. story-point-to-hour ratios, per-event or per-review effort estimates)
   calibrated from the last four program increments, and point-in-time capacity/commitment notes for
   PI 27.1.
7. **Program increment calendar** — dates and planning events for PI 26.4, PI 27.1, and PI 27.2.
8. **Escalation** — the path for unresolved dependency conflicts (engineering managers to Directors
   to the PTT Leadership Team, which meets weekly on Mondays) and the explicit routing of compliance
   or policy-interpretation questions to FCC Policy & Advisory or the Privacy Office rather than to
   engineering teams.

## System ownership register (summary)

The register distinguishes **technical owner** (accountable engineering manager/lead) from
**business owner** (accountable product or data owner) for each system, and assigns a support tier:

| System ID | System | Owning team | Tier |
|---|---|---|---|
| SYS-CBO | Crestline Business Online - Wire Center module | CBO Wire Center squad | T1 |
| SYS-CBO-SPS | CBO Status Projection Service | CBO Platform | T2 |
| SYS-CES | Commercial Entitlements Service | CBO Platform | T1 |
| SYS-PPH | PRISM Payments Hub (Volaris 9.4) | Payments Hub Engineering | T1 |
| SYS-PNG-FFC | Payment Network Gateway - Fedwire Funds Connector | PNE | T1 |
| SYS-PNG-GPI | Payment Network Gateway - Swift Alliance & gpi Connector | PNE | T1 |
| SYS-PRSP-HMS | PRSP - Hold Management Service | FCT | T1 |
| SYS-PRSP-SEN | PRSP - Sentinel Fraud Scoring (vendor) | FCT | T1 |
| SYS-PRSP-SSC | PRSP - SanctionScreen | FCT | T1 |
| SYS-ENS | Enterprise Notification Service | Enterprise Notification Platform | T2 |
| SYS-TDIP | Treasury Data & Insights Platform | TDIP | T2 |
| SYS-CDP | Core Deposit Platform | Deposits Technology | T1 |
| SYS-IWB | Investigations Workbench | Payment Operations Tech | T2 |

Most payments-critical systems (CBO Wire Center, CES, PPH, both Payment Network Gateway
connectors, and all three PRSP components) carry Tier 1 (24x7 critical) support, reflecting their
role in client-facing wire initiation, entitlements, and financial-crimes screening/holds.

## Governance forums and lead times

Teams planning cross-system changes must account for forum cadence and submission lead time before
go-live:

| Forum | Cadence | Submission lead time |
|---|---|---|
| Payments Architecture Review Board (ARB) | Monthly, 2nd Tuesday | 10 business days |
| Payments Platform Demand Board | Monthly | Request by prior month-end |
| FCT Change Advisory | Bi-weekly | 5 business days |
| Disclosure Review Committee (DRC) | Bi-weekly, Thursday | 5 business days |
| MRM Model Inventory & Validation | Continuous (Archer) | Register before development |
| Privacy Impact Assessment (PIA) | Continuous (OneTrust) | ~4 weeks |

The ARB review is specifically required for new client-facing integrations to payment systems,
the FCT Change Advisory requires FCC sign-off for hold/screening changes and observes a year-end
freeze (Dec-15 to Jan-05), and MRM Tier 2 model validation takes 10-14 weeks plus queue time —
these lead times are the planning constraints product teams must sequence against.

## Engagement routes and planning factors

Section 6 of the source directory gives first-pass sizing factors for cross-team dependency work,
calibrated from the trailing four program increments. Representative factors include: CBO Wire
Center squad (~6.5 hrs/story point, ~42 pts/sprint velocity, via Jira CBO); Payments Hub Engineering
(~8 hrs/point including vendor-platform and regression overhead, routed through the Payments
Platform Demand Board with a 6-8 week scheduling lead time); Financial Crimes Technology (~8
hrs/point plus a 20% independent compliance-testing overhead, via FCT Change Advisory and FCC
sign-off); Enterprise Notification Platform (~12 ENS hours per new event type, via a ServiceNow
"ENS Event Onboarding" request with a 6-week SLA); and Model Risk Management (EUA registration
~16 hours; Tier 2 validation 160-240 validator hours, via Archer). As of PI 27.1, Payments Hub
Engineering was noted as ~90% committed (driven by November-2026 address-enforcement work and
FedNow outbound), the heaviest reported commitment level among the listed teams.

## Program increment calendar

| PI | Dates | Planning event |
|---|---|---|
| PI 26.4 | 2026-09-07 to 2026-11-27 | Complete |
| PI 27.1 | 2026-12-01 to 2027-03-05 | PI planning 2026-11-17/18 (dependency asks due 2026-11-06) |
| PI 27.2 | 2027-03-15 to 2027-06-11 | PI planning 2027-03-02/03 |

## Escalation path

Dependency conflicts that cannot be resolved between engineering managers escalate first to the
respective Directors, then to the PTT Leadership Team, which meets weekly on Mondays. Compliance or
policy-interpretation questions are explicitly routed to FCC Policy & Advisory (Jordan Ellis) or the
Privacy Office (Ethan Brooks) rather than being decided by engineering teams — separating technical
dependency escalation from compliance/policy judgment calls.

## Related documents

CNB-ORG-PTT-2026-06 cross-references the following related documents, consistent with its role as
an org/ownership index into system- and architecture-level references maintained elsewhere in PTT:

| Related document | Relevance to this document |
|---|---|
| CBO-ARCH-WC-4.1 | Current-state architecture for the CBO Wire Center module owned by the CBO Wire Center squad |
| PPH-SYS-OVW-9.2 | System overview for PRISM Payments Hub (PPH), owned by Payments Hub Engineering |
| PNG-TDD-6.0 | Technical design document for the Payment Network Gateway connectors owned by PNE |
| PRSP-HMS-3.4 | Design reference for the PRSP Hold Management Service owned by FCT |
| ENS-INT-3.2 | Integration reference for the Enterprise Notification Service |
| TDIP-CAT-2026.2 | Catalog/reference for the Treasury Data & Insights Platform (TDIP) |

## Why this document exists

As an org and ownership directory rather than a technical architecture document, CNB-ORG-PTT-2026-06
exists to answer "who do I contact" and "how do I size this" questions that recur across every
cross-team payments initiative — dependency identification, intake routing, and planning-factor
estimation — and to make explicit which governance forums and lead times gate different classes of
change (client-facing payment integrations, hold/screening changes, model validation, and
client-data use). Its quarterly refresh cadence, combined with the explicit precedence of
interim organizational announcements, signals that it is meant to be a convenient, broadly accurate
baseline rather than a real-time directory.
