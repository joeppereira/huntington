# Project context for Claude

This repo is **huntington** — a pipeline that turns bank PRDs, reference UI images, and
free-text feedback into a structured UI spec and a generated dashboard, scoped to
**customer-facing** experiences only.

## Read first (in order)

1. **`specs/context.md`** — what this is, the customer-facing scope boundary (the
   hardest constraint to get wrong — see below), principles, anti-goals.
2. **`specs/README.md`** — full spec index, build order, cross-spec contracts.
3. **`specs/06-agents-and-memory.md`** — the six agents and six memory types.

## Load-bearing reminders

- **Customer-facing only.** Internal/bank-ops requirements are extracted for
  traceability (Requirement Memory) but never become a UI spec component or generated
  HTML. A requirement's `audience` tag is set once at ingestion and never silently
  changed downstream. Get this wrong and the failure mode is either shipping an ops
  screen to a client, or dropping client-facing scope — both are traceability failures.
- **Every generated UI element traces to a `req_id`.** Checked bidirectionally
  (`specs/04-validation.md` Gate 2): every customer-facing requirement has a citing
  component or an explicit exception, and every component cites a real, customer-facing
  requirement.
- **The security denylist gate is zero-tolerance at generation time.** A hit in shipped
  customer-facing HTML is a severity-1 incident (`specs/07-indicators.md`), not a
  routine defect — this directly implements the source PRD's own requirement to
  suppress fraud/hold-reason language that could tip off bad actors.
- **Design tokens are the only source of visual values.** No generated HTML may contain
  a color/font/spacing value absent from the spec's declared token set.
- **No agent invents a number or a status.** If this pipeline is ever wired to live
  data, every figure comes from a backend; generation agents narrate, they don't compute.
- **This is a multi-PRD pipeline, not a one-off.** Reference Memory accumulates design
  tokens and component patterns across PRDs — check it before proposing a new pattern
  that already exists (e.g., the FedEx-style journey tracker).
- **Leading vs. lagging indicators are never blended.** Leading = pre-review signal;
  lagging = post-review outcome. Report them as two sections, always.

## How memory and these docs relate

Per-session memory at `~/.claude/projects/.../memory/` is conversational context for
the assistant across chats. `specs/` and the six memory types in
`specs/06-agents-and-memory.md` are the pipeline's own source of truth for a given run.
When they disagree, `specs/` wins.
