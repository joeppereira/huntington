# 01 — Ingestion

Turns a PRD (docx), reference image(s), and/or free-text input into one structured,
classified **Requirements Document**. Owned by the `requirements-extractor` agent
(see `06-agents-and-memory.md`). Writes **Requirement Memory**.

## 1. Inputs

| Input type | Examples | Extraction method |
|---|---|---|
| `.docx` PRD | Wire Tracking Center PRD, Huntington Payment OPs doc | Convert to text, preserving section/table structure |
| `.md` spec | `ui_specification_returns_dashboard.md`-style design specs | Parsed as-is; already semi-structured |
| Image(s) | Screenshots of existing/reference UIs | Vision-model read: layout regions, component inventory, color/typography inference, visible text content |
| Free text | User-typed requirements or clarifications | Parsed as-is, same requirement schema as PRD-derived items |

A single pipeline run may combine multiple inputs (e.g., a PRD plus a reference
screenshot of the desired visual style) — they merge into one Requirements Document,
not parallel ones.

## 2. Output: the Requirements Document

One record per requirement:

```yaml
req_id: REQ-JT-01              # stable; see "req_id stability" contract in specs/README.md
title: FedEx-Style Progress Bar
description: >
  Domestic wires must display a visual milestone timeline...
source:
  document: "Wire Tracking Center - PRD.docx"
  section: "3.3 Journey Tracking & SWIFT gpi Integration"
audience: customer             # customer | internal — see §3, hard gate
ambiguous: false               # see §4
ambiguity_notes: null
risk_flags: []                 # see §5, e.g. [security-sensitive]
depends_on_backend: true       # true when the PRD itself flags backend work (e.g. REQ-JT-01's "Settled" note)
```

## 3. Audience classification — hard gate

Every requirement gets `audience: customer` or `audience: internal`. This is not a
best-effort tag; it is checked before the Requirements Document leaves this stage.

- **Default to `internal`** when a requirement describes bank-employee workflows,
  queues, case management, or fraud/risk-code mapping — anything a client never sees.
- **Tag `customer`** when a requirement describes something rendered in or triggered
  from the client-facing app, even if the underlying data is sensitive (e.g., REQ-EX-01's
  *vetted* hold-reason copy is customer-facing; the fraud-code-to-copy mapping behind it
  is internal and stays in Requirement Memory as context only).
- A requirement that is **genuinely both** (rare) is split into two requirements with a
  shared `split_from` pointer, each independently classified. Never pass a mixed
  requirement downstream unsplit.

Only `audience: customer` requirements are eligible for `02-ui-spec-synthesis.md`.
`audience: internal` requirements still get a `req_id` and live in Requirement Memory —
they inform spec synthesis as context (e.g., "a fraud-hold exists" without exposing
"why") but never become a spec component themselves.

## 4. Ambiguity — flagged, never silently resolved

A requirement is `ambiguous: true` when it lacks a concrete acceptance criterion (e.g.,
"the system shall display contextual operational intelligence" with no defined trigger
or data source — REQ-DB-02 as written). Ambiguous requirements still get extracted and
classified, but:

- They are listed in the run's output for human clarification before spec synthesis
  treats them as resolved.
- The extractor **must not** silently invent the missing specificity (e.g., deciding
  unilaterally what "contextual operational intelligence" means). It may propose an
  interpretation, but tags it as a proposal, not a fact.
- Ambiguity count is a leading indicator (`07-indicators.md`).

## 5. Risk flags

Set `risk_flags: [security-sensitive]` when a requirement's description matches
fraud/compromised-credential/hold-reason language (the same category the PRD itself
calls out in REQ-EX-01). This flag follows the requirement into Requirement Memory and
is checked again at the denylist gate in `04-validation.md` §3 — catching it here is
leading signal; catching it there is the enforcement.

## 6. Gate before handoff

Before the Requirements Document is considered complete:

- Every requirement has `req_id`, `description`, `source`, `audience`.
- No requirement is left with `audience: null`.
- Ambiguous requirements are listed separately, not mixed silently into the confident set.

This gate is schema validation, run automatically (`04-validation.md` §1, Gate 1).
