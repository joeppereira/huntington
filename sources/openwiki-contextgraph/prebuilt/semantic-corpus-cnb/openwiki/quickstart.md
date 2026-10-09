---
type: routing-guide
title: "Quickstart: Navigating the CNB Payments Estate Wiki"
description: Routing map into the CNB payments-estate knowledge graph - what the corpus is, how entity types map to folders, and which pages answer common multi-hop estate-discovery questions.
tags: [quickstart, navigation, crestline-national-bank, payments, index]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-5c11d5768c3be60ea1158084
    resource: repo://sources/estate/cnb-memo-2026-09-realignment-of-cross-border-network-integration.md
  - id: openwiki-source-49303e801f124d97df9c3ea3
    resource: repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md
  - id: openwiki-source-3cc45df143c5eec31fe1f9f6
    resource: repo://sources/estate/pir-2024-07-wire-status-lite-pilot-inc-2024-1182-post-implementation-review.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## What this corpus is

This wiki documents the payments IT estate of Crestline National Bank (CNB),
built from 15 internal architecture, policy, org and backlog documents (see
[Overview](overview.md) for the full document list). It exists so that a
product manager's AI agent can answer estate-discovery questions before
proposing a new feature in Crestline Business Online (CBO) - especially
"what exists, what's missing, who owns it, and what are we allowed to show a
client." Start at [Overview](overview.md) for the architecture narrative;
use this page to jump directly to the right folder or page.

## Folders, by entity type

| Folder | Holds | Start here |
|---|---|---|
| [organizations/](organizations/crestline-national-bank.md) | The bank and business/engineering org units | [Crestline National Bank](organizations/crestline-national-bank.md), [Payments & Treasury Technology](organizations/payments-treasury-technology.md) |
| [systems/](systems/prism-payments-hub.md) | Named systems and services | [PRISM Payments Hub](systems/prism-payments-hub.md), [CBO Wire Center](systems/cbo-wire-center.md) |
| [interfaces/](interfaces/pph-v2-payments-api.md) | APIs, Kafka topics, batch feeds | [PPH v1 Wire Status API](interfaces/pph-v1-wire-status-api.md), [PPH v2 Payments API](interfaces/pph-v2-payments-api.md) |
| [teams/](teams/cbo-wire-center-squad.md) | Engineering teams and 2nd-line functions | [CBO Wire Center Squad](teams/cbo-wire-center-squad.md), [Financial Crimes Compliance](teams/financial-crimes-compliance.md) |
| [people/](people/marcus-chen.md) | Directors, tech leads, owners, named contacts | [Marcus Chen](people/marcus-chen.md), [Laura Kim](people/laura-kim.md) |
| [policies/](policies/pol-fcc-014.md) | Policy/standard rules | [POL-FCC-014](policies/pol-fcc-014.md), [DUS-07](policies/dus-07.md), [MRM-POL-02](policies/mrm-pol-02.md) |
| [decisions/](decisions/adr-pay-019.md) | ADRs and ARB decisions | [ADR-PAY-019](decisions/adr-pay-019.md), [ADR-PAY-021](decisions/adr-pay-021.md), [ADR-PAY-023](decisions/adr-pay-023.md) |
| [projects/](projects/cbo-3120-wire-status-lite-pilot.md) | Epics, pilots, initiatives | [CBO-3120 Wire Status Lite Pilot](projects/cbo-3120-wire-status-lite-pilot.md), [PPH-2190 v1 Sunset Migration](projects/pph-2190-v1-sunset-migration.md) |
| [incidents/](incidents/inc-2024-1182.md) | Incidents and post-implementation reviews | [INC-2024-1182](incidents/inc-2024-1182.md), [PIR-2024-07](incidents/pir-2024-07.md), [CMP-2026-1189](incidents/cmp-2026-1189.md) |
| [datasets/](datasets/pay-wire-txn-hist.md) | Catalog datasets and feature tables | [pay_wire_txn_hist](datasets/pay-wire-txn-hist.md), [GPI_TRACKER_SNAPSHOT](datasets/gpi-tracker-snapshot.md) |
| [concepts/](concepts/wire-lifecycle-state-model.md) | Domain concepts needed to read the rest | [Wire Lifecycle State Model](concepts/wire-lifecycle-state-model.md), [Hold Reason Taxonomy & Disclosure Tiers](concepts/hold-reason-taxonomy-disclosure-tiers.md) |
| [documents/](documents/cbo-arch-wc-4.1.md) | Metadata for each of the 15 source documents | [CBO-ARCH-WC-4.1](documents/cbo-arch-wc-4.1.md), [PPH-API-CAT-2026.3](documents/pph-api-cat-2026.3.md) |

