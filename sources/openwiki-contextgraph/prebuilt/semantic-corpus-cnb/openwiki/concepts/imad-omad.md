---
type: Concept
entity_id: imad-omad
title: "IMAD and OMAD: Fedwire message identifiers"
description: Explains the Fedwire Input/Output Message Accountability Data identifiers (IMAD, OMAD), which component assigns and carries each one through PRISM Payments Hub (PPH), and why OMAD's absence from the v1 API blocks a true domestic settlement-status feature.
tags: [fedwire, imad, omad, payments-hub, settlement-status, pacs.002, identifiers]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-550c0e3f038aab7950cab477
    resource: repo://sources/estate/cbo-arch-wc-4.1-wire-center-current-state-architecture.md
  - id: openwiki-source-4452149a3b4502b4c763a559
    resource: repo://sources/estate/jira-export-wt-discovery-2026-10-05.md
  - id: openwiki-source-0163a9a7923ee437e942692a
    resource: repo://sources/estate/png-tdd-6.0-payment-network-gateway-fedwire-and-gpi-technical-design.md
  - id: openwiki-source-a4ee8b1dfcb7e3cec0a315e4
    resource: repo://sources/estate/pph-api-cat-2026.3-prism-payments-hub-api-and-event-catalog.md
  - id: openwiki-source-19beabaf3acaad354d39ee1e
    resource: repo://sources/estate/pph-sys-ovw-9.2-prism-payments-hub-system-overview-and-lifecycle-state-model.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

IMAD and OMAD are the two Fedwire Funds Service message-identification references
that bracket a domestic wire's trip through the Federal Reserve:

- **IMAD** (Input Message Accountability Data) is assigned by the **sender** - in
  Crestline's case, PRISM Payments Hub (PPH) acting as the Fedwire sender - and
  stamped on the outbound pacs.008/pacs.009 message at release.
- **OMAD** (Output Message Accountability Data) is assigned by the **Federal
  Reserve** and returned in the **pacs.002** acknowledgment once the Fed accepts
  (settles) the message.

Both identifiers are Fedwire-specific; they have no equivalent on the Swift
CBPR+ rail, where the comparable end-to-end tracking concept is the UETR used by
Swift gpi (see the gpi Tracker integration in
[Payment Network Gateway](../interfaces/fedwire-network-ack-topics.md)). The
practical significance of IMAD vs. OMAD inside PPH is an availability gap: IMAD
has always been exposed to API consumers, but OMAD - the only concrete artifact
of the Federal Reserve's acceptance - is available solely on the Kafka
acknowledgment topic and in the v2 payment-detail API, never in the legacy v1
API that most channels still use.

## IMAD: sender's input reference

PPH assigns the IMAD at release, when it builds the outbound pacs.008/pacs.009
message, and carries it as an identifier throughout the payment's lifecycle:

| Representation | Where it appears |
|---|---|
| v1 REST (`GET /pph/v1/wires/{wireRef}/status`) | `fedRef` field (IMAD; `null` for Swift wires) |
| v2 REST (`GET /pph/v2/payments/{paymentId}`) | `identifiers.imad` |
| Fed error path | `admi.002` technical/business error messages are published with the IMAD reference |

Because IMAD is available in v1, it is the only Fedwire reference that
downstream channel systems historically received. CBO Wire Center displays the
IMAD on the wire-detail screen (sourced from the v1 `fedRef` field) but does not
persist it - it is a display-only field, not a stored identifier.

## OMAD: the Federal Reserve's acceptance reference

For each accepted value message, the Federal Reserve returns a pacs.002
carrying the OMAD and a Fed-assigned creation timestamp. The Fedwire Funds
Connector (FFC) module of the Payment Network Gateway publishes these
acknowledgments to the `net.fedwire.ack.v1` Kafka topic. Acceptance by the
Fedwire Funds Service constitutes final and irrevocable interbank settlement
between the sending and receiving banks under Regulation J / UCC Article 4A -
it does **not** confirm that the receiving bank has credited the beneficiary's
account.

OMAD is available only through:

- `net.fedwire.ack.v1` (published by FFC, consumed today only by PPH), and
- the v2 REST field `identifiers.omad` on `GET /pph/v2/payments/{paymentId}`.

It has never been exposed on any v1 API field, and the v1 `fedRef` field
explicitly carries IMAD only - OMAD and UETR are not available in v1 at all.

## Control flow: from release to OMAD

