---
type: Dataset
entity_id: wire-corridor-stats-daily
title: "wire_corridor_stats_daily Feature Table"
description: "Internal-classified TDIP feature table at currency x destination-country x day grain, built for Payment Ops dashboards, that aggregates wire counts, distinct originating clients, same-day ACCC rate and median hours to ACCC across all originating clients; its sample rows double as a worked example of DUS-07's client-facing cohort-aggregation thresholds, which thin corridors such as NGN/NG fail."
tags: [dataset, feature-table, tdip, corridor-statistics, wire-ops-dashboard, dus-07, gpi, accc, internal, mrm]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-6fa6253c97994be177c92ec3
    resource: repo://sources/estate/dus-07-v2.1-data-use-and-client-confidentiality-standard.md
  - id: openwiki-source-a8ab82acd285acae1ac9546d
    resource: repo://sources/estate/tdip-cat-2026.2-treasury-data-and-insights-platform-data-catalog-extract.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

`wire_corridor_stats_daily` is a feature table cataloged in the Treasury Data
& Insights Platform (TDIP) Payments domain (tracked as TDA-2140), at a grain
of **currency x destination country x day**. It aggregates outbound wire
activity across **all originating clients** into per-corridor daily
statistics: wire counts, distinct originating clients, a same-day ACCC
(funds confirmed credited) rate, and the median hours elapsed to ACCC. It is
classified **Internal** and is explicitly scoped by the catalog to Payment
Ops dashboards; it carries **no suppression flag**, meaning the table itself
does not withhold or mask rows for thin corridors. (Source:
<!-- openwiki: broken internal link [../sources/estate/tdip-cat-2026.2-treasury-data-and-insights-platform-data-catalog-extract.md] file "../sources/estate/tdip-cat-2026.2-treasury-data-and-insights-platform-data-catalog-extract.md" does not exist. Fix the href or restore the target, then delete this comment. -->
[TDIP-CAT-2026.2](../sources/estate/tdip-cat-2026.2-treasury-data-and-insights-platform-data-catalog-extract.md),
§3.)

Of the three Payments-domain feature tables in the catalog,
`wire_corridor_stats_daily` is the only one with an MRM link of **"None
(descriptive)"** - an affirmative determination that, unlike
`client_wire_history_features`'s "Not registered" status, it has been
assessed and found to fall outside MRM-POL-02's scope rather than simply
never reviewed.

## Grain, lineage, and derivation

The table is derived by joining two upstream Payments-domain sources, across
**all originating clients** (not scoped to a single client or beneficiary):

- `pay_wire_txn_hist` - wire transaction history sourced hourly via CDC from
  the Payment Processing Hub (PPH), Confidential - Client classified, owned
  by Laura Kim / Carlos Mendes.
- `gpi_tracker_events` - Swift gpi Tracker status snapshots, sourced from the
  `GPI_TRACKER_SNAPSHOT` Oracle table via the Payment Network Gateway
  (PNG/GPI-C), nightly at 05:00 ET (moving to hourly once TDA-2188
  completes, targeted 2026-11), with history available only from
  2025-03-01 onward.

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: an unescaped angle bracket inside a label breaks rendering; rephrase the label. -->
```text
flowchart LR
    WIRE["pay_wire_txn_hist\n(PPH via CDC, hourly,\nConfidential - Client)"]
    GPI["gpi_tracker_events\n(GPI_TRACKER_SNAPSHOT via GPI-C,\nnightly -> hourly post TDA-2188,\nsince 2025-03-01)"]
    WCS["wire_corridor_stats_daily\n(currency x destination country x day,\nInternal, no suppression flag)"]
    OPS["Payment Ops dashboards"]
    INSIGHTS["Client-facing corridor insights\nvia Insights API: NOT AVAILABLE"]

    WIRE --> WCS
    GPI -->|same-day ACCC rate,\nmedian hours to ACCC| WCS
    WCS --> OPS
    WCS -.would require DUS-07 cohort gating.-> INSIGHTS
```

*How `wire_corridor_stats_daily` is derived and consumed, and why it does not
currently reach client-facing surfaces.*

