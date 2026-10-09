---
type: Person
entity_id: hannah-lindqvist
title: Hannah Lindqvist
description: Tech Lead on Global Transaction Services Integration (GTSI), accountable for the Swift API gateway (Microgateway) and SwiftNet PKI service accounts, and Tech Lead for the Swift Alliance Gateway / gpi Connector capability transferred from Payment Networks Engineering.
tags: [person, tech-lead, gtsi, swift, pki, cross-border-payments, ownership]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-5c11d5768c3be60ea1158084
    resource: repo://sources/estate/cnb-memo-2026-09-realignment-of-cross-border-network-integration.md
  - id: openwiki-source-49303e801f124d97df9c3ea3
    resource: repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

Hannah Lindqvist is the Tech Lead on **Global Transaction Services Integration (GTSI)**, the team led by Director Elena Vasquez that owns Crestline National Bank's cross-border payment network integrations. She is one of the two accountable engineering leaders (alongside Engineering Manager Omar Siddiqui) named in the October 2026 realignment of cross-border network capabilities away from Payment Networks Engineering (PNE), and she has sole accountability for a distinct capability transferred in the same change: the Swift API gateway (Microgateway) and the SwiftNet PKI service accounts.

Within the existing PTT system ownership register, Hannah is also documented as GTSI's Tech Lead for the CHIPS connector and nostro reconciliation integration, work that predates and sits alongside the newly transferred Swift responsibilities.

## Role and accountabilities

| Capability | Prior owner | New owner (team) | Accountable leader(s) |
|---|---|---|---|
| Swift Alliance Gateway, gpi Connector (SYS-PNG-GPI) and gpi Tracker integration | Payment Networks Engineering (Raj Malhotra) | GTSI (Elena Vasquez) | Omar Siddiqui (EM); **Hannah Lindqvist (Tech Lead)** |
| Swift API gateway (Microgateway), SwiftNet PKI service accounts | Payment Networks Engineering | GTSI | **Hannah Lindqvist** |
| International wire tracking roadmap (incl. client-facing gpi capability) | Payment Networks Engineering | GTSI | Elena Vasquez; business sponsor Laura Kim |

Two distinct responsibilities follow from this table:

- **Shared technical leadership of the Swift Alliance Gateway / gpi Connector line (SYS-PNG-GPI).** Hannah is the named Tech Lead for this capability, working alongside Omar Siddiqui as Engineering Manager. This includes the gpi Tracker integration that moves with it.
- **Sole accountability for the Swift API gateway (Microgateway) and SwiftNet PKI service accounts.** Unlike the gpi Connector line, this capability lists Hannah Lindqvist as the only named accountable leader, making her the point of contact for the Microgateway and for the lifecycle and custody of SwiftNet PKI service accounts once they move to GTSI.

The international wire tracking roadmap (including any client-facing gpi capability) is accountable to Elena Vasquez and business sponsor Laura Kim rather than to Hannah directly, though it is closely related to the gpi capabilities Hannah co-leads.

Separately from this realignment, the PTT Organization & Ownership Directory lists Hannah as GTSI's Tech Lead contact for the **CHIPS connector** and **nostro reconciliation integration**, reflecting GTSI's broader cross-border and correspondent-banking integration remit beyond the Swift-specific work above.

## Organizational context

- **Team:** Global Transaction Services Integration (GTSI), led by Director Elena Vasquez. See [GTSI](../teams/gtsi.md).
- **Key peer:** Omar Siddiqui, Engineering Manager, GTSI — co-accountable for the Swift Alliance Gateway / gpi Connector line and the manager to whom transferring PNE engineer Tomasz Nowak now reports.
- **Prior owning team:** Payment Networks Engineering (PNE), led by Director Raj Malhotra, which built and ran the Swift Alliance Gateway, gpi Connector, and SwiftNet PKI service accounts before the October 2026 transfer.
- **Engagement route:** From October 1, 2026, new requests for gpi data, Swift Tracker usage, or international wire status capabilities are raised in Jira project **GTSI** and directed to Omar Siddiqui; existing PNE (project PNG) tickets on these topics are triaged by GTSI during knowledge transfer rather than being re-opened against PNE.

## Related systems

- [Swift gpi Connector](../systems/swift-gpi-connector.md) (SYS-PNG-GPI) — the Swift Alliance Gateway and gpi Connector system that Hannah co-leads technically within GTSI after the transfer; its prior technical owners at PNE were Raj Malhotra and Tomasz Nowak.
- Swift API gateway (Microgateway) — the Swift-facing API gateway component moved to GTSI with Hannah as sole accountable leader.
- SwiftNet PKI service accounts — cryptographic service account identities used for SwiftNet connectivity, moved to GTSI under Hannah's accountability.

## Timeline and transition details

- **2026-09-02:** Realignment announced via CNB-MEMO-2026-09 (Office of the CIO, Payments & Treasury Technology), issued by Gregory Hall, MD.
- **2026-10-01:** Effective date of the transfer of the Swift Alliance Gateway/gpi Connector, the Swift API gateway (Microgateway), and SwiftNet PKI service accounts from PNE to GTSI.
- **Until 2026-12-15:** PNE on-call remains secondary support for SYS-PNG-GPI while knowledge transfer (tracked as GTSI-0112) completes.
- **2026-12 (Q4):** The PTT Organization & Ownership Directory (CNB-ORG-PTT-2026-06) is scheduled to be refreshed to reflect Hannah's and GTSI's expanded ownership formally; the version reviewed for this page (2026.2, published 2026-06-15) predates the realignment and still shows the gpi Connector under PNE.

## Related roadmap items

GTSI, the team Hannah leads technically alongside Omar Siddiqui, also owns two roadmap items connected to the transferred Swift capabilities:

- **GTSI-0107** — gpi Tracker Real-Time Service initiative; not funded for 2026, with discovery planned for 2027-Q2 subject to the 2027 portfolio review.
- **GTSI-0115** — Swift Tracker API contract renewal, due 2027-01-31.

## Notes and caveats

The PTT Organization & Ownership Directory (CNB-ORG-PTT-2026-06, published 2026-06-15) predates the September 2026 realignment memo and was not yet refreshed to show the Swift Alliance Gateway/gpi Connector or the Microgateway/PKI service accounts under GTSI or Hannah Lindqvist; it only reflects her pre-existing CHIPS connector and nostro reconciliation integration role. The realignment memo (CNB-MEMO-2026-09) states organizational announcements issued between quarterly directory refreshes take precedence, so the responsibilities described in the Role and accountabilities table above are authoritative pending the directory's Q4 refresh.
