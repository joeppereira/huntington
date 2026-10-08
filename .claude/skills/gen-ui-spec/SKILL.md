---
name: gen-ui-spec
description: Synthesize a structured UI Specification (design tokens, layout, component tree) from a Requirements Document produced by /ingest-prd. Use once requirements are extracted and classified, before any HTML is generated.
---

Read `specs/02-ui-spec-synthesis.md` first.

1. Confirm a Requirements Document exists (from `/ingest-prd`) and that ambiguous
   requirements have been resolved or explicitly accepted as-is by the user.
2. Delegate synthesis to the `ui-spec-synthesizer` subagent, passing the Requirements
   Document (filtered to `audience: customer`), any reference image/tokens, and
   Reference Memory for pattern reuse.
3. Report back: requirement coverage (should be 100% or every gap explicitly excepted
   with a reason), any new design tokens proposed (vs. reused), and any component
   reused from a prior PRD's pattern library.