Because the ACCC-timing features depend on `gpi_tracker_events`, which is
sourced through the Swift gpi Tracker and covers **outbound international
(Swift) wires**, the corridor statistics sample below is itself drawn from
outbound Swift wires only; the table's ACCC-rate and hours-to-ACCC columns
cannot currently be produced for domestic Fedwire corridors, since Fedwire
acceptance/acknowledgment events (`net.fedwire.ack.v1`) are not ingested into
TDIP (tracked as TDA-2210). As with the other feature table built on
`gpi_tracker_events`, freshness and historical depth are bounded by the
less-fresh, shorter-history gpi feed rather than by the hourly, 7-year
`pay_wire_txn_hist` feed.

## Corridor statistics sample

The catalog's worked example (§3.1) reports a rolling 90-day window ending
2026-08-31, over outbound Swift wires, for six currency/destination-country
corridors:

| Currency / country | Wires | Distinct originating clients | Largest client share | Same-day ACCC | Median hours to ACCC |
|---|---|---|---|---|---|
| EUR / DE | 31,200 | 1,140 | 4% | 92% | 2.1 |
| GBP / GB | 18,450 | 860 | 6% | 94% | 1.6 |
| CAD / CA | 12,900 | 1,020 | 5% | 90% | 2.4 |
| MXN / MX | 2,950 | 88 | 21% | 81% | 4.9 |
| INR / IN | 1,730 | 64 | 9% | 76% | 6.2 |
| NGN / NG | 140 | 11 | 38% | 52% | 19.5 |

The six rows span roughly two orders of magnitude in volume, from the
highest-traffic EUR/DE corridor (31,200 wires, 1,140 distinct clients, a
4% largest-client share) down to the thin NGN/NG corridor (140 wires, 11
distinct clients, a 38% largest-client share). Same-day ACCC rate and median
hours to ACCC move together with corridor liquidity and volume: the
higher-volume, developed-market corridors (EUR/DE, GBP/GB, CAD/CA) complete
same-day 90%+ of the time with medians of roughly 1.6-2.4 hours, while the
thinner corridors (MXN/MX, INR/IN, and especially NGN/NG) show materially
lower same-day completion (81%, 76%, 52% respectively) and longer medians
(4.9, 6.2, and 19.5 hours respectively).

## DUS-07 cohort-aggregation gating

[DUS-07](../policies/dus-07.md) §5 permits aggregated, multi-client cohort
statistics to be shown **to clients** only when, for the measurement window,
all of the following hold simultaneously:

1. the cohort contains at least **500 transactions**;
2. the cohort contains at least **20 distinct originating clients**;
3. no single client contributes more than **15%** of cohort volume;
4. statistics are refreshed at least monthly; and
5. wording and disclaimer are approved by the Disclosure Review Committee.

A cohort failing any one of these conditions must be **suppressed**, not
rounded or approximated, if it were ever to be surfaced client-facing.

Applying these thresholds to the sample above as a purely transaction-count
and distinct-client test:

| Currency / country | Wires >= 500? | Distinct clients >= 20? | Largest share <= 15%? | Would pass DUS-07 §5 volume/client gates? |
|---|---|---|---|---|
| EUR / DE | yes (31,200) | yes (1,140) | yes (4%) | yes |
| GBP / GB | yes (18,450) | yes (860) | yes (6%) | yes |
| CAD / CA | yes (12,900) | yes (1,020) | yes (5%) | yes |
| MXN / MX | yes (2,950) | yes (88) | no (21%) | no |
| INR / IN | yes (1,730) | yes (64) | no (9% - passes this gate, but see below) | no (see note) |
| NGN / NG | **no (140)** | **no (11)** | no (38%) | no |

INR/IN passes the 500-transaction, 20-distinct-client, and 15%-largest-share
gates individually (1,730 wires, 64 clients, 9% largest share), so among the
six sample rows it is **not** disqualified by DUS-07 §5's volume/concentration
tests; MXN/MX fails solely on largest-client share (21% > 15%). **NGN/NG is
the row that fails outright on the two headline thresholds the catalog calls
out**: at 140 wires and 11 distinct originating clients, it falls short of
both the 500-transaction floor and the 20-distinct-client floor (and
separately also fails the 15% concentration gate, at 38%). Per DUS-07 §5,
the NGN/NG cohort would have to be **suppressed entirely** - not rounded,
not approximated - in any client-facing rendering of corridor statistics,
regardless of whether the other four approval conditions (monthly refresh,
DRC-approved wording) were otherwise satisfied.

