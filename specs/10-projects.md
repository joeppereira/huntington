# 10 — Projects: one PRD, one separable project

Every PRD processed by this pipeline is its own **project**: a self-contained directory
executed, versioned, reviewed, shipped, and archivable independently of every other
PRD. The pipeline (specs, agents, skills, schemas, standards) is shared infrastructure;
the work products are not.

## 1. Layout

```
huntington/
├── specs/                      # shared — the pipeline and runtime specs (01–10)
├── .claude/agents|skills/      # shared — the six agents and six skills
├── schemas/                    # shared — requirements + ui-spec JSON Schemas
├── shared/
│   ├── reference-memory/       # shared — cross-PRD pattern library (tokens, components,
│   │                           #   approved spec/HTML pairs). Append via promotion only (§4).
│   ├── feedback-standing/      # shared — `scope: standing` feedback (05-iteration.md §5)
│   └── denylist/               # shared — the security denylist (04-validation.md §4)
└── projects/
    └── <slug>/                 # one per PRD — e.g. wire-tracking-center
        ├── project.yaml        # manifest: name, sources, status, current versions
        ├── inputs/             # the source PRD docx / images / text, verbatim
        ├── requirements/       # Requirement Memory (this project only)
        ├── spec/               # Spec Memory, versioned (spec-v1.md, spec-v2.md, …)
        ├── ui/                 # generated HTML, versioned (ui-v1.html, …) + fragment manifest
        ├── feedback/           # `scope: this-run` Feedback Memory
        ├── validation/         # Validation Memory: gate results per run
        └── runs/               # Run/Episodic Memory: one record per pipeline run
```

Five of the six memory types (`06-agents-and-memory.md`) live **inside** the project
directory. The sixth — Reference Memory — is shared by design: it is how the second PRD
costs less than the first. Standing-scope feedback is likewise shared, because "never
use red for warnings" applies to every future project, not one.

## 2. The manifest: `project.yaml`

```yaml
name: wire-tracking-center
title: Wire Tracking Center
sources:
  - inputs/wire-tracking-center-prd.docx
status: ingesting        # ingesting | specifying | generating | iterating | shipped | archived
spec_version: null        # current, e.g. v3
ui_version: null
signed_off_by: null       # Gate 7 record: who, when (null until shipped)
signed_off_at: null
```

`status` is the single source of truth for where a project is in the pipeline; skills
check it before running (e.g., `/gen-ui` on a project still `ingesting` is an error,
not a convenience).

## 3. Separability rules

1. **Self-contained execution.** Every skill invocation names (or infers from cwd) the
   active project; all reads and writes of project-scoped memory happen under that
   project's directory. Running project A can never touch project B's files.
2. **No cross-project reads.** A project never reads another project's directories.
   Cross-PRD learning flows through exactly two shared channels: `shared/reference-memory/`
   and `shared/feedback-standing/`. If something in project A would help project B,
   promote it (§4) — don't reach across.
3. **Copyable and archivable.** A project directory plus the shared `specs/`, `schemas/`,
   and `shared/` content is sufficient to resume, review, or audit that project on
   another machine. Nothing a project needs lives in a path outside those.
4. **Independent lifecycle.** Projects ship, stall, or get archived (status `archived`,
   directory retained) without blocking any other project. Concurrent projects are
   expected and safe because of rules 1–2.
5. **Shared assets are read-only to project runs**, with the single exception of
   promotion (§4). An agent working a project may read the denylist, reference memory,
   and standing feedback; it may not edit them as a side effect of project work.

## 4. Promotion: the only write path into shared memory

When a project ships (Gate 7 sign-off recorded in `project.yaml`), its approved
token set, reusable component patterns, and final spec/HTML pair are **promoted** into
`shared/reference-memory/` as a deliberate step — recorded in the project's final run
record, naming exactly what was promoted. Standing-scope feedback is promoted at
iteration time (`05-iteration.md` §5), since waiting for ship would mean repeating the
preference meanwhile. Nothing else writes to `shared/` from inside a project run.

## 5. Indicators across projects

`07-indicators.md` roll-ups read across `projects/*/runs/` — that is the ledger the
`indicator-reporter` aggregates. Per-project indicators stay in the project; the trend
("iteration rounds to approval dropping as reference memory grows") is only meaningful
across projects, which is why run records live in a uniform shape in every project.

## 6. Creating a project

`/ingest-prd` creates the project when given a new PRD: slugify the title, scaffold the
layout above, copy the source file(s) into `inputs/` verbatim (the original artifact is
part of the audit trail), write `project.yaml` with `status: ingesting`, then run
extraction. A PRD revision goes to the **same** project (new requirement versions, same
req_ids per the stability contract) — a genuinely different product area gets a new one.
