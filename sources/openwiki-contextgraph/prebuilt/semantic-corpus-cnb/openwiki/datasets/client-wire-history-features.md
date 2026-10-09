---
type: Dataset
entity_id: client-wire-history-features
title: "client_wire_history_features Feature Table"
description: Prototype, Confidential - Client TDIP feature table at originating-client x beneficiary grain that summarizes a client's own wire completion history (count, median and p90 release-to-ACCC, last_seen); unproductionized, unregistered in MRM, and the closest existing asset to a client-facing "typical completion time" feature.
tags: [dataset, feature-table, tdip, prototype, wire-history, completion-time, mrm, dus-07, gpi, confidential-client]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-6fa6253c97994be177c92ec3
    resource: repo://sources/estate/dus-07-v2.1-data-use-and-client-confidentiality-standard.md
  - id: openwiki-source-661f09048ce207829077c40d
    resource: repo://sources/estate/mrm-pol-02-v7.0-model-risk-management-policy-extract.md
  - id: openwiki-source-0163a9a7923ee437e942692a
    resource: repo://sources/estate/png-tdd-6.0-payment-network-gateway-fedwire-and-gpi-technical-design.md
  - id: openwiki-source-1601c697250670250350a70c
    resource: repo://sources/estate/pol-fcc-014-v3.2-customer-communication-of-payment-status-holds-and-exceptions-standard.md
  - id: openwiki-source-a8ab82acd285acae1ac9546d
    resource: repo://sources/estate/tdip-cat-2026.2-treasury-data-and-insights-platform-data-catalog-extract.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

`client_wire_history_features` is a feature table cataloged in the Treasury
Data & Insights Platform (TDIP) Payments domain, at a grain of
**originating client x beneficiary key**. It summarizes, for each client and
each beneficiary that client has paid, that pairing's historical wire volume
and completion-time behavior: a wire **count**, the **median** and **p90**
release-to-ACCC duration, and a **last_seen** timestamp.

It is classified **Confidential - Client** and explicitly marked in the
catalog as a **prototype (not productionized)**. Unlike the other two
Payments-domain feature tables, it has no entry in the Model Risk Management
inventory at all - the catalog's MRM-link column records it simply as
**"Not registered"** - and it is the dataset the catalog identifies as the
closest existing asset to a client-facing "typical completion time" feature,
without itself being usable for that purpose today. (Source:
[TDIP-CAT-2026.2](../../sources/estate/tdip-cat-2026.2-treasury-data-and-insights-platform-data-catalog-extract.md),
§3.)

## Grain, lineage, and derivation

The table is derived by joining two upstream Payments-domain sources:

- `pay_wire_txn_hist` - wire transaction history sourced hourly via CDC from
  the Payment Processing Hub (PPH), Confidential - Client classified, owned
  by Laura Kim / Carlos Mendes.
- `gpi_tracker_events` - Swift gpi Tracker status snapshots, sourced from the
  `GPI_TRACKER_SNAPSHOT` Oracle table maintained by the Payment Network
  Gateway (PNG/GPI-C), nightly at 05:00 ET (moving to hourly once TDA-2188
  completes, targeted 2026-11), with history available only from
  2025-03-01 onward.

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: an unescaped angle bracket inside a label breaks rendering; rephrase the label. -->
```text
flowchart LR
    WIRE["pay_wire_txn_hist\n(PPH via CDC, hourly,\nConfidential - Client)"]
    GPI["gpi_tracker_events\n(GPI_TRACKER_SNAPSHOT via GPI-C,\nnightly -> hourly post TDA-2188,\nsince 2025-03-01)"]
    CWH["client_wire_history_features\n(originating client x beneficiary key,\nConfidential - Client, prototype)"]
    INSIGHTS["Wire history / corridor insights\nendpoint: NOT AVAILABLE"]

    WIRE --> CWH
    GPI -->|release/status/ACCC timestamps| CWH
    CWH -.closest existing asset to.-> INSIGHTS
```

