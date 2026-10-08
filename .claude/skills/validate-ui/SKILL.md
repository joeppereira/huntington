---
name: validate-ui
description: Run the huntington pipeline's validation gates (schema, bidirectional traceability, security denylist, design-token consistency, accessibility, golden-set regression) against the current requirements/spec/UI artifacts. Use after ingestion, after spec synthesis, after generation, and before any human sign-off.
---

Read `specs/04-validation.md` first — it defines which gates run at which stage and
which are blocking.

1. Determine which stage just produced output (ingestion, synthesis, or generation) and
   run only the gates scheduled for that stage per `04-validation.md` §1.
2. Delegate to the `validator` subagent.
3. **Any Gate 3 (security denylist) hit in generated output is a severity-1 finding** —
   surface it first, on its own, before the rest of the report.
4. Report pass/fail per gate with specifics. For Gate 6 (golden-set regression),
   present the diff for human judgment rather than treating it as pass/fail.
5. Never mark anything `shipped` from this skill alone — Gate 7 (human sign-off) is a
   separate, explicit action the user takes.
