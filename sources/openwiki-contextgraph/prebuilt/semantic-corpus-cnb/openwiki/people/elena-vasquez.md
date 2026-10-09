---
type: Person
entity_id: elena-vasquez
title: Elena Vasquez
description: Director, Global Transaction Services Integration (GTSI) at Crestline National Bank; accountable leader for the Swift Alliance/gpi Connector, gpi Tracker integration, and the international wire tracking roadmap including the gpi Tracker Real-Time Service initiative (GTSI-0107).
tags: [people, gtsi, global-transaction-services-integration, director, swift, gpi, cross-border, payments-treasury-technology, engineering-leadership]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-95e454ddd82fc29fca46b0a9
    resource: repo://sources/estate/arb-pay-reg-2026q3-payments-arb-adr-register-and-minutes.md
  - id: openwiki-source-5c11d5768c3be60ea1158084
    resource: repo://sources/estate/cnb-memo-2026-09-realignment-of-cross-border-network-integration.md
  - id: openwiki-source-49303e801f124d97df9c3ea3
    resource: repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md
  - id: openwiki-source-4452149a3b4502b4c763a559
    resource: repo://sources/estate/jira-export-wt-discovery-2026-10-05.md
  - id: openwiki-source-0163a9a7923ee437e942692a
    resource: repo://sources/estate/png-tdd-6.0-payment-network-gateway-fedwire-and-gpi-technical-design.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

Elena Vasquez is **Director, Global Transaction Services Integration
(GTSI)** within Payments & Treasury Technology (PTT) at Crestline National
Bank (CNB). As of October 1, 2026 she is the accountable leader for
Crestline's cross-border payment network integrations — the Swift
Alliance Gateway and gpi Connector, the Swift gpi Tracker integration, and
the broader international wire tracking roadmap — following a
realignment that consolidated these capabilities under GTSI. She is also
the named owner of **GTSI-0107**, the gpi Tracker Real-Time Service
(GTRS) initiative.

## Role and organizational placement

Vasquez leads GTSI, one of the engineering organizations under PTT's CIO
line (**Gregory Hall**, MD, CIO Payments & Treasury Technology). Her
direct team contacts are **Omar Siddiqui** (Engineering Manager) and
**Hannah Lindqvist** (Tech Lead), who together with the rest of GTSI own
the CHIPS connector and nostro reconciliation integration in addition to
the cross-border capabilities realigned to the team in late 2026. GTSI's
intake is Jira project **GTSI** and Slack channel `#gtsi-crossborder`; the
team's planning factor is approximately 1 story point per 7 engineering
hours, with roadmap intake occurring quarterly.

See [GTSI](../teams/gtsi.md) for the team's full engagement and planning
details.

## The October 2026 cross-border realignment

Before October 1, 2026, the Swift Alliance Gateway, gpi Connector
(`SYS-PNG-GPI`), and gpi Tracker integration were owned by Payment
Networks Engineering (PNE) under **Raj Malhotra**. Per
**CNB-MEMO-2026-09** ("Realignment of Cross-Border Network Integration,"
issued by Gregory Hall), effective October 1, 2026 this capability —
along with the Swift API gateway (Microgateway), SwiftNet PKI service
accounts, and the international wire tracking roadmap (including any
client-facing gpi capability) — moved from PNE to GTSI, with Vasquez as
the accountable leader. The international wire tracking roadmap carries a
named business sponsor, **Laura Kim** (Director, Payments Platform
Product). The Fedwire Funds Connector (`SYS-PNG-FFC`) was explicitly
**not** part of this realignment and remains with PNE under Raj Malhotra.

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: an unescaped angle bracket inside a label breaks rendering; rephrase the label. -->
```text
graph TD
  GH["Gregory Hall<br/>MD, CIO Payments & Treasury Technology"]
  LK["Laura Kim<br/>Director, Payments Platform Product<br/>(business sponsor, wire tracking roadmap)"]
  EV["Elena Vasquez<br/>Director, GTSI"]
  RM["Raj Malhotra<br/>Director, Payment Networks Engineering"]
  GPI["Swift Alliance Gateway & gpi Connector<br/>(SYS-PNG-GPI), gpi Tracker integration"]
  FFC["Fedwire Funds Connector<br/>(SYS-PNG-FFC) - stays with PNE"]

  GH --> EV
  GH --> RM
  EV --> GPI
  LK -.->|business sponsor| GPI
  RM --> FFC
  RM -.->|transferred 2026-10-01| GPI
```

