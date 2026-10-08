---
name: ingest-prd
description: Ingest a bank PRD (docx/md), reference image(s), and/or free text into a structured, audience-classified Requirements Document. Use at the start of a new dashboard/feature pipeline run, or when adding a new PRD to the huntington project.
---

Read `specs/01-ingestion.md` and `specs/context.md` first.

1. Collect the input(s) named by the user: a `.docx`/`.md` file path, image path(s),
   and/or pasted free text.
2. Delegate extraction to the `requirements-extractor` subagent with all inputs and a
   pointer to `specs/01-ingestion.md`.
3. Report back: total requirements extracted, the customer/internal split, any
   ambiguous requirements needing clarification, and any `security-sensitive` flags —
   don't just say "done," surface what needs a human decision before stage 02 runs.
