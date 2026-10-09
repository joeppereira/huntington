---
type: Team
entity_id: treasury-data-analytics
title: "Treasury Data & Analytics (TDIP team)"
description: Engineering team within Payments & Treasury Technology (PTT) that owns the Treasury Data & Insights Platform (TDIP); covers its leadership, intake route and planning capacity, and the extended lead time for Restricted-classified dataset access.
tags: [team, tdip, treasury-data-analytics, ptt, data-engineering, data-governance, collibra, dar, intake, planning-factor]
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

Treasury Data & Analytics (internally abbreviated **TDA**, and commonly
referred to by the name of the platform it owns, **TDIP**) is one of the
engineering teams within Crestline National Bank's Payments & Treasury
Technology (PTT) organization, led by **Gregory Hall** (MD, CIO Payments &
Treasury Technology). The team builds and operates the
[Treasury Data & Insights Platform](../systems/treasury-data-insights-platform.md)
(system id **SYS-TDIP**), the bank's Snowflake/dbt/Feast/SageMaker analytics
platform for the Payments domain. (Source:
<!-- openwiki: broken internal link [../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md] file "../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md" does not exist. Fix the href or restore the target, then delete this comment. -->
[CNB-ORG-PTT-2026-06](../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md),
§3, §4.)

## Leadership and key contacts

| Role | Name | Notes |
|---|---|---|
| Director | [Wei Zhang](../people/wei-zhang.md) | Team leader in the PTT engineering directory |
| EM, Data Engineering | [Carlos Mendes](../people/carlos-mendes.md) | Technical owner of SYS-TDIP; owns ingestion/platform backlog (e.g. `TDA-2188`, `TDA-2210`) |
| Lead Data Scientist | Dr. [Aisha Rahman](../people/aisha-rahman.md) | Owns feature-table/data-science deliverables (e.g. `TDA-2140`) |

This reflects a two-workstream structure inside the team: Carlos Mendes leads
platform and source-ingestion engineering, while Dr. Aisha Rahman leads
feature-table and data-science delivery, both reporting to Wei Zhang. (Source:
<!-- openwiki: broken internal link [../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md] file "../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md" does not exist. Fix the href or restore the target, then delete this comment. -->
[CNB-ORG-PTT-2026-06](../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md),
§3.)

The team's business-side data owner for the payments-dataset slice of TDIP is
**Laura Kim** (Director, Payments Platform Product), reflecting PTT's general
pattern of splitting technical ownership (held by the owning engineering
team) from business/data ownership (held by the product owner who depends on
the data). Other payments-domain datasets inside TDIP carry different business
owners — for example `client_hierarchy` and `cbo_wire_events` are
business-owned by Marcus Chen, and the Restricted `dda_txn_history` dataset is
business-owned by Mark Sullivan (Deposits Data Ownership), outside PTT.
(Source:
<!-- openwiki: broken internal link [../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md] file "../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md" does not exist. Fix the href or restore the target, then delete this comment. -->
[CNB-ORG-PTT-2026-06](../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md),
<!-- openwiki: broken internal link [../sources/estate/tdip-cat-2026.2-treasury-data-and-insights-platform-data-catalog-extract.md] file "../sources/estate/tdip-cat-2026.2-treasury-data-and-insights-platform-data-catalog-extract.md" does not exist. Fix the href or restore the target, then delete this comment. -->
§3.1, §4; [TDIP-CAT-2026.2](../sources/estate/tdip-cat-2026.2-treasury-data-and-insights-platform-data-catalog-extract.md),
§2.)

## System ownership

| System ID | System | Technical owner | Business owner | Support tier |
|---|---|---|---|---|
| SYS-TDIP | Treasury Data & Insights Platform | Carlos Mendes | Laura Kim (payment data) | T2 |

