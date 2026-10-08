# 04 — Validation

Validation is not a final step bolted on after generation. Gates run inline, after each
stage produces output, so a failure is caught at the cheapest point to fix it. Owned by
the `validator` agent. Writes **Validation Memory**. Reads whatever the current stage
produced plus Requirement Memory and Spec Memory for cross-checking.

## 1. When gates run

| Gate | Runs after | Blocking? |
|---|---|---|
| 1. Schema validation | `01-ingestion.md`, `02-ui-spec-synthesis.md` | Yes |
| 2. Traceability (bidirectional) | `02-ui-spec-synthesis.md` | Yes |
| 3. Security/compliance denylist | `01` (flagging), `03-ui-generation.md` (enforcement) | Yes at 03; advisory at 01 |
| 4. Design-token consistency | `03-ui-generation.md` | Yes |
| 5. Accessibility | `03-ui-generation.md` | Yes |
| 6. Golden-set regression | `03-ui-generation.md`, once a prior approved version exists | Advisory — surfaces a diff, doesn't block |
| 7. Human sign-off | End of every round, before `shipped` status | Yes, always |

"Blocking" means the pipeline halts and reports the failure; it does not mean a human
must intervene immediately for every gate — a blocked run can be retried automatically
once the upstream stage corrects itself (e.g., re-running synthesis after a coverage gap).

## 2. Gate 1 — Schema validation

The Requirements Document and the UI Specification each conform to their JSON Schemas
(`schemas/requirements.schema.json`, `schemas/ui-spec.schema.json`). Missing required
fields, malformed `req_id` references, or an undeclared `audience` value fail here.

## 3. Gate 2 — Traceability (bidirectional)

- Every `audience: customer` req_id is cited by ≥1 spec component, or explicitly marked
  `out_of_scope_for_ui` with a reason.
- Every spec component's `satisfies` list points to req_ids that exist and are
  `audience: customer`.
- A component citing an `audience: internal` req_id is a hard failure — this is the
  primary defense for the scope boundary in `specs/context.md`.

## 4. Gate 3 — Security/compliance denylist

A maintained denylist of patterns that must never appear in customer-facing copy:
fraud/compromised-credential language, raw internal hold/fraud codes, account/routing
numbers outside their designated masked display fields. Checked:

- **At ingestion (advisory):** flags `risk_flags: [security-sensitive]` requirements for
  extra scrutiny during spec synthesis. A hit here is healthy — it means the gate is
  doing its job before anything is generated.
- **At generation (blocking):** scans the assembled HTML's visible text content. Any hit
  here is a **severity-1 incident**, not a routine validation failure (see
  `07-indicators.md` — this is the one lagging indicator with zero tolerance, tracked
  separately from ordinary defect counts).

This directly implements the PRD's own REQ-EX-01 requirement: the system must suppress
sensitive trigger reasons so as not to tip off bad actors, and the copy must be vetted.

## 5. Gate 4 — Design-token consistency

Static scan of generated HTML for hex colors, arbitrary Tailwind values, or font
declarations not traceable to a token in the spec's token set. Zero tolerance for drift
— every value must resolve to a named token.

## 6. Gate 5 — Accessibility

- Contrast ratio ≥ WCAG AA for text/background pairs.
- Semantic landmarks (`nav`, `main`, `header`) present.
- Icons/buttons carry `alt`/`aria-label` where they convey meaning without visible text.
- Logical keyboard focus order through interactive elements (progress steps, action
  buttons, filters).

## 7. Gate 6 — Golden-set regression

Once a dashboard type has ≥1 human-approved version, a new generation (from iteration or
a PRD revision) is diffed against the last-approved version. Unexpected structural
changes outside the touched section are surfaced, not auto-blocked — the point is to
catch generation agents making unrequested changes elsewhere in the document, which is
exactly the failure iteration (`05-iteration.md`) is designed to avoid via scoped
regeneration.

## 8. Gate 7 — Human sign-off

No spec or UI reaches `shipped` status without an explicit human approval recorded in
Run/Episodic Memory (who, when, which version). Draft and iteration rounds don't need
this gate; shipping does, always.