```mermaid
sequenceDiagram
    participant PPH as PRISM Payments Hub
    participant FFC as Fedwire Funds Connector
    participant FED as Federal Reserve (Fedwire Funds Service)
    participant TOPIC as net.fedwire.ack.v1

    PPH->>PPH: Release - assign IMAD, build pacs.008/pacs.009
    PPH->>FED: Send value message (state SENT_TO_NETWORK)
    FED-->>FFC: pacs.002 positive ack with OMAD and Fed timestamp
    FFC->>TOPIC: Publish acknowledgment (EV-PNG-01)
    TOPIC-->>PPH: PPH consumes ack, transitions to NETWORK_ACCEPTED
    PPH->>PPH: v2 identifiers.omad populated; stateHistory timestamp = PPH processing time
    Note over PPH: v1 fedRef remains IMAD only - OMAD never reaches v1 consumers
```
This shows IMAD assigned at release and OMAD arriving later via the Fed's
pacs.002 and the `net.fedwire.ack.v1` topic, reaching only the v2 API.

A rejection path exists as well: Fed technical or business rejects are
reported via `admi.002` or a negative pacs.002 and are published with the
IMAD reference (there is no OMAD for a rejected message), driving PPH's
`NETWORK_REJECTED` state.

## A subtle timestamp gap

Even where OMAD is available (v2), the timestamp a consumer sees by default is
not the Federal Reserve's own timestamp. The v2 `stateHistory` timestamp for
`NETWORK_ACCEPTED` is the time PPH *processed* the acknowledgment, not the
Fed's creation timestamp carried inside the pacs.002. The authoritative Fed
timestamp (and the OMAD itself) exist only on `net.fedwire.ack.v1`; no current
PPH v2 API field surfaces the Fed's own acceptance timestamp alongside OMAD.
Backlog item PPH-2207 proposes a `settlement` object (`fedSettlementTs` sourced
from pacs.002/OMAD, plus a rail-specific `settlementStatus`) to close this gap,
but it has no product sponsor and remains parked in the backlog.

## Why the gap blocks a true settlement-status feature

The IMAD/OMAD availability split compounds an existing v1 state-modeling
limitation: the v1 `status` field collapses the four distinct v2 lifecycle
states `RELEASED`, `SENT_TO_NETWORK`, `NETWORK_ACCEPTED`, and `COMPLETED` into
a single value, `PROCESSED`. A v1 consumer therefore cannot distinguish "PPH
released the wire for transmission" from "the Federal Reserve has actually
settled it" - and even if it could, it would have no OMAD field to display as
evidence of that settlement, because OMAD was never added to v1.

Concretely, this means:

- **CBO Wire Center** labels any `PROCESSED` wire "Completed" (renamed from
  "Processed" after client feedback), without being able to confirm or display
  Federal Reserve acceptance; it stores no OMAD at all, consistent with it not
  being available in v1.
- A domestic-wire "true settlement status" capability - one that can say with
  Fed-backed authority "this wire is irrevocably settled, as of this Fed
  timestamp" - requires both the v2 lifecycle distinction (`NETWORK_ACCEPTED`
  vs. `COMPLETED`) **and** the OMAD/Fed-timestamp pair that only exists on
  `net.fedwire.ack.v1` and v2 `identifiers.omad`. No current interface
  combines those into a single consumer-facing settlement field; that is
  exactly the gap PPH-2207 would close.
- Analytics ingestion of the Fed-acceptance signal is also stalled: a separate
  backlog item (ingesting `net.fedwire.ack.v1` into the data platform for
  settlement-time analytics) is blocked on a Kafka ACL from Payment Networks
  Engineering and has no business sponsor.
- The risk is not hypothetical: a client-facing complaint cited reliance on a
  "Completed" status for an international wire that was later rejected,
  prompting a regulatory complaint review and underscoring that collapsed,
  OMAD-free status values can mislead clients about finality.

Until a client-facing consumer migrates off the v1 API (sunset 2027-03-31) and
a v2 settlement object is built and sponsored, no channel can surface a
Fed-authoritative, OMAD-backed domestic settlement status; the most that is
available today is the coarse, network-agnostic `PROCESSED`/`NETWORK_ACCEPTED`
distinction, and only to v2 consumers.

## Related concepts

- [Fedwire Network ACK Topics](../interfaces/fedwire-network-ack-topics.md) - the `net.fedwire.ack.v1` topic that carries OMAD from the Fed to PPH.
- [Fed ACK Events dataset](../datasets/fed-ack-events.md) - structure and downstream use of the acknowledgment events.
- [PPH v2 Payments API](../interfaces/pph-v2-payments-api.md) - the only API surface exposing `identifiers.omad` today.
