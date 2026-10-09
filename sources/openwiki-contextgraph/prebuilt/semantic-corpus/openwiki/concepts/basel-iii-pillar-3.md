---
type: RiskConcept
title: Basel III Pillar 3
description: Explains the Basel III Pillar 3 market-disclosure regime and how Meridian Harbor Financial Corp. (a fictional bank) structures its FY2025 Pillar 3 report, including scope, controls, section map, and data lineage.
tags: [basel-iii, pillar-3, regulatory-capital, disclosure, risk-management, mhfc]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-05T01:46:21.335Z
sources:
  - id: openwiki-source-c13af588d055d118eda543d5
    resource: repo://sources/reports/mhfc-2025-pillar3-disclosures.md
generated: { by: "openwiki/0.7.0", at: "2026-10-05T01:46:21.335Z" }
---

# Basel III Pillar 3

Pillar 3 is the market-discipline part of the Basel III framework. It complements the minimum capital requirements (Pillar 1) and the supervisory review process (Pillar 2). It requires banks to publish information on capital adequacy, risk exposures and risk management processes, so that market participants can assess a bank's capital position and risk profile.

The source document is the Pillar 3 report of Meridian Harbor Financial Corp. (MHFC) for the fiscal year ended December 31, 2025, published March 2026. MHFC is a fictional institution, and the document is labelled a synthetic proof-of-concept. This page explains the concept and how MHFC applies it. For the report itself, see [Pillar 3 Disclosures 2025](../reports/pillar3-disclosures-2025.md). For the central quantity behind most disclosed ratios, see [Risk-Weighted Assets](../metrics/risk-weighted-assets.md).

## Regime and scope in the MHFC report

- **Legal basis.** The report states it is prepared under 12 CFR 217 Subpart D (§217.61-63) and Subpart E (§217.171-173).
- **Reporting perimeter.** The disclosures cover the consolidated bank holding company. The principal insured depository institution, Meridian Harbor Bank, N.A., is subject to separate capital requirements and is described as well capitalized. The report states there are no restrictions on transferring funds or regulatory capital within the Firm beyond those generally applicable to U.S. bank holding companies.
- **Advanced approaches firm.** MHFC calculates RWA under both the Standardized and Advanced approaches. It uses the lower of each ratio under the two approaches, currently the Standardized one, to assess capital adequacy. The report calls this the "Collins Floor".
- **Assurance level.** The disclosures need not be audited. They are subject to the Firm's disclosure controls and to Disclosure Committee review. They are described as consistent with the FR Y-9C, FFIEC 101 and FR Y-15 regulatory filings.

Evidence: repo://sources/reports/mhfc-2025-pillar3-disclosures.md#L7-L37

## How the report is organised

The introduction maps each Pillar 3 requirement to a report section. This table is the main navigation aid for the regime:

| Pillar 3 topic | Section | Main content |
|---|---|---|
| Scope of application | 1 | Perimeter, approaches, controls |
| Capital structure | 3 | CET1 reconciliation, Tier 1 and Total capital, instruments |
| Capital adequacy | 4 | RWA by exposure type, RWA flow, countercyclical buffer (CCyB) geography, ratios and buffers |
| Leverage | 5 | Supplementary leverage ratio (SLR) and Tier 1 leverage |
| Credit risk | 6 | Exposure by type, geography and industry; PD bands; allowance; mitigation |
| Counterparty credit risk | 7 | SA-CCR and internal models, CVA |
| Securitization | 8 | SSFA and 1,250% risk weights |
| Market risk | 9 | VaR, stressed VaR, IRC, backtesting |
| Operational risk | 10 | Loss distribution approach |
| Interest rate risk in the banking book | 11 | NII and EVE shocks |
| Liquidity | 12 | LCR and NSFR |
| Stress testing and capital planning | 13 | Internal and supervisory scenarios |
| Model risk and data governance | 14-15 | Tier 1 model inventory, API lineage |

Sections 2 (risk governance) and 16 (remuneration) are also included. Section 2 covers risk appetite and committees. Section 16 covers deferral and clawback of incentive pay.

Evidence: repo://sources/reports/mhfc-2025-pillar3-disclosures.md#L39-L54

## Key disclosed relationships

**Capital ratios.** At December 31, 2025, CET1 capital was $98,450 million, Tier 1 capital $110,620 million and Total capital (Standardized) $128,900 million. Standardized RWA was $652,800 million and Advanced RWA $618,300 million. The resulting ratios are:

| Ratio | Standardized | Advanced |
|---|---|---|
| CET1 | 15.08% | 15.92% |
| Tier 1 | 16.95% | 17.89% |
| Total capital | 19.75% | 20.54% |

The CET1 requirement is 10.2% and the Standardized capital conservation buffer is 10.58% against 5.7% required. The 5.7% requirement is the stress capital buffer (3.2%) plus the G-SIB surcharge (2.5%) plus a 0% countercyclical buffer. The report states the Firm faced no limits on distributions or discretionary bonuses. For how RWA is built up and moves over the year, see [Risk-Weighted Assets](../metrics/risk-weighted-assets.md).

Evidence: repo://sources/reports/mhfc-2025-pillar3-disclosures.md#L99-L114, repo://sources/reports/mhfc-2025-pillar3-disclosures.md#L135-L149, repo://sources/reports/mhfc-2025-pillar3-disclosures.md#L186-L194

