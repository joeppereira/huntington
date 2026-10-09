---
type: Person
entity_id: ethan-brooks
title: Ethan Brooks
description: Data Governance Lead for the Commercial Bank within Crestline National Bank's Privacy Office; approver of the TDIP payments-domain data catalog (TDIP-CAT-2026.2), named standard contact for the DUS-07 Data Use & Client Confidentiality Standard, and the escalation point for data-governance and client-data policy-interpretation questions raised by Payments & Treasury Technology engineering teams.
tags: [person, data-governance, privacy-office, commercial-bank, tdip, dus-07, approver, escalation-contact]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-49303e801f124d97df9c3ea3
    resource: repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md
  - id: openwiki-source-6fa6253c97994be177c92ec3
    resource: repo://sources/estate/dus-07-v2.1-data-use-and-client-confidentiality-standard.md
  - id: openwiki-source-a8ab82acd285acae1ac9546d
    resource: repo://sources/estate/tdip-cat-2026.2-treasury-data-and-insights-platform-data-catalog-extract.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

Ethan Brooks is the **Data Governance Lead, Commercial Bank**, operating within Crestline National Bank's Privacy Office & Data Governance function (led by Chief Privacy Officer Rachel Goldberg). He is the named contact for Privacy Office & Data Governance engagement in the Payments & Treasury Technology (PTT) organization directory, the approver of record for the Treasury Data & Insights Platform (TDIP) payments-domain data catalog, and the day-to-day "standard contact" for the DUS-07 Data Use & Client Confidentiality Standard. Across the corpus he functions less as a system owner and more as the governance gate that payments and treasury engineering/data teams must clear whenever client data is classified, reused for a new purpose, or exposed through client-facing analytics.

## Role and scope

- **Function**: Privacy Office & Data Governance, a second-line partner function to Payments & Treasury Technology (PTT). The PTT organization directory lists Rachel Goldberg (Chief Privacy Officer) as the function's accountable leader and Ethan Brooks as the named contact for product/design reviews touching data governance.
- **Title**: Data Governance Lead, Commercial Bank — a commercial-bank-scoped governance role, distinct from Rachel Goldberg's bank-wide Chief Privacy Officer ownership of the DUS-07 standard itself.
- **Relationship to Rachel Goldberg**: Goldberg is the accountable *document owner* of DUS-07 and the function's accountable leader; Brooks is the operational point of contact — for DUS-07 questions and for PTT's data-governance escalations — making him the practical first stop before an issue would need to reach Goldberg or the Data Governance Council.

## Approver of TDIP-CAT-2026.2

Ethan Brooks is listed as an approver, alongside Wei Zhang (Director, Treasury Data & Analytics), of **TDIP-CAT-2026.2**, the published Treasury Data & Insights Platform data catalog extract covering payments-domain datasets, feature tables, classifications, ownership, freshness, and the client-facing Insights API serving pattern. His sign-off sits alongside the document owners, Carlos Mendes (EM, Treasury Data Platform) and Dr. Aisha Rahman (Lead Data Scientist), giving the catalog a data-governance approval in addition to its engineering/data-science ownership.

This approval is substantive rather than ceremonial: the catalog itself states that datasets classified Restricted require Privacy Office approval (SLA 15 business days) before access is granted, and the PTT engagement directory separately notes that Restricted-dataset requests routed through TDIP's Collibra Data Access Request (DAR) process carry a +15 business day penalty specifically for that Privacy Office review. Brooks's office is the approving party behind that SLA for payments-domain datasets such as `dda_txn_history` (Restricted - Client Confidential) and the `beneficiary_behavior_profile` feature table (Restricted - Client Confidential, FCT fraud/mule-detection use only).

## Standard contact for DUS-07

Brooks is named the **standard contact** for **DUS-07 v2.1 (Data Use and Client Confidentiality Standard)**, the Privacy Office standard that governs purpose limitation, cross-client confidentiality, and aggregation thresholds for client-facing analytics. DUS-07 is owned by Rachel Goldberg and was approved by the Data Governance Council (2026-01-08, effective 2026-01-15); Brooks is the person engineering and product teams are expected to contact with day-to-day questions about applying the standard, rather than escalating directly to Goldberg or the Council.

