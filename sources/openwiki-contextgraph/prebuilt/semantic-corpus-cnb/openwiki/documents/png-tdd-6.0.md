---
type: Document
entity_id: PNG-TDD-6.0
title: "PNG-TDD-6.0: Payment Network Gateway - Fedwire Funds Connector & Swift gpi Integration Technical Design"
description: Metadata record for Payment Networks Engineering's technical design covering the Fedwire Funds Connector (SYS-PNG-FFC) and the Swift Alliance & gpi Connector (SYS-PNG-GPI), including network connectivity, ISO 20022 handling, acknowledgments, gpi Tracker batch integration, and the Addendum A quota decision.
tags: [png-tdd-6.0, payment-network-gateway, fedwire, fedwire-funds-connector, swift-gpi-connector, iso-20022, gpi-tracker, payment-networks-engineering, document]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-95e454ddd82fc29fca46b0a9
    resource: repo://sources/estate/arb-pay-reg-2026q3-payments-arb-adr-register-and-minutes.md
  - id: openwiki-source-5c11d5768c3be60ea1158084
    resource: repo://sources/estate/cnb-memo-2026-09-realignment-of-cross-border-network-integration.md
  - id: openwiki-source-4452149a3b4502b4c763a559
    resource: repo://sources/estate/jira-export-wt-discovery-2026-10-05.md
  - id: openwiki-source-0163a9a7923ee437e942692a
    resource: repo://sources/estate/png-tdd-6.0-payment-network-gateway-fedwire-and-gpi-technical-design.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Summary