**Countercyclical buffer.** The U.S. CCyB is 0%. Foreign-jurisdiction rates (e.g., United Kingdom 2.00%, Germany 0.75%) are shown for transparency and Advanced approaches computation. The weighted firm-specific figure is 0.108% on non-U.S. exposure only.

Evidence: repo://sources/reports/mhfc-2025-pillar3-disclosures.md#L170-L182

**Leverage.** The SLR is Tier 1 capital divided by total leverage exposure ($110,620 million over $1,812,000 million), giving 6.10%. The Tier 1 leverage ratio is 7.91%. The report states the effective SLR requirement is 5.0% (3.0% minimum plus a 2.0% enhanced buffer). Internally, the risk appetite framework sets a stricter 5.5% SLR limit.

Evidence: repo://sources/reports/mhfc-2025-pillar3-disclosures.md#L198-L211, repo://sources/reports/mhfc-2025-pillar3-disclosures.md#L72

**Risk appetite as the internal counterpart.** The Board-approved appetite uses quantitative limits that the disclosures report against. Examples are Standardized CET1 of at least 13.0% (15.08% actual), LCR of at least 110% (116%), and a decline in NII under a -200 bp shock of at most 7.0% (6.0%). All listed metrics were within limits at year end.

Evidence: repo://sources/reports/mhfc-2025-pillar3-disclosures.md#L64-L77

**Liquidity and stress.** The LCR is 116% (Q4 average) and the NSFR is 128%. The internal severely adverse scenario produces a 12.6% minimum CET1 ratio. The Federal Reserve's supervisory severely adverse projection was 12.1%, which set the 3.2% stress capital buffer. Projection outputs of the capital planning model are deliberately not reproduced, because they refresh quarterly and are published in earnings materials.

Evidence: repo://sources/reports/mhfc-2025-pillar3-disclosures.md#L410-L437, repo://sources/reports/mhfc-2025-pillar3-disclosures.md#L443-L466

## Governance, model risk and data lineage

The disclosures sit on top of a governed pipeline:

1. **Three lines of defense.** Lines of business and Treasury/CIO own risks, Independent Risk Management and Compliance challenge them, and Internal Audit provides independent assurance. Committees own specific outputs. ALCO reviews the NII Sensitivity Model monthly, the Capital Governance Committee owns capital planning outputs, and the Allowance Committee approves CECL scenario weights and overlays.
2. **Tier 1 models.** Models behind capital, allowance, liquidity and interest rate risk figures follow a Model Risk Policy aligned with SR 11-7. Tier 1 models get annual independent validation by Model Risk Governance & Review (MRGR), quarterly monitoring and annual owner attestation. Material changes need MRGR approval and, for regulatory capital models, regulatory notification. The disclosures name three such models: MDL-ALM-014 (NII sensitivity, Section 11), MDL-CR-007 (CECL allowance, Section 6) and MDL-CAP-003 (capital planning, Section 13).
3. **Governed APIs.** Under the BCBS 239 principles, risk and regulatory data flow through governed APIs on the Developer Platform. Each API has a named data owner, schema, data-quality rules and service-level objectives. Each is registered as a critical data source, and a breaking schema or business-logic change automatically opens a model change review.

The API-to-disclosure mapping in Section 15 is:

| API | Supports disclosure sections |
|---|---|
| API-16 Regulatory Reporting | 3, 4, 5, 13 (capital, RWA, leverage exposure; also FR Y-9C) |
| API-10 Credit Risk Scoring | 4, 6 (PD/LGD, point-in-time and through-the-cycle) |
| API-11 Loan Servicing | 6, 11 |
| API-12 Market Data | 6, 9, 11 |
| API-13 FX Rates | 6, 9 |
| API-14 Macroeconomic Scenario | 6, 13 |
| API-15 Treasury Liquidity Positions | 11, 12 |
| API-09 Credit Decisioning | 6 (indirect) |
| API-08 Fraud Risk Signals | 10 |

API-16 outputs are automatically reconciled to the general ledger at legal-entity level (introduced in 2025). Data-quality exceptions on critical data elements go monthly to the Data and Technology Risk Committee. The report states none had a material impact on reported capital ratios.

Evidence: repo://sources/reports/mhfc-2025-pillar3-disclosures.md#L56-L91, repo://sources/reports/mhfc-2025-pillar3-disclosures.md#L470-L537

## Invariants and caveats for readers

- **Regulatory vs accounting parameters.** Advanced-approach PD/LGD are through-the-cycle with regulatory floors. CECL parameters are point-in-time and scenario-conditioned. API-10 exposes both through separate endpoints, so figures from the two uses should not be mixed.
- **Model limitations disclosed.** MDL-ALM-014 uses parallel shocks on a static balance sheet. It does not capture non-parallel curve moves, basis risk or mortgage prepayment optionality, and it holds deposit betas constant. MRGR flagged the constant betas as a medium finding. The compensating control is quarterly dynamic simulation.
- **Validation status.** MRGR's 2025 validation of MDL-CR-007 raised one medium and one low finding. MDL-CAP-003 was validated in February 2026 with nothing above low severity.
- **Internal inconsistency to note.** The 5.0% SLR requirement in Section 5 differs from the 5.5% appetite limit. Treat 5.5% as an internal limit, not the regulatory minimum.
- **Synthetic data.** All names, figures and events are invented. Do not treat any number as describing a real institution.

Evidence: repo://sources/reports/mhfc-2025-pillar3-disclosures.md#L283, repo://sources/reports/mhfc-2025-pillar3-disclosures.md#L379-L402, repo://sources/reports/mhfc-2025-pillar3-disclosures.md#L517
