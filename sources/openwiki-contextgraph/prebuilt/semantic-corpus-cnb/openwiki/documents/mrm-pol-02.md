---
type: Document
entity_id: MRM-POL-02
title: "MRM-POL-02: Model Risk Management Policy (Extract, v7.0)"
description: Metadata record for Crestline National Bank's Model Risk Management Policy extract, re-baselined to the April 2026 interagency guidance, covering model definition, tiering, validation and use limitations.
tags: [mrm-pol-02, model-risk-management, model-tiering, model-validation, end-user-analytic, interagency-guidance, governance, document]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-49303e801f124d97df9c3ea3
    resource: repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md
  - id: openwiki-source-6fa6253c97994be177c92ec3
    resource: repo://sources/estate/dus-07-v2.1-data-use-and-client-confidentiality-standard.md
  - id: openwiki-source-661f09048ce207829077c40d
    resource: repo://sources/estate/mrm-pol-02-v7.0-model-risk-management-policy-extract.md
  - id: openwiki-source-1601c697250670250350a70c
    resource: repo://sources/estate/pol-fcc-014-v3.2-customer-communication-of-payment-status-holds-and-exceptions-standard.md
  - id: openwiki-source-08ac07f04b390aa09d5edc51
    resource: repo://sources/estate/prsp-hms-3.4-hold-management-service-design-and-reason-taxonomy-restricted.md
  - id: openwiki-source-a8ab82acd285acae1ac9546d
    resource: repo://sources/estate/tdip-cat-2026.2-treasury-data-and-insights-platform-data-catalog-extract.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Summary

**MRM-POL-02** ("Model Risk Management Policy") is the second-line policy at Crestline National
Bank (CNB) owned by Model Risk Management (MRM) that defines what counts as a "model," assigns
models to risk tiers, and sets validation requirements and use limitations before a model's
output may be relied upon or shown to clients. The corpus holds only an **extract** of the full
policy (version 7.0), covering the updated model definition, tiering criteria, use limitations,
a sample of the Treasury & Payments model inventory, and current validation-queue capacity. For
the normative tiering rules and use limitations themselves, see the companion page
[MRM-POL-02 (Policy)](../policies/mrm-pol-02.md); this page records the document's identity,
version history, ownership, and governance metadata.

## Document metadata

| Field | Value |
|---|---|
| Document ID | MRM-POL-02 |
| Version / Status | 7.0 / Approved — Board Risk Committee |
| Document owner | Jonathan Price, Head of Model Risk Management |
| Approver(s) | Board Risk Committee (approved 2026-06-18) |
| Effective / Last reviewed | Effective 2026-07-01 |
| Classification | INTERNAL - CONFIDENTIAL |
| Regulatory alignment | Revised interagency Guidance on Model Risk Management issued 2026-04-17 (Federal Reserve SR 26-2; OCC Bulletin 2026-13; FDIC FIL-15-2026), which rescinded SR 11-7 / OCC 2011-12 |
| Related documents | POL-FCC-014; DUS-07; ADR-PAY-026; TDIP-CAT-2026.2 |

The document is marked "Uncontrolled when printed" on every page footer, meaning printed or
exported copies carry no guarantee of reflecting the current approved revision — MRM's system of
record (the model inventory in Archer) is authoritative for tiering and validation status.

## Changes in version 7.0

Version 7.0 re-baselines the policy following the April 17, 2026 interagency guidance that
rescinded the prior SR 11-7 / OCC 2011-12 regime. The extract calls out four key changes:

- A **model definition that requires complexity** — a quantitative method must apply
  statistical, economic, financial, or machine-learning techniques of meaningful complexity to
  produce estimates or predictions, narrowing what previously might have been treated as a model.
- A formal **End-User Analytic (EUA)** category for simple descriptive calculations (counts,
  medians, percentages over historical data) with no forward-looking estimation, which are
  registered with business-owner attestation but do not receive independent validation.
- **Risk-based tiering** that emphasizes model purpose and exposure rather than purely technical
  characteristics.
- A dedicated section on **vendor models**, requiring compensating controls and outcome
  monitoring where vendors cannot provide sufficient development information.

## Ownership and approval chain

- **Owner**: Jonathan Price, Head of Model Risk Management, is the accountable 2nd-line document
  owner for MRM-POL-02 and the model inventory. The PTT Organization & Ownership Directory
  (CNB-ORG-PTT-2026-06) independently confirms this role.
- **Validation lead**: Sophie Laurent is named as Validation Lead for Treasury & Operations
  models, both in the policy's own capacity notice and in the PTT directory's listing of Model
  Risk Management as a partner function.
- **Approver**: the **Board Risk Committee** approved version 7.0 on 2026-06-18, ahead of its
  2026-07-01 effective date — reflecting the elevated governance level (board-level, not
  management-committee) typical of a full regulatory-driven re-baseline.
- **Escalation**: per the PTT directory, Model Risk Management is a first/second-line partner
  function that engineering and product teams must engage for model registration and tiering
  decisions, rather than deciding model risk classification unilaterally.

## What this extract covers

