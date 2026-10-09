---
type: Policy
entity_id: MRM-POL-02
title: "MRM-POL-02: Model Risk Management Policy"
description: "Model Risk Management policy (v7.0, effective 2026-07-01) defining the Model/End-User Analytic (EUA) boundary, the Tier 1/2/3/EUA risk tiering and validation lead times, and the rule that customer-facing estimates are Tier 2 minimum while financial-crimes model outputs may never be used for product or marketing purposes."
tags: [policy, mrm-pol-02, model-risk-management, mrm, tiering, eua, validation, customer-facing-estimate, financial-crimes, governance]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-661f09048ce207829077c40d
    resource: repo://sources/estate/mrm-pol-02-v7.0-model-risk-management-policy-extract.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

MRM-POL-02 ("Model Risk Management Policy") is Crestline National Bank's
governing policy for what counts as a **model**, how models are classified
into risk **tiers**, what **validation** each tier requires before use, and
what **use limitations** apply to model outputs - most importantly, a flat
prohibition on using financial-crimes model outputs for product or
marketing purposes. It is document ID **MRM-POL-02**, version **7.0 /
Approved - Board Risk Committee**, owned by Jonathan Price (Head of Model
Risk Management), approved by the Board Risk Committee on 2026-06-18, and
effective **2026-07-01**. It is classified **INTERNAL - CONFIDENTIAL** and
lists **POL-FCC-014**, **DUS-07**, **ADR-PAY-026**, and
**TDIP-CAT-2026.2** as related documents.

Version 7.0 re-baselines the policy to the revised interagency Guidance on
Model Risk Management issued 2026-04-17 (Federal Reserve SR 26-2; OCC
Bulletin 2026-13; FDIC FIL-15-2026), which rescinded the prior SR 11-7 / OCC
2011-12 guidance. The re-baseline introduced four changes material to
Payments & Treasury Technology (PTT) work: (1) a model definition that
requires meaningful complexity, not just arithmetic; (2) a formal
**End-User Analytic (EUA)** category for simple descriptive calculations
that fall outside full model governance; (3) risk-based tiering that
emphasizes model *purpose and exposure* rather than technique; and (4) a
dedicated section on vendor models.

MRM-POL-02 is the policy that gates every predictive or customer-facing
estimate feature anywhere in the payments estate - it governs when a new
insight (such as those served through the [TDIP Insights API](../interfaces/tdip-insights-api.md),
per [ADR-PAY-026](../decisions/adr-pay-026.md)) may be classified, how long
that classification takes, and which existing model outputs (Sentinel fraud
scores, beneficiary mule-risk features) can never be repurposed for a
client-facing or product surface no matter how useful they might appear.

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: a semicolon inside a label breaks rendering; rephrase the label. -->
```text
flowchart TD
    DEF["Is it a quantitative method of\nmeaningful complexity producing an\nestimate/prediction used in decisions\nor communicated to clients?"]
    DEF -- "no - simple descriptive calc\n(counts, medians, percentages),\nno forward-looking estimation" --> EUA["EUA\nRegister in Archer +\nbusiness-owner attestation\n(no independent validation, ~2 weeks)"]
    DEF -- "yes" --> CFE{"Is it a customer-facing\nestimate (forward-looking value\nshown to a client)?"}
    CFE -- "yes" --> T2MIN["Tier 2 minimum\n(independent validation,\n10-14 weeks, 160-240 validator hours)"]
    CFE -- "no" --> CRIT{"Regulatory, capital,\nfinancial-crimes detection,\nor high financial exposure?"}
    CRIT -- "yes" --> T1["Tier 1\nFull independent validation;\nannual review"]
    CRIT -- "no, internal operational,\nlimited exposure" --> T3["Tier 3\nTargeted validation; 6-9 weeks"]
    T1 -- "financial-crimes outputs" --> BAN["Use limitation:\nmay NOT be used for product,\nmarketing, or client-facing purposes"]
```
*Classification path from the Model/EUA definition through tiering to the
financial-crimes use prohibition.*

## 1. Changes in version 7.0

Per the policy's own change log, v7.0 re-baselines against the April 17,
2026 interagency guidance that replaced SR 11-7. The key changes are: a
model definition that requires complexity; a formal EUA category for simple
calculations; risk-based tiering emphasizing model purpose and exposure;
and a dedicated section on vendor models.

## 2. Definitions

| Term | Definition |
|---|---|
| Model | A quantitative method applying statistical, economic, financial or machine-learning techniques of meaningful complexity to produce estimates or predictions used in decisions or communicated to clients. |
| End-User Analytic (EUA) | Simple descriptive calculations (counts, medians, percentages over historical data) with no forward-looking estimation. Registered in Archer with business-owner attestation; no independent validation. |
| Customer-facing estimate | Any forward-looking value shown to a client (e.g., expected delivery time, probability of completion). |

The Model/EUA boundary is the policy's central classification question: a
calculation with no forward-looking estimation (e.g. a historical median or
count) can be registered as an EUA with only business-owner attestation,
while anything that produces an estimate or prediction of meaningful
complexity must be classified as a Model and tiered under Section 3 below.

## 3. Tiering