**PNG-TDD-6.0** ("Payment Network Gateway - Fedwire Funds Connector & Swift gpi Integration:
Technical Design") is the technical design document, owned by **Payment Networks Engineering
(PNE)**, covering the two connector modules of the Payment Network Gateway: the **Fedwire Funds
Connector** ([Fedwire Funds Connector](../systems/fedwire-funds-connector.md), SYS-PNG-FFC) and
the **Swift Alliance & gpi Connector** ([Swift gpi Connector](../systems/swift-gpi-connector.md),
SYS-PNG-GPI). It describes network connectivity, ISO 20022 message handling and acknowledgments
for Fedwire, and Swift CBPR+/gpi messaging together with the batch gpi Tracker integration. This
page records the document's identity, ownership, and governance metadata; see the linked system
pages for the operational and architectural detail.

## Document metadata

| Field | Value |
|---|---|
| Document ID | PNG-TDD-6.0 |
| Version / Status | 6.0 (+ Addendum A) / Approved |
| Document owner | Payment Networks Engineering - Raj Malhotra (Director); Chen Wei (Fedwire); Tomasz Nowak (gpi) |
| Approver(s) | Raj Malhotra; Nikhil Bose (ARB) |
| Effective / Last reviewed | v6.0 2025-11-14; Addendum A 2026-03-03 |
| Classification | INTERNAL - CONFIDENTIAL |
| Related documents | PPH-SYS-OVW-9.2; PPH-API-CAT-2026.3; PNG-1544 |

The document is marked "Uncontrolled when printed" on every page footer. Support contacts are PNE
on-call (Tier 1) via `#payment-networks`, with gpi Tracker questions routed specifically to Tomasz
Nowak.

## Scope and ownership (as approved)

Section 1 states the design covers both modules of the Payment Network Gateway "owned and operated
by Payment Networks Engineering (PNE)": the Fedwire Funds Connector (FFC) and the Swift Alliance &
gpi Connector (GPI-C). This ownership statement reflects the document's effective and
last-reviewed dates (v6.0 2025-11-14; Addendum A 2026-03-03) and should be read alongside the
organizational change described below, which moved GPI-C ownership out of PNE after the document
was last revised.

## What the document covers

### Section 2 - Fedwire Funds Connector (SYS-PNG-FFC)

- **Connectivity and formats (2.1)**: FedLine Direct with dual MQ channels (primary Columbus,
  contingency Charlotte); ISO 20022 only since the Federal Reserve's single-day cutover on
  2025-07-14 (legacy FAIM format retired). Outbound message types are pacs.008 (customer
  transfer), pacs.009 (FI transfer), pacs.004 (return), camt.056 (return request), and camt.110
  (investigation). Inbound types are pacs.008/pacs.009/pacs.004 (published to
  `net.fedwire.inbound.v1`), pacs.002 acknowledgments, and admi.002 technical/business errors.
- **Acknowledgment handling (2.2)**: for every accepted value message the Federal Reserve returns
  a pacs.002 carrying the OMAD and a creation timestamp; FFC publishes these to
  `net.fedwire.ack.v1` (event EV-PNG-01). Errors (admi.002) are published with the IMAD reference.
  The document is explicit that Fedwire acceptance constitutes final settlement between the
  sending and receiving banks under Regulation J, and that the Federal Reserve does not report
  credit to the beneficiary's account at the receiving bank - acknowledgment is a network/legal
  settlement signal, not proof of beneficiary credit. Q3-2025 metrics cited: median Fed
  acknowledgment latency 4.2 s; median time from PPH RELEASED to Fed acceptance (including
  queueing) 6 min; Fed technical/business reject rate 0.07% of messages.
- **Topic access (2.3)**: `net.fedwire.ack.v1` and `net.fedwire.inbound.v1` are both produced by
  FFC, consumed by PPH, with PNE as ACL owner.

### Section 3 - Swift Alliance & gpi Connector (SYS-PNG-GPI)

- **Messaging (3.1)**: Swift CBPR+ ISO 20022 pacs.008 became mandatory for customer credit
  transfers from 2025-11-22 (end of MT/MX coexistence); CNB does not use MT103 contingency
  conversion. UETR is assigned by PPH at release (UUID v4) and carried in pacs.008; GPI-C maps
  Swift ACK/NAK back to PPH. Exceptions and investigations are moving to camt.110/camt.111 per
  Swift's November 2026 timeline.
- **gpi Tracker integration, current state (3.2)**: GPI-C retrieves Tracker updates via the Swift
  API through the Swift Microgateway, authenticated with SwiftNet PKI credentials bound to the
  GPI-C service account. The integration is **batch**, not real-time: every 4 hours (00:00, 04:00,
  08:00, 12:00, 16:00, 20:00 ET) GPI-C requests changed transactions for outbound UETRs from the
  last 30 days and upserts results into the Oracle table `GPI_TRACKER_SNAPSHOT` (columns include
  UETR as the join key to PPH v2 `identifiers.uetr`, LAST_STATUS/LAST_REASON, ROUTE_JSON,
  DEDUCTED_CHARGES_JSON, CONFIRMED_AMOUNT/CREDIT_TS, and SNAPSHOT_TS). Consumers are Payment
  Operations' Investigations Workbench (IWB) and the TDIP nightly `gpi_tracker_events` load. The
  design states plainly that **there is no internal API for gpi status** and that the snapshot
  table must not be exposed directly to channels; any client-facing capability would require a
  dedicated service with its own SLA, entitlements, and quota management.
- **Tracker API quota (3.3)**: the Swift Tracker API contract permits 250,000 calls/month
  (renewal 2027-01-31); usage was ~61% at the time of writing (batch pulls plus Ops ad-hoc
  lookups). Per-payment lookups from client channels were estimated at ~1.9 million calls/month
  (based on ~2,900 outbound international wires/day with repeated client views), roughly 7x the
  contracted quota. The document's design constraint is that any real-time capability must use a
  change-feed with internal fan-out rather than per-payment Tracker calls.
- **gpi statuses handled (3.4)**: documents the status/reason codes the connector interprets -
  ACSP/G000 (forwarded to next gpi agent, further updates expected), ACSP/G001 (forwarded to a
  non-gpi agent, tracking ends there), ACSP/G002-G004 (pending states, updates expected), ACCC
  (terminal credit to beneficiary, with credit timestamp and confirmed amount), and RJCT plus an
  ISO reason code (terminal, return expected via pacs.004).
- **Observed outcomes, Q3-2025 (3.5)**: 88% of outbound wires reach final status ACCC; 8% end
  tracking at a non-gpi agent (ACSP/G001); 2.5% are pending beyond 24 hours; 1.5% are rejected
  (RJCT); median release-to-ACCC across all corridors is 2 h 41 min; 34% of wires have at least one
  intermediary deduction reported (SHAR/CRED).

### Section 4 - Operations

Change windows are Saturday 22:00-02:00 ET. Monitoring uses Splunk dashboards `PNG-FFC-*` and
`PNG-GPI-*`. Business continuity relies on FedLine Advantage as Fedwire contingency and Swift
Alliance Lite2 as Swift standby.

### Addendum A (2026-03-03) - PNG-1544 decision

Addendum A records the Architecture Review Board's decision on **PNG-1544**, a request to increase
gpi batch frequency from 4 hours to 2 hours. The request was **declined** because projected
Tracker API usage would have exceeded the contracted monthly quota even at that reduced increase;
doubling batch frequency alone does not solve the underlying problem that per-payment, on-demand
Tracker calls (not batch frequency) are the real driver of quota risk at scale. The addendum
recommends a change-feed-based internal service as a future initiative rather than further
tightening of the batch schedule.

## Status after this document: superseded ownership and roadmap

Events after PNG-TDD-6.0's last revision changed who owns part of what it describes, without a
revision to this document itself:

- The Jira item PNG-1544 was marked **Won't Do**, "superseded by GTSI-0107" - the same outcome
  Addendum A records, now tracked under a different initiative.
- Per **CNB-MEMO-2026-09** ("Realignment of Cross-Border Network Integration," effective
  2026-10-01), ownership of the Swift Alliance Gateway, the gpi Connector (SYS-PNG-GPI), and gpi
  Tracker integration **moved from Payment Networks Engineering to Global Transaction Services
  Integration (GTSI)**, under Elena Vasquez (accountable leader), with Omar Siddiqui as EM and
  Hannah Lindqvist as Tech Lead. Tomasz Nowak - named in this document as the gpi Tracker contact
  - transferred to GTSI. PNE retained secondary on-call support for SYS-PNG-GPI only until
    2026-12-15, when knowledge transfer under GTSI-0112 completes. New gpi-related requests are
    raised in the Jira **GTSI** project rather than **PNG**.
- The **Fedwire Funds Connector (SYS-PNG-FFC)** and its topics (`net.fedwire.ack.v1`,
  `net.fedwire.inbound.v1`) were explicitly **not** moved and remain with PNE under Raj Malhotra.
- The real-time gpi capability this document's Addendum A pointed toward is tracked as
  **GTSI-0107** ("gpi Tracker Real-Time Service," a change-feed-based internal API), owned by
  GTSI/Elena Vasquez, **not funded for 2026**, with discovery planned for 2027-Q2. The Payments ARB
  (2026-Q3 session) separately reaffirmed that interim direct exposure of `GPI_TRACKER_SNAPSHOT`
  to client channels is **not approved** and that a quota-isolated read-only service would require
  ARB review - consistent with this document's own guidance in section 3.2/3.3.

Readers relying on this document for current operational ownership of SYS-PNG-GPI should treat the
Fedwire-related content (section 2) as still owned by PNE, but treat the gpi-related content
(section 3) as describing a system now owned by GTSI, pending CNB-ORG-PTT-2026-06's planned Q4
refresh.

## Related documents and pages

- **PPH-SYS-OVW-9.2** - PRISM Payments Hub system overview and lifecycle state model; defines the
  PPH states (e.g., RELEASED) referenced in this document's Fedwire latency metrics.
- **PPH-API-CAT-2026.3** - PRISM Payments Hub API and event catalog.
- **PNG-1544 / GTSI-0107** - the declined batch-frequency increase and its successor real-time
  Tracker initiative, discussed in Addendum A and the supersession note above.
- [Fedwire Funds Connector](../systems/fedwire-funds-connector.md) and
  [Swift gpi Connector](../systems/swift-gpi-connector.md) - system pages describing the two
  connector modules this design document specifies.
