---
type: Person
entity_id: wei-zhang
title: Wei Zhang
description: Director, Treasury Data & Analytics at Crestline National Bank, leading the Treasury Data & Insights Platform (TDIP) team and approving the TDIP-CAT-2026.2 data catalog that governs TDIP's payments-domain datasets, feature tables, and Insights API.
tags: [person, director, tdip, treasury-data-analytics, ptt, data-governance, tdip-cat-2026.2, data-catalog]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-49303e801f124d97df9c3ea3
    resource: repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md
  - id: openwiki-source-a8ab82acd285acae1ac9546d
    resource: repo://sources/estate/tdip-cat-2026.2-treasury-data-and-insights-platform-data-catalog-extract.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

Wei Zhang is the **Director, Treasury Data & Analytics** at Crestline National
Bank, leading the engineering team that builds and operates the **Treasury
Data & Insights Platform (TDIP)** within the Payments & Treasury Technology
(PTT) organization. The team is listed in the PTT engineering directory as
"Treasury Data & Analytics (TDIP)," tracked under Jira project `TDA` and
Slack channel `#tdip-help`, with Carlos Mendes (EM, Data Engineering) and
Dr. Aisha Rahman (Lead Data Scientist) as Wei Zhang's named key contacts and
direct leads for the team's two main workstreams: platform/ingestion
engineering and data science/feature delivery, respectively.

Wei Zhang's most concrete documented responsibility is as **approver of
TDIP-CAT-2026.2**, the published Data Catalog Extract (Payments Domain) &
Insights API that is the authoritative internal record of TDIP's datasets,
feature tables, classifications, ownership, and client-facing Insights API
serving pattern.

## Role within Payments & Treasury Technology (PTT)

Wei Zhang sits among the PTT engineering team leaders reporting into the PTT
organization led by Gregory Hall (MD, CIO Payments & Treasury Technology),
alongside peers such as Marcus Chen (Director, Digital Treasury Product),
Laura Kim (Director, Payments Platform Product), Raymond Ortiz (Director,
Payments Hub Engineering), Raj Malhotra (Director, Payment Networks
Engineering), Elena Vasquez (Director, GTSI), Victor Petrov (Director,
Financial Crimes Technology), Anjali Deshpande (Director, CBO Wire Center
squad), and Sanjay Iyer (Director, Enterprise Notification Platform). Gregory
Hall's leadership scope explicitly spans "channels, payments hub, networks,
data," placing TDIP's data remit under the same executive sponsorship as the
rest of PTT engineering.

As a Director, Wei Zhang is part of the escalation path defined for PTT:
dependency conflicts that cannot be resolved between engineering managers
escalate to the respective Directors, and unresolved Director-level
conflicts escalate further to the weekly PTT Leadership Team (Mondays).

## System and data ownership

