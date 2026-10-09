---
type: Person
entity_id: nikhil-bose
title: Nikhil Bose
description: Chief Architect, Payments & Treasury at Crestline National Bank; chairs the Payments Architecture Review Board (ARB) and approves cross-cutting payments and payment-network architecture documents.
tags: [people, payments, enterprise-architecture, chief-architect, payments-arb, governance, crestline-national-bank, ptt]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-95e454ddd82fc29fca46b0a9
    resource: repo://sources/estate/arb-pay-reg-2026q3-payments-arb-adr-register-and-minutes.md
  - id: openwiki-source-550c0e3f038aab7950cab477
    resource: repo://sources/estate/cbo-arch-wc-4.1-wire-center-current-state-architecture.md
  - id: openwiki-source-49303e801f124d97df9c3ea3
    resource: repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md
  - id: openwiki-source-0163a9a7923ee437e942692a
    resource: repo://sources/estate/png-tdd-6.0-payment-network-gateway-fedwire-and-gpi-technical-design.md
  - id: openwiki-source-a4ee8b1dfcb7e3cec0a315e4
    resource: repo://sources/estate/pph-api-cat-2026.3-prism-payments-hub-api-and-event-catalog.md
  - id: openwiki-source-19beabaf3acaad354d39ee1e
    resource: repo://sources/estate/pph-sys-ovw-9.2-prism-payments-hub-system-overview-and-lifecycle-state-model.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Role

Nikhil Bose is the **Chief Architect, Payments & Treasury** within Payments &
Treasury Technology (PTT) at Crestline National Bank. In the PTT leadership
roster he sits alongside the MD/CIO (Gregory Hall) and the business-side
product leaders (Marcus Chen, Laura Kim, Danielle Okafor) as the
architecture-governance counterpart to engineering and product leadership,
rather than as the manager of a delivery team.

| Field | Value |
|---|---|
| Title | Chief Architect, Payments & Treasury |
| Organization | Payments & Treasury Technology (PTT) |
| Governance role | Chair, Payments Architecture Review Board (ARB) |
| Peer leadership | Gregory Hall (MD, CIO PTT); Marcus Chen (Digital Treasury Product); Laura Kim (Payments Platform Product); Danielle Okafor (Treasury Management Products) |

His single defining function, as recorded in the PTT organization directory,
is chairing the **Payments Architecture Review Board (ARB)** — the
cross-cutting architecture governance forum for channel, payments, and data
teams. See
[Payments ARB / Enterprise Architecture](../teams/payments-arb-enterprise-architecture.md)
for the forum he chairs.

## Chair of the Payments Architecture Review Board

The ARB meets monthly on the second Tuesday, with submissions due 10 business
days in advance via the ARB intake form; upcoming sessions as of the most
recent directory refresh are 2026-11-10 and 2026-12-08. It is **required** for
any new client-facing integration to payment systems, and it also acts as the
approval and record-of-decision body for Payments architecture decision
records (ADRs). As Chair, Nikhil Bose is the **approver of record** for
[ARB-PAY-REG-2026Q3](../documents/arb-pay-reg-2026q3.md), the published
2026-Q3 extract combining the current ADR register with the minutes of the
board's 2026-09-08 session; Jenna Ross (ARB Secretariat) is the document's
owner, while Bose is its approver.

### ADR register he chairs approval of

As of the 2026-Q3 extract, five ADRs are Accepted and binding under his
board's authority:

| ADR | Title | Applies to |
|---|---|---|
| [ADR-PAY-017](../decisions/adr-pay-017.md) | Kafka (Confluent) is the integration backbone for payment lifecycle events | All payment systems |
| [ADR-PAY-019](../decisions/adr-pay-019.md) | Channel status integrations must be event-driven; no polling of PPH | All channels |
| [ADR-PAY-021](../decisions/adr-pay-021.md) | Hold reason details never leave the financial-crimes trust boundary | PPH v2, channels, data |
| [ADR-PAY-023](../decisions/adr-pay-023.md) | UETR is the canonical end-to-end correlation id for all outbound wires | PPH, gateways, channels, TDIP |
| [ADR-PAY-026](../decisions/adr-pay-026.md) | Client-facing analytical outputs are served via the TDIP Insights API | Channels, TDIP |

### Decisions from the 2026-09-08 session

The minutes captured alongside the register, from the session Bose chaired,
record four items with a distinct business owner each, reinforcing that the
Chair convenes and approves board decisions without personally owning every
underlying system or initiative:

- **PPH v1 sunset** — no extension beyond 2027-03-31 for the PRISM Payments
  Hub v1 adapter (owner: Kevin O'Brien); remaining v1 consumers must present
  migration plans at the 2026-11-10 session.
- **gpi real-time service** — the proposed GTRS initiative (GTSI-0107) is not
  funded for 2026; interim direct exposure of the `GPI_TRACKER_SNAPSHOT` table
  to channels is explicitly **not approved**, and any future read-only,
  quota-isolated service for that purpose would itself require a fresh ARB
  review (owner: Elena Vasquez).
- **Status projection reuse** — the board reaffirmed the Status Projection
  Service (SPS) pattern as the reference architecture for client-facing status
  of any payment type, not only wires (owner: Arjun Mehta).
- **Structured address enforcement** — PPH and gateway enforcement of
  structured address fields remains on track for November 2026, with an
  expected increase in repair holds (owner: Raymond Ortiz).

These items show the ARB, under Bose's chairmanship, acting both as a funding
gate (gpi real-time service), a sunset/deprecation authority (PPH v1), and a
pattern-reuse arbiter (SPS) — not merely a document sign-off forum.

## Approver of architecture documents

Beyond the ARB register itself, Nikhil Bose is named as a co-approver on
architecture documents that cross team or domain boundaries, reflecting the
Chief Architect's sign-off role on current-state and technical-design
artifacts that have ARB-level significance:

| Document | Domain | Co-approver(s) |
|---|---|---|
| [CBO-ARCH-WC-4.1](../documents/cbo-arch-wc-4.1.md) | Wire Center (channel) current-state architecture | Anjali Deshpande (Director, Digital Treasury Channels Engineering) |
| [PNG-TDD-6.0](../documents/png-tdd-6.0.md) | Payment Network Gateway — Fedwire Funds Connector & Swift gpi Connector technical design | Raj Malhotra (Director, PNE) |

Notably, the PRISM Payments Hub's own system documents —
[PPH-SYS-OVW-9.2](../documents/pph-sys-ovw-9.2.md) and
[PPH-API-CAT-2026.3](../documents/pph-api-cat-2026.3.md) — are approved by
Payments Hub Engineering's own leadership (Raymond Ortiz, Kevin O'Brien) and
product owner (Laura Kim) rather than by Bose directly. This distinguishes two
layers of architecture sign-off within PTT: system-owning engineering
leadership approves documents scoped to their own system, while the Chief
Architect's approval is reserved for documents with cross-system or
cross-channel implications (a channel's current-state architecture that
integrates with PPH; a shared network-gateway technical design) and for the
ARB's own binding register. The PTT organization directory
(CNB-ORG-PTT-2026-06) itself is approved by Gregory Hall (MD, CIO PTT), not
Bose, underscoring that Bose's approval authority is specifically
architectural/governance in scope rather than organizational.

## Relationships

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: an unescaped angle bracket inside a label breaks rendering; rephrase the label. -->
```text
flowchart TD
    GH[Gregory Hall<br/>MD, CIO PTT] --- NB[Nikhil Bose<br/>Chief Architect, Payments & Treasury]
    NB -->|Chairs| ARB[Payments Architecture<br/>Review Board]
    ARB -->|Approves / binds| ADRs[ADR register<br/>ADR-PAY-017/019/021/023/026]
    NB -->|Approver| REG[ARB-PAY-REG-2026Q3<br/>register & minutes]
    JR[Jenna Ross<br/>ARB Secretariat] -->|Owns document| REG
    NB -->|Co-approver| CBOARCH[CBO-ARCH-WC-4.1<br/>Wire Center architecture]
    AD[Anjali Deshpande<br/>Director, Channels Eng.] -->|Co-approver| CBOARCH
    NB -->|Co-approver, ARB| PNGTDD[PNG-TDD-6.0<br/>Fedwire & gpi technical design]
    RM[Raj Malhotra<br/>Director, PNE] -->|Co-approver| PNGTDD
```

- **[Payments ARB / Enterprise Architecture](../teams/payments-arb-enterprise-architecture.md)**
  — the governance forum Bose chairs; its secretariat function is run by
  Jenna Ross, who owns the published ADR register and minutes Bose approves.
- **Gregory Hall** (MD, CIO PTT) — owns all PTT engineering end to end and
  approves the PTT organization directory; Bose's architecture-governance
  authority sits alongside, not inside, Hall's engineering reporting line.
- **Anjali Deshpande** (Director, Digital Treasury Channels Engineering) —
  co-approver with Bose of the Wire Center current-state architecture
  (CBO-ARCH-WC-4.1).
- **Raj Malhotra** (Director, Payment Networks Engineering) — co-approver
  with Bose, representing the ARB, of the Fedwire/gpi connector technical
  design (PNG-TDD-6.0).
- **Raymond Ortiz, Kevin O'Brien, Laura Kim** (Payments Hub Engineering /
  product) — approve PPH's own system-overview and API-catalog documents
  independently of Bose, illustrating the boundary between system-level and
  cross-cutting architecture sign-off described above.
- **Kevin O'Brien, Elena Vasquez, Arjun Mehta, Raymond Ortiz** — business
  owners of the four items decided at the 2026-09-08 ARB session Bose chaired.

## Source notes

Nikhil Bose's title, scope, and ARB chairmanship are recorded in the PTT
Organization, System Ownership & Engagement Directory
(CNB-ORG-PTT-2026-06, published 2026-06-15, next refresh 2026-12). His role
as ARB Chair and approver of the Payments ADR register and 2026-09-08 minutes
is recorded in ARB-PAY-REG-2026Q3 (published 2026-09-12). His co-approver
role on cross-cutting architecture documents is recorded in the approver
fields of CBO-ARCH-WC-4.1 (last reviewed 2026-08-20) and PNG-TDD-6.0 (v6.0
2025-11-14, Addendum A 2026-03-03). Because the organization directory is
refreshed only quarterly, any organizational announcement issued between
refreshes would take precedence over the leadership scope recorded here until
folded into the next refresh.
