---
type: Person
entity_id: marcus-chen
title: Marcus Chen
description: Director, Digital Treasury Product at Crestline National Bank; Product Owner of the CBO Wire Center and the broader Payments & Transfers product line, business/data owner of record for CBO's wire and entitlements systems, and exporter of the WT-discovery Jira backlog snapshot.
tags: [people, digital-treasury-product, cbo, wire-center, product-owner, data-owner, ptt, treasury-management-products]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-49303e801f124d97df9c3ea3
    resource: repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md
  - id: openwiki-source-4452149a3b4502b4c763a559
    resource: repo://sources/estate/jira-export-wt-discovery-2026-10-05.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

Marcus Chen is **Director, Digital Treasury Product** within Payments &
Treasury Technology (PTT) at Crestline National Bank (CNB). He is the
**Product Owner of the CBO Wire Center and the broader Payments & Transfers**
product line, the named **business owner of record** for the Wire Center
module and its supporting CBO platform systems in the PTT system ownership
register, and the data owner recorded for two Treasury Data & Insights
Platform (TDIP) datasets tied to the channel. He also personally exported the
**WT-discovery** Jira saved filter used as a cross-team discovery snapshot for
Wire Center dependency work.

## Role and reporting line

Chen reports to **Danielle Okafor** (EVP, Head of Treasury Management
Products), who holds portfolio-level, P&L business ownership of Treasury
Management (TM) products — including Crestline Business Online (CBO) — while
Chen executes day-to-day product ownership and sprint-level prioritization
beneath her. He is a peer of **Laura Kim** (Director, Payments Platform
Product; Product Owner of PRISM Payments Hub) under PTT's leadership
structure, which reports in turn to **Gregory Hall** (MD, CIO Payments &
Treasury Technology).

Chen's product-ownership role is organizationally distinct from — and
deliberately separated from — engineering delivery for the same systems.
Engineering for the Wire Center and the CBO platform sits under
**Anjali Deshpande** (Director, Digital Treasury Channels Engineering), who
leads the [CBO Wire Center squad](../teams/cbo-wire-center-squad.md) (Tom
Becker, Engineering Manager; Lucas Ferreira, Tech Lead) and CBO Platform &
Entitlements (Nadia Haddad, Engineering Manager; Arjun Mehta, Tech Lead).
Chen sets roadmap priorities and is the accountable business owner in the
system ownership register; Deshpande's organization owns technical design
authority, delivery, and on-call/support accountability.

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: a semicolon inside a label breaks rendering; rephrase the label. -->
```text
graph TD
  GH["Gregory Hall<br/>MD, CIO Payments &amp; Treasury Technology"]
  DO["Danielle Okafor<br/>EVP, Head of Treasury Management Products"]
  MC["Marcus Chen<br/>Director, Digital Treasury Product<br/>Product Owner: CBO Wire Center, Payments &amp; Transfers"]
  AD["Anjali Deshpande<br/>Director, Digital Treasury Channels Eng."]
  LK["Laura Kim<br/>Director, Payments Platform Product (peer)"]
  WC["CBO Wire Center squad<br/>Tom Becker (EM), Lucas Ferreira (Tech Lead)"]
  PE["CBO Platform &amp; Entitlements<br/>Nadia Haddad (EM), Arjun Mehta (Tech Lead)"]

  DO --> MC
  GH --> AD
  GH --> LK
  AD --> WC
  AD --> PE
  MC -.->|Product Owner /<br/>business owner| WC
  MC -.->|business owner| PE
```

## Product and business ownership

### CBO Wire Center and CBO platform systems

Per the PTT system ownership register (CNB-ORG-PTT-2026-06), Chen is the
named **business owner** for three systems operated by Digital Treasury
Channels Engineering:

| System ID | System | Owning team | Technical owner | Support tier |
|---|---|---|---|---|
| SYS-CBO | [Crestline Business Online – Wire Center module](../systems/cbo-wire-center.md) | [CBO Wire Center squad](../teams/cbo-wire-center-squad.md) | Tom Becker / Lucas Ferreira | T1 (24x7 critical) |
| SYS-CBO-SPS | CBO Status Projection Service | CBO Platform & Entitlements | Arjun Mehta | T2 |
| SYS-CES | Commercial Entitlements Service | CBO Platform & Entitlements | Nadia Haddad | T1 (24x7 critical) |

