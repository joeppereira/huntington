---
type: Person
title: Dana K. Whitfield, Chief Risk Officer
description: Profile of Dana K. Whitfield, Chief Risk Officer of the fictional Meridian Harbor Financial Corp. It covers her reporting lines, the independent risk function she leads, the model risk (MRGR) function that reports to her, her committee and compensation roles, and her public statements on credit.
tags: [person, executive, cro, risk-management, model-risk, mrgr, meridian-harbor, leadership]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-05T01:46:21.335Z
sources:
  - id: openwiki-source-eb14da62fbec45aad876fb64
    resource: repo://sources/reports/mhfc-2025-annual-report.md
  - id: openwiki-source-c13af588d055d118eda543d5
    resource: repo://sources/reports/mhfc-2025-pillar3-disclosures.md
  - id: openwiki-source-9da334bbfcfb68cd7514ff33
    resource: repo://sources/reports/mhfc-q2-2026-earnings-supplement.md
generated: { by: "openwiki/0.7.0", at: "2026-10-05T01:46:21.335Z" }
---

# Dana K. Whitfield, Chief Risk Officer

Dana K. Whitfield is the Chief Risk Officer (CRO) of [Meridian Harbor Financial Corp.](../organizations/meridian-harbor-financial-corp.md) (MHFC). MHFC is a **fictional** institution, and the source documents are labelled synthetic. The sources give no biography, tenure or compensation for Whitfield. They record her title, her reporting lines, the structure of the function she leads and one set of remarks on an earnings call.

## Reporting lines and mandate

The Pillar 3 disclosures say the CRO reports to **both** the Chief Executive Officer ([Eleanor V. Ashcombe](chief-executive-officer.md)) and the **Board Risk Committee**. The CRO leads an **independent risk management function** organized by risk stripe: credit, market, liquidity, model, operational, compliance and reputational.

The firm uses a three-lines-of-defense model:

| Line | Who | Role |
|---|---|---|
| First | Lines of business and Treasury/CIO | Own the risks they generate. |
| Second | Independent Risk Management and Compliance | Set risk appetite, policies and limits, and challenge the first line. The CRO leads this line. |
| Third | Internal Audit | Gives independent assurance to the Audit Committee. |

The dual reporting line (management and Board) is the structural basis for the function's independence from the businesses it challenges.

## What reports into the CRO's organization

The sources attribute these responsibilities to the Chief Risk Office or its independent risk stripes:

- **Model risk.** The Model Risk Governance & Review (MRGR) function **reports to the Chief Risk Officer**. It oversees the Model Risk Policy, which aligns with SR 11-7. It acts as the independent validator for the firm's Tier 1 models. See [Model Risk Governance & Review](../teams/model-risk-governance-review.md) and [Model risk and SR 11-7](../concepts/model-risk-sr-11-7.md).
- **Credit risk.** The annual report says credit risk is managed by the independent Chief Risk Office and the lines of business within a Board-approved risk appetite framework.
- **Market risk.** Market Risk Management is part of the independent risk function. It sets limits, monitors exposures and reports to the Board Risk Committee.
- **Liquidity oversight.** Treasury/CIO runs liquidity risk management. Independent oversight comes from a Liquidity Risk Oversight function within the Chief Risk Office.
- **Operational and other risk.** The operational risk framework (risk and control self-assessments, key risk indicators, scenario analysis, loss data collection) sits within the same risk-stripe structure.

## The model risk line in practice

Because MRGR reports to the CRO, the CRO's organization is the independent validator of the models that drive disclosed figures. The annual report and Pillar 3 disclosures describe how this works.

- **Tiering.** Each model gets a risk tier by materiality and complexity. Tier 1 models need annual independent validation, documented ongoing monitoring and approval by the Firmwide Model Risk Committee before use. The inventory holds about 2,900 models.
- **Validation cadence.** The Pillar 3 disclosures add quarterly performance monitoring and annual attestation by model owners. Material model changes require MRGR approval. Regulatory capital models also require regulatory notification.
- **Change control.** Upstream APIs are registered as critical data sources in the model inventory. A breaking change to an API's schema or business logic opens a model change review.

