---
type: ModelComponent
title: Capital Baseline Projection
description: The Baseline_Projection sheet of the Capital Planning & Stress Projection Model (MDL-CAP-003). It rolls CET1 capital, RWA, share count and capital headroom forward nine quarters (Q3 2026 to Q3 2028) under the firm's baseline plan.
tags: [capital-planning, cet1, baseline-projection, mdl-cap-003, rwa, distributions]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-05T01:46:21.335Z
sources:
  - id: openwiki-source-d7481767c8aa79de795d1f43
    resource: repo://sources/models/capital-planning-model.md
generated: { by: "openwiki/0.7.0", at: "2026-10-05T01:46:21.335Z" }
---

# Capital Baseline Projection

The baseline projection is the `Baseline_Projection` sheet of the Excel workbook behind the [Capital Planning Model](../capital-planning-model.md) (MDL-CAP-003). It projects quarter-end CET1 capital, standardized RWA, the [CET1 ratio](../../metrics/cet1-ratio.md), share count and headroom over nine quarters under the firm's financial and distribution plan. The projection starts from the Q2 2026 actuals and runs from Q3 2026 to Q3 2028. The workbook is a synthetic proof-of-concept model for the fictional Meridian Harbor Financial Corp. The figures below come from that model.

The component has no code. It is a grid of formulas that read the `Assumptions` sheet. Its outputs feed the `Summary` sheet and serve as the reference path for the `Stress_Projection` sheet.

## Responsibilities

- Roll CET1 capital forward one quarter at a time: CET1(t) = CET1(t-1) + net income − preferred dividends − common dividends − share repurchases + other CET1 movements.
- Roll standardized RWA forward at a constant quarterly growth rate.
- Derive the CET1 ratio, the share count, and dollar headroom against both the management target and the regulatory requirement.
- Supply the baseline figures that `Summary` uses for ratio and distribution outputs, and the planned dividend run-rate used in the indicative stress capital buffer (SCB) formula.

