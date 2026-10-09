---
type: Scenario
title: Internal Severely Adverse Scenario
description: The firm's internally developed severely adverse macroeconomic and market scenario (set SA-2025-INT), distributed by the Macroeconomic Scenario API and used by the Capital Planning & Stress Projection Model (MDL-CAP-003) to project a minimum stressed CET1 ratio of 12.90% and an indicative stress capital buffer.
tags: [scenario, severely-adverse, stress-testing, capital-planning, cet1, mdl-cap-003, api-14, sa-2025-int]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-05T01:46:21.335Z
sources:
  - id: openwiki-source-c3acaa34a43dd572034594c6
    resource: repo://sources/api_docs/apis/api-14-macroeconomic-scenario-api.md
  - id: openwiki-source-d7481767c8aa79de795d1f43
    resource: repo://sources/models/capital-planning-model.md
  - id: openwiki-source-eb14da62fbec45aad876fb64
    resource: repo://sources/reports/mhfc-2025-annual-report.md
  - id: openwiki-source-c13af588d055d118eda543d5
    resource: repo://sources/reports/mhfc-2025-pillar3-disclosures.md
  - id: openwiki-source-9da334bbfcfb68cd7514ff33
    resource: repo://sources/reports/mhfc-q2-2026-earnings-supplement.md
generated: { by: "openwiki/0.7.0", at: "2026-10-05T01:46:21.335Z" }
---

# Internal Severely Adverse Scenario

The internal severely adverse scenario is the firm's own deep-recession and market-shock scenario, run at least semi-annually alongside the Federal Reserve's supervisory CCAR severely adverse scenario. It is the stress case in the nine-quarter capital projection of [Capital Planning & Stress Projection Model (MDL-CAP-003)](../models/capital-planning-model.md). The scenario is published as the scenario set `SA-2025-INT` through the [Macroeconomic Scenario API (API-14)](../apis/api-14-macroeconomic-scenario-api.md). The institution (Meridian Harbor Financial Corp.) and all figures are synthetic.

## Scenario definition

The 2025 Pillar 3 disclosure gives the headline peak or trough values:

| Variable | Internal severely adverse value |
| --- | --- |
| U.S. unemployment rate (peak) | 10.2% |
| U.S. real GDP (peak-to-trough) | -6.4% |
| Equity prices (S&P 500-style index, trough) | -41% |
| House prices (trough) | -28% |
| Commercial real estate prices (trough) | -35% |
| 10-year Treasury yield (trough) | 0.9% |
| BBB corporate spread (peak) | +5.4 pp |
| Global market shock | Instantaneous, applied in the first quarter |

For comparison, the approved `MSC-2025Q4` set returned by API-14 uses probability-weighted Upside, Baseline and Downside paths. Its Downside path peaks at 6.8% unemployment with house prices -8.5% and CRE prices -14%. The severely adverse set is therefore much harsher than the Downside scenario used for CECL weighting. It is a separate, internally owned set and does not carry a probability weight in the CECL scheme described in the API examples.

## Delivery through API-14

- API-14 (`/scenarios/v1`, v1.6) distributes approved macroeconomic scenario sets with their probability weights. The paths cover unemployment, GDP, house prices, CRE prices, rates and spreads.
- Sets are versioned and locked after Scenario Committee approval. Consumers read them through `GET /scenario-sets`, `GET /scenario-sets/{setId}` and `GET /scenario-sets/{setId}/paths/{variable}`. `SA-2025-INT` is named in the API documentation as an example set ID.
- The `scenarios:read` scope is enough for consumers. `scenarios:approve` is a separate scope. The API is internal only, restricted-classified and limited to 30 requests per minute.
- The internal severely adverse set was added in API v1.5 (October 2025). The v1.6 migration to the strategic data platform (2Q26) cut load time from six hours to under forty minutes. A new set is published within one business day of approval.
- Upstream inputs are economics research, Federal Reserve supervisory scenarios and Scenario Committee approvals. Downstream consumers are the CECL model (MDL-CR-007), MDL-CAP-003 and the Credit Risk Scoring API (API-10). The scope list also names stress testing and ALM as intended consumers.

## How the capital model applies it

