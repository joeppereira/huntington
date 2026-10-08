# huntington specs

A pipeline that turns bank PRDs + reference images + free-text feedback into a
structured UI spec and a generated UI, scoped to **customer-facing** banking experiences
only (see [`context.md`](context.md) for why that boundary matters and how it's enforced).

**Read in this order:** [`context.md`](context.md) (what this is, scope boundary,
principles, anti-goals) → the numbered specs below → [`06-agents-and-memory.md`](06-agents-and-memory.md)
(who does the work and what they remember) → [`07-indicators.md`](07-indicators.md) (how
we know it's working).

**Build sequence: 01 → 02 → 03 → 04 → 05 (the generation pipeline), then 08 → 09 (the
running app the generated prototypes are a design contract for).** 06 and 07 are cross-cutting — every other
spec assumes the agents and memory types defined in 06, and every stage emits the
indicators defined in 07. Validation (04) is not a final step bolted on at the end; its
gates run inline after 01, after 02, and after 03 (see 04 §1 "when gates run").

| # | Spec | Scope | Key decisions |
|---|---|---|---|
| 1 | [Ingestion](01-ingestion.md) | PRD/image/text → structured, classified requirements | docx/image/text → one Requirements Document; audience classification (`customer` vs `internal`) is a hard gate, not a filter; ambiguity is flagged, never silently resolved |
| 2 | [UI spec synthesis](02-ui-spec-synthesis.md) | Customer-facing requirements (+ reference image/tokens) → structured UI spec | Operates on `audience: customer` requirements only; every spec component cites ≥1 req_id; 100% requirement coverage or explicit out-of-scope-for-UI marking |
| 3 | [UI generation](03-ui-generation.md) | UI spec → single-file Tailwind HTML | Generated section-by-section from the spec's component tree so iteration can re-render one section without touching the rest; no value outside the declared token set |
| 4 | [Validation](04-validation.md) | Gates between every stage, not just at the end | Schema → traceability → security denylist (zero-tolerance) → design-token consistency → accessibility → golden-set regression → human sign-off |
| 5 | [Iteration](05-iteration.md) | Free-text feedback → scoped deltas → scoped regeneration | Feedback parsed into deltas; only affected sections regenerate; traceability + security gates always re-run in full, never scoped down; every round is versioned and diffable |
| 6 | [Agents and memory](06-agents-and-memory.md) | 6 agents, 6 memory types, who writes/reads what | One agent per pipeline stage plus a feedback-integrator and an indicator-reporter; each agent is the primary writer of one memory type |
| 7 | [Indicators](07-indicators.md) | Leading (pre-review) and lagging (post-review) metrics | Leading indicators predict rework risk before a human looks; lagging indicators report what happened after; security/traceability lapses are severity-1 incidents, not just metrics |
| 8 | [App architecture](08-app-architecture.md) | The customer-facing runtime the prototypes are a design contract for | BFF-only topology (browser never touches core systems or SWIFT); mockable-by-contract adapters; per-view latency budgets and freshness model; the one write path (held-wire Confirm/Reject) architecturally separated with step-up auth, idempotency, audit-before-ack; degradation designed as reviewed UI states |
| 9 | [Standards](09-standards.md) | Security, privacy, operational standards for the running app | Every standard testable yes/no; tipping-off suppression is a data-layer control (raw codes never transmitted, not just never displayed); fail closed always; privacy by contract/schema, not discipline; degraded states have automated tests; audit completeness continuously reconciled |

## Cross-spec contracts (change these only with a spec edit)

- Audience tag `customer | internal` (specs 1, 2, 6) — set once at ingestion, never
  re-derived downstream. A requirement's audience never changes without a human decision
  recorded in Requirement Memory.
- `req_id` stability (specs 1–5) — once assigned, a req_id is never reused or silently
  renumbered across PRD revisions; a changed requirement gets a new version, not a new id.
- Design token set (specs 2, 3, 4) — the single source of visual truth; specs 3 and 4
  both read it, neither invents values outside it.
- The denylist (spec 4 §3) — one implementation, checked at ingestion (flagging) and
  before ship (blocking); a hit at ingestion is healthy signal, a hit at ship is an incident.
- Memory types (spec 6) — one taxonomy, six types, each with exactly one primary writer;
  every other agent may read any memory type but writes only its own.
