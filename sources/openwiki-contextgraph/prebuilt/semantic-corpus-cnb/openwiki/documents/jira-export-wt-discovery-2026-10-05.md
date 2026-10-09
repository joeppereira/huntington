---
type: Document
entity_id: jira-export-wt-discovery-2026-10-05
title: "JIRA-EXP-2026-10-05: Wire Center & Dependency Team Backlog Export (WT-discovery)"
description: Metadata record for a Jira Cloud export snapshot of the saved filter "WT-discovery," capturing wire-related backlog items updated since 2024-01-01 across the CBO, PPH, PNG, GTSI, FCT, ENS, and TDA Jira projects.
tags: [cbo, pph, png, gtsi, fct, ens, tda, wire-center, jira-export, backlog, document, api-lifecycle]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-4452149a3b4502b4c763a559
    resource: repo://sources/estate/jira-export-wt-discovery-2026-10-05.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Summary

**JIRA-EXP-2026-10-05** is a point-in-time export of the Jira Cloud saved filter **"WT-discovery"**
("Wire Center & Dependency Team Backlog"), scoped to wire-related issues updated since 2024-01-01
across seven Jira projects: **CBO** (Crestline Business Online), **PPH** (Payment Processing Hub),
**PNG** (Payment Networks Gateway/Engineering), **GTSI** (gpi/Swift Tracker Integration), **FCT**
(Fraud/Controls/HMS Tier?), **ENS** (Event Notification Service), and **TDA** (Treasury Data/Analytics
platform). It was exported by Marcus Chen (Product Owner, CBO Wire Center) and is used as a discovery
artifact — a consolidated cross-team snapshot of backlog items, dependencies, and risks relevant to
the Wire Center module and its upstream/downstream integrations. The export is explicitly a
**snapshot**, not a live or maintained record: issue statuses, assignees, and sprint targets reflect
the state of Jira at export time (2026-10-05 08:14 ET) and will drift from the live tracker.

## Document metadata

| Field | Value |
|---|---|
| Document ID | JIRA-EXP-2026-10-05 |
| Version / Status | export / Snapshot |
| Document owner | Exported by Marcus Chen (Product Owner, CBO Wire Center) |
| Approver(s) | n/a (export, not an approved document) |
| Effective / Last reviewed | Exported 2026-10-05 08:14 ET |
| Classification | INTERNAL - CONFIDENTIAL |
| Related documents | CBO-ARCH-WC-4.1; PPH-API-CAT-2026.3; PRSP-HMS-3.4 |
| Saved filter | "WT-discovery": projects CBO, PPH, PNG, GTSI, FCT, ENS, TDA — wire-related items updated since 2024-01-01 |

The export carries an **INTERNAL - CONFIDENTIAL** classification and the "uncontrolled when printed"
footer convention used across Crestline National Bank documentation templates, meaning the export is
a frozen artifact — it should not be treated as reflecting current issue state beyond the snapshot
timestamp.

## Structure of the export

The export has three sections:

1. **Issue list** — a flat table of 24 issues across the seven projects with key, type, summary,
   status, sprint/target, points, assignee/owner, labels, cross-links, and last-updated date.
2. **Issue details (selected)** — expanded descriptions and comment threads for a subset of issues
   judged most relevant to the Wire Center v1→v2 migration and related discovery questions.
3. **Linked records outside Jira** — two non-Jira records (a Pega complaint case and a ServiceNow
   incident) cross-referenced from the issue list.

## Thematic groupings in the issue list

The 24 issues cluster into several threads relevant to Wire Center:

