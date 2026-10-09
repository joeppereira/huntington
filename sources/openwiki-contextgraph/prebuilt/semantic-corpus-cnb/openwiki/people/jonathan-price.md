---
type: Person
entity_id: jonathan-price
title: Jonathan Price
description: Head of Model Risk Management at Crestline National Bank; second-line accountable owner of MRM-POL-02 and the enterprise model inventory governing model definition, tiering, validation and use limitations for Payments & Treasury Technology.
tags: [people, model-risk-management, mrm, second-line, policy-owner, mrm-pol-02, model-inventory, ptt, partner-function, governance]
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

Jonathan Price is Head of Model Risk Management (MRM) at Crestline National
Bank (CNB). In the Payments & Treasury Technology (PTT) organization's
leadership roster and partner-function directory he is named as the
second-line accountable owner of **MRM-POL-02**, the Model Risk Management
Policy, and of the **model inventory** that registers and tracks every model
and End-User Analytic (EUA) in use across the bank. He is not a member of a
PTT engineering team; he and his delegates are an accountable second-line
governance partner that engineering and product teams must register models
with, and secure validation and tiering sign-off from, before a model's
output may be relied upon or shown to clients.

## Role and scope

- **Title**: Head of Model Risk Management.
- **Second-line ownership**: Named in PTT's leadership roster as "2nd line owner of MRM-POL-02 and model inventory."
- **Partner function accountable owner**: Named as the accountable leader for Model Risk Management (MRM) in the directory's partner-functions table, alongside Financial Crimes Compliance (Catherine Doyle), Payment Operations (Denise Carter), and other first-/second-line functions that PTT engineering teams engage rather than own.
- **Delegated contact**: For day-to-day product and design reviews and Treasury/Operations-adjacent model and EUA registrations, teams are directed to Sophie Laurent, Validation Lead for Treasury & Operations models, rather than to Price directly.
- **Document owner**: Named directly on MRM-POL-02 v7.0 as "Jonathan Price, Head of Model Risk Management," the accountable 2nd-line document owner, approved by the Board Risk Committee on 2026-06-18.

## Document ownership: MRM-POL-02

Price owns **MRM-POL-02** v7.0, the Model Risk Management Policy, re-baselined
to the revised interagency Guidance on Model Risk Management issued
2026-04-17 (Federal Reserve SR 26-2; OCC Bulletin 2026-13; FDIC FIL-15-2026),
which rescinded the prior SR 11-7 / OCC 2011-12 regime. As document owner,
his organization sets enterprise-wide rules that engineering and product
teams building quantitative, forward-looking or client-facing calculations
must follow, including:

- **Model definition**: a quantitative method must apply statistical, economic, financial, or machine-learning techniques of *meaningful complexity* to produce estimates or predictions used in decisions or communicated to clients — narrowing what counts as a model relative to the prior regime.
- **End-User Analytic (EUA) category**: simple descriptive calculations (counts, medians, percentages over historical data) with no forward-looking estimation are registered in Archer with business-owner attestation only, and receive no independent validation — a lighter-weight path introduced in v7.0.
- **Risk-based tiering**: four tiers — Tier 1 (regulatory, capital, financial-crimes detection, or high financial exposure; full independent validation with annual review), Tier 2 (customer-facing estimates or models influencing client decisions/treatment; independent validation, 10-14 weeks typical, 160-240 validator hours), Tier 3 (internal operational models with limited exposure; targeted validation, 6-9 weeks), and EUA (registration plus attestation, ~2 weeks). **Customer-facing estimates are Tier 2 at minimum** and may not be shown to clients before validation completes and use conditions (disclaimers, monitoring thresholds) are approved.
- **Use limitations**: models and their inputs may be used only for registered purposes. Outputs of Tier 1 financial-crimes models — including Sentinel payment fraud scores (`M-FCT-0021`) and beneficiary mule-risk features (`M-FCT-0034`), both owned by Victor Petrov — may not be used for product, marketing or client-facing purposes.
- **Vendor models**: where vendors cannot provide sufficient development information, compensating controls and outcome monitoring are required in lieu of full transparency into model internals.

