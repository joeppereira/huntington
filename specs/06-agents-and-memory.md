# 06 — Agents and Memory

Six agents, each the primary writer of exactly one memory type. Every agent may read any
memory type; none writes outside its own. This is the cross-cutting spec every other
numbered spec assumes.

## Agents

| Agent | Stage | Primary writes | Reads |
|---|---|---|---|
| `requirements-extractor` | `01-ingestion.md` | Requirement Memory | Reference Memory (prior PRD patterns, for consistent req_id/section conventions) |
| `ui-spec-synthesizer` | `02-ui-spec-synthesis.md` | Spec Memory | Requirement Memory, Reference Memory, Feedback Memory (standing preferences) |
| `ui-generator` | `03-ui-generation.md` | *(none — stateless renderer; the output file is the artifact)* | Spec Memory, Reference Memory |
| `validator` | `04-validation.md`, inline after 01/02/03 | Validation Memory | Requirement Memory, Spec Memory, the generated artifact |
| `feedback-integrator` | `05-iteration.md` | Feedback Memory | All other memory types (must resolve a delta against current state) |
| `indicator-reporter` | cross-cutting, end of every run | Run/Episodic Memory | All other memory types (computes indicators in `07-indicators.md`) |

Each agent is defined as a Claude Code subagent at `.claude/agents/<name>.md`.
Corresponding user-invocable skills live at `.claude/skills/<name>/SKILL.md` and delegate
to these agents.

## Memory types

### 1. Requirement Memory
The structured Requirements Document(s), versioned, with `req_id → source pointer →
audience tag → risk flags → ambiguity notes`. One record per PRD intake, but req_ids are
stable across a PRD's revisions (see `specs/README.md` cross-spec contract). This is the
traceability root everything else cites back to.

### 2. Spec Memory
The structured UI Specification(s): design tokens, layout architecture, component tree,
each component's `satisfies` citations. Versioned per iteration round (`05-iteration.md`
§4). This is what `ui-generator` renders and what `validator` checks coverage against.

### 3. Reference Memory
An append-only, cross-PRD pattern library: approved design-token sets, approved
component patterns (e.g., the "FedEx-style journey tracker" once it exists), and prior
approved UI specs/HTML in full (e.g., `ui_specification_returns_dashboard.md` +
`dashboard_aggregates.html` as the project's first reference pair). Grows every time a
PRD ships. Exists so the second and third PRD reuse patterns instead of reinventing them
(`02-ui-spec-synthesis.md` §5).

### 4. Feedback Memory
User corrections and preferences captured during iteration, each tagged `scope:
this-run` or `scope: standing` (`05-iteration.md` §5), with the *why* when the user gave
one — mirrors the "lead with the rule, then why" structure used for durable feedback
elsewhere in this environment. Standing-scope entries are consulted by
`ui-spec-synthesizer` on every future run, not just the one where the feedback was given.

### 5. Validation Memory
Per-run gate results: which of the seven gates in `04-validation.md` passed or failed,
denylist hits (flagged at ingestion vs. caught at generation — the distinction matters,
see `04` §4), token-consistency violations, accessibility findings, golden-set diffs.
The audit trail for "why was this blocked" and "has this failure mode happened before."

### 6. Run/Episodic Memory
One record per pipeline run: which PRD/inputs, timestamps per stage, spec/UI versions
produced, indicator values (`07-indicators.md`), and human sign-off status (who, when,
which version was approved). `indicator-reporter` reads across all Run/Episodic records
to compute trends over time — this is the ledger, not a snapshot.

## Why this taxonomy and not a conversational-agent memory model

A conversational assistant's memory (user profile, standing feedback, project state,
external references) is organized around *one agent, many turns*. This pipeline is the
opposite shape: *many agents, one document's lifecycle*. The six types above are
organized around pipeline stages (Requirement → Spec → Reference) plus process concerns
that cut across every stage (Feedback, Validation, Episodic) — each has exactly one
agent responsible for keeping it correct, which is what makes the bidirectional
traceability guarantees in `04-validation.md` actually enforceable rather than aspirational.
