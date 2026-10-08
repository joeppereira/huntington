# 08 — App Architecture (the customer-facing runtime)

Specs 01–05 govern the *generation pipeline* (PRD → UI spec → prototype). This spec
governs the **running customer-facing application** those prototypes are the design
contract for: the FedEx-style wire tracking experience a corporate treasury client
uses. `09-standards.md` defines the security/privacy/operational standards this
architecture must satisfy; this spec defines the shape that makes satisfying them
possible.

## 1. Position in the estate

The app is a module **inside the bank's existing Online Treasury Channel** (per the
PRD's executive summary) — it does not own login, entitlements, or session management.
It inherits the channel's SSO, step-up authentication, and entitlement model, and must
never implement a parallel auth path.

## 2. Topology

```
Browser (SPA, built from the approved UI specs)
   │   HTTPS, channel session
   ▼
BFF (backend-for-frontend) — the ONLY thing the browser talks to
   │        │           │
   ▼        ▼           ▼
Payments  SWIFT gpi   Alerts/Subscription
core      adapter     service
adapter
```

- **The browser never calls a core banking system or SWIFT API directly.** Every
  upstream is behind the BFF, which owns aggregation, caching, redaction, and
  entitlement enforcement per request.
- **Adapters are mockable by contract.** Each upstream (payments core, SWIFT gpi,
  alerts) is an adapter with a frozen interface and a deterministic mock, so the entire
  app is drivable end-to-end before any real integration exists — and testable forever
  after without one. Real adapter vs. mock is a deployment config, never a code change.
- **Frontend:** the generated single-file prototypes (spec 03) are the design contract;
  the production frontend is a framework build (React assumed, decided at
  implementation) that implements the same component tree, tokens, and traceability
  annotations. Component ids and `satisfies` req_ids carry through as data attributes
  so traceability survives into production code.

## 3. Data contracts

- One versioned contract per view: `WireSummary` (dashboard rows/aggregates),
  `WireDetail` (full record + fee breakdown), `JourneyTimeline` (domestic milestones),
  `GpiRoute` (international route + intermediaries), `HeldWireReview` (vetted reason
  copy + available actions), `SubscriptionState`.
- **Redaction happens in the BFF, not the frontend.** `HeldWireReview` carries only the
  client-safe reason string from the server-side fraud-code mapping table; the raw
  internal code never appears in any payload, logged or otherwise, that leaves the BFF
  (see `09-standards.md` §Security). "Not displayed" is not the bar — "never
  transmitted" is.
- Account numbers are masked at the contract level (`****1234`); the unmasked value has
  no field in any browser-bound contract.

## 4. Latency budgets and freshness model

Different views have different staleness tolerances — design to them explicitly rather
than making everything "real-time":

| View | Budget (p95, BFF response) | Freshness |
|---|---|---|
| Dashboard aggregates | 500 ms | cached, ≤60 s stale acceptable |
| Wire search/filter | 800 ms | near-live from payments core |
| Wire detail + domestic timeline | 800 ms | near-live |
| gpi international route | 1.5 s first load | cached per wire with TTL; background refresh; show last-known + timestamp, never block the page on SWIFT |
| Held-wire Confirm/Reject | 2 s for the acknowledged submit | **synchronous and never cached** — see §5 |

- SWIFT gpi is the slow, rate-limited upstream: the BFF caches per-wire gpi state,
  refreshes on view + background schedule, and prefers gpi push/webhook over polling
  where available. The UI always renders cached state immediately with an "as of" time.
- Status changes reach the browser by polling the BFF (simple, cacheable) first;
  server-push is an optimization decided by measured need, not assumed day one.

## 5. The money-moving path (Confirm/Reject) is architecturally separate

Everything else in this app is read-only. Held-wire Confirm/Reject (REQ-EX-02) is the
one write path, and it gets its own rules:

- **Step-up authentication** via the channel's existing mechanism, per action.
- **Idempotency key** generated client-side per decision; replays return the original
  result, never double-execute.
- **Entitlement check at the BFF per request** — not per session — against the
  channel's entitlement service (the user authorized for this account, this action,
  this amount tier).
- **No caching anywhere on this path**; the response is the authoritative result.
- **Immutable audit event** (who, what wire, which action, when, from where) emitted
  before the response is returned — if the audit write fails, the action fails.

## 6. Degradation is designed, not accidental

Every upstream can be down without taking the app down:

- gpi unavailable → international wires show last-cached route with "tracking update
  unavailable, as of \<time\>" — never a blank panel, never a spinner forever.
- Payments core degraded → dashboard shows cached aggregates clearly labeled stale;
  search disabled with an honest message.
- Alerts service down → subscription toggles disabled with a message; no silent
  accept-and-drop of a subscription request.
- Held-wire actions **fail closed**: if entitlements, step-up, or the audit trail is
  unavailable, the action is unavailable — degraded never means "skip a safety check."

Each degraded state is a designed UI state in the spec's component tree
(`interaction_states` includes `degraded`), generated and reviewed like any other state
— not an afterthought handled by an error boundary.

## 7. What this spec deliberately defers

- Frontend framework choice and build tooling — decided when implementation starts;
  the contracts above are framework-neutral.
- Real upstream integration details (payments core API shape, gpi credential model) —
  each real adapter gets a short integration note when built; the mock contract is the
  spec until then.
- Mobile/native — the SPA is responsive per the UI specs; native apps are a separate
  scope decision.
