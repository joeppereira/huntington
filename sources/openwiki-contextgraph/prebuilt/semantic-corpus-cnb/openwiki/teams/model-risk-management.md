---
type: Team
entity_id: model-risk-management
title: Model Risk Management (MRM)
description: Second-line partner function (accountable leader Jonathan Price) that owns MRM-POL-02 and the enterprise model inventory, gating every quantitative, forward-looking or client-facing calculation in Payments & Treasury Technology behind registration, risk-based tiering and independent validation.
tags: [model-risk-management, mrm, second-line, partner-function, jonathan-price, sophie-laurent, mrm-pol-02, model-inventory, tiering, validation, ptt, governance]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-49303e801f124d97df9c3ea3
    resource: repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md
  - id: openwiki-source-661f09048ce207829077c40d
    resource: repo://sources/estate/mrm-pol-02-v7.0-model-risk-management-policy-extract.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

**Model Risk Management (MRM)** is a second-line partner function in
Crestline National Bank's (CNB) Payments & Treasury Technology (PTT)
organization. Like Financial Crimes Compliance, it is listed in the PTT
directory's "Partner functions (first and second line)" table rather than in
the engineering team directory or the system ownership register: MRM owns
no PTT system of record and employs no PTT engineering staff. Instead, it is
the accountable second-line governance function that any PTT engineering or
product team must engage whenever it builds, changes, or reuses a
quantitative, forward-looking, or client-facing calculation — for model
registration, risk tiering, and independent validation sign-off before that
calculation's output may be relied upon internally or shown to a client.

| Field | Value |
|---|---|
| Function | Model Risk Management (MRM) |
| Accountable | Jonathan Price, Head of Model Risk Management |
| Line | Second line of defense |
| Policy owned | MRM-POL-02 v7.0, "Model Risk Management Policy" |
| Named contact for product/design reviews | Sophie Laurent, Validation Lead, Treasury & Operations models |
| Inventory system of record | Archer (continuous intake) |
| Appears in engineering team directory (Sec. 3)? | No |
| Appears in system ownership register (Sec. 4)? | No |

## Accountable leadership and named contacts

Jonathan Price, Head of Model Risk Management, is named in both the PTT
leadership roster and the partner-functions table as the "2nd line owner of
MRM-POL-02 and model inventory." He is also the named document owner of
MRM-POL-02 v7.0, approved by the Board Risk Committee on 2026-06-18. Routine
product and design review work, and Tier 2 validation intake for Treasury
and Payment Operations models, is delegated to **Sophie Laurent, Validation
Lead, Treasury & Operations models**, the named "Contact for product /
design reviews" in the partner-functions table and the named contact in
MRM-POL-02's own capacity notice. PTT engineering and product teams are
directed to engage Laurent for day-to-day registrations and reviews rather
than escalating to Price directly.
([Leadership](repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L28-L39);
[Partner functions](repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L65-L77))

See [Jonathan Price](../people/jonathan-price.md) and
[Sophie Laurent](../people/sophie-laurent.md) for individual role detail, and
[MRM-POL-02](../policies/mrm-pol-02.md) for the full policy record.

## Why MRM exists: the control it owns

