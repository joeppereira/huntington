---
type: Person
entity_id: gregory-hall
title: Gregory Hall
description: MD, CIO Payments & Treasury Technology at Crestline National Bank; top engineering leader of PTT and sole issuer/approver of CNB-MEMO-2026-09, which realigned cross-border Swift network ownership from Payment Networks Engineering to GTSI.
tags: [people, payments-treasury-technology, ptt, cio, engineering-leadership, cnb, organizational-announcement, governance]
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

Gregory Hall is **Managing Director, CIO Payments & Treasury Technology
(PTT)** at Crestline National Bank (CNB). He is the single accountable
leader for all PTT engineering — channels, the payments hub, payment
networks, and payments data — and the approver of record for both the
quarterly PTT Organization, System Ownership & Engagement Directory
(**CNB-ORG-PTT-2026-06**) and the organizational announcements issued
between its refreshes. He authored and signed
**CNB-MEMO-2026-09**, "Realignment of Cross-Border Network Integration,"
issued 2026-09-02 and effective 2026-10-01, which moved ownership of
Crestline's Swift-based cross-border network capabilities from Payment
Networks Engineering (PNE) to Global Transaction Services Integration
(GTSI).

## Role and organizational placement

Hall sits at the top of the PTT engineering organization, which spans the
Digital Treasury Channels teams (CBO Wire Center squad, CBO Platform &
Entitlements), Payments Hub Engineering, Payment Networks Engineering
(PNE), Global Transaction Services Integration (GTSI), Financial Crimes
Technology, Enterprise Notification Platform, and Treasury Data &
Analytics (TDIP). Business ownership of products — Treasury Management
products, Crestline Business Online, the PRISM Payments Hub — is held
separately by product-side leaders (Danielle Okafor, Marcus Chen, Laura
Kim) who are peers rather than reports in Hall's CIO line; architecture
and second-line partners (Chief Architect Nikhil Bose, Chief BSA/AML
Officer Catherine Doyle, Head of Model Risk Management Jonathan Price,
Chief Privacy Officer Rachel Goldberg) sit alongside him as governance
counterparts whose sign-off gates specific classes of PTT change. He is
the sole named approver of **CNB-ORG-PTT-2026-06**, the PTT Business
Management Office's quarterly reference for system ownership,
accountable leaders, and engagement routes across PTT and its first- and
second-line partners. See
[Payments & Treasury Technology (PTT)](../organizations/payments-treasury-technology.md)
for the full org chart, system ownership register, and governance forums
Hall's organization operates under.

## CNB-MEMO-2026-09: the cross-border network realignment

On 2026-09-02, Hall issued **CNB-MEMO-2026-09** to PTT Leadership,
Treasury Management Products, and Payment Operations, framing the change
as a response to growing cross-border volumes and Swift's ISO 20022
roadmap continuing beyond the end of MT/MX coexistence. Effective
2026-10-01, the memo consolidated cross-border network capabilities under
a single accountable leader, Elena Vasquez (Director, GTSI):

- **Moved to GTSI:** the Swift Alliance Gateway and gpi Connector
  (`SYS-PNG-GPI`) and gpi Tracker integration (accountable leads Omar
  Siddiqui, EM, and Hannah Lindqvist, Tech Lead); the Swift API gateway
  (Microgateway) and SwiftNet PKI service accounts (Hannah Lindqvist);
  and the international wire tracking roadmap, including any
  client-facing gpi capability (Elena Vasquez, with business sponsor
  Laura Kim).
- **Explicitly not moved:** the Fedwire Funds Connector (`SYS-PNG-FFC`,
  including the `net.fedwire.ack.v1` and `net.fedwire.inbound.v1`
  topics), which remains with PNE under Raj Malhotra (EM Brian Walsh).
  Raj Malhotra additionally assumed ownership of the FedNow and RTP
  connectors from 2026-11-01, separate from the cross-border transfer.
- **People change:** Tomasz Nowak (Senior Engineer, gpi Connector)
  transferred from PNE to GTSI, reporting to Omar Siddiqui.
- **Transition mechanics:** PNE on-call remained secondary support for
  `SYS-PNG-GPI` until 2026-12-15, when knowledge transfer tracked as
  **GTSI-0112** was to complete. From 2026-10-01, all new requests for
  gpi data, Swift Tracker usage, or international wire status
  capabilities had to be raised in Jira project **GTSI** (directed to
  Omar Siddiqui) rather than PNE's **PNG** project; tickets already
  logged against PNG for gpi topics were triaged by GTSI during the
  transfer rather than reopened in PNG.
- **Roadmap note:** GTSI was assigned ownership of the gpi Tracker
  Real-Time Service initiative (**GTSI-0107**), which the memo states is
  not funded for 2026, with discovery planned for 2027-Q2 subject to the
  2027 portfolio review; teams with near-term gpi data needs were asked
  to engage GTSI early so requirements could inform that discovery. GTSI
  was also made responsible for the Swift Tracker API contract renewal
  due 2027-01-31 (**GTSI-0115**).

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: an unescaped angle bracket inside a label breaks rendering; rephrase the label. -->
```text
graph TD
  GH["Gregory Hall<br/>MD, CIO Payments & Treasury Technology<br/>(author/approver, CNB-MEMO-2026-09)"]
  RM["Raj Malhotra<br/>Director, Payment Networks Engineering"]
  EV["Elena Vasquez<br/>Director, GTSI"]
  FFC["Fedwire Funds Connector (SYS-PNG-FFC)<br/>stays with PNE"]
  FEDNOW["FedNow / RTP connectors<br/>to PNE from 2026-11-01"]
  GPI["Swift Alliance Gateway, gpi Connector (SYS-PNG-GPI),<br/>gpi Tracker integration, Swift API gateway,<br/>SwiftNet PKI, int'l wire tracking roadmap"]

  GH -->|signs| RM
  GH -->|signs| EV
  RM --> FFC
  RM --> FEDNOW
  RM -.->|transferred 2026-10-01| GPI
  EV --> GPI
```

Hall's memo also notes that CNB-ORG-PTT-2026-06, the quarterly directory
normally approved by Hall, lagged the announcement — it was published
2026-06-15 and would not reflect the realignment until its Q4 refresh —
so the directory's own governing principle (that organizational
announcements issued between refreshes take precedence) applied directly
to a transfer Hall himself ordered. The memo closes by thanking Raj
Malhotra and the PNE team for building and running the transferred
services and Elena Vasquez's team for taking them forward.

## Related documents and pages

- [CNB-MEMO-2026-09](../documents/cnb-memo-2026-09.md) — the realignment
  memo itself, authored and signed by Hall.
- [CNB-ORG-PTT-2026-06](../documents/cnb-org-ptt-2026-06.md) — the
  quarterly PTT directory Hall approves, listing him as MD and scoping
  his authority over all PTT engineering.
- [Payments & Treasury Technology (PTT)](../organizations/payments-treasury-technology.md)
  — the organization Hall leads, including its full engineering team
  directory, system ownership register, and governance forums.
- [Elena Vasquez](elena-vasquez.md) — Director, GTSI, the accountable
  leader Hall's memo designated for the transferred cross-border
  capabilities.
