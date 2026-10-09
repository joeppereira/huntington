---
type: Document
entity_id: DUS-07
title: "DUS-07: Data Use and Client Confidentiality Standard (v2.1)"
description: Metadata record for Crestline National Bank's Privacy Office standard governing purpose limitation, cross-client confidentiality, and aggregation thresholds for client-facing analytics.
tags: [dus-07, data-use, client-confidentiality, privacy-office, aggregation-thresholds, purpose-limitation, governance, document]
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
  - id: openwiki-source-a8ab82acd285acae1ac9546d
    resource: repo://sources/estate/tdip-cat-2026.2-treasury-data-and-insights-platform-data-catalog-extract.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Summary

**DUS-07** ("Data Use & Client Confidentiality Standard") is the Privacy Office standard at
Crestline National Bank (CNB) governing how client data may be used, combined, and disclosed —
in particular in analytics and insights shown to clients through digital channels such as
Crestline Business Online (CBO). The corpus holds only an **extract** of the full standard,
covering purpose limitation, data classification, cross-client confidentiality, aggregation
thresholds for cohort statistics, use of a client's own data, and the approval workflows that
gate access to restricted data and new client-facing uses. For the normative rules themselves,
see the companion page [DUS-07 (Policy)](../policies/dus-07.md); this page records the
document's identity, ownership, and governance metadata.

## Document metadata

| Field | Value |
|---|---|
| Document ID | DUS-07 |
| Version / Status | 2.1 / Approved |
| Document owner | Rachel Goldberg, Chief Privacy Officer |
| Approver(s) | Data Governance Council (approved 2026-01-08) |
| Effective / Last reviewed | Effective 2026-01-15 |
| Classification | INTERNAL - CONFIDENTIAL |
| Standard contact | Ethan Brooks, Data Governance Lead, Commercial Bank |
| Related documents | POL-FCC-014; MRM-POL-02; TDIP-CAT-2026.2 |

The document is marked "Uncontrolled when printed" on every page footer, meaning printed or
exported copies carry no guarantee of reflecting the current approved revision — the Privacy
Office's system of record is authoritative. It applies to both consumer and commercial clients:
consumer data is additionally subject to the Gramm-Leach-Bliley Act privacy provisions, while
commercial client data is protected by contractual confidentiality under the Treasury Management
Services Agreement, section 14.

## Ownership and approval chain

- **Owner**: Rachel Goldberg, Chief Privacy Officer, is the accountable document owner. The PTT
  Organization & Ownership Directory (CNB-ORG-PTT-2026-06) independently confirms her as "Owner of
  DUS-07 Data Use & Client Confidentiality Standard."
- **Standard contact**: Ethan Brooks, Data Governance Lead for the Commercial Bank, is the named
  day-to-day contact for questions on the standard and sits within the Privacy Office & Data
  Governance partner function.
- **Approver**: the **Data Governance Council** approved version 2.1 on 2026-01-08, ahead of its
  2026-01-15 effective date.
- **Escalation**: per the PTT directory, compliance or policy-interpretation questions about this
  standard route to the Privacy Office (Ethan Brooks) rather than being decided unilaterally by
  engineering teams.

## What this extract covers

The extract is organized into seven numbered sections:

1. **Purpose** — scope (consumer and commercial clients) and the external legal/contractual bases
   (GLBA; Treasury Management Services Agreement s14) layered on top of the standard.
2. **Classification (summary)** — a four-tier scheme (Public, Internal, Confidential - Client,
   Restricted - Client Confidential) used to label client-related data.
3. **Purpose limitation** — the rule that data collected for one purpose (e.g. fraud detection,
   AML monitoring, credit) may not be reused for another purpose, including product features,
   without Privacy Office (and, for financial-crimes data, FCC) approval; derived feature tables
   inherit the most restrictive permitted purpose of their inputs.
4. **Cross-client confidentiality** — the prohibition on using one client's data, including its
   behavior as a payment counterparty, to generate content shown to a different client, even when
   anonymized or presented as a pattern/typical value.
5. **Aggregated cohort statistics shown to clients** — the five-condition test (minimum
   transaction and client counts, concentration cap, refresh cadence, DRC-approved wording) a
   cohort must pass before it may be surfaced to clients, with mandatory suppression (not
   rounding) on failure.
6. **Use of a client's own data** — the minimum comparable-transaction threshold and
   basis-disclosure requirement for single-client insights.
7. **Approvals** — the approval paths and SLAs for Restricted dataset access, new client-facing
   uses of client data, and (effectively barred) use of financial-crimes data outside FCC
   purposes.

The detailed numeric thresholds and rule text from these sections are documented on the
[DUS-07 policy page](../policies/dus-07.md) rather than restated here.

## Relationships

- **Governs**: client-facing analytics and insights work on [CBO Wire Center](./cbo-arch-wc-4.1.md)'s
  digital channels and on the [TDIP data catalog (TDIP-CAT-2026.2)](./tdip-cat-2026.2.md), which cites
  DUS-07 as a related document and requires DUS-07 data-access approval as step (2) of its
  insight-onboarding process.
- **Related document — POL-FCC-014**: the customer communication standard for payment status,
  holds, and exceptions incorporates DUS-07 Section 5's aggregation thresholds directly into its
  own rule for client-facing timing insights (own data or qualifying DUS-07 §5 cohorts, MRM
  registration, DRC disclaimer, no display for tier G/R holds).
- **Related document — MRM-POL-02**: the model risk management policy extract lists DUS-07 among
  its related documents, reflecting that client-facing predictive insights built on client data
  must satisfy both model-risk registration and DUS-07's purpose-limitation and confidentiality
  rules.
- **Related document — TDIP-CAT-2026.2**: the Treasury Data & Insights Platform data catalog
  extract lists DUS-07 among its related documents and names it as the source of the data-access
  approval gate (step 2 of onboarding a new insight), alongside MRM-POL-02 registration and DRC
  wording approval.
- **Owning function — Privacy Office & Data Governance**: led by Rachel Goldberg with Ethan Brooks
  as the Commercial Bank data governance contact, per the PTT Organization & Ownership Directory
  (CNB-ORG-PTT-2026-06).
- **Approving body — Data Governance Council**: approved the current (2.1) version.
- **Disclosure Review Committee (DRC)**: approves the wording and disclaimers required by DUS-07
  Section 5 before aggregated cohort statistics may be shown to clients, and is chaired by
  Patricia Moore (Legal - Treasury & Payments), per the PTT directory.

## Operational notes

- Access requests to Restricted-classified datasets require both the data owner's and the Privacy
  Office's sign-off, processed through Collibra's Data Access Request (DAR) workflow with a
  15-business-day service level.
- New client-facing uses of client data require a Privacy Impact Assessment, with an indicative
  turnaround of roughly four weeks.
- Use of financial-crimes data for purposes outside FCC's own purposes requires joint Privacy
  Office and FCC approval and is described in the standard as "generally not approved."
