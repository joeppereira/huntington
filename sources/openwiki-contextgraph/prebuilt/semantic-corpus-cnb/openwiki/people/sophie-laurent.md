---
type: Person
entity_id: sophie-laurent
title: Sophie Laurent
description: Validation Lead for Treasury & Operations models within Model Risk Management (MRM) at Crestline National Bank; named contact for Tier 2 model validation submissions and the Tier 2 validation queue.
tags: [people, model-risk-management, mrm, validation, tier-2, treasury, payment-operations, second-line, mrm-pol-02, partner-function]
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

Sophie Laurent is the **Validation Lead, Treasury & Operations models**
within Model Risk Management (MRM) at Crestline National Bank (CNB). She is
named in two independent governance records — the Payments & Treasury
Technology (PTT) Organization, System Ownership & Engagement Directory
(CNB-ORG-PTT-2026-06) and the Model Risk Management Policy
(MRM-POL-02 v7.0) — as the point of contact that Treasury and Payment
Operations product/engineering teams engage for model and End-User Analytic
(EUA) reviews and for Tier 2 independent validation submissions. She sits
within Jonathan Price's second-line MRM function rather than inside any PTT
engineering team, and is not herself the accountable policy owner of
MRM-POL-02 or the model inventory — that accountability rests with Price.

## Role and scope

- **Title**: Validation Lead, Treasury & Operations models, within Model Risk Management.
- **Named contact for product/design reviews**: the PTT directory's partner-functions table lists Model Risk Management as accountable to Jonathan Price, with Laurent named as the specific "Contact for product / design reviews" — the role other partner functions (FCC, Payment Operations, Privacy Office, etc.) fill with their own named reviewers.
- **Scope limited to Treasury & Operations**: her title and listing scope her validation-lead role to Treasury and Payment Operations models and EUAs, as distinct from Financial Crimes Technology's Tier 1 models (Sentinel fraud score `M-FCT-0021`, beneficiary mule-risk features `M-FCT-0034`), which are owned by Victor Petrov and are not in her named portfolio.
- **Tier 2 validation queue contact**: MRM-POL-02's capacity notice (Section 6) names her directly as the contact for Tier 2 validation submissions, tying the policy document's operational guidance to the same individual named in the PTT directory.

## What she validates

Under MRM-POL-02 v7.0, Model Risk Management tiers models by purpose and
exposure, with validation effort scaling accordingly:

| Tier | Criteria | Validation before use |
|---|---|---|
| Tier 1 | Regulatory, capital, financial-crimes detection, or high financial exposure | Full independent validation; annual review |
| Tier 2 | Customer-facing estimates; models influencing client decisions or treatment | Independent validation; 10-14 weeks typical; 160-240 validator hours |
| Tier 3 | Internal operational models with limited exposure | Targeted validation; 6-9 weeks |
| EUA | Descriptive only (counts, medians, percentages over historical data; no forward-looking estimation) | Registration + attestation (~2 weeks); no independent validation |

Customer-facing estimates are Tier 2 at minimum and may not be shown to
clients before validation completes and use conditions (disclaimers,
monitoring thresholds) are approved. Within the Treasury & Payments
inventory extract in MRM-POL-02, the models and EUA most relevant to
Laurent's named scope are:

| Model ID | Name | Tier | Owner | Status |
|---|---|---|---|---|
| `M-TRS-0142` | Treasury Insights cash forecast | 3 (re-tiering to 2 under v7.0 review) | Wei Zhang | Validated 2025-09 (9 weeks) |
| `EUA-TRS-0007` | Ops corridor completion dashboard | EUA | Denise Carter | Registered 2026-05 |

`M-TRS-0142` is a Treasury model under active re-tiering from Tier 3 to
Tier 2 under the revised v7.0 criteria — which, if it lands on Tier 2 as a
customer-facing estimate, would move it into the fuller independent
validation band (10-14 weeks, 160-240 validator hours) that Laurent's queue
handles. `EUA-TRS-0007` is a Payment Operations EUA that receives
registration and business-owner attestation rather than independent
validation, placing it outside the Tier 1-3 validation workload itself but
still within the Treasury & Operations model/EUA population her function
tracks.

## Engagement and capacity

- **Intake route**: new models and EUAs register in Archer before
  development begins, not merely before go-live. Tier 2 validation runs
  10-14 weeks plus queue time once registered.
- **Capacity notice (Q4-2026)**: the Tier 2 validation queue was
  approximately **6 weeks** before work starts, as of MRM-POL-02's current
  capacity notice. Submissions to Laurent's queue should include
  development documentation, data lineage, and proposed monitoring.
- **Planning factor**: the PTT directory's engagement-routes table
  estimates EUA registration at roughly 16 hours of MRM effort and Tier 2
  validation at 160-240 validator hours — the effort figures product and
  engineering teams should use when sizing work that will pass through
  Laurent's queue.
- **Escalation boundary**: model-risk classification and policy
  interpretation are second-line decisions made within MRM, not by the
  engineering or product teams submitting models — consistent with the PTT
  directory's broader rule that compliance/policy questions are not decided
  unilaterally by engineering.

## Relationships

- **Jonathan Price** — Head of Model Risk Management; second-line
  accountable owner of MRM-POL-02 and the model inventory. Laurent is his
  named delegate for Treasury/Operations-adjacent product and design
  reviews and Tier 2 validation intake, rather than an independent policy
  owner.
- **Wei Zhang** — Director, Treasury Data & Analytics; owner of
  `M-TRS-0142`, the Treasury Insights cash-forecast model under re-tiering
  review, which falls within Laurent's Treasury model scope.
- **Denise Carter** — accountable leader, Payment Operations; business
  owner of `EUA-TRS-0007`, the registered ops corridor completion
  dashboard, which falls within Laurent's Treasury & Operations scope as an
  EUA rather than a validated model.
- **Victor Petrov** — Director, Financial Crimes Technology; owner of the
  Tier 1 Sentinel fraud score and beneficiary mule-risk features, which sit
  outside Laurent's named Treasury & Operations portfolio.
- **Laura Kim** — Director, Payments Platform Product; business data owner
  for payment datasets feeding client-facing analytical outputs (e.g. via
  TDIP) that may require MRM registration and tiering before any
  forward-looking or client-facing claim is shown to clients.

## Related pages

- [Model Risk Management](../teams/model-risk-management.md)
- [MRM-POL-02 (document record)](../documents/mrm-pol-02.md)
- [CNB-ORG-PTT-2026-06 (document record)](../documents/cnb-org-ptt-2026-06.md)
- [Payments & Treasury Technology](../organizations/payments-treasury-technology.md)
