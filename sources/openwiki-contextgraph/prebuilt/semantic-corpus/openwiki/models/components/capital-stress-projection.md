---
type: ModelComponent
title: Capital Stress Projection
description: The Stress_Projection sheet of MDL-CAP-003, which rolls CET1 capital and RWA forward nine quarters under the severely adverse scenario and yields the minimum stressed CET1 ratio (12.90% in Q3 2027) that drives the indicative stress capital buffer and the pass/fail check against the regulatory requirement.
tags: [stress-testing, cet1, severely-adverse, capital-planning, mdl-cap-003, ppnr, rwa, excel]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-05T01:46:21.335Z
sources:
  - id: openwiki-source-d7481767c8aa79de795d1f43
    resource: repo://sources/models/capital-planning-model.md
generated: { by: "openwiki/0.7.0", at: "2026-10-05T01:46:21.335Z" }
---

# Capital Stress Projection

The stress projection is the `Stress_Projection` sheet of the [Capital Planning & Stress Projection Model (MDL-CAP-003)](../capital-planning-model.md). It takes the Q2 2026 starting capital position, applies the severely adverse scenario's income, loss and RWA paths, and produces a quarterly CET1 capital, RWA and CET1 ratio path for Q3 2026 to Q3 2028. The lowest ratio on that path is the model's **minimum stressed CET1 ratio**. The scenario itself is described in [Internal Severely Adverse Scenario](../../scenarios/internal-severely-adverse.md). The institution and all figures are synthetic.

## Responsibilities

- Project quarter-end CET1 capital, standardized RWA and CET1 ratio for nine quarters under stress.
- Show headroom in $mm against both the 13.0% management target and the regulatory requirement for every quarter.
- Supply the minimum stressed ratio (`MIN(Stress_Projection!C20:K20)`) to the `Summary` sheet. That feeds the peak-to-trough decline, the [indicative stress capital buffer](indicative-stress-capital-buffer.md), and the "Stress minimum above requirement?" check.

It is the stressed counterpart to the [baseline projection](capital-baseline-projection.md). Both sheets start from the same `Assumptions` cells.

## Mechanism

Each projected quarter (columns C to K) is calculated left to right. Column B holds the Q2 2026 actuals taken from `Assumptions` (CET1 $101,200mm, RWA $668,400mm, 1,381mm shares, ratio 15.14%).

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: an unescaped angle bracket inside a label breaks rendering; rephrase the label. -->
```text
flowchart TD
    PPNR["PPNR (input)"] --> PTI["Pre-tax income = PPNR + provisions + trading/counterparty losses"]
    PROV["Provision for credit losses (input)"] --> PTI
    TRD["Trading & counterparty losses (input)"] --> PTI
    PTI --> TAX["Tax = -pre-tax x 22% (benefit on losses)"]
    PTI --> NI["Net income = pre-tax + tax"]
    TAX --> NI
    NI --> END["Ending CET1"]
    PREF["Preferred dividends (flat)"] --> END
    CD["Common dividends = prior shares x $1.15"] --> END
    BB["Buybacks = 0 (suspended)"] --> END
    OTH["Other CET1 movements -150"] --> END
    RWAG["RWA growth path (input)"] --> RWA["RWA(t) = RWA(t-1) x (1+g)"]
    END --> RATIO["CET1 ratio = CET1 / RWA"]
    RWA --> RATIO
    RATIO --> MIN["Minimum -> Summary"]
```

1. **Pre-tax income** = PPNR + provision for credit losses + trading and counterparty losses (`SUM(C7:C9)`). Losses are entered as negative numbers.
2. **Income tax** = `-pre-tax income x effective tax rate` (22%, FY2025 effective rate). Negative pre-tax income therefore produces a positive tax line, i.e. a tax benefit is recognised on losses rather than being capped at zero. The Q3 2026 benefit is +$1,166mm. Net income is pre-tax income plus the tax line.
3. **Ending CET1** = beginning CET1 + net income + preferred dividends + common dividends + share repurchases + other CET1 movements. Beginning CET1 is the prior quarter's ending CET1.
4. **Common dividends** = prior-quarter shares x $1.15 dividend per share.
5. **Share repurchases** are zero in every stress quarter. The cell notes label this "Buybacks suspended under stress (CCAR convention)". The share-count roll-forward still references the buyback row, so the count stays at 1,381mm and dividends stay flat at $1,588.15mm a quarter, in contrast to the baseline where buybacks shrink the share count and the dividend.
6. **RWA** compounds from the Q2 2026 base using a scenario-specific growth path rather than the baseline 1% per quarter. The ratio formula is guarded with `IF(RWA=0,0,...)`.
7. **Headroom** = ending CET1 minus (management target 13.0% or regulatory requirement 10.20%) x RWA.

### Scenario inputs

The sheet's operative inputs are scenario levers (blue font). They are not computed in the workbook:

| Quarter | PPNR | Provisions | Trading & counterparty | RWA growth |
| --- | --- | --- | --- | --- |
| Q3 2026 | 7,400 | -7,300 | -5,400 | +2.2% |
| Q4 2026 | 7,100 | -6,800 | 0 | +1.5% |
| Q1 2027 | 6,800 | -6,100 | 0 | +0.8% |
| Q2 2027 | 6,600 | -5,300 | 0 | +0.4% |
| Q3 2027 | 6,500 | -4,400 | 0 | 0.0% |
| Q4 2027 | 6,600 | -3,700 | 0 | -0.2% |
| Q1 2028 | 6,800 | -3,200 | 0 | -0.4% |
| Q2 2028 | 7,000 | -2,900 | 0 | -0.4% |
| Q3 2028 | 7,200 | -2,700 | 0 | -0.4% |