He is simultaneously the **Product Owner** the CBO Wire Center squad engages
for sprint-level prioritization and backlog decisions (Jira project `CBO`,
Slack `#cbo-wire-center`), and the business owner of record whose sign-off
stands behind these systems in governance contexts — for example, demand for
Wire Center work is sized against a planning factor of roughly 1 story point
≈ 6.5 engineering hours at ~42 points/sprint velocity, with PI 27.1 capacity
tracked at ~85% committed.

### Payments & Transfers product line

Beyond the Wire Center, Chen's product-ownership scope is recorded in CNB's
leadership directory as covering **CBO Wire Center and Payments & Transfers**
as a combined product line — i.e., his accountability is not limited to the
Wire Center module alone but extends to the broader set of CBO payment and
transfer capabilities built on top of it.

## Data ownership

Chen is recorded as data owner in the TDIP data catalog (TDIP-CAT-2026.2) for
two Payments-domain datasets:

- **[`cbo_wire_events`](../datasets/cbo-wire-events.md)** — an Internal-classified,
  hourly-refreshed clickstream dataset (13-month retention) capturing Wire
  Center portal usage events. Chen is the **sole** recorded owner/steward,
  unlike most other Payments-domain datasets, which pair a business owner
  with a TDIP data-engineering steward — consistent with his combined
  product-ownership and channel business-ownership role for the system that
  generates the events.
- **[`client_hierarchy`](../datasets/client-hierarchy.md)** — a daily-refreshed,
  Confidential - Client dataset (current plus two years of history) sourced
  from CIF and the Commercial Entitlements Service (SYS-CES, which he also
  business-owns), used as the entitlement-aware client-to-account join key
  across TDIP analytics. Here ownership is **joint** with **Carlos Mendes**
  (EM, Treasury Data Platform), the same technical-steward pairing used for
  other wire-related TDIP datasets.

## WT-discovery Jira export

