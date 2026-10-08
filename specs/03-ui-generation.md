# 03 — UI Generation

Turns a UI Specification into a runnable, single-file Tailwind HTML dashboard — the
shape demonstrated by `dashboard_aggregates.html`. Owned by the `ui-generator` agent.
Stateless with respect to memory (reads **Spec Memory** and **Reference Memory**; writes
no persistent memory of its own — the generated file itself is the artifact).

## 1. Why single-file HTML first

A component-framework build (React/etc.) is a later, deliberate decision — not assumed
here. Single-file Tailwind HTML is the fastest path from spec to something a
stakeholder can open in a browser and react to, and it matches both reference artifacts
this project started from. Don't introduce a build step before someone needs one.

## 2. Section-by-section generation

The component tree in the UI spec is the unit of generation, not the whole document:

- Each top-level component (e.g., sidebar, header/tabs, journey-progress-bar,
  held-wire-review-panel) is generated independently from its own spec entry.
- This is what makes `05-iteration.md` cheap: a feedback delta that touches one
  component regenerates only that component's HTML fragment, not the whole file.
- The assembler (not the generation agent) stitches fragments into the final document in
  the order the spec's layout architecture defines.

## 3. Token compliance — enforced, not just requested

Every class/value the generator emits must resolve to a token declared in the spec's
design-token set (§2.1 of `02-ui-spec-synthesis.md`). Concretely:

- Tailwind utility classes are chosen from the mapping of token → class established when
  the spec was written (e.g., `token.brand.primary` → `bg-emerald-600`), not picked ad
  hoc by the generator per component.
- No arbitrary-value Tailwind syntax (`bg-[#123abc]`) unless that exact value traces to a
  named token. This is checked statically in `04-validation.md` §4.

## 4. What the generator must not do

- Must not invent a requirement or a component not present in the spec (generation is a
  rendering step, not a design step — design decisions belong in `02`).
- Must not fabricate data values for anything the eventual real app would source from a
  backend. Sample/placeholder data is clearly a visual placeholder (e.g., realistic but
  obviously-demo values), never presented as if live.
- Must not surface `audience: internal` content — by construction this shouldn't be
  possible (the generator only ever sees a spec built from `audience: customer`
  requirements), but the denylist scan in `04-validation.md` §3 checks the generated
  output anyway, not just the spec, as defense in depth.

## 5. Gate before handoff

- Every spec component has a corresponding HTML fragment.
- No fragment references a token-mapped class with a literal override.
- The assembled document renders (valid HTML, no console errors from the Tailwind CDN
  build) — a basic smoke check, not full validation (that's `04`).