The PTT system ownership register lists **SYS-TDIP** ("Treasury Data &
Insights Platform") as owned by the TDIP team, with Carlos Mendes as
technical owner, Laura Kim as business owner for the payment-data slice, and
a **T2** support tier (business hours plus on-call). This reflects a
cross-functional ownership split typical of PTT's data systems: Wei Zhang's
team holds technical/platform accountability, while the business-side data
ownership for specific payments datasets is distributed to the product
owners who depend on them (for example, Laura Kim for payment datasets and
Marcus Chen for `client_hierarchy`).

TDIP's planning factor in the PTT engagement directory is **1 story point ≈
6 engineering hours**, the lowest per-point estimate of any PTT team, with
demand raised through **Jira TDA** and dataset access governed through
**Collibra DAR** (Data Access Request), where Restricted-classified datasets
carry an additional **15 business days** for Privacy Office approval. As of
PI 27.1 planning, TDIP capacity was tracked at roughly **75% committed**.

## Approval authority over the TDIP data catalog

Wei Zhang is named as **approver** of **TDIP-CAT-2026.2**, alongside Ethan
Brooks (Data Governance), for the catalog document owned jointly by Carlos
Mendes and Dr. Aisha Rahman. This catalog is the reference for:

- **Payments-domain datasets** on TDIP — including `pay_wire_txn_hist`,
  `gpi_tracker_events`, `client_hierarchy`, `cbo_wire_events`, and
  `dda_txn_history` — each recorded with its source system, refresh cadence,
  history depth, data-governance classification, and data owner/steward.
- **Feature tables** derived from those datasets, such as
  `wire_corridor_stats_daily`, `beneficiary_behavior_profile`, and the
  prototype `client_wire_history_features`, each tagged with a
  classification/permitted-purpose statement and, where applicable, a Model
  Risk Management (MRM) inventory link.
- The **Insights API** (ADR-PAY-026), the versioned, entitlement-checked
  serving layer through which TDIP publishes client-facing analytical
  outputs — currently a single GA endpoint,
  `GET /tdip/insights/v1/cash-forecast/{clientId}` (EP-TDIP-01) — and the
  four-step onboarding process for new insights: MRM inventory registration
  (MRM-POL-02), data access approval (DUS-07), serving endpoint build
  (~13-21 points typical), and Disclosure Review Committee (DRC) approval of
  client-facing wording.

TDIP runs on Snowflake (Enterprise, US-East) with dbt transformations, a
Feast feature store, and Amazon SageMaker for model training and batch
scoring; the catalog Wei Zhang approves governs how datasets built on that
stack are classified and who may access them, with Restricted datasets
requiring Privacy Office approval.

As approver, Wei Zhang's sign-off sits above the platform's two named
governance gaps recorded in the same catalog: `fed_ack_events` (Fed
acceptance/OMAD timestamps) is not yet ingested (TDA-2210, backlog), and
`gpi_tracker_events` remains on a nightly refresh cadence until TDA-2188
completes (targeted 2026-11) — both of which currently limit TDIP to
hourly-or-slower freshness for wire data, with no sub-minute serving
available.

## Relationships

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: an unescaped angle bracket inside a label breaks rendering; rephrase the label. -->
```text
flowchart TD
    GH["Gregory Hall<br/>MD, CIO Payments & Treasury Technology"]
    WZ["Wei Zhang<br/>Director, Treasury Data & Analytics"]
    CM["Carlos Mendes<br/>EM, Data Engineering"]
    AR["Dr. Aisha Rahman<br/>Lead Data Scientist"]
    EB["Ethan Brooks<br/>Data Governance"]
    LK["Laura Kim<br/>Director, Payments Platform Product<br/>(business owner, SYS-TDIP payment data)"]
    CAT["TDIP-CAT-2026.2<br/>data catalog & Insights API extract"]
    SYS["SYS-TDIP<br/>Treasury Data & Insights Platform"]

    GH --> WZ
    WZ --> CM
    WZ --> AR
    WZ -->|approver| CAT
    EB -->|co-approver| CAT
    CM -->|co-owner| CAT
    AR -->|co-owner| CAT
    WZ -->|technical ownership, via team| SYS
    LK -->|business owner, payment data| SYS
```

- **Carlos Mendes** — Engineering Manager for Data Engineering on TDIP,
  reporting to Wei Zhang; co-owner of TDIP-CAT-2026.2; technical owner of
  `SYS-TDIP` and several payments-domain source datasets.
- **Dr. Aisha Rahman** — Lead Data Scientist on TDIP, reporting to Wei
  Zhang; co-owner of TDIP-CAT-2026.2; data-science owner of the
  `wire_corridor_stats_daily` feature table.
- **Ethan Brooks** — Data Governance; co-approver of TDIP-CAT-2026.2
  alongside Wei Zhang, and accountable contact for Privacy Impact
  Assessment / Restricted-data approvals referenced in the catalog.
- **Laura Kim** — Director, Payments Platform Product; business owner of
  record for `SYS-TDIP`'s payment-data slice even though technical ownership
  sits with Wei Zhang's team, making the two the joint accountability points
  for payments analytics data.
- **Gregory Hall** — MD, CIO Payments & Treasury Technology; the executive
  whose scope ("channels, payments hub, networks, data") encompasses Wei
  Zhang's Treasury Data & Analytics remit, and the authority above the
  Director-level escalation tier Wei Zhang sits in.
- [Treasury Data & Analytics](../teams/treasury-data-analytics.md) — the
  team page for the organization Wei Zhang directs.

## Operational notes

- Engagement with the TDIP team for cross-team dependencies is raised
  through **Jira TDA**, with dataset access requests routed via **Collibra
  DAR** and an additional 15-business-day SLA for Restricted-classified
  data.
- TDIP-CAT-2026.2 lists **DUS-07** (Data Use & Client Confidentiality
  Standard), **MRM-POL-02** (model risk policy), **ADR-PAY-026** (Insights
  API architecture decision record), and **PNG-TDD-6.0** as related
  governance documents that bound what Wei Zhang's team can ingest, build,
  and serve.
- The PTT organization directory (CNB-ORG-PTT-2026-06) is refreshed
  quarterly; the next refresh is scheduled for 2026-12 (Q4), after which
  Wei Zhang's recorded leadership scope and team roster should be
  rechecked for changes.