Because `GPI_TRACKER_SNAPSHOT` is populated by GPI-C through the Swift
Tracker API over SwiftNet, it only carries status and ACCC-credit timestamps
for **outbound international (Swift) wires** that were assigned a UETR -
it does not cover domestic Fedwire wires, whose acceptance/acknowledgment
events (`net.fedwire.ack.v1`) are not ingested into TDIP at all (tracked as
backlog item TDA-2210). Consequently, the release-to-ACCC completion-time
features on `client_wire_history_features` are inherently scoped to a
client's **international wire corridors**; the table cannot currently
produce a comparable completion-time statistic for that same client's
domestic Fedwire wires, because no analogous domestic settlement-event feed
exists to derive it from.

Because `gpi_tracker_events` is the less-fresh of the two inputs (nightly
until TDA-2188 lands, versus hourly CDC for `pay_wire_txn_hist`), and
because gpi history only begins 2025-03-01, both the freshness and the
historical depth of `client_wire_history_features` are bounded by the gpi
feed rather than by the wire-transaction feed, even though the latter alone
retains seven years of history.

## Feature contents

| Feature | Description |
|---|---|
| `count` | Number of historical wires from the originating client to the beneficiary key. |
| median release-to-ACCC | Median elapsed time, for that client/beneficiary pairing, between wire release and the Swift gpi ACCC event (funds confirmed credited to the beneficiary account). |
| `p90` | 90th-percentile release-to-ACCC duration for the same pairing - a tail-latency view alongside the median. |
| `last_seen` | Timestamp of the most recent wire observed for the client/beneficiary pairing. |

These are purely descriptive, backward-looking statistics computed over a
single client's own transaction history to a single beneficiary - they are
not a forecast or a probability of completion, and the catalog does not
describe any forward-looking or predictive feature on this table.

## Classification and permitted use

`client_wire_history_features` carries the **Confidential - Client**
classification, the tier [DUS-07](../policies/dus-07.md) defines as covering
"a client's own transactions, wire history, beneficiaries" - a lighter tier
than the **Restricted - Client Confidential** classification applied to
[`beneficiary_behavior_profile`](beneficiary-behavior-profile.md) (whose
inputs include account-level deposit data) but a heavier tier than the
**Internal** classification on `wire_corridor_stats_daily` (whose output is
cross-client cohort statistics with no single-client attribution).

Because its grain is **originating client x beneficiary**, every row
describes one client's own historical behavior toward one counterparty,
which is the exact scenario DUS-07 §6 addresses: "a client's own historical
transactions may be used to generate insights shown to that client (for
example the typical time for that client's past wires to a given
beneficiary to complete)," subject to a minimum of 5 comparable transactions
and disclosure of the count and period used. This is a materially easier
compliance bar than the cohort-aggregation rule in DUS-07 §5 (at least 500
transactions, 20 distinct originating clients, no client over 15% of
volume, monthly refresh, DRC-approved wording) that would apply to a
cross-client table such as `wire_corridor_stats_daily` if it were ever shown
to clients. This is why the catalog treats `client_wire_history_features`,
not the corridor table, as the closest existing asset to a client-facing
"typical completion time" feature: its grain already matches the one DUS-07
exception written for exactly that use case.

That said, DUS-07 §4's cross-client confidentiality rule still constrains
any such use: the beneficiary side of each row is a counterparty, and the
standard prohibits using information about one client's (or counterparty's)
account behavior to generate content shown to a different client, even
presented as a "typical value." Any client-facing feature built from this
table must be scoped so that only the originating client's own aggregated
view of its own payment history is shown - never, say, a beneficiary's
receiving-side statistics aggregated across multiple unrelated originating
clients.

## MRM status: unregistered, not merely "descriptive"

The TDIP catalog's MRM-link column distinguishes three states across its
three feature tables:

| Feature table | Classification | MRM link |
|---|---|---|
| `wire_corridor_stats_daily` | Internal | **None (descriptive)** - an explicit determination that no MRM registration is required |
| `beneficiary_behavior_profile` | Restricted - Client Confidential | **Input to M-FCT-0034** - registered Tier 1 financial-crimes model |
| `client_wire_history_features` | Confidential - Client | **Not registered** |