Chen personally exported **JIRA-EXP-2026-10-05**, the saved Jira Cloud filter
**"WT-discovery"** (document owner: "Exported by Marcus Chen, Product Owner,
CBO Wire Center"), on **2026-10-05 08:14 ET**. The filter scopes wire-related
issues updated since 2024-01-01 across seven Jira projects — `CBO`, `PPH`,
`PNG`, `GTSI`, `FCT`, `ENS`, and `TDA` — and functions as a consolidated,
point-in-time discovery artifact for Wire Center's upstream/downstream
dependencies rather than a maintained or live record; see
[JIRA-EXP-2026-10-05](../documents/jira-export-wt-discovery-2026-10-05.md) for
the full export summary. As Product Owner of the system at the center of the
filter's scope, Chen is the natural owner of this kind of cross-team backlog
discovery work: the export spans five engineering teams he does not manage
directly, reflecting his role as the business-side integration point across
the Wire Center's dependency graph.

### Backlog items tied directly to Chen

The export records several issues where Chen appears as assignee/owner or
commenter, illustrating his direct hands-on involvement in Wire Center
product decisions rather than only portfolio-level oversight:

- **CBO-3790** ("ACH Payment Tracker" epic, 89 points, Done, released
  R25.4/2025-11) — Chen is recorded as the epic's assignee/owner. It delivered
  a timeline-and-status-notification feature for ACH payments, including the
  reusable `<cbo-journey-timeline>` component (CBO-3802) and the
  Kafka-consumer-backed Status Projection Service (CBO-3815).
- **CBO-4402** ("Map PPH v1 status `PROCESSED` to client label 'Completed'",
  Done, R26.1/2026-02) — Chen commented that clients found the legacy label
  "Processed" confusing and that "Completed" tested better in a six-client
  survey, directly motivating the label change.

### A documented tension: the "Completed" label and CBO-4419

The same "Completed" relabeling Chen sponsored in CBO-4402 is directly
implicated in a later client-facing failure recorded in the same export:
**CBO-4419** (Bug, Open) reports that an international wire displayed
"Completed" on 2026-09-16, after which the beneficiary bank rejected it
(ISO 20022 reason `AC04`) the next day; the client had already shipped goods
on the strength of the "Completed" status. This is tracked as a linked,
open regulatory complaint (`CMP-2026-1189`). The sources do not reconcile
these two issues explicitly, but read together they show that the
client-tested "Completed" label change Chen championed for clarity was tied
to PPH's internal processing state rather than confirmed network settlement
— a gap that [PPH-2207](../documents/jira-export-wt-discovery-2026-10-05.md)
(a backlogged, unsponsored proposal to add a rail-specific settlement object)
would address, but which has no committed sponsor as of the export date.

### Backlog risk and unscheduled work under his ownership

Other items in the export bear on decisions within Chen's product-ownership
scope:

- **CBO-4471** ("Migrate Wire Center from PPH v1 to PPH v2 APIs", Epic, 34
  points, Backlog/unscheduled) must complete before the PPH v1 API's
  2027-03-31 sunset (no extension per the Architecture Review Board,
  2026-09-08), but as of 2026-10-05 was not yet placed in a program
  increment and is blocked on CES account-filter mapping work (CBO-4473).
  Prioritizing this migration against feature work is a decision within
  Chen's Product Owner authority.
- **CBO-4388** (Sprint 26.20, "Show hold reason tooltip on 'Pending Review'
  wires") is an in-progress, client-requested feature — populating a tooltip
  from PPH v1's `holdReasonDesc` field — that collides with an open,
  unresolved risk in the same export: **FCT-2004** flags that
  `holdReasonDesc` can contain Hold Reason Code (HRC) values and
  financial-crimes analyst free text that must not be shown to channel
  consumers. The feature (flag `WC_HOLD_TOOLTIP`, default ON) is targeted for
  production 2026-10-22 while the remediation decision on FCT-2004 remains
  pending, placing a shipped-or-about-to-ship Wire Center feature in tension
  with an open financial-crimes data-leakage risk raised against the same
  underlying field.

## Engagement route and planning factors

Demand for CBO Wire Center squad work is raised through Jira project `CBO`
and prioritized by Chen as Product Owner (CNB-ORG-PTT-2026-06, §6). The
directory's calibrated planning factor for the squad is roughly 1 story point
≈ 6.5 engineering hours at ~42 points/sprint velocity, with PI 27.1 capacity
reported at ~85% committed — the planning baseline against which Chen must
weigh new feature asks (e.g., further wire status/trust fixes) against
committed work such as the unscheduled PPH v1→v2 migration (CBO-4471).

## Relationships

- Reports to: [Danielle Okafor](danielle-okafor.md), EVP, Head of Treasury
  Management Products.
- Peer of: [Laura Kim](laura-kim.md), Director, Payments Platform Product.
- Engineering counterpart for delivery: [Anjali Deshpande](anjali-deshpande.md),
  Director, Digital Treasury Channels Engineering — leads the
  [CBO Wire Center squad](../teams/cbo-wire-center-squad.md) and CBO Platform
  & Entitlements, the teams that build what Chen's product line prioritizes.
- Product Owner of: [CBO Wire Center](../systems/cbo-wire-center.md) (SYS-CBO)
  and the Payments & Transfers product line.
- Business owner of record for: SYS-CBO, SYS-CBO-SPS, and SYS-CES (CBO
  Platform & Entitlements systems), per CNB-ORG-PTT-2026-06.
- Data owner for: [`cbo_wire_events`](../datasets/cbo-wire-events.md) (sole
  owner) and [`client_hierarchy`](../datasets/client-hierarchy.md) (joint
  with [Carlos Mendes](carlos-mendes.md)), per TDIP-CAT-2026.2.
- Exporter of: [JIRA-EXP-2026-10-05 / "WT-discovery"](../documents/jira-export-wt-discovery-2026-10-05.md),
  a cross-project Jira snapshot covering CBO, PPH, PNG, GTSI, FCT, ENS, and
  TDA wire-related backlog items.
- Named directly in the organization directory: [CNB-ORG-PTT-2026-06](../documents/cnb-org-ptt-2026-06.md)
  (leadership table and system ownership register) and
  [Payments & Treasury Technology](../organizations/payments-treasury-technology.md)
  / [Treasury Management Products](../organizations/treasury-management-products.md)
  (organization writeups derived from it).
