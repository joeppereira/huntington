---
type: Document
entity_id: PPH-SYS-OVW-9.2
title: "PPH-SYS-OVW-9.2: PRISM Payments Hub - System Overview & Wire Lifecycle State Model"
description: Metadata record for Payments Hub Engineering's system overview document defining PRISM Payments Hub's architecture, processing stages, the thirteen canonical v2 wire lifecycle states and their v1 status collapse, identifier scope, hold integration, and cutoff/operating-window rules.
tags: [pph-sys-ovw-9.2, prism-payments-hub, wire-lifecycle, lifecycle-state-model, payments-hub-engineering, system-overview, fedwire, swift-cbpr, document]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-19beabaf3acaad354d39ee1e
    resource: repo://sources/estate/pph-sys-ovw-9.2-prism-payments-hub-system-overview-and-lifecycle-state-model.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Summary

**PPH-SYS-OVW-9.2** ("PRISM Payments Hub - System Overview & Wire Lifecycle State
Model") is the authoritative system overview document for the PRISM Payments Hub
(PPH), CNB's wire orchestration platform for all channels and rails (Fedwire,
Swift CBPR+, and internal book transfer). It is owned by **Sunita Rao** (Principal
Engineer) and **Kevin O'Brien** (EM), Payments Hub Engineering, approved by
**Raymond Ortiz** (Director) and **Laura Kim** (Payments Platform Product),
classified INTERNAL - CONFIDENTIAL, and was last reviewed 2026-05-30 at version
9.2 / Approved. This page records the document's identity, scope, and governance
metadata; the system and state-machine content it defines is maintained in depth
on [PRISM Payments Hub](../systems/prism-payments-hub.md) and
[Wire Lifecycle State Model](../concepts/wire-lifecycle-state-model.md).

## Document metadata

| Field | Value |
|---|---|
| Document ID | PPH-SYS-OVW-9.2 |
| Version / Status | 9.2 / Approved |
| Document owner | Sunita Rao (Principal Engineer) / Kevin O'Brien (EM), Payments Hub Engineering |
| Approver(s) | Raymond Ortiz (Director); Laura Kim (Payments Platform Product) |
| Effective / Last reviewed | Last reviewed 2026-05-30 |
| Classification | INTERNAL - CONFIDENTIAL |
| Related documents | PPH-API-CAT-2026.3; PNG-TDD-6.0; PRSP-HMS-3.4; ADR-PAY-021; ADR-PAY-023 |

The document is marked "Uncontrolled when printed" on every page footer, consistent
with the rest of the Payments & Treasury Technology document estate.

## What the document covers

### Section 1 - Overview and platform facts

PPH is built on the vendor **Volaris Payment Platform 9.4** and runs on-premises
in an active-active configuration across the Columbus and Charlotte data centers.
It receives instructions from all channels, validates and enriches them,
coordinates screening and holds with the Payment Risk & Screening Platform (PRSP),
performs funds control against the Core Deposit Platform (CDP), and routes
outbound traffic to the Payment Network Gateway (Fedwire Funds Connector or Swift
Alliance/gpi Connector). As of the Q2-2026 averages cited in the document, PPH
processes roughly 14,200 outgoing domestic (Fedwire) wires, 2,900 outgoing
international (Swift CBPR+) wires, 18,500 incoming wires across all rails, and
6,300 book transfers per business day; CBO is the largest outgoing channel at
~67%. The stated availability target is 99.95% during Fedwire operating hours.
The document also flags the vendor roadmap item that the **Volaris 9.6 upgrade**
(scheduled April 2027) removes the legacy v1 API adapter - the technical driver
behind the PPH v1 API sunset tracked in PPH-2190 and documented in
[PPH-API-CAT-2026.3](pph-api-cat-2026.3.md).

### Section 2 - Processing stages

The document defines seven sequential processing stages a wire moves through:
Intake (channel submits via v1/v2 API, file, or Swift) → Validation & enrichment
(format, ABA/BIC routing, ISO 20022 mapping, structured address checks - mandatory
for Swift CBPR+ and Fedwire from November 2026) → Screening (synchronous call to
PRSP's SanctionScreen + Sentinel; a hit creates a Hold Management Service (HMS)
hold and moves the payment to `HELD`) → Funds control (memo debit against CDP;
insufficient funds create `HRC-05` holds with auto-retry until 5:30 p.m. ET) →
Release (UETR assigned for all outbound wires since ADR-PAY-023; pacs.008/pacs.009
message built) → Network (sent to the Fedwire Funds Connector or Swift
Alliance/gpi Connector; acknowledgment updates state) → Close (accounting close to
`COMPLETED`; later returns via pacs.004 transition the wire to `RETURNED`).

### Section 3 - Canonical v2 lifecycle states

The document's core contribution is the canonical thirteen-state v2 lifecycle
model - `RECEIVED`, `VALIDATING`, `SCREENING`, `HELD`, `REPAIR`, `FUNDS_CONTROL`,
`WAREHOUSED`, `RELEASED`, `SENT_TO_NETWORK`, `NETWORK_ACCEPTED`,
`NETWORK_REJECTED`, `COMPLETED`, `CANCELLED`, and `RETURNED` - together with each
state's meaning, typical duration, and the single v1 `status` value shown to
consumers for that state. Its single most load-bearing finding is that the legacy
v1 status API collapses four distinct v2 states (`RELEASED`, `SENT_TO_NETWORK`,
`NETWORK_ACCEPTED`, `COMPLETED`) into one value, `PROCESSED`, so v1 consumers
cannot distinguish a wire that has merely been released from one the network has
acknowledged or one that has reached internal accounting close. The full state
table, transition diagram, and the downstream consequences of this collapse
(including the CMP-2026-1189 client complaint and the 2024 Wire Status Lite pilot
incident) are documented on
[Wire Lifecycle State Model](../concepts/wire-lifecycle-state-model.md).