The trading and counterparty loss is a single Q3 2026 shock. Provisions peak in the first quarter and decay. Per the README, stress losses are top-down inputs supplied by the enterprise stress testing program, and the scenario paths come from [API-14 Macroeconomic Scenario API](../../apis/api-14-macroeconomic-scenario-api.md). The workbook does not itself translate macro variables into losses.

## Resulting path and outputs

| Quarter | Ending CET1 ($mm) | RWA ($mm) | CET1 ratio | Headroom vs 13.0% target ($mm) |
| --- | --- | --- | --- | --- |
| Q2 2026 (actual) | 101,200 | 668,400 | 15.14% | n/a |
| Q3 2026 | 95,068 | 683,105 | 13.92% | 6,264 |
| Q4 2026 | 93,304 | 693,351 | 13.46% | 3,168 |
| Q1 2027 | 91,852 | 698,898 | 13.14% | 995 |
| Q2 2027 | 90,867 | 701,694 | 12.95% | -353 |
| **Q3 2027** | 90,507 | 701,694 | **12.90%** | -713 |
| Q4 2027 | 90,771 | 700,290 | 12.96% | -267 |
| Q1 2028 | 91,581 | 697,489 | 13.13% | 907 |
| Q2 2028 | 92,781 | 694,699 | 13.36% | 2,470 |
| Q3 2028 | 94,293 | 691,920 | 13.63% | 4,343 |

Key reading points:

- **Trough**: the minimum is 12.90% in Q3 2027, the quarter RWA stops growing and CET1 capital reaches its low of $90,507mm. The peak-to-trough decline from the starting ratio is 2.24 percentage points (`Summary!B10 = B6 - B9`).
- **Recovery**: from Q4 2027 CET1 capital rises as stressed net income turns positive and RWA shrinks, so the ratio recovers to 13.63% by Q3 2028. This is still below the baseline ending ratio of 16.15%.
- **Against the requirement**: the stress minimum of 12.90% exceeds the 10.20% regulatory requirement (4.5% minimum + 3.20% current SCB + 2.50% G-SIB surcharge). `Summary!B18` is therefore "YES"; otherwise it would read "NO - capital action required". Regulatory headroom never falls below about $18.9bn.
- **Against the management target**: the ratio falls below the 13.0% Board Capital Committee target in Q2 2027 to Q4 2027, with a worst shortfall of about $713mm. The management target is a soft constraint and the regulatory requirement is the pass/fail test.

## Downstream use

`Summary` consumes only the ratio row (`C20:K20`) from this sheet for the minimum-ratio metric. The indicative SCB is `MAX(2.5%, starting ratio - minimum stressed ratio + four quarters of planned baseline dividends / starting RWA)`. With a 2.24% decline and a 0.94% dividend add-on it comes to 3.18%, against a current SCB of 3.20%. See [Stress Capital Buffer](../../concepts/stress-capital-buffer.md), [CET1 ratio](../../metrics/cet1-ratio.md), [Risk-weighted assets](../../metrics/risk-weighted-assets.md) and [G-SIB surcharge](../../concepts/gsib-surcharge.md). Results are disclosed through the Annual Report (Capital Risk Management) and Pillar 3 (stress testing).

## Invariants, assumptions and limitations

- Stress uses the same `Assumptions` cells as the baseline (starting capital, preferred dividends, dividend per share, tax rate, other movements). Changing them moves both sheets, and the shared 22% tax rate and flat -$150mm "other movements" are not stressed.
- The dividend is held flat at the starting share count and there are no buybacks. A distribution-plan change in `Assumptions` affects stress only through the dividend per share and starting shares. The $3,000mm quarterly buyback input is deliberately ignored.
- No AOCI volatility modelling and no deferred-tax-asset threshold deductions (README limitations). The full tax benefit on the Q3 2026 loss is assumed recoverable.
- Starting CET1 and RWA come from [API-16 Regulatory Reporting API](../../apis/api-16-regulatory-reporting-api.md). Liquidity constraints on distributions are cross-checked separately against [API-15](../../apis/api-15-treasury-liquidity-positions-api.md). Neither is computed in this sheet.
- The hard-coded scenario rows (PPNR, provisions, trading losses, RWA growth) have no formulas, so they must be refreshed manually from the stress testing program and API-14 when the scenario changes.

## Operating and changing the sheet

- Edit only blue-font input cells (scenario rows 7-9 and 18, plus `Assumptions`). Rows 10-17 and 19-23 are formulas.
- Any change to the row layout needs matching edits to the `Summary` formulas that reference `Stress_Projection!C20:K20`.
- The model is Tier 1 and independently validated by Model Risk Governance & Review (last validation 2026-02-27, next due 2027-02-28). Material changes to stress mechanics fall under [SR 11-7 model risk management](../../concepts/model-risk-sr-11-7.md).
- There are no automated tests. Verification is by recalculating the workbook and reconciling the `Summary` outputs (minimum 12.90%, decline 2.24%, requirement check "YES").