MRM's reason for existence in the payments stack is a single enterprise
policy, **MRM-POL-02, "Model Risk Management Policy"** (v7.0, approved by
the Board Risk Committee 2026-06-18, effective 2026-07-01), re-baselined to
the revised interagency Guidance on Model Risk Management issued 2026-04-17
(Federal Reserve SR 26-2; OCC Bulletin 2026-13; FDIC FIL-15-2026), which
rescinded the prior SR 11-7 / OCC 2011-12 regime. Version 7.0 introduced four
changes material to PTT engineering work: a model definition that requires
*meaningful complexity* rather than mere arithmetic; a formal **End-User
Analytic (EUA)** category for simple descriptive calculations that fall
outside full model governance; risk-based tiering that emphasizes model
*purpose and exposure* over technique; and a dedicated section on vendor
models.
([Changes in v7.0](repo://sources/estate/mrm-pol-02-v7.0-model-risk-management-policy-extract.md#L25-L27))

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: a semicolon inside a label breaks rendering; rephrase the label. -->
```text
flowchart TD
    DEF["Quantitative method of meaningful\ncomplexity producing an estimate or\nprediction, used in decisions or\ncommunicated to clients?"]
    DEF -- "no - simple descriptive calc\n(counts, medians, percentages),\nno forward-looking estimation" --> EUA["EUA\nRegister in Archer +\nbusiness-owner attestation\n(no independent validation, ~2 weeks)"]
    DEF -- "yes" --> CFE{"Customer-facing estimate\n(forward-looking value shown\nto a client)?"}
    CFE -- "yes" --> T2["Tier 2 minimum\nIndependent validation,\n10-14 weeks, 160-240 validator hours"]
    CFE -- "no" --> CRIT{"Regulatory, capital,\nfinancial-crimes detection,\nor high financial exposure?"}
    CRIT -- "yes" --> T1["Tier 1\nFull independent validation;\nannual review"]
    CRIT -- "no, internal operational,\nlimited exposure" --> T3["Tier 3\nTargeted validation; 6-9 weeks"]
    T1 -- "financial-crimes model outputs" --> BAN["Use limitation:\nmay NOT be used for product,\nmarketing or client-facing purposes"]
    EUA --> ARCHER[("Model inventory\n(Archer)")]
    T2 --> ARCHER
    T1 --> ARCHER
    T3 --> ARCHER
```
*Classification path MRM applies to every candidate model or EUA, from the
Model/EUA definition through risk tiering to the financial-crimes use
prohibition; every path registers in the Archer model inventory.*

## Model definition, tiering and validation lead times

MRM-POL-02 defines a **Model** as a quantitative method applying
statistical, economic, financial, or machine-learning techniques of
meaningful complexity to produce estimates or predictions used in decisions
or communicated to clients, and an **End-User Analytic (EUA)** as a simple
descriptive calculation (counts, medians, percentages over historical data)
with no forward-looking estimation, registered in Archer with
business-owner attestation only and no independent validation. A
**customer-facing estimate** is any forward-looking value shown to a client
(e.g., expected delivery time, probability of completion), and is **Tier 2
at minimum** — it may not be shown to a client before independent validation
completes and use conditions (disclaimers, monitoring thresholds) are
approved.
([Definitions](repo://sources/estate/mrm-pol-02-v7.0-model-risk-management-policy-extract.md#L29-L35))

| Tier | Criteria | Validation before use |
|---|---|---|
| Tier 1 | Regulatory, capital, financial-crimes detection, or high financial exposure | Full independent validation; annual review |
| Tier 2 | Customer-facing estimates; models influencing client decisions or treatment | Independent validation; 10-14 weeks typical; 160-240 validator hours |
| Tier 3 | Internal operational models with limited exposure | Targeted validation; 6-9 weeks |
| EUA | Descriptive only | Registration + attestation (~2 weeks) |

([Tiering](repo://sources/estate/mrm-pol-02-v7.0-model-risk-management-policy-extract.md#L36-L43))

Use limitations apply on top of tiering: models and their inputs may be used
only for their registered purposes, and outputs of Tier 1 financial-crimes
models — including the Sentinel payment fraud score (`M-FCT-0021`) and
beneficiary mule-risk features (`M-FCT-0034`), both owned by Victor Petrov
in Financial Crimes Technology — may never be used for product, marketing,
or client-facing purposes, regardless of how useful they might appear for
such a purpose. Where a vendor cannot provide sufficient development
information for a model it supplies, MRM requires compensating controls and
outcome monitoring in lieu of full transparency into model internals.
([Use limitations](repo://sources/estate/mrm-pol-02-v7.0-model-risk-management-policy-extract.md#L44-L49))

## Model inventory (Treasury & Payments extract)

MRM owns and maintains the enterprise model inventory in Archer. The
Treasury & Payments extract published alongside MRM-POL-02 v7.0 lists, at
minimum:

| Model ID | Name | Tier | Owner | Status |
|---|---|---|---|---|
| `M-FCT-0021` | Sentinel payment fraud score (vendor) | 1 | Victor Petrov | Validated 2025-12 |
| `M-FCT-0034` | Beneficiary mule-risk features | 1 | Victor Petrov | Validated 2026-02 |
| `M-TRS-0142` | Treasury Insights cash forecast | 3 (re-tiering to 2 under v7.0 review) | Wei Zhang | Validated 2025-09 (9 weeks) |
| `EUA-TRS-0007` | Ops corridor completion dashboard | EUA | Denise Carter | Registered 2026-05 |

([Inventory extract](repo://sources/estate/mrm-pol-02-v7.0-model-risk-management-policy-extract.md#L50-L67))

`M-TRS-0142` illustrates the Tier 2 customer-facing floor in practice: it
was validated in 2025-09 as a Tier 3 model but is under active re-tiering to
Tier 2 under v7.0's revised criteria, which would move it into the fuller
160-240 validator-hour independent-validation band if it is confirmed as a
customer-facing estimate. `EUA-TRS-0007` sits outside the Tier 1-3
validation workload entirely, having received registration and
business-owner attestation only. Registration in the inventory is required
**before development begins** on a new model or EUA, not merely before
go-live, which makes MRM a gate on project planning as well as on release.
([MRM Model Inventory & Validation forum](repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L98-L118))

## Engagement routes, lead times and capacity

PTT engineering teams reach MRM through defined governance forums and
planning factors rather than direct escalation to Price:

- **MRM Model Inventory & Validation** — continuous intake via Archer;
  register before development begins; Tier 2 validation runs 10-14 weeks
  typical plus queue time.
- **Capacity notice (Q4-2026)** — the Tier 2 validation queue runs
  approximately **6 weeks** before work starts, on top of the 10-14 week
  typical validation effort. Submissions should include development
  documentation, data lineage, and proposed monitoring. Contact: Sophie
  Laurent.
- **Planning factors** (PTT directory, calibrated from the last four program
  increments) — EUA registration ≈ 16 engineering hours of MRM effort; Tier
  2 validation ≈ 160-240 validator hours.
- **Escalation boundary** — model-risk classification and
  policy-interpretation questions are second-line decisions made within
  MRM, not decided unilaterally by engineering or product teams submitting
  models, consistent with the PTT directory's broader rule that compliance
  or policy questions route to the accountable second-line function rather
  than being resolved by engineering.

([Governance forums](repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L98-L119);
[Engagement routes and planning factors](repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L120-L138);
[Capacity notice](repo://sources/estate/mrm-pol-02-v7.0-model-risk-management-policy-extract.md#L68-L71);
[Escalation](repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L148-L150))

For a product team sizing a new customer-facing predictive feature (e.g. an
expected-delivery-time estimate), the practical planning implication is that
MRM registration must happen before development starts, the Tier 2 floor
applies as soon as the feature is customer-facing, and the combined queue
plus validation lead time (roughly 6 weeks queue + 10-14 weeks validation)
should be built into the program-increment plan well ahead of the target
release, alongside any separate sign-offs required from other second-line
partner functions such as Financial Crimes Compliance or the Disclosure
Review Committee for the same feature.

## Relationships

- **Jonathan Price** — Head of Model Risk Management; accountable second-line
  owner of MRM-POL-02 and the model inventory; document owner of record
  approved by the Board Risk Committee. See [Jonathan Price](../people/jonathan-price.md).
- **Sophie Laurent** — Validation Lead, Treasury & Operations models; named
  contact for product/design reviews and for Tier 2 validation submissions
  in Laurent's scope. See [Sophie Laurent](../people/sophie-laurent.md).
- **Peer second-line/partner-function leaders** — Catherine Doyle (Financial
  Crimes Compliance, owner of POL-FCC-014), Rachel Goldberg (Privacy Office,
  owner of DUS-07), Denise Carter (Payment Operations, business owner of
  `EUA-TRS-0007`), Andrew Feldman (Legal - Treasury & Payments), Farah Ali
  (Information Security - Digital Channels), Kim Nguyen (Commercial Service
  Center), and Mark Sullivan (Deposits Data Ownership).
- **Model owners under MRM governance** — Victor Petrov (Director, Financial
  Crimes Technology; owner of the Tier 1 Sentinel fraud score and
  beneficiary mule-risk features), Wei Zhang (Director, Treasury Data &
  Analytics; owner of the Treasury Insights cash-forecast model under
  re-tiering review), and Denise Carter (owner of the registered
  `EUA-TRS-0007`).
- **Business-sponsor governance partner** — Danielle Okafor (EVP, Head of
  Treasury Management Products) must clear MRM registration and validation
  sign-off before shipping any client-facing predictive or estimated
  completion-time statement, alongside separate sign-off from Catherine
  Doyle's Financial Crimes Compliance function under POL-FCC-014.

## Related pages

- [Jonathan Price](../people/jonathan-price.md)
- [Sophie Laurent](../people/sophie-laurent.md)
- [MRM-POL-02](../policies/mrm-pol-02.md)
- [MRM-POL-02 (document record)](../documents/mrm-pol-02.md)
- [CNB-ORG-PTT-2026-06 (document record)](../documents/cnb-org-ptt-2026-06.md)
- [Payments & Treasury Technology](../organizations/payments-treasury-technology.md)
- [Financial Crimes Compliance](financial-crimes-compliance.md)
