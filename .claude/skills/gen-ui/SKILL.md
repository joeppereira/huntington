---
name: gen-ui
description: Render a UI Specification into a single-file Tailwind HTML dashboard, section by section. Use once /gen-ui-spec has produced a spec with full requirement coverage.
---

Read `specs/03-ui-generation.md` first.

1. Confirm a UI Specification exists (from `/gen-ui-spec`) and has passed Gate 1
   (schema) and Gate 2 (traceability) per `specs/04-validation.md`.
2. Delegate rendering to the `ui-generator` subagent, component by component per the
   spec's tree, so each component is independently regenerable later.
3. Immediately run `/validate-ui` on the output — generation is never considered done
   until the generated artifact passes Gates 3–5.
4. Report back: the output file path, and a one-line note on what's placeholder data
   vs. spec-driven content.