See [MRM-POL-02](../policies/mrm-pol-02.md) for the full policy record and
[MRM-POL-02 (document record)](../documents/mrm-pol-02.md) for version
history and document metadata.

## Model inventory oversight

Price's second-line function owns the model inventory tracked in Archer,
which (per the policy's Treasury & Payments extract) includes at minimum:

| Model ID | Name | Tier | Owner | Status |
|---|---|---|---|---|
| `M-FCT-0021` | Sentinel payment fraud score (vendor) | 1 | Victor Petrov | Validated 2025-12 |
| `M-FCT-0034` | Beneficiary mule-risk features | 1 | Victor Petrov | Validated 2026-02 |
| `M-TRS-0142` | Treasury Insights cash forecast | 3 (re-tiering to 2 under v7.0 review) | Wei Zhang | Validated 2025-09 (9 weeks) |
| `EUA-TRS-0007` | Ops corridor completion dashboard | EUA | Denise Carter | Registered 2026-05 |

Registration in this inventory is required **before development** begins on
a new model or EUA, not merely before go-live — reflecting MRM's role as a
gate on project planning as well as on release.

## Engagement routes into Price's organization

PTT engineering teams reach Price's function through defined governance
forums and planning factors rather than direct escalation:

- **MRM Model Inventory & Validation** (continuous intake via Archer; register before development): Tier 2 validation runs 10-14 weeks plus queue time.
- **Capacity notice (Q4-2026)**: the Tier 2 validation queue runs approximately **6 weeks** before work starts; submissions should include development documentation, data lineage and proposed monitoring. Contact: Sophie Laurent.
- **Planning factors** (PTT directory, calibrated from the last four program increments): EUA registration ≈ 16 engineering hours; Tier 2 validation ≈ 160-240 validator hours.
- **Escalation**: model-risk classification and policy-interpretation questions are second-line decisions routed through MRM, not decided unilaterally by engineering teams.

## Relationships

- **Peer second-line/partner-function leaders**: Catherine Doyle (EVP, Chief BSA/AML Officer; owner of POL-FCC-014), Rachel Goldberg (Chief Privacy Officer; owner of DUS-07), Denise Carter (Payment Operations), Andrew Feldman (Legal - Treasury & Payments), Farah Ali (Information Security - Digital Channels), Kim Nguyen (Commercial Service Center), and Mark Sullivan (Deposits Data Ownership).
- **Delegated contact**: Sophie Laurent, Validation Lead, Treasury & Operations models — the named MRM contact for product/design reviews and for Treasury/Operations-adjacent model and EUA registrations.
- **Model owners under his governance**: Victor Petrov (Director, Financial Crimes Technology; owner of the Tier 1 Sentinel fraud score and beneficiary mule-risk features), Wei Zhang (Director, Treasury Data & Analytics; owner of the Treasury Insights cash-forecast model), and Denise Carter (Head of Payment Operations; owner of the registered `EUA-TRS-0007` ops corridor completion dashboard).
- **Business-sponsor governance partner**: Danielle Okafor (EVP, Head of Treasury Management Products) must clear MRM registration and sign-off from Price's organization before shipping any client-facing predictive or estimated completion-time statement, alongside separate sign-off from Catherine Doyle's function under POL-FCC-014.
- **Validation Lead and queue**: Sophie Laurent is also the named point of contact in MRM-POL-02's own capacity notice, tying the policy document and the partner-function directory to the same individual.

## Related pages

- [MRM-POL-02](../policies/mrm-pol-02.md)
- [MRM-POL-02 (document record)](../documents/mrm-pol-02.md)
- [Model Risk Management](../teams/model-risk-management.md)
- [CNB-ORG-PTT-2026-06 (document record)](../documents/cnb-org-ptt-2026-06.md)
- [Payments & Treasury Technology](../organizations/payments-treasury-technology.md)