<!-- openwiki: broken internal link [../../../sources/models/capital-planning-model.md#L35-L41] heading anchor "L35-L41" does not exist in "../../../sources/models/capital-planning-model.md". Fix the href or restore the target, then delete this comment. -->
<!-- openwiki: broken internal link [../../../sources/models/capital-planning-model.md#L166-L290] heading anchor "L166-L290" does not exist in "../../../sources/models/capital-planning-model.md". Fix the href or restore the target, then delete this comment. -->
Sources: [README formulas](../../../sources/models/capital-planning-model.md#L35-L41), [Baseline_Projection formulas](../../../sources/models/capital-planning-model.md#L166-L290).

## Inputs

All inputs come from the `Assumptions` sheet (blue cells are hard-coded inputs). Baseline rows reference them with absolute references. No scenario or API data is read directly on this sheet.

| Input | Value | Provenance noted in the model |
|---|---|---|
| Starting CET1 capital | $101,200mm | API-16 Regulatory Reporting API, Q2 2026 |
| Starting standardized RWA | $668,400mm | API-16, Q2 2026 |
| Starting common shares | 1,381mm | Transfer agent, 2026-06-30 |
| Quarterly net income | $6,600mm, growing 0.8% per quarter | Financial plan 2026-2028 |
| Preferred dividends | $260mm per quarter | Contractual |
| Common dividend per share | $1.15 per quarter, flat | Board-declared |
| Share repurchases | $3,000mm per quarter | Board-authorised $30bn program, 2025-2028 |
| Assumed share price | $262, flat | Used for share-count roll-forward |
| RWA growth | 1.0% per quarter | Balance sheet plan |
| Other CET1 movements | −$150mm per quarter | AOCI, deductions and employee stock plans, net |
| Management target CET1 ratio | 13.0% | Board Capital Committee |
| Regulatory CET1 requirement | 10.2% (4.5% minimum + 3.2% current SCB + 2.5% G-SIB surcharge) | `Assumptions!B23` formula |

<!-- openwiki: broken internal link [../../../sources/models/capital-planning-model.md#L116-L141] heading anchor "L116-L141" does not exist in "../../../sources/models/capital-planning-model.md". Fix the href or restore the target, then delete this comment. -->
Source: [Assumptions sheet](../../../sources/models/capital-planning-model.md#L116-L141).

## Mechanics

The sheet has one column per quarter. Column B is the Q2 2026 actual, and columns C to K are the nine projected quarters. Each row follows a fixed pattern.

1. **Opening balance.** Beginning CET1 equals the prior column's ending CET1. The Q2 2026 actual ending CET1 comes straight from `Assumptions`.
2. **Net income.** `Assumptions!B9 × (1 + growth)^n`, with n = 0 for Q3 2026 and n = 8 for Q3 2028. Net income is a compounded plan input and is independent of RWA or the capital position.
3. **Preferred dividends and buybacks.** Both are constant outflows ($260mm and $3,000mm per quarter).
4. **Common dividends.** The dividend is the prior quarter-end share count multiplied by the dividend per share. A quarter's dividend therefore reflects buybacks only through the previous quarter.
5. **Share count.** Shares(t) = Shares(t-1) + buyback(t) / assumed price. The buyback is stored as a negative number, so shares fall by about 11.45mm per quarter. Dividends fall from $1,588mm to $1,483mm over the horizon.
6. **Ending CET1.** The sum of the opening balance and rows 7 to 11.
7. **RWA.** RWA(t) = RWA(t-1) × (1 + growth), with growth pulled per quarter from `Assumptions!B15`.
8. **CET1 ratio.** Ending CET1 / RWA, guarded with `IF(RWA=0, 0, …)` for projected quarters.
9. **Headroom.** Ending CET1 − (target or requirement ratio × RWA), in $mm. Headroom is computed for projected quarters only.

<!-- openwiki: broken internal link [../../../sources/models/capital-planning-model.md#L179-L223] heading anchor "L179-L223" does not exist in "../../../sources/models/capital-planning-model.md". Fix the href or restore the target, then delete this comment. -->
<!-- openwiki: broken internal link [../../../sources/models/capital-planning-model.md#L224-L272] heading anchor "L224-L272" does not exist in "../../../sources/models/capital-planning-model.md". Fix the href or restore the target, then delete this comment. -->
<!-- openwiki: broken internal link [../../../sources/models/capital-planning-model.md#L273-L290] heading anchor "L273-L290" does not exist in "../../../sources/models/capital-planning-model.md". Fix the href or restore the target, then delete this comment. -->
Sources: [net income, dividends, repurchases formulas](../../../sources/models/capital-planning-model.md#L179-L223), [ending CET1, RWA, ratio, shares](../../../sources/models/capital-planning-model.md#L224-L272), [headroom](../../../sources/models/capital-planning-model.md#L273-L290).

## Baseline outputs

With the current inputs the plan is accretive throughout. Net income exceeds distributions and other CET1 movements by roughly $1.6bn in the first quarter (CET1 rises from $101,200mm to $102,802mm), and the gap widens each quarter.

- CET1 capital rises from $101,200mm to $118,027mm.
- RWA rises from $668,400mm to $731,019mm.
- The CET1 ratio rises every quarter, from 15.14% to 16.15% at Q3 2028.
- The baseline minimum is 15.23%, in the first projected quarter, Q3 2026. It is the minimum over the projected columns only (`MIN(C15:K15)`) and excludes the Q2 2026 starting ratio.
- Headroom against the 13.0% management target grows from about $15.0bn to about $23.0bn. The Q3 2028 figure is reported on `Summary` as additional distribution capacity at the target.
- Headroom against the 10.2% regulatory requirement grows from about $33.9bn to about $43.5bn.
- Cumulative buybacks over the horizon are $27,000mm, which is nine quarters of $3,000mm, and sit below the $30bn authorised program.

<!-- openwiki: broken internal link [../../../sources/models/capital-planning-model.md#L151-L164] heading anchor "L151-L164" does not exist in "../../../sources/models/capital-planning-model.md". Fix the href or restore the target, then delete this comment. -->
<!-- openwiki: broken internal link [../../../sources/models/capital-planning-model.md#L75-L108] heading anchor "L75-L108" does not exist in "../../../sources/models/capital-planning-model.md". Fix the href or restore the target, then delete this comment. -->
Sources: [Baseline_Projection values](../../../sources/models/capital-planning-model.md#L151-L164), [Summary](../../../sources/models/capital-planning-model.md#L75-L108).

## Relationship to the stress projection and Summary

The baseline and `Stress_Projection` sheets share the same roll-forward identity and the same starting position. The stress sheet differs in these ways:

- **Income:** net income is built from pre-provision net revenue (PPNR) less provisions less trading and counterparty losses, taxed at 22%. A tax benefit is recognised on losses.
- **Buybacks:** buybacks are suspended, following the CCAR convention.
- **Common dividends:** dividends are held flat, because the share count never falls.
- **RWA:** RWA follows a scenario growth path instead of a constant 1% per quarter.

`Summary` reads the baseline sheet in these ways:

- Starting ratio is `Baseline_Projection!B15`.
- Ending ratio is `K15`.
- Baseline minimum is the MIN over `C15:K15`.
- Cumulative buybacks are the sum of `C10:K10`.
- Q3 2028 excess capital versus target is `K17`.
- Four quarters of planned dividends divided by starting RWA, `-SUM(C9:F9) / B14`, is the dividend add-on in the indicative SCB.

The indicative SCB is `MAX(2.5%, start CET1 ratio − minimum stressed ratio + dividend add-on)`. The baseline therefore influences the SCB only through the starting ratio and the first four quarters of common dividends. It does not set the stress path.

<!-- openwiki: broken internal link [../../../sources/models/capital-planning-model.md#L322-L444] heading anchor "L322-L444" does not exist in "../../../sources/models/capital-planning-model.md". Fix the href or restore the target, then delete this comment. -->
<!-- openwiki: broken internal link [../../../sources/models/capital-planning-model.md#L92-L108] heading anchor "L92-L108" does not exist in "../../../sources/models/capital-planning-model.md". Fix the href or restore the target, then delete this comment. -->
<!-- openwiki: broken internal link [../../../sources/models/capital-planning-model.md#L446-L456] heading anchor "L446-L456" does not exist in "../../../sources/models/capital-planning-model.md". Fix the href or restore the target, then delete this comment. -->
Sources: [Stress_Projection formulas](../../../sources/models/capital-planning-model.md#L322-L444), [Summary formulas](../../../sources/models/capital-planning-model.md#L92-L108), [stress cell notes](../../../sources/models/capital-planning-model.md#L446-L456).

## Invariants, limits and failure modes

- **Sign convention.** Outflow rows (preferred dividends, common dividends, repurchases, other movements) are stored as negative values and summed. Changing an input's sign convention double-counts or reverses the flow.
- **Hard-coded horizon.** The nine quarters are physical columns (C to K). The net income exponent is typed into each cell (`^0` … `^8`), not derived from the column. Extending the horizon or inserting a quarter means copying and adjusting these formulas by hand.
- **Flat price and dividend.** The share price and dividend per share are constant, so dividends fall only because the buyback shrinks the share count.
- **Independent drivers.** Net income and RWA growth are independent plan inputs. The sheet does not link earnings to balance sheet growth, so changing the RWA growth assumption does not change net income.
- **Documented simplifications.** The model has no AOCI volatility modelling and no deferred-tax-asset threshold deductions. AOCI and deductions are lumped into the flat −$150mm "other movements" line.
- **Requirement stack.** The regulatory requirement is static in the baseline. It uses the current SCB of 3.2%, while `Summary` also shows the requirement under the indicative SCB (10.18%).

<!-- openwiki: broken internal link [../../../sources/models/capital-planning-model.md#L56-L60] heading anchor "L56-L60" does not exist in "../../../sources/models/capital-planning-model.md". Fix the href or restore the target, then delete this comment. -->
<!-- openwiki: broken internal link [../../../sources/models/capital-planning-model.md#L116-L141] heading anchor "L116-L141" does not exist in "../../../sources/models/capital-planning-model.md". Fix the href or restore the target, then delete this comment. -->
<!-- openwiki: broken internal link [../../../sources/models/capital-planning-model.md#L103-L104] heading anchor "L103-L104" does not exist in "../../../sources/models/capital-planning-model.md". Fix the href or restore the target, then delete this comment. -->
Sources: [README limits](../../../sources/models/capital-planning-model.md#L56-L60), [Assumptions](../../../sources/models/capital-planning-model.md#L116-L141), [Summary B13-B14](../../../sources/models/capital-planning-model.md#L103-L104).

## Operating and changing the component

- **Governance.** MDL-CAP-003 is a Tier 1 (High) model, owned by Corporate Treasury - Capital Management and validated independently by Model Risk Governance & Review. The last validation was 2026-02-27 and the next is due 2027-02-28. Changes to baseline logic or inputs fall inside that governance.
- **Refresh.** Each cycle, update the starting CET1, RWA and share count to the latest quarter's actuals from API-16, and the dividend and buyback plan to the Board-approved figures. Treasury liquidity positions from API-15 are cross-checked against distributions outside the sheet.
- **Extension points.** The levers are the blue input cells on `Assumptions`. The main ones are net income growth, RWA growth, buyback amount, share price and other CET1 movements. Per-quarter paths would require replacing the absolute references with per-column inputs, as the stress sheet already does for RWA growth.
- **Checks after a change.** Verify that the Q2 2026 column still ties to `Assumptions`. Verify that the starting ratio matches the reported CET1 ratio. Verify that `Summary` rows 6 to 8, 16 and 17 still point to the baseline cells.

<!-- openwiki: broken internal link [../../../sources/models/capital-planning-model.md#L9-L60] heading anchor "L9-L60" does not exist in "../../../sources/models/capital-planning-model.md". Fix the href or restore the target, then delete this comment. -->
Sources: [README metadata and key inputs](../../../sources/models/capital-planning-model.md#L9-L60).
