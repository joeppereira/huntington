# UI Specification v1 — Wire Tracking Center

Synthesized per `specs/02-ui-spec-synthesis.md` from `requirements/requirements-v1.yaml`
(audience: customer only). Design tokens reused from
`shared/reference-memory/returns-dashboard-ui-spec.md` (same product family) — zero new
tokens proposed.

## 1. Design Tokens

| Token | Value | Tailwind class basis |
|---|---|---|
| `token.font.family` | Inter | `font-['Inter']` via body style |
| `token.brand.primary` | #059669 Emerald 600 | `emerald-600` |
| `token.brand.subtle` | #D1FAE5 Emerald 100 | `emerald-100` |
| `token.nav.bg` | #0F172A Slate 900 | `slate-900` |
| `token.nav.border` | #1E293B Slate 800 | `slate-800` |
| `token.status.error` | #E11D48 Rose 600 / #FFE4E6 Rose 100 | `rose-600` / `rose-100` |
| `token.status.warn` | #92400E Amber 800 / #FEF3C7 Amber 100 | `amber-800` / `amber-100` |
| `token.status.action` | #2563EB Blue 600 / #DBEAFE Blue 100 | `blue-600` / `blue-100` |
| `token.base.bg` | #F9FAFB Gray 50 | `gray-50` |
| `token.base.surface` | #FFFFFF | `white` |
| `token.base.text` | #111827 Gray 900 | `gray-900` |
| `token.base.text-secondary` | #6B7280 Gray 500 | `gray-500` |

Weights: 400 body, 500 labels/tabs, 600/700 headers/metrics (reference set).

## 2. Layout Architecture

- **App shell:** fixed dark sidebar (w-64, `token.nav.bg`) + scrollable light main
  workspace (`token.base.bg`), max-w-[1600px] inner container. Sidebar collapses under `md`.
- **Sidebar nav** (per PRD §1 — module sits alongside existing channel features):
  Balances, Payments & Transfers, FX Global, **Wire Tracking Center (active)**,
  Reporting & Analytics, Security & Administration.
- **Header:** breadcrumbs `Treasury / Payments / Wire Tracking Center`, page title,
  persistent **Contact Support** button (REQ-SS-02).
- **Horizontal tabs:** All Wires · Outgoing · Incoming · International · Held for Review
  · Returned · Alerts & Notifications. Active: 2px emerald bottom border.

## 3. Component Tree

| component_id | satisfies | notes |
|---|---|---|
| `app-shell-sidebar` | — (layout) | channel nav context |
| `header-support` | REQ-SS-02 | persistent Contact Support button |
| `nav-tabs` | REQ-SF-02 (partial: type/status views) | tab set above |
| `metrics-tiles` | REQ-DB-01 | 4 tiles: count + $ value each (Outgoing, Incoming Today, Pending Review, International in Transit) |
| `insights-strip` | REQ-DB-02 | PROPOSAL rendering (req is ambiguous): emerald-tinted strip, PRD example copy as placeholder |
| `search-bar` | REQ-SF-01 | single input, placeholder enumerates all 7 search parameters |
| `filter-row` | REQ-SF-02 | date-range select, wire-type select, status select |
| `wire-table` | REQ-SF-01, REQ-SF-02 | result grid: ID, beneficiary, type, amount, status badge, updated. Row click → detail |
| `wire-detail` | REQ-SF-03 | full metadata panel for selected wire |
| `fee-breakdown` | REQ-SF-04 | originating / intermediary / beneficiary bank fees + total |
| `journey-timeline` | REQ-JT-01 | 5-step FedEx-style bar; "Settled" step rendered with `pending-backend` treatment + footnote (depends_on_backend) |
| `gpi-route` | REQ-JT-02 | horizontal route: Originated → SWIFT Sent → Intermediary → Beneficiary Bank → Delivered, node states |
| `route-insights` | REQ-JT-03 | intermediary count, currency completion rate, typical recipient fees |
| `detail-actions` | REQ-SS-01, REQ-SS-03, REQ-SS-04 | Explain delays link, Download report, Share status, Notify-me toggle |
| `held-wires-panel` | REQ-EX-01, REQ-EX-02 | vetted-copy reason per wire (NEVER internal codes/fraud language), Confirm + Reject buttons |
| `release-insight` | REQ-EX-03 | post-action insight line (static demo state shown on one card) |
| `returned-wires-panel` | REQ-EX-04 | return reason, root-cause insight, recommended resolution, full timeline fidelity |
| `alerts-panel` | REQ-SS-05 | category subscriptions: Outgoing (Released/Receipt Confirmed/Settled/Returned), Incoming, International |

## 4. Coverage

All 18 `audience: customer` requirements cited. `out_of_scope_for_ui`: none.
REQ-JT-01's "Settled" state is included but visually marked pending-backend per the
PRD's own note. Internal reqs (REQ-TECH-01..03) inform treatments (footnote, vetted
copy) but are cited by no component.

## 5. Interaction states

Status badges: Settled (`brand.subtle`/`brand.primary`), Pending (`status.warn`),
Held (`status.error` tint), In Transit (`status.action` tint), Returned (`status.error`).
All components define `default`; `journey-timeline`/`gpi-route` define
complete/active/upcoming/pending-backend. Degraded states (spec 08 §6) deferred to the
production build — this is the design-contract prototype.

## 6. Placeholder data rule

All figures/names are obviously-demo values (Acme Manufacturing, Globex GmbH, round
timestamps). No real account/routing numbers; account display is masked format `••••1234`.
