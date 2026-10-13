# 11 — Backlog (headline customer user stories)

Four stories for the **corporate treasury client** — the headline, high-value slices of
the Wire Tracking Center, the customer-facing experience this PRD exists to deliver.
Drawn directly from `projects/wire-tracking-center/requirements/requirements-v1.yaml`
(`audience: customer` only) and realized in
`projects/wire-tracking-center/spec/spec-v1.md`.

Scope reminder ([`context.md`](context.md)): customer-facing only. Internal requirements
(REQ-TECH-01..03) inform treatments but get no story here. Every figure is sourced from a
backend — generation never invents a number or a status.

---

## US-1 — Track a wire's journey end to end ("FedEx for wires")
*Requirements: REQ-JT-01, REQ-JT-02, REQ-JT-03 · Components: `journey-timeline`, `gpi-route`, `route-insights`*

**As** a treasury client, **I can see where my wire is in its lifecycle on a visual
timeline**, so I can answer "where is my money?" without calling the bank.

**Why it's headline:** this is the signature differentiator of the product — the
self-service journey visualization that replaces support calls.

**Acceptance criteria**
- Domestic wires show the milestone bar: Wire Submitted → Wire Approved → Bank Received
  → Confirmation Number Generated → Settled (REQ-JT-01).
- International wires show the SWIFT gpi route: Originated → SWIFT Sent → Intermediary
  Node(s) → Beneficiary Bank → Delivered (REQ-JT-02).
- International view surfaces intermediary bank count, currency-specific completion
  rates, and historical recipient-side fees (REQ-JT-03).
- The "Settled" step renders in a `pending-backend` state with a footnote where final
  settlement status is not yet available (REQ-JT-01 note; depends on REQ-TECH-01).
- No status is invented; node states come from backend/gpi data only.

---

## US-2 — Review and act on a held wire safely
*Requirements: REQ-EX-01, REQ-EX-02, REQ-EX-03 · Components: `held-wires-panel`, `release-insight`*

**As** a treasury client, **I can see wires held for my review with a plain-language
reason and Confirm or Reject them**, so I can clear holds myself without exposure to
sensitive risk details.

**Why it's headline:** it's the one state-changing action the client takes, and it's
security-critical — the PRD's CRITICAL requirement to suppress fraud/trigger language
lives here.

**Acceptance criteria**
- Held wires show only vetted, client-safe hold reasons; internal fraud/risk trigger
  codes and language are never displayed or transmitted (REQ-EX-01; cf. REQ-TECH-03).
- Client can Confirm (authorize release) or Reject a held wire from the UI (REQ-EX-02).
- On Confirm/Reject, a predictive insight on time-to-completion or cancellation next
  steps is shown (REQ-EX-03).
- The action is security-sensitive: the backlog item carries the write-path safeguards
  from `08-app-architecture.md` (step-up auth, idempotency, audit-before-ack).

---

## US-3 — Understand and resolve a returned wire
*Requirements: REQ-EX-04 · Components: `returned-wires-panel`*

**As** a treasury client, **I can open a returned wire and see why it came back and what
to do next**, so I can fix and resubmit without a support ticket.

**Why it's headline:** returns are the highest-anxiety, highest-support-cost event;
turning a dead-end into a guided resolution is direct client value.

**Acceptance criteria**
- Returned-wires view shows full tracking fidelity (same timeline detail as an active
  wire) plus the return reason (REQ-EX-04).
- Displays root-cause insight and recommended resolution steps (REQ-EX-04).
- Return reasons follow the same client-safe copy rule as held wires — no internal
  codes.

---

## US-4 — Stay ahead of wire status without watching the screen
*Requirements: REQ-SS-01, REQ-SS-04, REQ-SS-05 · Components: `detail-actions`, `alerts-panel`*

**As** a treasury client, **I can subscribe to alerts and get contextual answers about
delays**, so I'm notified of status changes instead of polling and can self-serve common
questions.

**Why it's headline:** proactive notification + self-service is what deflects the
"where's my wire?" call volume the product is built to reduce.

**Acceptance criteria**
- Client can subscribe to a specific wire ("Notify me when released/settled") (REQ-SS-04).
- Category-level alert subscriptions exist: Outgoing (Released, Receipt Confirmed,
  Settled, Returned), Incoming, International (REQ-SS-05).
- A clickable "Explain delays" feature surfaces contextual FAQs based on the wire's
  current delayed status/stage (REQ-SS-01).
- Alert categories and copy use declared design tokens only; no fabricated status values.
