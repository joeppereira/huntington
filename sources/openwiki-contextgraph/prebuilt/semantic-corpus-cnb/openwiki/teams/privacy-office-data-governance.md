---
type: Team
entity_id: privacy-office-data-governance
title: Privacy Office & Data Governance
description: Second-line function led by Chief Privacy Officer Rachel Goldberg that owns the DUS-07 Data Use & Client Confidentiality Standard, runs Privacy Impact Assessments for new client-data uses, and approves Collibra Data Access Requests for Restricted datasets.
tags: [privacy-office, data-governance, dus-07, privacy-impact-assessment, collibra, rachel-goldberg, ethan-brooks, data-classification, second-line]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-49303e801f124d97df9c3ea3
    resource: repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md
  - id: openwiki-source-6fa6253c97994be177c92ec3
    resource: repo://sources/estate/dus-07-v2.1-data-use-and-client-confidentiality-standard.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

Privacy Office & Data Governance is a second-line-of-defense function at Crestline National Bank accountable for how client data may be used, combined, and disclosed — particularly in analytics or features shown back to clients. The function is led by **Rachel Goldberg, Chief Privacy Officer**, who is the named document owner of [DUS-07](../policies/dus-07.md) (Data Use & Client Confidentiality Standard) and the escalation point for any new client-facing use of client data. Day-to-day engagement with engineering and product teams — including policy interpretation questions that engineering teams are not authorized to decide themselves — routes through **Ethan Brooks, Data Governance Lead, Commercial Bank**, who is listed as the standard contact on DUS-07 and as the Privacy Office contact in the Payments & Treasury Technology (PTT) partner-function directory.

The function sits alongside other first- and second-line partner functions referenced by payments and treasury engineering teams, such as Financial Crimes Compliance (FCC), Model Risk Management (MRM), and Information Security, but is distinct from them: Privacy Office governs *data use and confidentiality*, not financial-crimes detection, model validation, or technical security review.

## Responsibilities

- **Owns DUS-07**, the standard governing purpose limitation, cross-client confidentiality, and aggregation thresholds for client-facing analytics. See [DUS-07 Data Use and Client Confidentiality Standard](../policies/dus-07.md) for the full control detail.
- **Approves new client-facing uses of client data** via the Privacy Impact Assessment (PIA) process.
- **Approves access to Restricted-classified datasets** jointly with the data owner, via Collibra Data Access Request (DAR) workflow.
- **Co-approves (with FCC)** any proposed use of financial-crimes data outside FCC purposes — a combination the standard notes is "generally not approved."
- Acts as the compliance/policy-interpretation escalation path for engineering teams when a dependency or design question turns on data-use or confidentiality rules rather than a purely technical decision.

## Key people

| Role | Name | Notes |
|---|---|---|
| Chief Privacy Officer | [Rachel Goldberg](../people/rachel-goldberg.md) | DUS-07 document owner; accountable for Privacy Office & Data Governance function |
| Data Governance Lead, Commercial Bank | [Ethan Brooks](../people/ethan-brooks.md) | DUS-07 standard contact; Privacy Office contact for product/design reviews; receives escalated policy-interpretation questions |

DUS-07 itself was approved by the **Data Governance Council** (approval dated 2026-01-08), which sits above the Privacy Office in the formal approval chain for the standard's content, even though Rachel Goldberg owns the document and the function operationally.

## Core mechanisms

### Data classification

DUS-07 defines four classification tiers that determine what controls apply to a dataset or output:

| Class | Examples |
|---|---|
| Public | Published rates, cutoff times |
| Internal | Aggregated operational metrics not attributable to a client |
| Confidential – Client | A client's own transactions, wire history, beneficiaries |
| Restricted – Client Confidential | Account-level activity in deposit systems; financial-crimes features; data about one client's accounts used for risk purposes |

Access to **Restricted** datasets is the trigger for the Collibra DAR approval described below. In the PTT system ownership register, several systems carry Restricted-class data under this classification, including the Core Deposit Platform (SYS-CDP, business owner Mark Sullivan, "Deposits Data Ownership") and the financial-crimes features produced by PRSP systems (SYS-PRSP-HMS, SYS-PRSP-SEN, SYS-PRSP-SSC).

### Collibra DAR approval for Restricted datasets

Any request for access to a Restricted dataset requires sign-off from **both** the data owner and the Privacy Office, executed through a Collibra Data Access Request (DAR). The standard lead time is **15 business days**. Engineering planning references treat this as an additive lead-time factor on top of normal team intake — for example, the Treasury Data & Analytics (TDIP) team's planning factor explicitly adds "+15 business days" for Collibra DAR requests touching Restricted data, on top of its normal Jira-TDA intake.