- **PPH v1 → v2 migration and sunset pressure.** `PPH-2190` (epic, In Progress) tracks consumer
  migration off the PPH v1 API ahead of a **2027-03-31 sunset**, driven by the v1 adapter not being
  supported on the Volaris 9.6 platform upgrade; its comments note the Architecture Review Board
  (ARB, 2026-09-08) denied any extension beyond that date. `PPH-2190` lists three consumers: IVR
  (migrated), CRM (in progress), and `cbo-wire-bff` (**not started**). The corresponding Wire Center
  work is tracked as `CBO-4471` ("Migrate Wire Center from PPH v1 to PPH v2 APIs," Epic, 34 points,
  Backlog/unscheduled), which depends on `CBO-4473` ("CES: account-filter mapping for PPH v2 search")
  and is explicitly not yet placed in a program increment (PI 26.4 or PI 27.1 draft) as of the export
  date. See [CBO-4471: PPH v1→v2 Migration](../projects/cbo-4471-pph-v1-to-v2-migration.md) and
  [PPH-2190: v1 Sunset Migration](../projects/pph-2190-v1-sunset-migration.md) for the detailed
  write-ups of these two linked backlog items.
- **Client-facing status/label fidelity and trust.** `CBO-4402` (Done) renamed the client-facing label
  for PPH v1 status `PROCESSED` from "Processed" to "Completed" based on client feedback. `CBO-4419`
  (Bug, Open) reports a client complaint (linked to Pega case `CMP-2026-1189`) where a wire displayed
  "Completed" and was later returned/rejected by the beneficiary bank (ISO 20022 reason code `AC04`),
  after which the client had already shipped goods — this is a direct consequence of the "Completed"
  label being tied to PPH's processing state rather than confirmed network settlement, and motivates
  `PPH-2207`'s proposal (Backlog, no sponsor) to add a rail-specific settlement object
  (`fedSettlementTs` sourced from pacs.002/OMAD, `settlementStatus`) to the PPH v2 API so consumers are
  no longer limited to approximating settlement time from `stateHistory`.
- **Hold-reason transparency vs. data leakage.** `CBO-4388` (In Progress, Sprint 26.20) adds a
  client-facing tooltip populated from PPH v1's `holdReasonDesc` field, truncated at 120 characters,
  behind feature flag `WC_HOLD_TOOLTIP` (merged to `release/26.21`, targeted for production
  2026-10-22). `FCT-2004` (Risk, Open) flags that this same `holdReasonDesc` field is sourced from HMS
  hold descriptions and may contain Hold Reason Code (HRC) values and analyst free-text not meant for
  channel consumers — raised to both PPH (Sunita Rao) and CBO (Tom Becker) with remediation options of
  stopping the sync or redacting at the API gateway, still pending a decision as of the export.
  `FCT-1893` (Backlog, deprioritized 2025-Q3) is a related, separately deprioritized proposal for a
  purpose-built "client-safe" hold-status facade endpoint that would return only an approved
  disclosure tier and copy key, never raw HRC or analyst notes.
