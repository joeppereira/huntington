---
type: Decision
entity_id: ADR-PAY-023
title: "ADR-PAY-023: UETR as Canonical Correlation ID"
description: Payments ARB decision (2025-09-09, accepted) making UETR the canonical end-to-end correlation identifier for every outbound wire, assigned by PRISM Payments Hub (PPH) at release and available only to v2 API/event consumers, never to legacy v1 consumers.
tags: [adr, payments, pph, uetr, correlation-id, swift-gpi, fedwire, identifiers, payments-arb]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-95e454ddd82fc29fca46b0a9
    resource: repo://sources/estate/arb-pay-reg-2026q3-payments-arb-adr-register-and-minutes.md
  - id: openwiki-source-19beabaf3acaad354d39ee1e
    resource: repo://sources/estate/pph-sys-ovw-9.2-prism-payments-hub-system-overview-and-lifecycle-state-model.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Status

**Accepted** — 2025-09-09. Registered in the Payments Architecture Review
Board (ARB) ADR register (ARB-PAY-REG-2026Q3) and still in force as of the
2026-Q3 register extract. Applies to **PPH, gateways, channels, and TDIP**.

## Context

Before this decision, the Unique End-to-End Transaction Reference (UETR) was
understood primarily as a Swift gpi artifact: a tracking identifier needed
only for international (Swift CBPR+) wires so that the Swift Alliance & gpi
Connector (GPI-C) could follow a payment across gpi agents. Domestic Fedwire
transfers, which have no gpi tracking relationship, did not reliably carry a
UETR, and consumers wanting an identifier that could tie a PPH payment to
downstream lifecycle events, gpi tracking data, and TDIP analytics had no
single, rail-agnostic correlation key to rely on.

ADR-PAY-023 resolves this by designating UETR itself — not a Swift-only
value, but PRISM Payments Hub's (PPH's) own identifier — as the canonical
end-to-end correlation id for **every** outbound wire PPH releases,
regardless of rail.

## Decision

- PPH assigns a UETR to **every outbound wire at release**, including
  Fedwire wires carried on `pacs.008`, not only Swift CBPR+ wires. See
  [UETR](../concepts/uetr.md) for the assignment mechanics: UETR is minted as
  a UUID v4 at the **RELEASE** lifecycle stage, never earlier and never
  reassigned afterward.
- Consumers that need to correlate a PPH payment with Swift gpi tracking data
  must obtain the UETR from the **v2 API** (`identifiers.uetr` on
  `GET /pph/v2/payments/{paymentId}`) or from **v2 lifecycle events** — there
  is no other supported source for it.
- **v1 consumers do not receive UETR.** The legacy v1 API and its lifecycle
  status model have no field carrying UETR at all; this gap is permanent for
  v1 and is not planned to be backfilled, consistent with the broader v1
  sunset (Volaris 9.6 removes the v1 adapter, no extension beyond
  2027-03-31).

## Consequences

- UETR becomes the one identifier that is both rail-agnostic (populated
  consistently for Fedwire and Swift CBPR+ alike) and externally meaningful
  (it is also the key Swift gpi uses), making it PPH's preferred correlation
  id for any new cross-system integration, in contrast to IMAD/OMAD (Fedwire-
  specific) or `cboRef` (channel-specific, CBO only). See
  [IMAD and OMAD](../concepts/imad-omad.md) for how those rail-specific
  identifiers relate to UETR.
- Any consumer that still integrates only against the v1 API — including
  most CNB channels prior to the v1 sunset — structurally cannot obtain a
  payment's UETR and therefore cannot correlate that payment with Swift gpi
  tracking data or any other UETR-keyed dataset; migrating to the v2 API or
  v2 lifecycle events is required to get it.
- Downstream, UETR is the join key [GPI_TRACKER_SNAPSHOT](../datasets/gpi-tracker-snapshot.md)
  and its TDIP copy, [`gpi_tracker_events`](../datasets/gpi-tracker-events.md),
  use to associate Swift gpi tracking updates back to a PPH payment, and it
  is the column TDIP's base wire-history dataset,
  [`pay_wire_txn_hist`](../datasets/pay-wire-txn-hist.md), populates for that
  purpose. Universal Fedwire UETR assignment was implemented operationally in
  **2025-10**, one month after this ADR's acceptance: `pay_wire_txn_hist.uetr`
  is populated for Swift wires back to 2018 (predating this ADR, because
  Swift gpi tracking already required a UETR) but only for Fedwire wires from
  2025-10 onward. Any UETR-based join against Fedwire history before that
  date will find no value to join on.
- Because UETR now applies across rails, it depends on the Kafka lifecycle
  event backbone established by [ADR-PAY-017](adr-pay-017.md) to propagate to
  v2 event consumers, and it must be read alongside, not instead of,
  rail-specific identifiers: UETR confirms Swift network delivery or
  gpi status, not Fedwire settlement finality, which is carried separately
  via OMAD on `net.fedwire.ack.v1`.

## Related

- [UETR (Unique End-to-End Transaction Reference)](../concepts/uetr.md) — the
  identifier this ADR governs: its format, assignment timing, and role as a
  join key across PPH, the gpi Tracker snapshot, and TDIP.
- [PPH v2 Payments API](../interfaces/pph-v2-payments-api.md) — the only API
  surface exposing `identifiers.uetr`.
- [Wire transaction history dataset (`pay_wire_txn_hist`)](../datasets/pay-wire-txn-hist.md) —
  downstream TDIP dataset whose `uetr` column population date for Fedwire
  wires (2025-10) directly reflects this ADR's rollout.
- [ADR-PAY-017: Kafka as the Integration Backbone](adr-pay-017.md) — the
  event backbone this ADR relies on to propagate UETR to v2 lifecycle event
  consumers.
- [ADR-PAY-019: Event-Driven Channel Status (No Polling)](adr-pay-019.md) —
  a related Payments ARB decision governing how channels consume PPH status,
  registered in the same ADR register.
