---
type: Person
entity_id: laura-kim
title: Laura Kim
description: Director, Payments Platform Product at Crestline National Bank; Product Owner of PRISM Payments Hub, Business Data Owner for payment datasets, and business sponsor of the Swift gpi tracking roadmap.
tags: [people, payments, product-owner, data-owner, prism-payments-hub, ptt, gpi]
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

Laura Kim is the **Director, Payments Platform Product** within Payments & Treasury
Technology (PTT) at Crestline National Bank. She sits in the PTT leadership line
reporting into Gregory Hall (MD, CIO Payments & Treasury Technology), alongside
peers such as Marcus Chen (Director, Digital Treasury Product) and Nikhil Bose
(Chief Architect, Payments & Treasury).

Laura Kim holds three distinct, related roles:

- **Product Owner of PRISM Payments Hub (SYS-PPH)** — the core payments
  processing system (Volaris 9.4), engineered by
  [Payments Hub Engineering](../teams/payments-hub-engineering.md) under
  Raymond Ortiz (Director).
- **Business Data Owner for payment datasets** — the accountable business
  owner of record for multiple Tier-1/Tier-2 payment systems' data, including
  SYS-PPH, the Fedwire Funds Connector (SYS-PNG-FFC), the Swift Alliance & gpi
  Connector (SYS-PNG-GPI), and the payment-data slice of the Treasury Data &
  Insights Platform (SYS-TDIP).
- **Business sponsor of the international wire tracking / gpi roadmap** —
  named sponsor for the cross-border wire-tracking capability, including any
  client-facing Swift gpi functionality, following its 2026 realignment to
  Global Transaction Services Integration (GTSI).

## Responsibilities

### Product ownership of PRISM Payments Hub