## Common multi-hop questions and where to start

- **"Which systems and interfaces would a wire-tracking feature in CBO
  depend on, and what's each one's status?"** -
  [CBO Wire Center](systems/cbo-wire-center.md) ->
  [PRISM Payments Hub](systems/prism-payments-hub.md) ->
  [PPH v1 Wire Status API (deprecated)](interfaces/pph-v1-wire-status-api.md) /
  [PPH v2 Payments API](interfaces/pph-v2-payments-api.md) ->
  [Wire Lifecycle State Model](concepts/wire-lifecycle-state-model.md).

- **"What may we ever show a client about a held or screened wire, and which
  policy says so?"** -
  [POL-FCC-014](policies/pol-fcc-014.md) governs disclosure; the underlying
  codes are in
  [Hold Reason Taxonomy & Disclosure Tiers](concepts/hold-reason-taxonomy-disclosure-tiers.md),
  and [ADR-PAY-021](decisions/adr-pay-021.md) sets the confidentiality
  boundary enforced by [Hold Management Service](systems/hold-management-service.md).

- **"What was tried before for near-real-time wire status, and why did it
  fail?"** -
  [CBO-3120: Wire Status Lite Pilot](projects/cbo-3120-wire-status-lite-pilot.md) ->
  [INC-2024-1182](incidents/inc-2024-1182.md) ->
  [PIR-2024-07](incidents/pir-2024-07.md) ->
  [ADR-PAY-019](decisions/adr-pay-019.md) (the no-polling rule it produced).

- **"Who owns the Swift gpi connector today, and when/why did ownership
  change?"** -
  [Swift Alliance & gpi Connector](systems/swift-gpi-connector.md) ->
  [GTSI team](teams/gtsi.md) ->
  [CNB-MEMO-2026-09](documents/cnb-memo-2026-09.md) (effective 2026-10-01) ->
  [GTSI-0107](projects/gtsi-0107-gpi-real-time-service.md) for the roadmap
  this reorg enables.

- **"Which datasets could power a payment-timing or completion-time
  prediction, and what restricts using them client-facing?"** -
  [pay_wire_txn_hist](datasets/pay-wire-txn-hist.md) and
  [wire_corridor_stats_daily](datasets/wire-corridor-stats-daily.md) in
  [Treasury Data & Insights Platform](systems/treasury-data-insights-platform.md),
  gated by [DUS-07](policies/dus-07.md) aggregation thresholds,
  [MRM-POL-02](policies/mrm-pol-02.md) model tiering, and
  [ADR-PAY-026](decisions/adr-pay-026.md) (serve only via TDIP Insights API).

## Where to go next

- [Overview](overview.md) for the full architecture narrative and the
  estate's biggest unresolved tensions (v1 sunset, gpi real-time tracking
  gap, hold-disclosure limits).
- [Wire Lifecycle State Model](concepts/wire-lifecycle-state-model.md) and
  [Settlement, Release, and 'Completed' Semantics](concepts/settlement-release-completed-semantics.md)
  before designing any status-facing feature - they are the most load-bearing
  concepts in this estate.