| Tier | Criteria | Validation before use |
|---|---|---|
| Tier 1 | Regulatory, capital, financial-crimes detection, or high financial exposure | Full independent validation; annual review |
| Tier 2 | Customer-facing estimates; models influencing client decisions or treatment | Independent validation; 10-14 weeks typical; 160-240 validator hours |
| Tier 3 | Internal operational models with limited exposure | Targeted validation; 6-9 weeks |
| EUA | Descriptive only | Registration + attestation (~2 weeks) |

**Customer-facing estimates are Tier 2 at minimum**, and they may not be
shown to clients before independent validation is complete and use
conditions (disclaimers, monitoring thresholds) are approved. This is a
floor, not a default: a customer-facing estimate that also carries
regulatory, capital, or financial-crimes-detection exposure would still be
Tier 1, and the inventory below shows a Tier 3 customer-facing model
(M-TRS-0142) being re-tiered upward to Tier 2 to comply with this floor.

## 4. Use limitations

- Models and their inputs may be used only for registered purposes.
  **Outputs of financial-crimes models (Tier 1) - including Sentinel fraud
  scores (M-FCT-0021) and beneficiary mule-risk features (M-FCT-0034) - may
  not be used for product, marketing or client-facing purposes.** This
  prohibition is absolute: it is not conditioned on consent, anonymization,
  or aggregation, and it applies to the models' inputs and features as well
  as their raw outputs.
- **Vendor models**: where developers cannot provide sufficient information
  (e.g. a vendor withholding model internals), compensating controls and
  outcome monitoring are required in lieu of full transparency. M-FCT-0021
  (Sentinel payment fraud score) is itself a vendor model and falls under
  this provision.

## 5. Inventory extract (Treasury & Payments)

| Model ID | Name | Tier | Owner | Status |
|---|---|---|---|---|
| M-FCT-0021 | Sentinel payment fraud score (vendor) | 1 | Victor Petrov | Validated 2025-12 |
| M-FCT-0034 | Beneficiary mule-risk features | 1 | Victor Petrov | Validated 2026-02 |
| M-TRS-0142 | Treasury Insights cash forecast | 3 (re-tiering to 2 under v7.0 review) | Wei Zhang | Validated 2025-09 (9 weeks) |
| EUA-TRS-0007 | Ops corridor completion dashboard | EUA | Denise Carter | Registered 2026-05 |

Two financial-crimes models, **M-FCT-0021** and **M-FCT-0034**, are owned by
Victor Petrov (Director, Financial Crimes Technology) and are the models
named in the Section 4 use prohibition - their outputs may never reach a
product, marketing, or client-facing surface. **M-TRS-0142** is the backing
model for the TDIP Insights API's one GA endpoint, EP-TDIP-01
(`GET /tdip/insights/v1/cash-forecast/{clientId}`); it was validated in
2025-09 as a Tier 3 model under the pre-v7.0 tiering, but because it
produces a customer-facing estimate, the v7.0 re-baseline requires it to be
re-tiered to Tier 2 at minimum - the inventory extract records this
re-tiering as in flight at the review cadence in effect when the extract
was produced. **EUA-TRS-0007** illustrates the EUA path: a descriptive-only
ops dashboard registered with business-owner attestation and no independent
validation.

See [Beneficiary Behavior Profile](../datasets/beneficiary-behavior-profile.md)
for the Restricted-classified feature table that is the sole registered
input to M-FCT-0034, and whose own permitted use is scoped to FCT
fraud/mule detection as a direct consequence of feeding a Tier 1
financial-crimes model under this policy.

## 6. Capacity notice (Q4-2026)

The Tier 2 validation queue is approximately **6 weeks** before work starts,
on top of the 10-14 week typical validation duration itself - so a new
customer-facing estimate should budget on the order of four months from
submission to cleared validation. Submissions should include development
documentation, data lineage, and proposed monitoring. Contact: **Sophie
Laurent** (Validation Lead, Treasury & Operations models).

This capacity constraint is a direct, named driver of lead time for any
team building a new customer-facing analytic: [ADR-PAY-026](../decisions/adr-pay-026.md)
and the [TDIP Insights API](../interfaces/tdip-insights-api.md) both cite
the combination of the ~6-week intake queue and the 10-14 week Tier 2
validation window as the dominant source of delay when onboarding a new
insight, ahead of the data-access and Disclosure Review Committee steps
that also gate production release.

## Relationships

- **governs**: any predictive or customer-facing-estimate feature in the
  payments estate, including every insight served through the
  [TDIP Insights API](../interfaces/tdip-insights-api.md).
- **is required by**: [ADR-PAY-026](../decisions/adr-pay-026.md), which
  mandates that every client-facing analytic be classified under MRM-POL-02
  (as Model or EUA) before it may reach production or be shown to a client.
- **constrains the permitted use of**: [`beneficiary_behavior_profile`](../datasets/beneficiary-behavior-profile.md),
  the Restricted feature table that is the sole input to Tier 1 model
  M-FCT-0034 and therefore inherits its product/marketing/client-facing
  prohibition.
- **model ownership**: Victor Petrov owns M-FCT-0021 and M-FCT-0034 in the
  inventory above; Wei Zhang owns M-TRS-0142; Denise Carter owns
  EUA-TRS-0007.
- **related documents**: POL-FCC-014; DUS-07; ADR-PAY-026; TDIP-CAT-2026.2.