As Product Owner of [PRISM Payments Hub](../systems/prism-payments-hub.md),
Laura Kim is the business-side counterpart to the engineering leadership of
[Payments Hub Engineering](../teams/payments-hub-engineering.md) (Raymond
Ortiz, Director; Kevin O'Brien, EM; Sunita Rao, Principal Engineer). Demand for
PPH roadmap changes is prioritized through the monthly **Payments Platform
Demand Board**, which Laura Kim's product ownership role feeds into; engineering
capacity for PPH work is planned at roughly 1 story point per 8 engineering
hours (vendor platform plus regression testing) and was tracked at ~90%
committed for PI 26.4, including Fedwire address-enforcement and FedNow
outbound work landing in November 2026.

### Business Data Owner for payment datasets

Laura Kim is recorded as the accountable **business owner** in the PTT system
ownership register for:

| System ID | System | Technical owner | Tier |
|---|---|---|---|
| SYS-PPH | PRISM Payments Hub (Volaris 9.4) | Kevin O'Brien / Sunita Rao | T1 |
| SYS-PNG-FFC | Payment Network Gateway – Fedwire Funds Connector | Brian Walsh / Chen Wei (PNE) | T1 |
| SYS-PNG-GPI | Payment Network Gateway – Swift Alliance & gpi Connector | Raj Malhotra / Tomasz Nowak (PNE, pre-realignment) | T1 |
| SYS-TDIP | Treasury Data & Insights Platform (payment data) | Carlos Mendes (TDIP) | T2 |

This spans ownership across teams she does not manage directly (Payment
Networks Engineering, TDIP), which places her as the single business
accountability point for payment data regardless of which engineering team
currently holds technical ownership of the underlying system.

### Business sponsor of the gpi tracking roadmap

Under the September 2026 organizational realignment of cross-border network
integration (effective **October 1, 2026**), ownership of the Swift Alliance
Gateway, gpi Connector (SYS-PNG-GPI), gpi Tracker integration, and the broader
**international wire tracking roadmap** moved from Payment Networks
Engineering (Raj Malhotra) to Global Transaction Services Integration (Elena
Vasquez, Director; Omar Siddiqui, EM; Hannah Lindqvist, Tech Lead). Laura Kim
was named the **business sponsor** of that international wire tracking
roadmap, including any client-facing gpi capability, carrying her payment-data
business-ownership accountability forward across the engineering-team
transition.

Within that roadmap, GTSI separately owns the **gpi Tracker Real-Time Service**
initiative (GTSI-0107, not funded for 2026; discovery planned 2027-Q2 subject
to portfolio review) and the **Swift Tracker API contract renewal** due
2027-01-31 (GTSI-0115). Teams with near-term needs for gpi data are directed to
engage GTSI early so requirements can inform the 2027-Q2 discovery work. From
October 1, 2026, new requests for gpi data, Swift Tracker usage, or
international wire status capabilities are raised in Jira project **GTSI**
rather than **PNG**; PNE on-call remained secondary support for SYS-PNG-GPI
only until 2026-12-15, pending knowledge transfer (GTSI-0112).

## Relationships

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: an unescaped angle bracket inside a label breaks rendering; rephrase the label. -->
```text
flowchart LR
    GH[Gregory Hall<br/>MD, CIO PTT] --> LK[Laura Kim<br/>Director, Payments Platform Product]
    LK -->|Product Owner| PPH[PRISM Payments Hub<br/>SYS-PPH]
    LK -->|Business Data Owner| FFC[Fedwire Funds Connector<br/>SYS-PNG-FFC]
    LK -->|Business Data Owner| GPI[Swift Alliance & gpi Connector<br/>SYS-PNG-GPI]
    LK -->|Business Data Owner, payment data| TDIP[Treasury Data & Insights Platform<br/>SYS-TDIP]
    LK -->|Business sponsor| ROADMAP[International wire tracking<br/>/ gpi roadmap]
    PHE[Payments Hub Engineering<br/>Raymond Ortiz] -->|Technical owner| PPH
    PNE[Payment Networks Engineering<br/>Raj Malhotra] -->|Technical owner, FFC| FFC
    GTSI[GTSI<br/>Elena Vasquez] -->|Technical owner, GPI post 2026-10-01| GPI
    GTSI -->|Owns roadmap delivery| ROADMAP
```

- **[Payments Hub Engineering](../teams/payments-hub-engineering.md)** (Raymond
  Ortiz, Director) is the engineering team Laura Kim partners with most
  directly, as Product Owner of its flagship system,
  [PRISM Payments Hub](../systems/prism-payments-hub.md).
- **Payment Networks Engineering** (Raj Malhotra, Director) remains the
  technical owner of the Fedwire Funds Connector (SYS-PNG-FFC), for which
  Laura Kim is business data owner; Raj Malhotra's team also absorbs the
  FedNow and RTP connectors from 2026-11-01.
- **Global Transaction Services Integration (GTSI)** (Elena Vasquez, Director;
  Omar Siddiqui, EM; Hannah Lindqvist, Tech Lead) is the new technical owner,
  from October 1, 2026, of the Swift Alliance Gateway, gpi Connector, and gpi
  Tracker integration that underpin the roadmap Laura Kim sponsors.
- **Treasury Data & Analytics (TDIP)** (Wei Zhang, Director; Carlos Mendes, EM
  Data Engineering) is the technical owner of SYS-TDIP, for which Laura Kim
  is business owner of the payment-data slice.
- **Marcus Chen** (Director, Digital Treasury Product) is Laura Kim's
  Payments & Treasury Technology leadership peer, holding the parallel Product
  Owner role for CBO Wire Center and Payments & Transfers.

## Governance touchpoints

Roadmap and demand decisions affecting systems Laura Kim owns or sponsors pass
through PTT governance forums, notably:

- **Payments Platform Demand Board** — monthly; prioritizes the PPH roadmap
  that Laura Kim product-owns; requests due by prior month-end.
- **Payments Architecture Review Board (ARB)** — monthly (2nd Tuesday), chaired
  by Nikhil Bose; required for new client-facing integrations to payment
  systems, including client-facing gpi capability under the wire-tracking
  roadmap; 10 business days submission lead time.

## Source notes

Laura Kim's roles and system associations are documented in the PTT
Organization, System Ownership & Engagement Directory (CNB-ORG-PTT-2026-06,
published 2026-06-15, next refresh 2026-12), which is the quarterly reference
for PTT system ownership. Changes to the gpi/wire-tracking portion of her
sponsorship took effect via the Realignment of Cross-Border Network
Integration announcement (CNB-MEMO-2026-09, effective 2026-10-01), which
organizational announcements take precedence over the directory until its
next quarterly refresh.
