# huntington — context

Read this before any spec. It explains what this system is, why it is scoped the way it
is, and which constraints are real. The numbered specs assume it.

---

## What this is

A pipeline that turns a bank's product-requirements documents (Word docs), reference
screenshots/images of existing UIs, and free-text user input into:

1. a structured, versioned, requirement-traceable **UI specification** (design tokens,
   layout, components — the shape demonstrated by `ui_specification_returns_dashboard.md`), and
2. a generated, runnable **UI** (single-file Tailwind HTML first; a component framework
   is a later decision, not assumed now — the shape demonstrated by `dashboard_aggregates.html`).

A human reviews and approves every artifact before it ships. The pipeline accelerates the
first draft and the iteration loop; it does not replace design or product review.

**This is not a one-off.** The Wire Tracking Center PRD is the first worked example.
More PRDs of the same shape (Huntington Payment Ops, Returns/Exception dashboards, and
others not yet seen) will be fed through the same pipeline. Specs, agents, schemas, and
the reference pattern library are built so the second and third PRD cost less than the
first, not so the first one is maximally polished.

---

## The scope decision that shapes everything downstream

**In scope: the customer-facing application only.** The FedEx-style self-service
tracking experience a corporate treasury client sees and acts on — wire status, journey
visualization, held/returned-wire actions, alerts, support escalation.

**Out of scope for UI generation: internal/ops-facing tooling.** Bank-employee queues,
fraud-review consoles, case-management screens, and anything that exists only to let
bank staff service the customer-facing app. When a source PRD mixes both (most will —
PRDs are written for the whole feature, not just the client-visible slice), the pipeline
must **separate them at ingestion**, not after generation:

- Customer-facing requirements → flow through spec synthesis → generation → validation.
- Internal/ops-facing requirements → extracted and kept in Requirement Memory for
  traceability and context, explicitly tagged `audience: internal`, and **never** passed
  to the UI spec synthesizer or UI generator.

This split is a classification gate in `01-ingestion.md`, not a filter applied by hand
per PRD. Getting it wrong in one direction ships a bank-ops screen to a client; getting
it wrong in the other silently drops client-facing scope. Both are traceability failures,
tracked as indicators (`07-indicators.md`).

A requirement can be ambiguous on audience (e.g., REQ-EX-01's hold-reason copy is
customer-facing, but the fraud-code mapping behind it is not) — the spec component for
"Held Wire Review" renders only the vetted customer-safe copy; the internal mapping
table is Requirement Memory context, never a UI spec component.

---

## Principles

- **Every generated artifact traces to a requirement ID.** No orphan UI section, no
  silently dropped requirement. Coverage is bidirectional and checked both ways.
- **Specs are versioned and diffable**, before and after every iteration round.
- **Security-sensitive content is denylist-checked before it reaches generated UI.**
  Fraud/risk trigger language, raw account/routing numbers, internal hold codes — zero
  tolerance, blocking gate, not a lint warning. This is the direct software expression of
  the PRD's own "CRITICAL SECURITY REQUIREMENT" (suppress fraud-tip-off language).
- **Design tokens are the only source of visual values.** Generated HTML never hardcodes
  a color, font, or spacing value absent from the spec's declared token set.
- **No agent invents a number or a status.** If a future version of this pipeline wires
  generated UI to live data, every figure and status is sourced from a backend system,
  never fabricated by a generation agent. (Carried over deliberately from
  `bionic-wealth-advisor`'s "no model computes a number" rule — it is a load-bearing
  constraint in financial UI, not a style preference.)
- **Human sign-off is a required gate** before a spec or UI is marked `shipped`. Agents
  draft; humans approve. Nothing auto-ships.
- **Leading indicators are measured pre-review; lagging indicators are measured
  post-review.** Never conflate the two — a leading indicator predicts rework risk before
  a human has looked at anything; a lagging indicator reports what actually happened
  after they did.

## Anti-goals

- Not a general PRD-management or requirements-tracking tool — it exists to get from PRD
  to a reviewable UI draft fast, nothing more.
- Not a WYSIWYG design tool. No human drags boxes; they write PRDs/feedback in text and
  review generated output.
- Not an internal ops-tooling generator. If a future need for bank-employee UI emerges,
  it is a deliberate scope expansion with its own context doc, not a quiet extension of
  this one.
- No fully autonomous ship path. There is always a human-sign-off gate (`04-validation.md`).

## Read next

`specs/README.md` has the build order and the full spec index.