T2 means business-hours support plus on-call, as opposed to the 24x7 T1 tier
held by client-facing transaction systems such as PRISM Payments Hub or CBO
Wire Center. This distinguishes TDIP's operational posture from the
systems whose data it consumes. (Source:
<!-- openwiki: broken internal link [../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md] file "../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md" does not exist. Fix the href or restore the target, then delete this comment. -->
[CNB-ORG-PTT-2026-06](../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md),
§4.)

## Engagement route, intake, and capacity

Work is requested through **Jira project `TDA`**, with `#tdip-help` as the
team's Slack channel. Dataset and feature-table *access* — as opposed to
engineering work — is requested separately through **Collibra**, the system
of record for TDIP's data-access governance (see "Restricted-dataset access
lead time" below). (Source:
<!-- openwiki: broken internal link [../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md] file "../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md" does not exist. Fix the href or restore the target, then delete this comment. -->
[CNB-ORG-PTT-2026-06](../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md),
§3, §6.)

Planning factors for sizing cross-team dependencies on TDIP, as published in
the PTT engagement directory (calibrated from the last four program
increments as of PI 27.1 planning):

| Planning factor | Intake route / lead time | Capacity note (PI 27.1) |
|---|---|---|
| 1 story point ≈ 6 engineering hours | Jira `TDA`; Collibra DAR for data access (**Restricted: +15 business days**) | ~75% committed |

A story point on TDIP work is calibrated lighter (≈6 hours) than most other
PTT engineering teams — compare Payments Hub Engineering and Payment Networks
Engineering at ≈8 hours/point — reflecting the nature of data-pipeline and
analytics work relative to vendor-platform/regression-heavy engineering.
TDIP's ~75% committed capacity for PI 27.1 (2026-12-01 to 2027-03-05, with
dependency asks due 2026-11-06) is in the middle of the PTT engineering
teams' range, below Payments Hub Engineering (~90%, driven by Nov-2026
address-enforcement and FedNow outbound work) but above CBO Platform &
Entitlements (~70%). (Source:
<!-- openwiki: broken internal link [../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md] file "../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md" does not exist. Fix the href or restore the target, then delete this comment. -->
[CNB-ORG-PTT-2026-06](../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md),
§6, §7.)

## Restricted-dataset DAR lead time

TDIP's own data catalog states the governing rule directly: access to TDIP
datasets is governed in **Collibra**, and any dataset classified
**Restricted requires Privacy Office approval under a 15-business-day SLA**.
The PTT engagement directory's planning-factor table expresses the same
control as an addition to the standard Jira `TDA` intake route: *"Jira TDA;
Collibra DAR (Restricted: +15 business days)"* — i.e., a Data Access Request
(DAR) submitted in Collibra for a Restricted-classified dataset adds 15
business days on top of whatever engineering lead time the requesting work
otherwise requires. (Source:
<!-- openwiki: broken internal link [../sources/estate/tdip-cat-2026.2-treasury-data-and-insights-platform-data-catalog-extract.md] file "../sources/estate/tdip-cat-2026.2-treasury-data-and-insights-platform-data-catalog-extract.md" does not exist. Fix the href or restore the target, then delete this comment. -->
[TDIP-CAT-2026.2](../sources/estate/tdip-cat-2026.2-treasury-data-and-insights-platform-data-catalog-extract.md),
<!-- openwiki: broken internal link [../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md] file "../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md" does not exist. Fix the href or restore the target, then delete this comment. -->
§1; [CNB-ORG-PTT-2026-06](../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md),
§6.)

