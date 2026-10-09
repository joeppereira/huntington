---
type: Person
entity_id: raj-malhotra
title: Raj Malhotra
description: Director, Payment Networks Engineering (PNE) at Crestline National Bank; retained ownership of the Fedwire Funds Connector through the 2026-10-01 cross-border realignment and assumed ownership of the FedNow and RTP connectors from 2026-11-01.
tags: [people, payment-networks-engineering, director, fedwire, fedwire-funds-connector, fednow, rtp, swift-gpi, payments-treasury-technology, engineering-leadership, ownership-transfer]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-5c11d5768c3be60ea1158084
    resource: repo://sources/estate/cnb-memo-2026-09-realignment-of-cross-border-network-integration.md
  - id: openwiki-source-49303e801f124d97df9c3ea3
    resource: repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md
  - id: openwiki-source-0163a9a7923ee437e942692a
    resource: repo://sources/estate/png-tdd-6.0-payment-network-gateway-fedwire-and-gpi-technical-design.md
  - id: openwiki-source-19beabaf3acaad354d39ee1e
    resource: repo://sources/estate/pph-sys-ovw-9.2-prism-payments-hub-system-overview-and-lifecycle-state-model.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

Raj Malhotra is **Director, Payment Networks Engineering (PNE)** within
Payments & Treasury Technology (PTT) at Crestline National Bank (CNB).
Before October 2026 he was PNE's accountable leader for both of the
bank's payment-network gateway systems — the **Fedwire Funds Connector**
(`SYS-PNG-FFC`) and the **Swift Alliance Gateway & gpi Connector**
(`SYS-PNG-GPI`). **CNB-MEMO-2026-09** ("Realignment of Cross-Border
Network Integration," issued by Gregory Hall, effective 2026-10-01)
narrowed PNE's cross-border scope by moving the Swift/gpi capability to
Global Transaction Services Integration (GTSI) under Elena Vasquez, while
explicitly keeping the Fedwire Funds Connector with Malhotra. The same
memo then widened PNE's domestic scope again: effective **2026-11-01**,
Malhotra additionally assumed ownership of the **FedNow and RTP
connectors**, so PNE's net trajectory across the two memo dates is a
swap of cross-border Swift responsibility for domestic instant-payments
responsibility rather than a simple reduction.

## Role and organizational placement

Malhotra reports into Payments & Treasury Technology's engineering line,
led by **Gregory Hall** (MD, CIO Payments & Treasury Technology), as one
of several engineering directors alongside Payments Hub Engineering
(Raymond Ortiz), GTSI (Elena Vasquez), and others. Within PNE, Malhotra's
named direct contacts are **Brian Walsh** (Engineering Manager, Fedwire)
and **Chen Wei** (Tech Lead, Fedwire); before the realignment, **Tomasz
Nowak** (Senior Engineer, gpi Connector) also reported into PNE before
transferring to GTSI under Omar Siddiqui. Business ownership of PNE's
systems sits separately with **Laura Kim**, Director of Payments Platform
Product and Business Data Owner for payment datasets, consistent with
PTT's general split between business ownership (roadmap, prioritization)
and engineering ownership (technical design authority, on-call/support
accountability) that Malhotra holds on the engineering side. See
[Payment Networks Engineering](../teams/payment-networks-engineering.md)
for the team's full engagement and planning details.

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: an unescaped angle bracket inside a label breaks rendering; rephrase the label. -->
```text
graph TD
  GH["Gregory Hall<br/>MD, CIO Payments & Treasury Technology"]
  RM["Raj Malhotra<br/>Director, Payment Networks Engineering (PNE)"]
  BW["Brian Walsh<br/>EM, Fedwire"]
  CW["Chen Wei<br/>Tech Lead, Fedwire"]
  FFC["SYS-PNG-FFC<br/>Fedwire Funds Connector (Tier 1)<br/>retained by PNE"]
  FEDNOW["FedNow connector<br/>assumed 2026-11-01"]
  RTP["RTP connector<br/>assumed 2026-11-01"]
  GPI["SYS-PNG-GPI<br/>Swift Alliance Gateway & gpi Connector<br/>moved to GTSI 2026-10-01"]
  EV["Elena Vasquez<br/>Director, GTSI"]
  LK["Laura Kim<br/>Director, Payments Platform Product<br/>(Business Owner)"]

  GH --> RM
  RM --> BW
  RM --> CW
  BW --> FFC
  CW --> FFC
  RM --> FEDNOW
  RM --> RTP
  RM -.->|transferred 2026-10-01| GPI
  GPI --> EV
  LK -.->|Business Owner| FFC
```

## The 2026-10-01 cross-border realignment: what PNE kept

Per **CNB-MEMO-2026-09** (issued 2026-09-02 by Gregory Hall, effective
2026-10-01), three cross-border capability areas moved out of PNE to
GTSI: the Swift Alliance Gateway/gpi Connector (`SYS-PNG-GPI`) and gpi
Tracker integration, the Swift API gateway (Microgateway) and SwiftNet
PKI service accounts, and the international wire tracking roadmap
(including any client-facing gpi capability). The memo is explicit that
the **Fedwire Funds Connector (`SYS-PNG-FFC`)**, including the
`net.fedwire.ack.v1` and `net.fedwire.inbound.v1` topics it owns, **does
not move** and remains with Payment Networks Engineering under Malhotra,
with Brian Walsh continuing as Engineering Manager. PNE's on-call
retained only secondary support for `SYS-PNG-GPI` through a
knowledge-transfer window (**GTSI-0112**) targeted to complete
2026-12-15; that transitional duty does not touch Malhotra's FFC
accountability. From 2026-10-01, new demand for gpi data, Swift Tracker
usage, or international wire status capability is raised against Jira
project **GTSI** rather than PNE's **PNG** project.

## The 2026-11-01 change: FedNow and RTP connector ownership

The same memo separately states that Malhotra **additionally assumes
ownership of the FedNow and RTP connectors from 2026-11-01**. This is an
unrelated change bundled into CNB-MEMO-2026-09 alongside the cross-border
handoff: it adds domestic instant-payments connector scope to PNE rather
than following from the Swift/gpi transfer. The memo does not name an
engineering manager, tech lead, or system ID for the FedNow/RTP
connectors, and as of CNB-ORG-PTT-2026-06's last published refresh
(2026.2, 2026-06-15 — before either 2026-10-01 or 2026-11-01 took
effect) the system ownership register still lists only `SYS-PNG-FFC` and
`SYS-PNG-GPI` under PNE; the directory's Q4 refresh was expected to
reflect the realignment but had not yet published the FedNow/RTP
addition as of the sources reviewed here. Separately, the PRISM Payments
Hub system overview lists a **FedNow outbound expansion** as a PI 27.1
commitment, and CNB-ORG-PTT-2026-06's PI 27.1 capacity note for Payments
Hub Engineering flags "FedNow outbound" alongside November 2026 address
enforcement as a driver of that team's ~90% committed capacity — placing
Malhotra's new FedNow connector ownership in PNE alongside a related,
separately owned initiative in Payments Hub Engineering.

## System ownership: Fedwire Funds Connector (SYS-PNG-FFC)

CNB's system ownership register lists PNE as the owning team for
`SYS-PNG-FFC` (Payment Network Gateway - Fedwire Funds Connector), with
Brian Walsh and Chen Wei as technical owners, Laura Kim as business
owner, and a Tier 1 (24x7 critical) support classification. Malhotra is
also listed as document owner (with Chen Wei for Fedwire and, before the
realignment, Tomasz Nowak for gpi) and as an approver, alongside Chief
Architect Nikhil Bose, of **PNG-TDD-6.0** ("Payment Network Gateway -
Fedwire and gpi Technical Design"), the technical design document
covering both connectors. See
[Fedwire Funds Connector](../systems/fedwire-funds-connector.md) for the
system itself.

## Engagement and planning

New engineering demand for PNE-owned systems is raised through Jira
project **PNG** and the **#payment-networks** Slack channel. PNE's
standing change windows run Saturdays 22:00–02:00 ET, and its planning
factor is approximately 1 story point per 8 engineering hours; as of the
PI 27.1 planning cycle (dependency asks due 2026-11-06, PI planning
2026-11-17/18), PNE capacity was reported at roughly 80% committed.
Requests touching gpi data, Swift Tracker usage, or international wire
status should be routed to GTSI (Omar Siddiqui) via Jira project GTSI
rather than PNG from 2026-10-01 onward; Fedwire, and from 2026-11-01
FedNow and RTP, requests continue to go through Malhotra's team via the
PNG project.

## Relationships

- leads: [Payment Networks Engineering](../teams/payment-networks-engineering.md)
- retains ownership of: [Fedwire Funds Connector](../systems/fedwire-funds-connector.md) (`SYS-PNG-FFC`), per [CNB-MEMO-2026-09](../documents/cnb-memo-2026-09.md)
- transferred ownership of the Swift Alliance Gateway/gpi Connector (`SYS-PNG-GPI`) to: Elena Vasquez / [GTSI](../teams/gtsi.md), effective 2026-10-01, per [CNB-MEMO-2026-09](../documents/cnb-memo-2026-09.md)
- assumed ownership of: the FedNow and RTP connectors, effective 2026-11-01, per [CNB-MEMO-2026-09](../documents/cnb-memo-2026-09.md)
- reports to: Gregory Hall (MD, CIO Payments & Treasury Technology)
- works with: Brian Walsh (EM, Fedwire), Chen Wei (Tech Lead, Fedwire), Laura Kim (business owner, payment datasets)
- predates in the directory: [CNB-ORG-PTT-2026-06](../documents/cnb-org-ptt-2026-06.md), which as last published (2026.2, 2026-06-15) had not yet reflected either the 2026-10-01 or 2026-11-01 changes

## Related pages

- [Fedwire Funds Connector](../systems/fedwire-funds-connector.md) — the Tier 1 system Malhotra's team continues to own
- [Payment Networks Engineering](../teams/payment-networks-engineering.md) — the team Malhotra directs
- [CNB-MEMO-2026-09](../documents/cnb-memo-2026-09.md) — the memo establishing both the 2026-10-01 and 2026-11-01 changes
- [CNB-ORG-PTT-2026-06](../documents/cnb-org-ptt-2026-06.md) — the quarterly directory predating the realignment
