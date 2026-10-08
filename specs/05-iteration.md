# 05 — Iteration

How free-text user feedback updates an in-progress spec and UI without re-running the
whole pipeline from scratch. Owned by the `feedback-integrator` agent. Writes **Feedback
Memory**. Reads everything else to resolve a delta against current state.

## 1. Feedback → deltas

Free-text feedback (e.g., "make the hold-reason badge less alarming" or "add a
subscribe button to each wire row") is parsed into one or more typed deltas:

```yaml
delta_type: modify_component   # add_component | remove_component | modify_component
                                # | change_token | reprioritize_requirement
target: held-wire-review-badge
change: "reduce visual severity: amber instead of rose, unless status is actually denied"
req_id_context: [REQ-EX-01]
```

A single feedback message may produce multiple deltas. Each delta is resolved
independently against current Spec Memory before being applied.

## 2. Scoped regeneration

- A delta that only touches a component's `visual_treatment` or copy regenerates only
  that component's HTML fragment (`03-ui-generation.md` §2).
- A delta that adds/removes a component re-runs spec synthesis for the affected area of
  the component tree, then generation for the new/changed fragments only.
- A delta that changes a token (e.g., "use our brand blue, not emerald") regenerates
  every fragment referencing that token — this is the one case where "scoped" still
  means "touches many files," because the token is shared by design.

## 3. What never gets scoped down

Regardless of how small the delta, two gates always re-run in full against the whole
document, never just the touched section:

- **Traceability** (`04-validation.md` §3) — a scoped edit can accidentally orphan a
  requirement or introduce a stray citation; only a full check catches that.
- **Security/compliance denylist** (`04-validation.md` §4) — a one-word copy edit is
  exactly the kind of change that can introduce a leak; this gate is cheap enough to run
  every time regardless of scope.

## 4. Versioning

Every iteration round produces a new spec version and (for touched sections) a new UI
version, both diffable against the prior round. Nothing is edited in place — "spec v3"
always exists alongside "spec v2," so a human can see exactly what changed and why
(the delta that caused it, traced back to the feedback that produced the delta).

## 5. Standing feedback vs. one-off feedback

Not all feedback is scoped to the current dashboard. "Never use red for warnings, use
amber" is a standing preference that should apply to every future PRD this pipeline
processes, not just the one being edited right now. The feedback-integrator tags each
delta `scope: this-run` or `scope: standing`; standing-scope feedback is written to
Feedback Memory in a way Reference Memory and future `ui-spec-synthesizer` runs can
pick up automatically (see `06-agents-and-memory.md` §Feedback Memory), so the user
never has to repeat a preference across PRDs.