As of the 2026.2 catalog, the only Restricted-classified dataset documented in
TDIP's payments-domain catalog is **`dda_txn_history`** (Restricted - Client
Confidential; sourced daily from the Core Deposit Platform, 7-year history,
owned by Mark Sullivan / Deposits Data Engineering). The
**`beneficiary_behavior_profile`** feature table is also Restricted - Client
Confidential, with its permitted purpose limited to Financial Crimes
Technology (FCT) fraud/mule-detection features, feeding model `M-FCT-0034`.
Any new consumer of either of these — or of any future dataset TDIP
classifies Restricted — must plan for the 15-business-day DAR approval as a
serial addition to normal engineering lead time, not work that can run in
parallel with it, since DAR approval in Collibra is a governance gate rather
than a Jira engineering task. (Source:
<!-- openwiki: broken internal link [../sources/estate/tdip-cat-2026.2-treasury-data-and-insights-platform-data-catalog-extract.md] file "../sources/estate/tdip-cat-2026.2-treasury-data-and-insights-platform-data-catalog-extract.md" does not exist. Fix the href or restore the target, then delete this comment. -->
[TDIP-CAT-2026.2](../sources/estate/tdip-cat-2026.2-treasury-data-and-insights-platform-data-catalog-extract.md),
§2, §3.)

This Restricted-access control sits alongside — and is distinct from — two
other governance gates that commonly apply to TDIP-sourced, client-facing
work: MRM model-inventory registration/validation under MRM-POL-02 (Tier 2
validation runs 10-14 weeks plus queue) for any new model or scored output,
and Disclosure Review Committee (DRC) approval of client-facing wording with
a 5-business-day submission lead time. Onboarding a new Insights API
analytical output specifically requires, in order: (1) MRM inventory
registration, (2) data access approval per DUS-07 (which is where the
Restricted-dataset DAR lead time applies if the underlying data is
Restricted), (3) serving-endpoint build (~13-21 points typical), and (4) DRC
approval of client-facing wording and disclaimers. (Source:
<!-- openwiki: broken internal link [../sources/estate/tdip-cat-2026.2-treasury-data-and-insights-platform-data-catalog-extract.md] file "../sources/estate/tdip-cat-2026.2-treasury-data-and-insights-platform-data-catalog-extract.md" does not exist. Fix the href or restore the target, then delete this comment. -->
[TDIP-CAT-2026.2](../sources/estate/tdip-cat-2026.2-treasury-data-and-insights-platform-data-catalog-extract.md),
<!-- openwiki: broken internal link [../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md] file "../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md" does not exist. Fix the href or restore the target, then delete this comment. -->
§4; [CNB-ORG-PTT-2026-06](../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md),
§5.)

## Escalation

As with other PTT engineering teams, dependency conflicts involving TDIP that
cannot be resolved between engineering managers escalate to Wei Zhang
(Director), and unresolved Director-level conflicts escalate further to the
weekly PTT Leadership Team (Mondays). Compliance or policy-interpretation
questions touching TDIP's data (e.g., Restricted-classification disputes)
route instead to the Privacy Office (Ethan Brooks) and are not decided by
engineering teams. (Source:
<!-- openwiki: broken internal link [../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md] file "../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md" does not exist. Fix the href or restore the target, then delete this comment. -->
[CNB-ORG-PTT-2026-06](../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md),
§8.)

## Relationships

- Owns and operates the
  [Treasury Data & Insights Platform](../systems/treasury-data-insights-platform.md)
  (SYS-TDIP), including its Payments-domain datasets, feature tables, and the
  client-facing Insights API serving layer.
- Depends on upstream source-system owners for ingestion: PRISM Payments Hub
  (Laura Kim) for `pay_wire_txn_hist`, GTSI/Payment Networks Engineering for
  `gpi_tracker_events` (via `GPI_TRACKER_SNAPSHOT`), the Core Deposit Platform
  team (Mark Sullivan) for the Restricted `dda_txn_history`, CBO Platform
  (Marcus Chen) for `client_hierarchy`, and the CBO Wire Center squad for
  `cbo_wire_events` clickstream.
- Supplies feature tables and the Insights API to downstream consumers
  including Payment Operations dashboards and Financial Crimes Technology
  fraud/mule-detection models (via `beneficiary_behavior_profile` as an input
  to model `M-FCT-0034`).
- Is approved/overseen by Ethan Brooks (Data Governance) for its published
  data catalog, and by the Privacy Office for Restricted-dataset access under
  DUS-07.
