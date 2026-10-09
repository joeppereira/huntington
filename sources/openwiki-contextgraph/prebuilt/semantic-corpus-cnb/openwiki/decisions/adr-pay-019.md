---
type: Decision
entity_id: ADR-PAY-019
title: "ADR-PAY-019: Event-Driven Channel Status (No Polling)"
description: Payments ARB decision (2024-06-11, accepted) that channel status integrations must consume Prism Payments Hub (PPH) lifecycle events rather than poll PPH, limiting synchronous status calls to throttled, user-initiated refresh; adopted after INC-2024-1182 and PIR-2024-07.
tags: [adr, payments, pph, event-driven, polling, wire-center, status-projection, incident-followup]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-95e454ddd82fc29fca46b0a9
    resource: repo://sources/estate/arb-pay-reg-2026q3-payments-arb-adr-register-and-minutes.md
  - id: openwiki-source-550c0e3f038aab7950cab477
    resource: repo://sources/estate/cbo-arch-wc-4.1-wire-center-current-state-architecture.md
  - id: openwiki-source-3cc45df143c5eec31fe1f9f6
    resource: repo://sources/estate/pir-2024-07-wire-status-lite-pilot-inc-2024-1182-post-implementation-review.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

# ADR-PAY-019: Event-Driven Channel Status (No Polling)

## Status

Accepted, 2024-06-11. Registered in the Payments Architecture Review Board (ARB) ADR register (ARB-PAY-REG-2026Q3) and reaffirmed in the 2026-09-08 ARB minutes, where the board explicitly reaffirmed the CBO Status Projection Service (SPS) as the reference pattern for client-facing status of any payment type. Applies to **all channels** integrating with Prism Payments Hub (PPH).

## Context

In January-May 2024, Crestline Business Online (CBO) piloted "Wire Status Lite" (CBO-3120): the browser auto-refreshed each visible wire's status from the PPH v1 synchronous status API (`GET /pph/v1/wires/{ref}/status`) every 30 seconds. On 2024-05-31 (month-end), combined pilot and production refresh traffic drove roughly 85 TPS against that API, exhausting PPH's API thread pool and delaying wire release for 47 minutes. This is incident [INC-2024-1182](../incidents/inc-2024-1182.md), analyzed in the post-implementation review [PIR-2024-07](../incidents/pir-2024-07.md).

The PIR's impact assessment: 1,240 wires delayed; 312 wires released after the 6:00 p.m. ET Fedwire customer cutoff (value moved to the next day); 14 clients compensated via interest claims totaling $41,800. No regulatory notification was required because no client data was exposed.

The PIR identified three root causes:

1. A polling architecture against a shared, synchronous status API with no client-side backoff.
2. No capacity test had been run at month-end volumes before the pilot was exposed to production traffic.
3. Status semantics (e.g., what "Processed" means to a client) were not validated with Compliance or Legal before the feature was exposed to users.

The PIR also surfaced a client-facing finding that motivated later downstream decisions: 37% of surveyed pilot users believed "Processed" meant the beneficiary had received the funds, and users could not get an explanation of held wires without FCC guidance (addressed separately in hold-reason-confidentiality work, ADR-PAY-021).

## Decision

Channel teams must obtain payment status by **consuming PPH lifecycle events** into a channel-owned read model, not by polling PPH's synchronous status API. The reference implementation pattern is the CBO Status Projection Service ([CBO Status Projection Service](../systems/cbo-status-projection-service.md)): a Kafka consumer of payment lifecycle events materializing a Postgres read model, exposed to the channel BFF via `/cbo/sps/v1`.

Synchronous status calls against PPH are permitted only for **user-initiated refresh**, and must be throttled. In [Wire Center](../systems/cbo-wire-center.md) this is implemented as a 60-second server-side cache and a refresh throttle of 1 call per 60 seconds per wire against `GET /pph/v1/wires/{ref}/status` (EP-PPH-01); PPH itself rate-limits the shared v1 status API to 20 TPS.

This is codified in CBO-ARCH-WC-4.1 §7 ("Constraints and known limitations"), item 1: *"No status polling. Per ADR-PAY-019 (following INC-2024-1182), Wire Center must not poll PPH for status; only user-initiated refresh is permitted (throttled 1 per 60 s per wire). New status capabilities must be event-driven."* Any new channel status capability — milestone tracking, gpi/international status, hold-state surfacing, etc. — must be built as an event-driven consumer, not as additional polling against PPH.

## Consequences

- New status features must budget for: Kafka topic onboarding (e.g., `pay.wire.lifecycle.v2`), a projection/mapping module translating lifecycle events into channel-facing status, and replay handling for the read model.
- As of the CBO-ARCH-WC-4.1 current-state review (last reviewed 2026-08-20), Wire Center itself still does not use this pattern: it continues to rely on synchronous PPH v1 calls, and SPS is only configured for ACH (CBO-3815), not wires. Wire support for SPS is tracked as future work requiring a new mapping module and a consumer ACL onto `pay.wire.lifecycle.v2`. This is a known gap against ADR-PAY-019, not a reversal of it — Wire Center's synchronous calls remain within the ADR's throttled-refresh exception, but any new wire status capability (e.g., milestone tracking) must be event-driven rather than extending polling.
- The ARB has since reaffirmed SPS as the reference pattern for client-facing status of **any** payment type (2026-09-08 minutes), reinforcing ADR-PAY-019's event-driven requirement across rails, not just wires.
- A related ARB discussion in 2026-09-08 minutes declined to approve direct interim exposure of a gpi snapshot (`GPI_TRACKER_SNAPSHOT`) to channels, noting that any read-only, quota-isolated service for that purpose would itself require ARB review — consistent with keeping channel-facing status read-only and event-sourced rather than ad hoc synchronous pulls.
- One PIR action item remains open and carries forward independent of this ADR: validating client-facing status terminology with FCC and Legal before any future tracking feature ships (owner: CBO Product).

## Related

- [INC-2024-1182](../incidents/inc-2024-1182.md) — the incident that prompted this decision.
- [PIR-2024-07](../incidents/pir-2024-07.md) — post-implementation review documenting root causes and actions, one of which became this ADR.
- [CBO Status Projection Service](../systems/cbo-status-projection-service.md) — the reference event-driven status pattern (Kafka consumer → Postgres read model → `/cbo/sps/v1`).
- [Wire Center](../systems/cbo-wire-center.md) — the channel whose polling incident drove this ADR, and which is referenced in CBO-ARCH-WC-4.1 §7 as subject to its no-polling constraint.
