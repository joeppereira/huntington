---
type: Person
entity_id: omar-siddiqui
title: Omar Siddiqui
description: Engineering Manager on Global Transaction Services Integration (GTSI), accountable since 2026-10-01 for the Swift Alliance/gpi Connector, gpi Tracker integration, and all new intake for gpi data, Swift Tracker usage, and international wire status requests.
tags: [person, engineering-manager, gtsi, gpi, swift, cross-border-payments, knowledge-transfer]
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

Omar Siddiqui is the Engineering Manager (EM) on the **Global Transaction Services Integration (GTSI)** team, reporting into Elena Vasquez (Director, GTSI). As of **2026-10-01** he is the accountable engineering owner and single intake point for:

- gpi data requests,
- Swift Tracker usage, and
- international wire status capability requests.

This ownership was established by `CNB-MEMO-2026-09` ("Realignment of Cross-Border Network Integration"), which consolidated cross-border network capabilities that previously sat with Payment Networks Engineering (PNE) under GTSI.

## How requests reach him

From 2026-10-01, all new requests for gpi data, Swift Tracker usage, or international wire status capabilities must be raised as Jira issues in the **GTSI** project and directed to Omar Siddiqui, rather than opened against the legacy **PNG** (Payment Networks Engineering) project. Any requests already logged against PNG for gpi topics are triaged by GTSI during the knowledge-transfer period rather than being recreated.

GTSI's general planning factor is roughly 1 story point ≈ 7 engineering hours, intake runs through Jira GTSI with a quarterly roadmap cadence, and the team's capacity for PI 27.1 is noted as ~75% committed.

## Scope of ownership

The memo moved the following capabilities to GTSI, with Omar Siddiqui named EM (Hannah Lindqvist is Tech Lead):

| Capability | Moved from | Moved to | Accountable |
|---|---|---|---|
| Swift Alliance Gateway, gpi Connector (`SYS-PNG-GPI`), and gpi Tracker integration | Payment Networks Engineering (Raj Malhotra) | GTSI (Elena Vasquez) | Omar Siddiqui (EM); Hannah Lindqvist (Tech Lead) |
| Swift API gateway (Microgateway), SwiftNet PKI service accounts | Payment Networks Engineering | GTSI | Hannah Lindqvist |
| International wire tracking roadmap (incl. any client-facing gpi capability) | Payment Networks Engineering | GTSI | Elena Vasquez; business sponsor Laura Kim |

The **Fedwire Funds Connector (`SYS-PNG-FFC`)** did not move and remains with PNE under Raj Malhotra (Brian Walsh, EM); it is out of scope for Omar Siddiqui's team.

On the system-ownership register, `SYS-PNG-GPI` (Payment Network Gateway - Swift Alliance & gpi Connector) is a Tier 1 system whose technical owner is listed as Raj Malhotra / Tomasz Nowak pending the directory's Q4 refresh, since the organizational memo takes precedence over the not-yet-refreshed directory. Tomasz Nowak (Senior Engineer, gpi Connector) transferred from PNE to GTSI and now reports to Omar Siddiqui.

## Knowledge transfer in progress

Omar Siddiqui owns `GTSI-0112` ("Knowledge transfer: gpi Connector & Swift API gateway from PNE to GTSI"), an Epic in progress targeting completion **2026-12-15**, tracked per `CNB-MEMO-2026-09`. Until that date, PNE on-call remains secondary support for `SYS-PNG-GPI`. See [GTSI-0112 gpi Knowledge Transfer](../projects/gtsi-0112-gpi-knowledge-transfer.md) for the project itself.

He also owns `GTSI-0115` ("Swift gpi Tracker API contract renewal"), a To Do story tracking the Swift Tracker API contract's 250,000-calls/month quota and its renewal due **2027-01-31**.

## Relationship to the gpi Tracker Real-Time Service (GTSI-0107)

GTSI (not Omar Siddiqui individually, but his team under Elena Vasquez) owns the longer-term `GTSI-0107` initiative ("gpi Tracker Real-Time Service", a change-feed based internal API over the Swift gpi Tracker). It is not funded for 2026; discovery is planned for 2027-Q2 subject to the 2027 portfolio review, and the Payments ARB has not approved exposing the existing `GPI_TRACKER_SNAPSHOT` table directly to channels. Teams with near-term needs for gpi data are expected to engage GTSI (via Omar Siddiqui's intake route) early so their requirements can inform that discovery, since today's gpi Tracker integration is a 4-hour batch process with no internal real-time API.

## Team and reporting context

| Attribute | Value |
|---|---|
| Role | Engineering Manager (EM) |
| Team | Global Transaction Services Integration (GTSI) |
| Director | Elena Vasquez |
| Tech Lead (peer) | Hannah Lindqvist |
| Direct report (transferred) | Tomasz Nowak (Senior Engineer, gpi Connector) |
| Jira / Slack | Jira project GTSI; `#gtsi-crossborder` |
| Effective date of new scope | 2026-10-01 |

See also [GTSI team](../teams/gtsi.md) for the broader team directory entry.
