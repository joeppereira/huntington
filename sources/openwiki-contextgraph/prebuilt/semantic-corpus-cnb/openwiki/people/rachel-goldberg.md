---
type: Person
entity_id: rachel-goldberg
title: Rachel Goldberg
description: Chief Privacy Officer at Crestline National Bank and document owner of the DUS-07 Data Use & Client Confidentiality Standard, accountable for purpose limitation and cross-client confidentiality governance over client data.
tags: [people, privacy-office, data-governance, chief-privacy-officer, dus-07, compliance]
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

Rachel Goldberg is the **Chief Privacy Officer (CPO)** of Crestline National Bank. She is the accountable leader for the Privacy Office & Data Governance function and is the named document owner of [DUS-07, the Data Use & Client Confidentiality Standard](../policies/dus-07.md), which governs how client data may be used, combined, and disclosed — most notably in analytics and insights shown to clients.

She appears in the Payments & Treasury Technology (PTT) organization directory both as an enterprise leadership contact and as the accountable owner of a first/second-line partner function that payments engineering teams must engage when their work touches client data.

## Roles and responsibilities

| Capacity | Scope |
|---|---|
| Chief Privacy Officer (enterprise leadership) | Owner of DUS-07 Data Use & Client Confidentiality Standard |
| Accountable lead, Privacy Office & Data Governance (partner function to PTT) | Second-line privacy oversight for payments and treasury technology systems; approves Privacy Impact Assessments (PIAs) and access to Restricted datasets |

Within the PTT organization directory, Rachel Goldberg is listed under enterprise leadership as Chief Privacy Officer and separately under partner functions as the accountable owner of "Privacy Office & Data Governance," with **Ethan Brooks** (Data Governance Lead, Commercial Bank) named as the day-to-day contact for product and design reviews.

As DUS-07's document owner, she is the control point for:

- **Purpose limitation** — data collected or derived for one purpose (e.g., fraud detection, AML monitoring, credit) may not be repurposed, including for product features, without Privacy Office approval (and FCC approval for financial-crimes data). Feature tables inherit the most restrictive permitted purpose of their inputs.
- **Cross-client confidentiality** — information about one client, including its behavior as a counterparty, must never be used to generate content shown to another client, even presented as an anonymized pattern or typical value.
- **Aggregated cohort statistics** — client-facing cohort statistics are permitted only when the cohort has at least 500 transactions, at least 20 distinct originating clients, no single client contributing more than 15% of cohort volume, monthly refresh, and Disclosure Review Committee–approved wording; cohorts failing any test must be suppressed, not approximated.
- **Use of a client's own data** — a client's own historical transactions may be used to generate insights shown back to that client, provided the insight is based on at least 5 comparable transactions and discloses its basis (count and period).
- **Approvals gating** — access to Restricted datasets requires data-owner plus Privacy Office sign-off (via Collibra Data Access Request, ~15 business days); new client-facing uses of client data require a Privacy Impact Assessment (~4 weeks); use of financial-crimes data outside FCC-approved purposes requires joint Privacy Office + FCC approval and is generally not granted.

See [DUS-07](../policies/dus-07.md) for the full standard and [Privacy Office & Data Governance](../teams/privacy-office-data-governance.md) for the team that operationalizes these controls day to day.

## Relationships

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: an unescaped angle bracket inside a label breaks rendering; rephrase the label. -->
```text
flowchart TB
    RG["Rachel Goldberg<br/>Chief Privacy Officer"]
    DUS07["DUS-07<br/>Data Use & Client Confidentiality Standard"]
    PODG["Privacy Office &<br/>Data Governance team"]
    EB["Ethan Brooks<br/>Data Governance Lead, Commercial Bank"]
    DGC["Data Governance Council<br/>(approver of DUS-07)"]
    DRC["Disclosure Review Committee<br/>(approves client-facing wording)"]
    FCC["Catherine Doyle<br/>Chief BSA/AML Officer / FCC"]
    LK["Laura Kim<br/>Business Data Owner, payment datasets"]

    RG -->|owns| DUS07
    RG -->|leads| PODG
    PODG -->|day-to-day contact| EB
    DUS07 -->|approved by| DGC
    DUS07 -->|cohort wording approval| DRC
    RG -->|joint approval for financial-crimes data use| FCC
    RG -->|PIA / Restricted data access approvals involve| LK
```

Key relationships:

- **Data Governance Council** approved the current version of DUS-07 (v2.1, effective 2026-01-15).
- **Ethan Brooks**, Data Governance Lead for the Commercial Bank, is the designated standard contact and the named point of contact for product/design reviews under the Privacy Office & Data Governance partner function.
- **Disclosure Review Committee (DRC)**, chaired by Patricia Moore under Legal - Treasury & Payments, must approve wording and disclaimers for any client-facing aggregated cohort statistics before they can be shown — a joint checkpoint with the Privacy Office's DUS-07 thresholds.
- **Catherine Doyle**, Chief BSA/AML Officer, is the joint approver (with the Privacy Office) when financial-crimes data is proposed for use outside its FCC-approved purpose — a use case DUS-07 states is "generally not approved."
- **Laura Kim**, Director of Payments Platform Product, is Business Data Owner for payment datasets and is the counterpart business owner whose data is subject to DUS-07's purpose-limitation and Restricted-dataset access rules.
- Payments & Treasury Technology engineering teams (e.g., Payments Hub Engineering, TDIP) engage the Privacy Office whenever they plan new client-facing uses of client data, since such uses require a Privacy Impact Assessment and may require Restricted-dataset access approval under DUS-07.

## Escalation path

Per the PTT organization directory's escalation section, compliance or policy interpretation questions are not decided by engineering teams; they route either to FCC Policy & Advisory (Jordan Ellis) or to the Privacy Office (Ethan Brooks, on Rachel Goldberg's behalf), depending on subject matter.

## Related pages

- [DUS-07 Data Use & Client Confidentiality Standard](../policies/dus-07.md)
- [Privacy Office & Data Governance](../teams/privacy-office-data-governance.md)
