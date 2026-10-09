---
type: Person
entity_id: carlos-mendes
title: Carlos Mendes
description: Engineering Manager for Data Engineering on the Treasury Data & Insights Platform (TDIP); document owner of the TDIP data catalog and technical owner of several payments-domain datasets, including the in-progress gpi_tracker_events hourly-load migration (TDA-2188) and the blocked fed_ack_events ingestion (TDA-2210).
tags: [person, engineering-manager, tdip, data-engineering, gpi-tracker-events, fed-ack-events, jira, data-catalog]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-4452149a3b4502b4c763a559
    resource: repo://sources/estate/jira-export-wt-discovery-2026-10-05.md
  - id: openwiki-source-a8ab82acd285acae1ac9546d
    resource: repo://sources/estate/tdip-cat-2026.2-treasury-data-and-insights-platform-data-catalog-extract.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

Carlos Mendes is the Engineering Manager for Data Engineering on the Treasury Data & Insights Platform (TDIP), the Snowflake/dbt/Feast-based analytics platform used for payments-domain data products. He is co-owner (with Dr. Aisha Rahman, Lead Data Scientist) of the published TDIP data catalog document (TDIP-CAT-2026.2), and is listed as data owner/steward - jointly with Laura Kim or Marcus Chen depending on the dataset - for several of TDIP's payments-domain source tables. He also holds two active Jira stories central to TDIP's near-term roadmap: the `gpi_tracker_events` hourly-load migration (TDA-2188) and the blocked `fed_ack_events` ingestion (TDA-2210).

## Role and ownership

- **Document owner, TDIP data catalog (TDIP-CAT-2026.2).** Carlos co-owns the published catalog extract describing TDIP's payments-domain datasets, feature tables, classifications, and the Insights API serving layer, alongside Dr. Aisha Rahman. The catalog was approved by Wei Zhang (Director, Treasury Data & Analytics) and Ethan Brooks (Data Governance).
- **Data owner / steward.** Carlos is named as data owner or steward (jointly with other business/data owners) for:
  - [`pay_wire_txn_hist`](../datasets/pay-wire-txn-hist.md) (with Laura Kim) - hourly CDC feed from PPH, 7-year history, classified Confidential - Client.
  - [`gpi_tracker_events`](../datasets/gpi-tracker-events.md) (with Laura Kim) - currently nightly load from the GPI_TRACKER_SNAPSHOT source (GPI-C), moving to hourly under TDA-2188.
  - `client_hierarchy` (with Marcus Chen) - daily feed from CIF + CES.
- Carlos's role spans both the data-engineering ownership of source ingestion pipelines and co-authorship of the governance/catalog artifact that documents them, making him the primary technical point of contact for payments-domain dataset questions on TDIP.

## TDA-2188: gpi_tracker_events hourly-load migration

Carlos is the assignee and owner of **TDA-2188** ("gpi_tracker_events: move load from nightly to hourly"), a 5-point story in progress with a target of 2026-11.

- **Current state:** [`gpi_tracker_events`](../datasets/gpi-tracker-events.md) loads nightly at 05:00 ET from the `GPI_TRACKER_SNAPSHOT` source feed (owned by GTSI, formerly PNE). History begins 2025-03-01.
- **Goal:** Reduce load latency from nightly to hourly, matching the cadence of other TDIP payments feeds such as `pay_wire_txn_hist` and `cbo_wire_events`.
- **Why it matters:** The TDIP data catalog's "Known gaps" section explicitly calls out that gpi data remains nightly until TDA-2188 completes, and that this is one of only a few reasons TDIP currently has no sub-minute (or even sub-hour) freshness for wire-related data. Downstream consumers affected by this cadence include the `wire_corridor_stats_daily` feature table (TDA-2140) and the prototype `client_wire_history_features` table, both of which are derived in part from `gpi_tracker_events`.
- **Status as of 2026-09-25:** In Progress, targeted for completion alongside the 2026-11 TDIP catalog refresh cadence.

## TDA-2210: fed_ack_events ingestion (blocked)

Carlos is also the assignee and owner of **TDA-2210** ("Ingest net.fedwire.ack.v1 (Fed acceptance / OMAD) into TDIP"), an 8-point story sitting in the backlog.

- **Purpose:** Ingest the `net.fedwire.ack.v1` event stream (Fed acceptance / OMAD acknowledgements) into TDIP as the [`fed_ack_events`](../datasets/fed-ack-events.md) dataset, which does not yet exist as an ingested dataset in the TDIP catalog (listed as "NOT INGESTED").
- **Why it matters:** This ingestion is required for settlement-time analytics on domestic wires. The catalog notes that `pay_wire_txn_hist` lifecycle timestamps alone are insufficient for accurate Fed settlement time; without `fed_ack_events`, consumers (such as the PPH-2207 proposal for a `v2` rail-specific settlement object) can only approximate Fed settlement time from PPH's own processing timestamps rather than true Fed receipt/acceptance time.
- **Blocker:** The story is blocked on a Kafka ACL grant from Payment Networks Engineering (PNE) for the `net.fedwire.ack.v1` topic. As of the 2026-04-18 comment, there was also no business sponsor identified, and the story remains unscheduled in the backlog.
- **Status as of 2026-04-18:** Backlog, not scheduled; blocked on Kafka ACL from PNE.

## Relationships

- Works alongside **Dr. Aisha Rahman** (Lead Data Scientist, TDIP) as co-owner of the TDIP data catalog, and as the feature-table owner of `wire_corridor_stats_daily` (TDA-2140), which depends on datasets Carlos stewards.
- Shares dataset stewardship with **Laura Kim** (`pay_wire_txn_hist`, `gpi_tracker_events`) and **Marcus Chen** (`client_hierarchy`).
- Depends on **Payment Networks Engineering / GTSI** (notably Raj Malhotra and Omar Siddiqui's teams, which own the gpi Connector and Swift gpi Tracker API) as upstream source owners for `gpi_tracker_events`, and on PNE for the blocked Kafka ACL needed by TDA-2210.
- His team's ingestion work underpins analytics consumers across CBO Wire Center (e.g., the `wire_corridor_stats_daily` Ops dashboards) and the broader [Treasury Data & Insights Platform](../systems/treasury-data-insights-platform.md).

## Operational notes

- TDA-2188 and TDA-2210 are tracked in the `TDA` Jira project, captured in the 2026-10-05 Wire Center & Dependency Team backlog export alongside related CBO, PPH, PNG, GTSI, FCT, and ENS wire-related items.
- Both stories are cited in the TDIP data catalog's "Known gaps" section as the two active data-engineering initiatives that currently limit TDIP's payments analytics: lack of Fed acceptance timestamps (TDA-2210) and nightly-only gpi freshness (TDA-2188).