### Section 4 - Rail-specific meaning of NETWORK_ACCEPTED

The document specifies that `NETWORK_ACCEPTED` means materially different things
per rail: for **Fedwire Funds**, it reflects the Federal Reserve's `pacs.002`
positive acknowledgment carrying the OMAD, representing final and irrevocable
interbank settlement under Regulation J/UCC Article 4A (but not confirmation of
credit to the beneficiary's own account); for **Swift CBPR+**, it reflects only a
SwiftNet delivery acknowledgment for `pacs.008` with no settlement implication,
since settlement occurs through correspondent nostro/vostro accounts and
beneficiary credit is knowable only via a Swift gpi `ACCC` status. The document
also notes that the v2 `stateHistory` timestamp recorded for `NETWORK_ACCEPTED` is
the time PPH processed the acknowledgment, not the Federal Reserve's creation
timestamp inside `pacs.002`; the authoritative Fed timestamp and OMAD travel
separately on the `net.fedwire.ack.v1` topic (tracked under PPH-2207). See
[Fedwire Funds Service](../concepts/fedwire-funds-service.md),
[IMAD and OMAD](../concepts/imad-omad.md), and
[Swift gpi / CBPR+](../concepts/swift-gpi-cbpr.md) for the mechanics behind this
distinction.

### Section 5 - Identifiers

The document scopes six identifiers attached to a payment and which interface
surfaces each is available on: `pphId` (assigned by PPH, internal key, available
in v1/v2/events), `cboRef` (assigned by CBO, channel reference, v2
`identifiers.cboRef` only when the channel is CBO), `IMAD` (assigned by PPH as
Fedwire sender, available as v1 `fedRef` and v2 `identifiers.imad`), `OMAD`
(assigned by the Federal Reserve, available only in v2 `identifiers.omad` and on
`net.fedwire.ack.v1` - not in v1 at all), `UETR` (assigned by PPH at release,
end-to-end tracking id, available in v2 `identifiers.uetr` and lifecycle v2
events), and `EndToEndId` (passed through from the originator or PPH, v2 only).
See [IMAD and OMAD](../concepts/imad-omad.md) and [UETR](../concepts/uetr.md) for
the full identifier mechanics and why OMAD's and UETR's absence from v1
specifically blocks settlement-status features built on that interface.

### Section 6 - Integration with Hold Management (PRSP-HMS)

When screening or funds control raises a hold, the Hold Management Service (HMS)
returns a `holdId` and PPH transitions the payment to `HELD`. The document notes
that, since a 2019 integration, PPH also synchronizes the HMS hold's free-text
*description* into the legacy v1 field `holdReasonDesc` for backward compatibility
with the Wire Room console, while the v2 API exposes only `hold.isHeld` and
`hold.holdId` per ADR-PAY-021 - deliberately dropping the free-text reason. See
[PRSP-HMS-3.4](prsp-hms-3.4.md) and
[Hold Reason Taxonomy & Disclosure Tiers](../concepts/hold-reason-taxonomy-disclosure-tiers.md)
for the hold-reason design this interacts with.

### Section 7 - Cutoffs and operating windows

The document specifies the Fedwire operating day (9:00 p.m. ET prior calendar day
to 7:00 p.m. ET), the Fedwire third-party customer transfer cutoff (6:00 p.m. ET,
with later items warehoused under `HRC-04`), the CBO same-day domestic wire cutoff
(5:30 p.m. ET), and currency-specific international cutoffs (e.g., EUR 2:00 p.m.
ET, GBP 1:00 p.m. ET, MXN 3:00 p.m. ET, JPY prior day).

### Section 8 - Upcoming changes

The document calls out three forward-looking changes: structured/hybrid postal
address enforcement for Swift CBPR+ and Fedwire from November 2026 (expected to
raise `HRC-06` repair holds), a FedNow outbound expansion committed for PI 27.1,
and the paired 2027-03-31 PPH v1 API sunset (PPH-2190) and April 2027 Volaris 9.6
upgrade.

## Related documents and pages

- **PPH-API-CAT-2026.3** - the PPH API and event catalog; consumes this
  document's v1/v2 state and identifier definitions to describe field-level
  availability and the v1 deprecation notice. See
  [PPH-API-CAT-2026.3](pph-api-cat-2026.3.md).
- **PNG-TDD-6.0** - the Payment Network Gateway technical design; its Fedwire
  latency metrics and acknowledgment handling reference the `RELEASED` and
  `NETWORK_ACCEPTED` states this document defines. See
  [PNG-TDD-6.0](png-tdd-6.0.md).
- **PRSP-HMS-3.4** - the Hold Management Service design this document's hold
  integration (section 6) depends on.
- **ADR-PAY-021** - the decision to drop the free-text hold reason from the v2
  API, referenced in section 6. See [ADR-PAY-021](../decisions/adr-pay-021.md).
- **ADR-PAY-023** - the decision to assign a UETR to all outbound wires at
  release, referenced in section 2. See [ADR-PAY-023](../decisions/adr-pay-023.md).
- [PRISM Payments Hub](../systems/prism-payments-hub.md) - the system page
  describing PPH's architecture and request flow in full.
- [Wire Lifecycle State Model](../concepts/wire-lifecycle-state-model.md) - the
  full v2 state table, transition diagram, and consequences of the v1
  `PROCESSED` collapse that this document originates.
