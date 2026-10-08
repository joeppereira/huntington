# 02 — UI Spec Synthesis

Turns `audience: customer` requirements (plus optional reference image/design tokens)
into a structured **UI Specification** — the shape demonstrated by
`ui_specification_returns_dashboard.md`: design tokens, layout architecture, component
tree. Owned by the `ui-spec-synthesizer` agent. Writes **Spec Memory**. Reads
**Requirement Memory** and **Reference Memory**.

## 1. Inputs

- The Requirements Document from `01-ingestion.md`, filtered to `audience: customer`.
- Optional reference image(s) (existing UI screenshot) — informs tokens and layout, not
  requirements.
- Optional existing design-token set from Reference Memory (e.g., a prior approved
  dashboard's palette/typography) — reused when the new PRD is for the same product
  family, so a second or third dashboard doesn't reinvent a visual language.
- `audience: internal` requirements are available as **context only** (e.g., "a
  fraud-hold mechanism exists") — never cited by a spec component.

## 2. Output structure

Mirrors the reference spec format:

1. **Design tokens** — typography (family, weights), color palette (semantic roles:
   brand/active, alerts/status by category, base/surface, text), spacing scale. Sourced
   from the reference image when present, else from Reference Memory's existing palette
   for this product family, else proposed and flagged for human confirmation.
2. **Layout architecture** — app shell (nav placement, breakpoints), header/navigation
   pattern, content grid.
3. **Component tree** — one entry per UI component, each declaring:
   ```yaml
   component_id: journey-progress-bar
   satisfies: [REQ-JT-01]          # required, see §3
   data_fields: [stage, timestamp, status]
   visual_treatment:                # tokens only, see §4
     active_color: token.brand.primary
     inactive_color: token.base.text-secondary
   interaction_states: [default, active, complete, error]
   ```

## 3. Requirement coverage — bidirectional, 100% or explicit exception

- Every `audience: customer` req_id must be cited by `satisfies` on ≥1 component, **or**
  explicitly marked `out_of_scope_for_ui: true` with a reason (e.g., REQ-JT-01's note
  that "Settled" status needs backend work first — the spec can still include the
  component with a defined-but-unreachable state, but must say so).
- Every component's `satisfies` list must point to req_ids that actually exist in the
  Requirements Document. No component invents a requirement to justify itself.
- This bidirectional check is Gate 2 in `04-validation.md`.

## 4. Visual values — tokens only

No component's `visual_treatment` may contain a literal color/size value. Every value is
a reference into the design-token set defined in §2.1. This is enforced at generation
time too (`03-ui-generation.md` §3) but is a synthesis-time discipline first — a spec
with inline hex codes is already wrong before any HTML exists.

## 5. Reusing patterns across PRDs

Because this pipeline will see multiple PRDs for the same institution (Wire Tracking
Center, then others), before proposing a new component the synthesizer checks Reference
Memory for an existing component of the same shape (e.g., a "FedEx-style journey
tracker" pattern). Reuse — with adaptation, not duplication — is preferred; a new
visually-divergent pattern for the same interaction concept is a design-consistency risk,
not a feature.

## 6. Gate before handoff

- Schema valid (tokens/layout/components all present and well-formed).
- 100% `audience: customer` requirement coverage (cited or explicitly excepted).
- No `audience: internal` requirement appears in any component's `satisfies` list.
- No literal visual value outside the declared token set.