Three Tier 1 models directly drive disclosed figures. MRGR is the independent validator for all three:

| Model | Owner | Last validated | Key 2025–26 validation finding |
|---|---|---|---|
| [Net Interest Income Sensitivity Model](../models/nii-sensitivity-model.md) (MDL-ALM-014) | Corporate Treasury – Asset & Liability Management | 2025-09-18 | Medium: deposit betas held constant across shock sizes. The compensating control is the quarterly dynamic simulation. |
| [CECL Lifetime Expected Credit Loss Model](../models/cecl-allowance-model.md) (MDL-CR-007) | Consumer & Wholesale Credit Risk – Allowance Methodology | 2025-11-04 | One medium finding (no explicit model for unfunded commitments, covered by an interim overlay) and one low finding (Card PD elasticity documentation). |
| [Capital Planning & Stress Projection Model](../models/capital-planning-model.md) (MDL-CAP-003) | Corporate Treasury – Capital Management | 2026-02-27 | No finding above low severity. |

Model owners are in the first line, so validation is independent of the teams that build and run each model.

## Governance forums and risk appetite

The Pillar 3 disclosures list the committees through which risk decisions flow. Whitfield is named only as co-chair of the first; the sources do not name her seat on the others.

- **Firmwide Risk Committee.** A senior management forum for firmwide risk issues, **chaired by the CEO and CRO**.
- **Firmwide Model Risk Committee.** Approves Tier 1 models and model risk appetite.
- **Allowance Committee.** Approves scenario weights, CECL model outputs and qualitative overlays each quarter.
- **Capital Governance Committee.** Chaired by the CFO. Oversees capital planning and CCAR.
- **Data and Technology Risk Committee.** Oversees critical data elements, API change management and BCBS 239 compliance.
- **ALCO.** Oversees liquidity, interest rate and capital risk.

The Board-approved risk appetite framework sets quantitative limits, and all were "Within" at December 31, 2025. They include:

- Standardized CET1 of at least 13.0% (actual 15.08%).
- Supplementary leverage ratio of at least 5.5% (actual 6.1%).
- LCR of at least 110% (actual 116%).
- NII decline under a –200 bp shock of at most 7.0% (actual 6.0%).
- Annual Card net charge-off rate of at most 4.5% (actual 3.42%).
- Single-name wholesale exposure of at most 10% of Tier 1 (actual 4.8%).

## Compensation input

In the remuneration section, the CRO and the Chief Compliance Officer provide input to the Board's Compensation & Management Development Committee. The input covers risk and control outcomes for every business and for individual material risk takers. It feeds incentive pay, which carries deferral, clawback and cancellation provisions. In 2025, 1.1% of eligible employees had incentive pay reduced for risk, control or conduct issues.

## Public statements (Q2 2026 earnings call)

Whitfield answered two analyst questions in the July 14, 2026 call, in paraphrased form:

- **Card reserve.** The Card allowance is roughly 6% of loans, which she said covers almost two years of current charge-offs. It is driven mainly by loan growth and scenario weights. A move entirely to the downside scenario would raise the firmwide allowance by over $4 billion, so weighting matters more than small baseline changes. The 2025 annual report gives the same sensitivity (about $20.2 billion, or $4.2 billion higher than reported). See [Allowance for credit losses](../metrics/allowance-for-credit-losses.md) and [CECL](../concepts/cecl.md).
- **Office commercial real estate.** Criticized office loans fell for a second straight quarter. Allowance coverage on office is close to 10%. Losses are expected to stay "elevated but manageable", and office is about 2% of total loans.

## Notes for readers

- The CRO is distinct from the CTO (Marcus O. Lindqvist), who oversees the Developer Platform. The CRO's organization still sets the model-risk and data-risk expectations those APIs must meet when they feed Tier 1 models.
- The 2025 annual report names the Chief Risk Office in its credit and liquidity sections without naming Whitfield. Her name appears in the Pillar 3 disclosures and the Q2 2026 earnings supplement.
