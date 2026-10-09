---
type: Person
entity_id: chen-wei
title: Chen Wei
description: "Tech Lead for the Fedwire Funds Connector within Payment Networks Engineering, and co-owner (document owner) of PNG-TDD-6.0, the technical design governing the Payment Network Gateway's Fedwire and Swift gpi modules."
tags: [person, tech-lead, fedwire, payment-networks-engineering, png-tdd-6.0, payment-network-gateway]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-0163a9a7923ee437e942692a
    resource: repo://sources/estate/png-tdd-6.0-payment-network-gateway-fedwire-and-gpi-technical-design.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Role

Chen Wei is the **Tech Lead for Fedwire** within **Payment Networks Engineering
(PNE)**, reporting into Raj Malhotra (Director, PNE). Chen Wei owns the Fedwire
side of the Payment Network Gateway (PNG) and is named as co-owner of
**PNG-TDD-6.0**, the technical design document for the gateway's two modules,
alongside Raj Malhotra (overall document owner) and Tomasz Nowak (Tech Lead,
gpi), who owns the Swift Alliance & gpi Connector (GPI-C) half of the same
document.

## Document ownership: PNG-TDD-6.0

PNG-TDD-6.0 ("Payment Network Gateway — Fedwire Funds Connector & Swift gpi
Integration: Technical Design") is the approved design of record for network
connectivity, ISO 20022 message handling, acknowledgment processing, and gpi
Tracker integration across both PNG modules. It is currently at version 6.0
plus Addendum A (effective 2025-11-14; Addendum A added 2026-03-03), classified
INTERNAL - CONFIDENTIAL, and approved by Raj Malhotra and Nikhil Bose (ARB).
Chen Wei's named co-ownership specifically covers Section 2 of the document,
**Fedwire Funds Connector (SYS-PNG-FFC)**, which is the design responsibility
most closely associated with this Tech Lead role.

## Area of responsibility: Fedwire Funds Connector (SYS-PNG-FFC)

The Fedwire Funds Connector is the module Chen Wei leads. It is the Payment
Network Gateway component that connects Crestline National Bank to the Federal
Reserve's Fedwire Funds Service over **FedLine Direct** (dual MQ channels:
primary Columbus, contingency Charlotte). Responsibilities documented under
this Tech Lead's area include:

- **ISO 20022 messaging** — since the Federal Reserve's single-day cutover on
  **2025-07-14** (legacy FAIM format retired with no coexistence period), FFC
  exchanges only ISO 20022 message types: outbound `pacs.008` (customer
  transfer), `pacs.009` (FI transfer), `pacs.004` (return), `camt.056` (return
  request), and `camt.110` (investigation); inbound `pacs.008` / `pacs.009` /
  `pacs.004` (published to `net.fedwire.inbound.v1`), `pacs.002`
  acknowledgments, and `admi.002` technical/business errors.
- **Acknowledgment handling** — for every accepted value message the Fed
  returns a `pacs.002` carrying the OMAD and a Fed creation timestamp; FFC
  publishes it to `net.fedwire.ack.v1` (catalog event EV-PNG-01). Errors
  (`admi.002`) are published keyed by the IMAD. Fed acceptance is final,
  irrevocable interbank settlement under Regulation J — it is not confirmation
  that the receiving bank has credited the beneficiary.
- **Topic ownership** — FFC produces `net.fedwire.ack.v1` and
  `net.fedwire.inbound.v1`; PNE owns the ACLs for both, and PPH (PRISM
  Payments Hub) is the sole authorized consumer of each.
- **Observed performance (Q3-2025)** — median Fed acknowledgment latency of
  4.2s (send to `pacs.002`); median 6 minutes from PPH `RELEASED` to Fed
  acceptance (including queueing); Fed technical/business rejects at 0.07% of
  messages.

See [Fedwire Funds Connector](../systems/fedwire-funds-connector.md) for the
connector's implementation detail.

## Operations

Fedwire/FFC falls under the PNG operational model documented in PNG-TDD-6.0:
standard change windows of Saturday 22:00–02:00 ET, Splunk monitoring
dashboards under the `PNG-FFC-*` prefix, and FedLine Advantage as the
business-continuity contingency channel. First-line support is PNE on-call
(T1), coordinated via `#payment-networks`.

## Relationship to the gpi side of PNG

Although Chen Wei's ownership is scoped to Fedwire, PNG-TDD-6.0 also governs
the Swift Alliance & gpi Connector (GPI-C), led by Tomasz Nowak, covering
Swift CBPR+ ISO 20022 migration, UETR tracking, and gpi Tracker batch
integration. The two Tech Leads co-own the single technical design document
because FFC and GPI-C are the two modules of the same Payment Network
Gateway, sharing document structure, approval chain (Raj Malhotra, Nikhil
Bose/ARB), and operational cadence (shared change windows and on-call
rotation) even though their message formats, counterparties, and topic
contracts are independent.