The extract is organized into six numbered sections:

1. **Changes in version 7.0** — summary of the re-baseline against the April 2026 interagency
   guidance (see above).
2. **Definitions** — "Model" (requires meaningful statistical/economic/financial/ML complexity),
   "End-User Analytic (EUA)" (simple descriptive calculations, no forward-looking estimation,
   Archer registration with business-owner attestation, no independent validation), and
   "Customer-facing estimate" (any forward-looking value shown to a client, e.g. expected
   delivery time or probability of completion).
3. **Tiering** — four tiers (Tier 1, Tier 2, Tier 3, EUA) with criteria and validation
   requirements ranging from full independent validation with annual review (Tier 1) down to
   registration plus attestation only (EUA); customer-facing estimates are Tier 2 at minimum and
   may not be shown to clients before validation completes and use conditions (disclaimers,
   monitoring thresholds) are approved.
4. **Use limitations** — models and their inputs may be used only for their registered purposes;
   Tier 1 financial-crimes model outputs (including Sentinel fraud scores and beneficiary
   mule-risk features) may not be used for product, marketing, or client-facing purposes; vendor
   models require compensating controls and outcome monitoring where developers cannot provide
   sufficient information.
5. **Inventory extract (Treasury & Payments)** — a sample of four entries from the model
   inventory: two Tier 1 financial-crimes models (Sentinel payment fraud score, beneficiary
   mule-risk features), one Treasury Insights cash-forecast model under re-tiering, and one
   registered EUA (ops corridor completion dashboard).
6. **Capacity notice (Q4-2026)** — current Tier 2 validation queue depth and submission
   expectations (see Operational notes).

The detailed tiering table, use-limitation rules, and inventory extract are documented on the
[MRM-POL-02 policy page](../policies/mrm-pol-02.md) rather than restated here.

## Relationships

- **Governs**: client-facing predictive insights served through
  [TDIP](../documents/tdip-cat-2026.2.md) and the Insights API (ADR-PAY-026) — TDIP's onboarding
  process requires MRM inventory registration under MRM-POL-02 as its first step, before DUS-07
  data-access approval and Disclosure Review Committee (DRC) wording sign-off.
- **Related document — POL-FCC-014**: the customer communication standard for payment status,
  holds, and exceptions requires that any client-facing timing insight be registered with Model
  Risk Management "where MRM-POL-02 applies," alongside DUS-07 Section 5 data-basis rules and a
  DRC-approved disclaimer.
- **Related document — DUS-07**: the Data Use & Client Confidentiality Standard lists MRM-POL-02
  among its related documents, reflecting that client-facing predictive insights built on client
  data must satisfy both model-risk registration/tiering and DUS-07's purpose-limitation and
  confidentiality rules.
- **Related document — ADR-PAY-026 / TDIP-CAT-2026.2**: both the architecture decision record
  for serving client-facing analytical outputs via the TDIP Insights API and the TDIP data
  catalog extract list MRM-POL-02 as a related document, since any model backing an Insights API
  endpoint (e.g. the Treasury Insights cash-forecast model, M-TRS-0142) must be registered and
  tiered under this policy.
- **Related document — PRSP-HMS-3.4**: the Hold Management Service design and reason taxonomy
  lists MRM-POL-02 among its related documents, consistent with the Tier 1 financial-crimes
  models (Sentinel fraud score M-FCT-0021, beneficiary mule-risk features M-FCT-0034) it consumes
  being governed by this policy's use limitations.
- **Owning function — Model Risk Management (MRM)**: led by Jonathan Price, with Sophie Laurent
  as the Treasury & Operations models Validation Lead, per the PTT Organization & Ownership
  Directory (CNB-ORG-PTT-2026-06).
- **Approving body — Board Risk Committee**: approved the current (7.0) version at board level,
  reflecting the scope of the regulatory re-baseline.
- **Model owners named in the inventory extract**: Victor Petrov (Director, Financial Crimes
  Technology) owns the two Tier 1 financial-crimes models; Wei Zhang (Director, Treasury Data &
  Analytics) owns the Treasury Insights cash-forecast model; Denise Carter (Payment Operations)
  owns the registered EUA dashboard.

## Operational notes

- The Tier 2 validation queue had approximately a **6-week** wait before work starts as of the
  Q4-2026 capacity notice; submissions must include development documentation, data lineage, and
  proposed monitoring.
- The named contact for Tier 2 Treasury & Operations model submissions is Sophie Laurent
  (Validation Lead, Treasury & Operations models).
- Indicative validator effort by tier, per the policy's own figures: Tier 2 customer-facing
  estimates take roughly 10–14 weeks and 160–240 validator hours; Tier 3 internal operational
  models take roughly 6–9 weeks; EUA registration plus attestation takes roughly 2 weeks.
- At least one inventory entry (M-TRS-0142, Treasury Insights cash forecast) is shown mid-process
  — previously Tier 3, it is called out as re-tiering to Tier 2 under v7.0, illustrating how the
  revised, purpose/exposure-based tiering criteria can move an existing model to a higher tier
  requiring fuller independent validation.