### Privacy Impact Assessment (PIA)

Any **new client-facing use of client data** — i.e., a use not already covered by an existing approval — requires a Privacy Impact Assessment, run continuously through OneTrust, with an expected turnaround of **approximately four weeks**. This is a distinct governance forum from, and runs in parallel with, other review bodies a payments feature may also need (Payments Architecture Review Board, Disclosure Review Committee, MRM Model Inventory, FCC Change Advisory). Teams sizing cross-team dependencies for a new client-facing data feature should budget the PIA's ~4-week lead time alongside these other forums rather than assuming it can be compressed.

### Purpose limitation and feature-table inheritance

Data collected or derived for one purpose (e.g., fraud detection, AML monitoring, credit decisioning) must not be reused for another purpose — including new product features — without Privacy Office approval, and additionally FCC approval if the data is financial-crimes data. A key operational invariant: **feature tables inherit the most restrictive permitted purpose of their inputs**. This means a downstream analytics or ML feature store cannot acquire broader usage rights than its most restrictive upstream source merely by aggregating or re-deriving data — engineering and data teams must track provenance of inputs to know what a derived feature table may legally be used for.

### Cross-client confidentiality

Information about one client — including that client's behavior as a counterparty to another client's transaction (e.g., activity in a receiving account after funds arrive) — must never be used to generate content shown to a different client. This bar applies even when the information is abstracted into "a pattern," "a typical value," or "an insight," and even when the counterparty is not named. This is a stricter rule than ordinary PII redaction: redacting a name is not sufficient if the underlying behavioral signal is still attributable to an identifiable other client's account.

### Aggregated cohort statistics shown to clients

Multi-client statistics may only be surfaced to a client if, for the measurement window, **all** of the following hold:

1. the cohort has at least **500 transactions**;
2. the cohort has at least **20 distinct originating clients**;
3. no single client contributes more than **15%** of cohort volume;
4. statistics refresh at least monthly; and
5. wording and disclaimers are approved by the Disclosure Review Committee (DRC, chaired by Patricia Moore, Legal – Treasury & Payments).

Failure of any single condition requires **suppression** of the cohort statistic — not rounding, not approximation, not substitution with a wider window. This is a hard failure mode, not a best-effort degradation, and is the most common way a client-facing analytics feature can violate DUS-07 if cohort composition shifts (e.g., a large client temporarily dominates volume and pushes a previously compliant cohort over the 15% concentration threshold).

### Use of a client's own data

A client's own historical data may be used to generate insights shown back to that same client (e.g., "your typical wire to this beneficiary completes in N days"), but only if the insight is based on **at least 5 comparable transactions**, and the insight must disclose its basis (the count and period used). This is the one case in DUS-07 where single-client data can be shown back to a client without cohort-style aggregation controls, provided the minimum sample size and disclosure requirements are met.

## Approval summary

| Activity | Required approval | Typical lead time |
|---|---|---|
| Access to Restricted datasets | Data owner + Privacy Office (Collibra DAR) | 15 business days |
| New client-facing use of client data | Privacy Impact Assessment (OneTrust) | ~4 weeks |
| Use of financial-crimes data outside FCC purposes | Privacy Office + FCC | Generally not approved |

## Relationships to other functions and systems

- **FCC (Financial Crimes Compliance)**, accountable under Catherine Doyle, must jointly approve any attempt to use financial-crimes data (e.g., PRSP fraud/sanctions features) outside its original FCC purpose; absent that joint approval such reuse is presumed disallowed.
- **Deposits Data Ownership** (Mark Sullivan) is the business/data owner for Core Deposit Platform datasets, which are Restricted-classified; any team requesting access to those datasets needs both Mark Sullivan's and the Privacy Office's sign-off via Collibra DAR.
- **TDIP (Treasury Data & Analytics)**, under Wei Zhang, is a primary consumer-facing analytics team whose planning factors explicitly bake in Collibra DAR lead time, making it one of the more directly affected engineering teams for DUS-07 compliance.
- **Disclosure Review Committee**, chaired by Patricia Moore in Legal – Treasury & Payments, is a required downstream approver for cohort-statistics wording and disclaimers under DUS-07 §5, operating on a bi-weekly (Thursday) cadence with a 5-business-day submission lead time.
- **Data Governance Council** approved DUS-07 v2.1 and sits above the Privacy Office for standard-level sign-off, distinguishing policy *approval* authority from the Privacy Office's day-to-day *ownership and operational approval* role (PIA, DAR).

## Related pages

- [DUS-07 Data Use and Client Confidentiality Standard](../policies/dus-07.md)
- [Rachel Goldberg](../people/rachel-goldberg.md)
- [Ethan Brooks](../people/ethan-brooks.md)