This gating is presently hypothetical rather than active: `wire_corridor_stats_daily`
is classified **Internal** and built for **Payment Ops dashboards**, not for
any client-facing surface, so DUS-07 §5 does not currently constrain its
existing Ops consumption. The thresholds matter because the catalog
identifies this same sample data as the basis for any future corridor-level
client insight - the dataset most likely to be proposed as a client-facing
"typical completion time by corridor" feature - at which point every row
would need to be evaluated against DUS-07 §5 before being shown to any
client, and thin corridors like NGN/NG (and concentrated ones like MXN/MX)
would need to be suppressed rather than displayed.

## Classification and MRM status

`wire_corridor_stats_daily` carries the **Internal** classification - the
lightest tier in the TDIP catalog's scheme, reserved for "aggregated
operational metrics not attributable to a client" per DUS-07 §2. This is a
lighter tier than the **Confidential - Client** classification on
`client_wire_history_features` and the **Restricted - Client Confidential**
classification on `beneficiary_behavior_profile`, reflecting that its output
is cross-client cohort statistics with no single-client attribution exposed.
The catalog records this table with **no suppression flag**, meaning the
Internal-facing dashboard rendering does not itself apply the DUS-07 §5
cohort-suppression logic described above - that logic would need to be added
if the data (or a derivative of it) were ever repurposed for a client-facing
surface.

The catalog's MRM-link column records `wire_corridor_stats_daily` as **"None
(descriptive)"**, distinguishing it from `client_wire_history_features`
("Not registered" - never reviewed) and from `beneficiary_behavior_profile`
("Input to M-FCT-0034" - a registered Tier 1 financial-crimes model). "None
(descriptive)" reflects an affirmative determination that count, rate, and
median statistics computed over historical data, with no forward-looking
estimation, fall outside MRM-POL-02's scope entirely - consistent with the
End-User Analytic (EUA) framing the catalog applies to similarly descriptive
corridor-completion statistics elsewhere (e.g. `EUA-TRS-0007`, the Ops
corridor completion dashboard).

## Relationship to the Insights API

[Treasury Data & Insights Platform](../interfaces/tdip-insights-api.md)'s
Insights API serving layer (ADR-PAY-026) is the only sanctioned path for
client-facing analytical outputs in the Payments domain. The catalog's
Insights API inventory lists exactly one GA endpoint
(`GET /tdip/insights/v1/cash-forecast/{clientId}`) and records **wire
history / corridor insights as not available**, explicitly noting: "No
endpoints exist for wire insights; `client_wire_history_features` is a
prototype." `wire_corridor_stats_daily` is not referenced by any Insights
API endpoint today; it is consumed only by Payment Ops dashboards outside
the Insights API serving pattern.

Were a corridor-level insight ever proposed for clients, it would need to
follow the catalog's four-step onboarding path: (1) MRM inventory
registration per MRM-POL-02 - re-evaluating whether the "None (descriptive)"
determination still holds once output is client-facing rather than purely
operational; (2) data access approvals per DUS-07, including the §5
cohort-threshold evaluation worked through above; (3) a versioned serving
endpoint build (~13-21 story points typical); and (4) Disclosure Review
Committee (DRC) approval of client-facing wording and disclaimers. None of
these steps has been completed for `wire_corridor_stats_daily`.

## Related pages

- [beneficiary_behavior_profile Feature Table](beneficiary-behavior-profile.md) - the Restricted, MRM-registered sibling feature table in the same TDIP catalog.
- [client_wire_history_features Feature Table](client-wire-history-features.md) - the Confidential - Client, unregistered prototype that is the catalog's closest existing asset to a client-facing "typical completion time" feature.
- [TDIP Insights API](../interfaces/tdip-insights-api.md) - the serving layer any production corridor insight built from this table would need to go through.
- [DUS-07 data-access and confidentiality standard](../policies/dus-07.md) - defines the 500-transaction / 20-distinct-client / 15%-share cohort-aggregation gates applied above.