DUS-07's rules are the governance backbone behind several practices documented elsewhere in the payments/treasury estate, all of which fall within Brooks's area of responsibility as standard contact:

- **Purpose limitation** — data collected for one purpose (fraud detection, AML monitoring, credit) cannot be reused for another, including new product features, without Privacy Office approval; feature tables inherit the most restrictive permitted purpose of their inputs (e.g. `beneficiary_behavior_profile` is restricted to FCT fraud/mule-detection use because it draws on financial-crimes-adjacent deposit data).
- **Cross-client confidentiality** — a client's behavior, including its behavior as a counterparty, must never be used to generate content shown to a different client, even anonymized or expressed as a pattern — a constraint directly relevant to any wire-corridor or counterparty-behavior analytics TDIP might expose.
- **Aggregated cohort statistics** — client-facing cohort statistics must clear a five-part test (≥500 transactions, ≥20 distinct originating clients, no client >15% of volume, at least monthly refresh, and Disclosure Review Committee-approved wording) or be suppressed outright.
- **Approvals** — Restricted-dataset access requires data owner plus Privacy Office sign-off (Collibra DAR, 15 business days); new client-facing uses of client data require a Privacy Impact Assessment (~4 weeks); use of financial-crimes data outside FCC purposes is "generally not approved."

## Escalation contact for data-governance questions

The PTT organization directory's escalation section is explicit that **compliance or policy-interpretation questions are not decided by engineering teams**: they route to FCC Policy & Advisory (Jordan Ellis) for financial-crimes questions, or to the Privacy Office — named as Ethan Brooks — for data-governance and client-confidentiality questions. This places Brooks above the normal engineering-manager → director → PTT Leadership Team dependency-escalation path for any disagreement that turns on how client data may be classified, combined, or used, rather than on engineering capacity or sequencing.

## Relationships

- **Rachel Goldberg** (Chief Privacy Officer) — accountable owner of DUS-07 and leader of the Privacy Office & Data Governance function in which Brooks operates as the Commercial Bank's governance lead and primary contact.
- **Carlos Mendes** and **Dr. Aisha Rahman** — document owners of [TDIP-CAT-2026.2](../documents/tdip-cat-2026.2.md), whose catalog Brooks approves from a data-governance standpoint.
- **Wei Zhang** — Director, Treasury Data & Analytics, co-approver of TDIP-CAT-2026.2 alongside Brooks; Zhang signs off on the technical/platform content while Brooks signs off on governance.
- **Laura Kim** — Director, Payments Platform Product and business/data owner for most TDIP payments-domain datasets; any Restricted-classification dataset she stewards (e.g. implicitly via `beneficiary_behavior_profile`'s inputs) requires Brooks's office's sign-off for access.
- **Jordan Ellis** (FCC Policy & Advisory) — the parallel escalation contact for financial-crimes/compliance policy questions, as distinguished from Brooks's data-governance/privacy remit in the same escalation clause.
- See [Privacy Office & Data Governance](../teams/privacy-office-data-governance.md) for the function-level writeup, and [Payments & Treasury Technology](../organizations/payments-treasury-technology.md) for the engineering organization whose work Brooks's approvals and escalation role gate.

## Operational notes

- Brooks's name appears consistently across three independent source documents — the PTT organization/engagement directory, the TDIP data catalog, and DUS-07 — each time in a governance-approval or escalation-contact capacity rather than as a system or engineering owner, indicating his role is cross-cutting across PTT's payments and treasury data products rather than scoped to a single system.
- Because DUS-07 Restricted-access approvals (15 business days) and PIA reviews (~4 weeks) sit on Brooks's side of the approval chain, they are recurring lead-time factors that PTT and TDIP teams must plan for when scoping new client-facing analytics work, as reflected in the engagement directory's planning factors for Jira TDA requests involving Restricted data.
