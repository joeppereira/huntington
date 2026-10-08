# huntington

A pipeline that turns bank PRDs (Word docs), reference UI images, and free-text
feedback into a structured, requirement-traceable UI specification and a generated,
runnable dashboard — scoped to **customer-facing** banking experiences only (the
FedEx-style self-service tracking view a client sees, not internal bank-ops tooling).

The Wire Tracking Center PRD is the first worked example. More PRDs of the same shape
(Huntington Payment OPs, Returns/Exception dashboards, and others) are expected over
time; the pipeline is built so each one costs less than the last.

## Start here

1. [`specs/context.md`](specs/context.md) — what this is, the customer-facing scope
   boundary, principles, anti-goals.
2. [`specs/README.md`](specs/README.md) — the full spec index and build order.
3. [`specs/06-agents-and-memory.md`](specs/06-agents-and-memory.md) — the six agents
   (`.claude/agents/`) and six memory types that do the work.
4. [`specs/07-indicators.md`](specs/07-indicators.md) — how we know it's working.

## Skills (`.claude/skills/`)

| Skill | Does |
|---|---|
| `/ingest-prd` | PRD/image/text → structured, audience-classified requirements |
| `/gen-ui-spec` | Requirements → structured UI spec (tokens, layout, components) |
| `/gen-ui` | UI spec → single-file Tailwind HTML, section by section |
| `/validate-ui` | Run the validation gates (traceability, security denylist, tokens, a11y) |
| `/iterate` | Free-text feedback → scoped deltas → scoped regeneration, versioned |
| `/audit-indicators` | Leading/lagging indicators for a run or a roll-up across runs |

## Example inputs this project started from

- `Wire Tracking Center - Product Requirements Document.docx` — the first PRD.
- `ui_specification_returns_dashboard.md` / `dashboard_aggregates.html` — a worked
  example of the target spec/output shape, for a different dashboard, derived from an
  image rather than a PRD (demonstrates both input paths this pipeline supports).
- `Huntington Payment OPs.docx` — a second PRD-shaped input.

## Status

Specs, agents, and skills are defined. No ingestion/generation code has been written
yet — this is the spec-first stage, matching the pattern used in `../service-graph`.
