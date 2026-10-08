---
name: iterate
description: Apply free-text feedback to an in-progress spec/UI with scoped regeneration and versioning. Use when the user gives feedback on a generated dashboard rather than starting a new PRD from scratch.
---

Read `specs/05-iteration.md` first.

1. Delegate to the `feedback-integrator` subagent with the user's feedback text and the
   current spec/UI version.
2. The subagent parses feedback into deltas, applies the minimum scoped regeneration
   (`/gen-ui` re-run only for touched components), and tags each delta `this-run` or
   `standing`.
3. Always re-run full-document traceability and security-denylist checks via
   `/validate-ui`, regardless of how small the delta — never scope those two down.
4. Report back: what changed, the new version number, a diff summary, and any
   `standing`-scope preference recorded for future PRDs.