The scenario drives the `Stress_Projection` sheet, described in [Capital Stress Projection](../models/components/capital-stress-projection.md). The model workbook states that the scenario paths come from API-14 (a "CCAR 2026 analogue"). Stress losses are not computed in the workbook. PPNR, provisions, trading and counterparty losses and the RWA growth path are top-down inputs supplied by the enterprise stress testing program.

Conventions applied under the scenario:

- Share repurchases are suspended (zero in all nine quarters), following the CCAR convention.
- Common dividends are held flat. Preferred dividends stay at $260mm a quarter and the share count stays at 1,381mm. Dividends are therefore $1,588.15mm per quarter.
- Tax is recognised at the 22% effective rate, with a tax benefit on losses.
- Other CET1 movements stay at -$150mm per quarter.
- RWA first rises because of draws on commitments and higher counterparty exposure, then shrinks. Quarterly growth is 2.2%, 1.5%, 0.8%, 0.4% and 0%, then -0.2% and -0.4% for the last three quarters.
- The market shock hits in the first projected quarter (Q3 2026) as a $5,400mm trading and counterparty loss. Pre-tax income that quarter is -$5,300mm.

## Resulting trajectory (Q2 2026 start)

| Quarter | CET1 ratio | Headroom vs 13.0% management target ($mm) |
| --- | --- | --- |
| Q2 2026 (actual) | 15.14% | n/a |
| Q3 2026 | 13.92% | 6,264 |
| Q4 2026 | 13.46% | 3,168 |
| Q1 2027 | 13.14% | 995 |
| Q2 2027 | 12.95% | -353 |
| Q3 2027 (trough) | 12.90% | -713 |
| Q4 2027 | 12.96% | -267 |
| Q1 2028 | 13.13% | 907 |
| Q2 2028 | 13.36% | 2,470 |
| Q3 2028 | 13.63% | 4,343 |

- CET1 capital falls from $101,200mm to a low of $90,507mm in Q3 2027. It recovers to $94,293mm by Q3 2028.
- The minimum stressed [CET1 ratio](../metrics/cet1-ratio.md) is 12.90%. That is a 2.24 percentage point peak-to-trough decline from 15.14%.
- The ratio falls below the 13.0% management target from Q2 2027 to Q4 2027. It stays well above the 10.20% regulatory requirement (4.5% + 3.2% SCB + 2.5% G-SIB surcharge) in every quarter, so the `Summary` check "Stress minimum above requirement?" returns YES.

## Downstream use

- **Indicative SCB.** `Summary` computes `MAX(2.5%, peak-to-trough decline + four quarters of planned baseline dividends / starting RWA)`. This is 2.24% + 0.94% = 3.18%, against the 3.2% preliminary supervisory SCB. See [Indicative Stress Capital Buffer](../models/components/indicative-stress-capital-buffer.md).
- **Risk appetite.** The Board risk appetite sets a floor of 10.2% on the minimum stressed CET1 ratio under the internal severely adverse scenario. The 2025 disclosure reported 12.6% (status: within), and the 2026 projection of 12.90% is above that floor.
- **Disclosure.** Results feed the Annual Report capital risk management section, Pillar 3 section 13 and the quarterly earnings supplement. The model is re-run each quarter with updated starting capital, RWA and scenario paths. The 2025 Pillar 3 report does not reproduce projection outputs because they are refreshed quarterly.
- **Reverse stress tests.** These are separate from this scenario. They search for scenarios that would breach requirements. The 2025 cases were a cyber event combined with a severe recession, and sustained negative policy rates.

## Invariants, risks and limitations

- API-14 distributes approved sets, and sets are versioned and locked after Scenario Committee approval. Changing a locked scenario therefore implies publishing a new version, which the sources imply but do not spell out.
- The workbook is simplified. It does not model AOCI volatility or deferred-tax-asset threshold deductions, and stress losses are not derived inside it. Changes to scenario severity only change capital results once the enterprise stress testing program refreshes the loss and RWA inputs.
- API-14 is a registered critical data source for MDL-CAP-003. A breaking schema or business-logic change opens a model change review. MDL-CAP-003 is a Tier 1 model, validated annually by Model Risk Governance & Review (last validated 2026-02-27).
- The API example documents Upside, Baseline and Downside fields (`peakUnemployment`, `realGdp2026`, `hpiChange`, `creChange`). It does not show the payload for `SA-2025-INT`. The values in the scenario table come from the Pillar 3 disclosure, not from the API documentation.
