# 07 — Indicators

Leading indicators are measured **before** human review and predict rework risk.
Lagging indicators are measured **after** human review and report what actually
happened. Never blend them into one score — a run can look healthy on every leading
indicator and still fail review, and that gap is itself the signal worth tracking.
Computed by the `indicator-reporter` agent from Run/Episodic Memory plus the other five
memory types.

## Leading indicators (pre-review)

| Indicator | What it measures | Why it leads |
|---|---|---|
| Requirement extraction coverage | parsed `req_id`s ÷ requirement-like statements detected in the source doc | A low number means the extractor is missing scope before synthesis ever starts |
| Requirement ambiguity rate | ambiguous requirements ÷ total, per PRD | High ambiguity predicts rework after a human clarifies intent later |
| Audience-classification confidence | requirements the extractor flagged as borderline `customer`/`internal` ÷ total | Predicts scope-boundary mistakes (`specs/context.md`) before they reach generation |
| Requirement→spec coverage at synthesis | `audience: customer` req_ids cited by a spec component ÷ total, before generation starts | Below 100% without an explicit exception means generation will produce incomplete UI |
| Design-token resolution rate | tokens resolved to concrete values ÷ tokens referenced | Unresolved tokens predict inconsistent or placeholder visuals downstream |
| Denylist hits at ingestion | security-sensitive flags raised during extraction | **A healthy number is not zero** — it means content that needed scrutiny got it before generation; track as a leading signal, not a defect count |
| Time: input → first-draft spec | wall-clock per run | Operational efficiency, not quality — track for cost planning, not as a quality gate |
| Self-validation first-pass rate | runs where Gates 1–2 (`04-validation.md`) pass without an extractor/synthesizer retry | Predicts how many rounds a run will likely need before human review |

## Lagging indicators (post-review)

| Indicator | What it measures | Zero-tolerance? |
|---|---|---|
| Time: input → human-approved ship | wall-clock from first ingestion to `shipped` sign-off | No — track as a trend |
| Iteration rounds to approval | count of `05-iteration.md` rounds before sign-off | No — a high count across many PRDs suggests the synthesis stage isn't capturing intent well enough |
| Post-ship manual edit volume | components/lines a human changed by hand after agent output, before approving | No — but a rising trend means agent output quality is regressing |
| Traceability gaps found in human review | requirements a reviewer finds missing from the shipped UI that gates didn't catch | No, but treat as a gate escape — investigate why Gate 2 missed it |
| Accessibility violations at final audit | WCAG/semantic findings in the shipped artifact | Should trend to zero; not a hard incident the way security is |
| **Denylist/security leaks in a shipped artifact** | sensitive content that reached a customer-facing surface | **Yes — any count > 0 is a severity-1 incident**, reported immediately, not batched into a periodic metrics review |
| Design-token drift in shipped HTML | hardcoded values that slipped past Gate 4 | Should trend to zero |
| Stakeholder first-review approval rate | reviews approved with zero requested changes ÷ total reviews | No — track as the headline quality signal across PRDs over time |
| Regression rate on re-generation | sections outside a delta's intended scope that changed anyway (per Gate 6) | No, but a rising trend means scoped regeneration (`05-iteration.md` §2) is leaking scope |

## Reporting

`indicator-reporter` writes one summary per run to Run/Episodic Memory and can roll up
across runs (e.g., "across the last 5 PRDs, average iteration rounds to approval has
dropped from 4 to 2" — the expected trend as Reference Memory's pattern library grows).
Any severity-1 security finding is surfaced immediately on its own, never folded into a
rolled-up report where it could be averaged away.