- **International (gpi) wire visibility gap.** `CBO-4480` (Spike, To Do) notes that gpi status today
  is visible only to Operations via the internal IWB tool, not to clients. `GTSI-0107` (Initiative,
  Planned) is a longer-term internal API (discovery 2027-Q2, build 2027-Q3/Q4, unfunded for 2026)
  that would expose a change-feed-based real-time gpi Tracker API; `GTSI-0112` tracks a knowledge
  transfer of the gpi Connector and Swift API gateway from PNE to GTSI; `GTSI-0115` tracks a Swift gpi
  Tracker API contract renewal (quota 250k calls/month, due 2027-01-31); and `PNG-1544` (Won't Do) — a
  proposal to increase gpi Tracker batch polling frequency — was superseded by the `GTSI-0107`
  change-feed approach.
- **Event-driven status infrastructure reuse.** `CBO-3790`/`CBO-3802`/`CBO-3815` (all Done) delivered
  the ACH Payment Tracker, its reusable `<cbo-journey-timeline>` UI component, and the Status
  Projection Service (SPS) — a Kafka-consumer-backed read model exposed via `/cbo/sps/v1`, explicitly
  designed to be extended to new payment types via a topic subscription plus a mapping module per
  type. A comment on `CBO-3815` notes that extending SPS to wires would require an ACL on
  `pay.wire.lifecycle.v2` and a mapping from v2 lifecycle state to client-facing milestones — a
  candidate reuse path for closing the Wire Center status-visibility gap without new polling.
- **Analytics/data-platform wire feeds.** `TDA-2140` (Done) delivered the
  `wire_corridor_stats_daily` feature table used by Ops dashboards; `TDA-2188` (In Progress) is
  moving `gpi_tracker_events` ingestion from nightly to hourly; `TDA-2210` (Backlog) would ingest
  `net.fedwire.ack.v1` (Fed acceptance/OMAD) into TDIP for settlement-time analytics but is blocked on
  a Kafka ACL from PNE and lacks a business sponsor.
- **Other wire-center backlog items** not otherwise detailed: `CBO-3120` (Closed/Won't Do — a "Wire
  Status Lite" polling pilot that was the direct cause of incident `INC-2024-1182`, a PPH v1
  thread-pool exhaustion during month-end, per post-incident review `PIR-2024-07`); `CBO-4302`/`CBO-4355`
  (Done — wire activity list filters and Fed reference/IMAD display); `CBO-4495` (Backlog — include
  remitter name in incoming wire notifications); `CBO-4522` (In Progress — WCAG 2.1 AA accessibility
  remediation); `PPH-2251` (Backlog — beneficiary-name search indexing); `PPH-2266` (Done — publishing
  ISO return reason from pacs.004 on `pay.wire.lifecycle.v2`); `FCT-1951` (Done — a duplicate-suspect
  client attestation pilot that updated control `CTRL-PAY-031` to allow digital attestation for
  HRC-01 holds under step-up auth, with releases over $5M still requiring Wire Room action); and
  `ENS-1120` (Planned — entity-level event subscriptions by `paymentId`/`caseId`).

## Linked records outside Jira

The export cross-references two records tracked in other systems:

| Record | System | Summary | Status |
|---|---|---|---|
| `CMP-2026-1189` | Complaints (Pega) | Client relied on a "Completed" status for an international wire later rejected (`AC04`); requests clarity on what "Completed" means | Open — regulatory complaint review pending |
| `INC-2024-1182` | ServiceNow | PPH v1 thread-pool exhaustion caused by Wire Status Lite polling at month-end | Closed — see `PIR-2024-07` |

`CMP-2026-1189` is the formal complaint record behind `CBO-4419`: a EUR 412,600 international wire
for client Halvorsen Industrial Supply showed "Completed" on 2026-09-16, was rejected by the
beneficiary bank the next day (`AC04`), and funds were returned 2026-09-21 — after the client had
already released goods based on the "Completed" status. `INC-2024-1182` is the incident that led to
the Architecture Decision Record (ADR-PAY-019) prohibiting Wire Center from polling PPH for status,
which in turn is why `CBO-3120` ("Wire Status Lite") was closed as Won't Do.

## How to use this snapshot

Because this is a frozen export rather than a live Jira view, readers should:

- Treat issue statuses, assignees, sprint targets, and comment timestamps as accurate **only as of
  2026-10-05 08:14 ET** — later changes in the live Jira instance will not be reflected here.
- Use the "Links" column and the "Issue details (selected)" section to trace cross-project
  dependencies (e.g., `CBO-4471` depending on `CBO-4473`; `TDA-2210` depending on a Kafka ACL from
  PNE) rather than relying on project boundaries alone.
- Cross-reference the two linked records outside Jira when assessing the business/regulatory impact
  of the PPH v1 status-mapping issues (`CBO-4402`, `CBO-4419`, `PPH-2207`).

## Relationship to other wiki pages

- [CBO-4471: PPH v1→v2 Migration](../projects/cbo-4471-pph-v1-to-v2-migration.md) — detailed treatment
  of the Wire Center epic to migrate `cbo-wire-bff` from PPH v1 to v2 APIs, sourced in part from this
  export.
- [PPH-2190: v1 Sunset Migration](../projects/pph-2190-v1-sunset-migration.md) — detailed treatment of
  the cross-consumer PPH v1 sunset tracking epic, sourced in part from this export.

## Source

This page is derived from the converted source document
[`jira-export-wt-discovery-2026-10-05.md`](../../sources/estate/jira-export-wt-discovery-2026-10-05.md),
itself converted from the original PDF `Jira_Export_WT-discovery_2026-10-05.pdf`.
</content>
