---
type: Person
entity_id: brian-walsh
title: Brian Walsh
description: Engineering Manager, Fedwire within Payment Networks Engineering (PNE) at Crestline National Bank; technical co-owner of the Fedwire Funds Connector (SYS-PNG-FFC).
tags: [people, payment-networks-engineering, fedwire, fedwire-funds-connector, engineering-manager, payments-treasury-technology]
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
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

Brian Walsh is **Engineering Manager, Fedwire**, within **Payment Networks
Engineering (PNE)**, part of Payments & Treasury Technology (PTT) at
Crestline National Bank (CNB). He is one of two named technical owners —
alongside **Chen Wei**, Tech Lead for Fedwire — of the **Fedwire Funds
Connector (FFC, system ID `SYS-PNG-FFC`)**, the Tier 1 (24x7 critical)
system that gives CNB its domestic ISO 20022 connectivity to the Federal
Reserve's Fedwire Funds Service. See
[Fedwire Funds Connector](../systems/fedwire-funds-connector.md) for the
system itself.

## Role and reporting line

Walsh reports to **Raj Malhotra**, Director of Payment Networks Engineering,
and leads the Fedwire engineering stream within PNE alongside Chen Wei
(Tech Lead, Fedwire). PNE as a whole is one of the engineering teams under
Payments & Treasury Technology, led at the top by **Gregory Hall** (MD,
CIO Payments & Treasury Technology). Business ownership of FFC sits
separately with **Laura Kim**, Director of Payments Platform Product and
Business Data Owner for payment datasets — following PTT's general pattern
of splitting business ownership (roadmap, prioritization) from engineering
ownership (technical design authority, on-call/support accountability),
which Walsh holds for FFC jointly with Chen Wei.

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: an unescaped angle bracket inside a label breaks rendering; rephrase the label. -->
```text
graph TD
  GH["Gregory Hall<br/>MD, CIO Payments & Treasury Technology"]
  RM["Raj Malhotra<br/>Director, Payment Networks Engineering (PNE)"]
  BW["Brian Walsh<br/>EM, Fedwire"]
  CW["Chen Wei<br/>Tech Lead, Fedwire"]
  FFC["SYS-PNG-FFC<br/>Fedwire Funds Connector (Tier 1)"]
  LK["Laura Kim<br/>Director, Payments Platform Product<br/>(Business Owner)"]

  GH --> RM
  RM --> BW
  RM --> CW
  BW --> FFC
  CW --> FFC
  LK -.->|Business Owner| FFC
```

Before an October 2026 organizational realignment, PNE also owned the
Swift Alliance & gpi Connector (`SYS-PNG-GPI`) under Tomasz Nowak (Senior
Engineer). That capability — along with the Swift API gateway
(Microgateway), SwiftNet PKI service accounts, and the international wire
tracking roadmap — moved to Global Transaction Services Integration (GTSI)
under Elena Vasquez, effective 2026-10-01. The Fedwire Funds Connector was
explicitly called out as **not** part of that move: it remains with PNE
under Raj Malhotra, with Walsh continuing as the accountable Fedwire
engineering manager. PNE on-call retained secondary support for
`SYS-PNG-GPI` only through a knowledge-transfer window ending 2026-12-15;
that does not affect Walsh's FFC responsibilities.

## System ownership: Fedwire Funds Connector (SYS-PNG-FFC)

Walsh and Wei are jointly listed as technical owner of record for
`SYS-PNG-FFC` in CNB's system ownership register, with Laura Kim as
business owner and a Tier 1 (24x7 critical) support classification. FFC is
the Payment Network Gateway module that connects CNB to the Fedwire Funds
Service over FedLine Direct (dual MQ channels, primary Columbus /
contingency Charlotte), exchanging ISO 20022 messages (`pacs.008`,
`pacs.009`, `pacs.004`, `camt.056`, `camt.110` outbound; `pacs.008` /
`pacs.009` / `pacs.004`, `pacs.002` acknowledgments, and `admi.002` errors
inbound) since the Federal Reserve's single-day ISO 20022 cutover on
2025-07-14. As technical owner, Walsh's team is accountable for FFC's
connectivity, acknowledgment handling (publishing Fed `pacs.002`
acknowledgments to `net.fedwire.ack.v1` and inbound messages to
`net.fedwire.inbound.v1`, both ACL-owned by PNE), and operational support
of a Tier 1 system that PRISM Payments Hub (PPH) depends on to release
Fedwire-bound wires. See [PNG-TDD-6.0](../documents/png-tdd-6.0.md) for the
full technical design and
[Fedwire Network Ack Topics](../interfaces/fedwire-network-ack-topics.md)
for the published topics FFC owns.

## Engagement and planning

New engineering demand for FFC is raised through Jira project **PNG** and
the **#payment-networks** Slack channel, which Walsh's team monitors
alongside the rest of PNE. PNE's standing change windows run
Saturdays 22:00–02:00 ET, and its planning factor is approximately 1 story
point per 8 engineering hours; as of the PI 27.1 planning cycle, PNE
capacity was reported at roughly 80% committed. Requests that previously
touched gpi/Swift Tracker topics should be routed to GTSI (Omar Siddiqui)
rather than PNG from 2026-10-01 onward; Fedwire-specific requests continue
to go through Walsh's team via the PNG project.

## Related pages

- [Fedwire Funds Connector](../systems/fedwire-funds-connector.md) — the
  system Walsh co-owns.
- [Fedwire Funds Service](../concepts/fedwire-funds-service.md) — the
  Federal Reserve rail FFC connects to.
- [PNG-TDD-6.0](../documents/png-tdd-6.0.md) — the technical design
  document for both Payment Network Gateway modules.