Key mechanics of the transition, per CNB-MEMO-2026-09:

- **People:** Tomasz Nowak (Senior Engineer, gpi Connector) transferred
  from PNE to GTSI, reporting to Omar Siddiqui.
- **Knowledge transfer:** tracked as **GTSI-0112** ("Knowledge transfer:
  gpi Connector & Swift API gateway from PNE to GTSI"), targeted to
  complete 2026-12-15. PNE on-call remains secondary support for
  `SYS-PNG-GPI` until that date.
- **Intake change:** from October 1, 2026, all new requests for gpi data,
  Swift Tracker usage, or international wire status capabilities must be
  raised in Jira project **GTSI** (directed to Omar Siddiqui) rather than
  PNE's **PNG** project; pre-existing PNG tickets for gpi topics are
  triaged by GTSI during the knowledge-transfer window.
- **Related but out of scope:** Raj Malhotra separately assumed ownership
  of the FedNow and RTP connectors from 2026-11-01 — an unrelated change
  bundled in the same memo but not part of the GTSI handoff.
- **Documentation lag:** the realignment memo pre-dates the quarterly
  PTT Organization & Ownership Directory (`CNB-ORG-PTT-2026-06`), whose
  Q4 refresh was expected to reflect the new ownership; the memo itself
  takes precedence over the directory until that refresh.

The existing Swift Alliance & gpi Connector (`SYS-PNG-GPI`) that Vasquez's
team inherits integrates with the Swift gpi Tracker via the Swift
Microgateway on a 4-hour batch cycle, upserting results into the Oracle
`GPI_TRACKER_SNAPSHOT` table consumed by Payment Operations' Investigations
Workbench and TDIP's nightly load; there is currently no internal API
exposing gpi status, and the snapshot table must not be exposed directly
to client channels.

## GTSI-0107: gpi Tracker Real-Time Service (GTRS)

Vasquez is the named owner of **GTSI-0107**, an initiative to build a
**gpi Tracker Real-Time Service** — an internal REST and event API built
over the Swift gpi Tracker change feed, intended to replace ad hoc batch
and snapshot-table access with a governed, quota-isolated service. As of
the October 2026 memo and the 2026-10-05 Jira export:

- GTSI-0107 is **Planned** but **not funded for 2026**; discovery is
  targeted for 2027-Q2 and build for 2027-Q3/Q4, subject to the 2027
  portfolio review.
- It supersedes an earlier, rejected PNE proposal (**PNG-1544**) to simply
  increase gpi Tracker batch frequency from 4 hours to 2 hours.
- The Payments Architecture Review Board (ARB), at its 2026-09-08 session,
  noted client demand for real-time gpi visibility but did **not**
  approve interim exposure of `GPI_TRACKER_SNAPSHOT` directly to channel
  teams; a read-only service with quota isolation would itself require
  ARB review before build.
- The Swift Tracker API contract (quota 250,000 calls/month, renewal
  2027-01-31, tracked as **GTSI-0115**) is cited as a hard constraint on
  design: naive per-payment lookups from client channels were estimated
  at roughly 1.9 million calls/month — about 7x the contract limit — so
  any real-time design must use a change-feed with internal fan-out
  rather than per-payment Tracker calls.
- Vasquez has indicated GTSI will scope GTSI-0107 after the GTSI-0112
  knowledge transfer completes, and has invited teams with near-term gpi
  needs (e.g., the Digital Treasury Channels team's backlogged spike
  `CBO-4480`, "International wire status visibility (gpi) for clients")
  to engage early so their requirements can inform discovery.

See [GTSI-0107: gpi Real-Time Service](../projects/gtsi-0107-gpi-real-time-service.md)
for the full initiative writeup.

## Related initiatives

- **GTSI-0112** — Knowledge transfer of the gpi Connector and Swift API
  gateway from PNE to GTSI, owned by Omar Siddiqui, targeted for
  2026-12-15 completion; this is the gating dependency before GTSI can
  independently support `SYS-PNG-GPI` and before GTSI-0107 discovery can
  be fully scoped.
- **GTSI-0115** — Swift gpi Tracker API contract renewal (quota 250,000
  calls/month; renewal due 2027-01-31), owned by Omar Siddiqui; the
  quota it governs is a key design constraint for GTSI-0107.