"Not registered" is a materially different status from `wire_corridor_stats_daily`'s
"None (descriptive)": the latter reflects an affirmative assessment that the
table is purely descriptive and therefore outside MRM-POL-02's scope, while
the former simply means no MRM review of any kind has happened yet for
`client_wire_history_features`. Under [MRM-POL-02](../policies/mrm-pol-02.md),
`count`, median, and percentile statistics over historical data with no
forward-looking estimation are the textbook definition of an **End-User
Analytic (EUA)** - the lightest governance category, requiring only Archer
registration and business-owner attestation (~2 weeks), by contrast with
the Tier 2 minimum (independent validation, 10-14 weeks, 160-240 validator
hours, currently a ~6-week queue) that applies to any **customer-facing
estimate** (a forward-looking value such as an expected delivery time). The
MRM inventory extract already lists a comparable EUA precedent,
`EUA-TRS-0007` (Ops corridor completion dashboard, registered 2026-05,
owner Denise Carter), showing that similarly descriptive wire-completion
statistics have been registered as EUAs elsewhere at Crestline. No such
registration exists yet for `client_wire_history_features`.

Whether `client_wire_history_features`-derived output would qualify for the
EUA path or would be reclassified as a Tier 2 customer-facing estimate
depends on exactly how any future feature is framed to the client (a
historical median versus a forward-looking "expected completion time"
claim); that framing decision, and the resulting MRM registration, has not
yet been made.

## Relationship to the Insights API

[Treasury Data & Insights Platform](../interfaces/tdip-insights-api.md)'s
Insights API serving layer is, per ADR-PAY-026, the only sanctioned path for
client-facing analytical outputs in the Payments domain - channel
backend-for-frontend layers must not compute analytics themselves, and each
insight requires MRM classification before production. The catalog's
Insights API inventory lists exactly one GA endpoint
(`GET /tdip/insights/v1/cash-forecast/{clientId}`, backed by model
M-TRS-0142) and records wire history / corridor insights as **not
available**, explicitly noting: "No endpoints exist for wire insights;
`client_wire_history_features` is a prototype."

The catalog describes the standard path to turn a prototype like this into a
production client-facing insight as four sequential steps: (1) MRM
inventory registration per MRM-POL-02, (2) data access approvals per DUS-07,
(3) serving-endpoint build (~13-21 story points typical), and (4) Disclosure
Review Committee (DRC) approval of client-facing wording and disclaimers.
None of these steps has been completed for `client_wire_history_features`;
it remains a backend feature table with no serving endpoint, no MRM
registration, and (because it has not been assessed as a new client-facing
use) no confirmed DUS-07 access approval either.

## Lifecycle status and what would have to change

As of the current catalog edition, `client_wire_history_features` is:

- **Unproductionized** - explicitly labeled a prototype, not a production
  asset, distinguishing it from the GA `wire_corridor_stats_daily` and
  `beneficiary_behavior_profile` tables.
- **Unregistered in MRM** - no EUA attestation and no model-tier
  classification exist for it, unlike its closest internal analog,
  `EUA-TRS-0007`.
- **Unserved** - no Insights API endpoint consumes it, and no channel
  surface (including Crestline Business Online) is documented as reading
  from it.
- **Scoped to Swift/gpi-tracked corridors only** - its completion-time
  features cannot currently be computed for domestic Fedwire wires, because
  `fed_ack_events` is not ingested (TDA-2210).

Any team wanting to build a genuine client-facing "typical completion time"
feature from this table's lineage would need to treat it as a new
client-facing use under DUS-07 (triggering, at minimum, the ~4-week Privacy
Impact Assessment path, since historical client-wire-history data was not
originally collected for this purpose), register the resulting output in
MRM per the EUA-vs-Tier-2 analysis above, build a versioned Insights API
endpoint per ADR-PAY-026, and obtain DRC-approved wording - all of which are
currently open rather than completed.

## Related pages

- [beneficiary_behavior_profile Feature Table](beneficiary-behavior-profile.md) - the Restricted, MRM-registered sibling feature table in the same TDIP catalog.
- [Dataset: cbo_wire_events](cbo-wire-events.md) - another Payments-domain TDIP dataset, Internal-classified, not currently a source for any feature table.
- [TDIP Insights API](../interfaces/tdip-insights-api.md) - the serving layer any production wire-history insight would need to go through.
- [DUS-07 data-access and confidentiality standard](../policies/dus-07.md) - governs the classification, aggregation-threshold, and "client's own data" rules discussed above.
- [MRM-POL-02 Model Risk Management Policy](../policies/mrm-pol-02.md) - governs the EUA-vs-Tier-2 registration path this table would need before any client-facing use.
