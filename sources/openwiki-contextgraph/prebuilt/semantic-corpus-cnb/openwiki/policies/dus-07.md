---
type: Policy
entity_id: DUS-07
title: "DUS-07: Data Use and Client Confidentiality Standard"
description: "Privacy Office standard (v2.1, effective 2026-01-15) governing purpose limitation, cross-client confidentiality, and the aggregation thresholds that gate any cohort statistic or client-own-data insight shown to a client."
tags: [policy, privacy, dus-07, data-use, confidentiality, aggregation-thresholds, tdip, disclosure-review-committee, data-governance]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-6fa6253c97994be177c92ec3
    resource: repo://sources/estate/dus-07-v2.1-data-use-and-client-confidentiality-standard.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

DUS-07 ("Data Use & Client Confidentiality Standard") is the Privacy
Office's governing standard for how client data may be used, combined, and
disclosed - most importantly, what may be shown back to clients in
analytics. It is document ID **DUS-07**, version **2.1 / Approved**, owned
by Rachel Goldberg (Chief Privacy Officer) with Ethan Brooks (Data
Governance Lead, Commercial Bank) as standard contact, approved by the Data
Governance Council on 2026-01-08 and effective 2026-01-15. It is classified
**INTERNAL - CONFIDENTIAL** and lists [POL-FCC-014](pol-fcc-014.md),
MRM-POL-02, and TDIP-CAT-2026.2 as related documents.

The standard applies to both consumer and commercial clients. Consumer data
carries the additional protection of Gramm-Leach-Bliley Act privacy
provisions; commercial client data is protected contractually under the
Treasury Management Services Agreement, s14.

In practice, DUS-07 is the policy that every client-facing analytical
surface in the Payments domain - most concretely, endpoints served through
the [TDIP Insights API](../interfaces/tdip-insights-api.md) - must clear
before any statistic, pattern, or "typical value" reaches a client.

## Data classification tiers (§2)

DUS-07 defines four classification tiers that TDIP and other data catalogs
use to scope permitted use:

| Class | Examples |
|---|---|
| Public | Published rates, cutoff times |
| Internal | Aggregated operational metrics not attributable to a client |
| Confidential - Client | A client's own transactions, wire history, beneficiaries |
| Restricted - Client Confidential | Account-level activity in deposit systems; financial-crimes features; data about one client's accounts used for risk purposes |

Datasets in the Payments domain are classified against this scheme
directly: for example
[`beneficiary_behavior_profile`](../datasets/beneficiary-behavior-profile.md)
is Restricted - Client Confidential (it inherits the most restrictive tier
of its inputs), while
[`wire_corridor_stats_daily`](../datasets/wire-corridor-stats-daily.md) is
Internal because its outputs are cross-client cohort statistics with no
single-client attribution exposed.

## Purpose limitation (§3)

Data collected or derived for one purpose - for example fraud detection,
AML monitoring, or credit - must not be used for another purpose, including
product features, without Privacy Office approval and, for financial-crimes
data, FCC approval as well. **Feature tables inherit the permitted purpose
of their most restrictive input.** This is why
`beneficiary_behavior_profile`, built on top of financial-crimes-scoped
inputs and registered as the sole input to Tier 1 model `M-FCT-0034` under
MRM-POL-02, cannot be repurposed for product or client-facing use without a
new Privacy Office (and FCC) approval and a separately validated model
registration - it does not inherit any broader permission just because the
underlying raw transactions could, in principle, support other analytics.

## Cross-client confidentiality (§4)

Information about one client - including the behavior of a client's account
as a *counterparty* (for example, activity in a counterparty's account
after it receives funds) - must not be used to generate content shown to
another client. This restriction applies:

- even if the information is presented as a pattern, a typical value, or an
  insight, rather than as raw data; and
- even if the counterparty is not named.

This is the rule that rules out using beneficiary/counterparty-behavior
features (such as `bene_median_hours_to_outflow` or
`bene_outflow_ratio_24h` on `beneficiary_behavior_profile`) in any
client-facing insight shown to the counterparty's own client, since the
underlying behavior belongs to a different client's account.

## Aggregated cohort statistics shown to clients (§5)

Statistics derived from multiple clients may be displayed to a client only
when **all** of the following hold for the measurement window:

1. the cohort contains at least **500 transactions**;
2. the cohort contains at least **20 distinct originating clients**;
3. no single client contributes more than **15%** of cohort volume;
4. statistics are refreshed at least monthly; and
5. wording and disclaimer are approved by the Disclosure Review Committee.

**Cohorts failing any condition must be suppressed (not rounded or
approximated).**

All five conditions must hold simultaneously for the same measurement
window; a cohort that fails even one of the first three quantitative gates
must be suppressed outright rather than shown with a caveat, a rounded
figure, or an approximated value.

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: an unescaped angle bracket inside a label breaks rendering; rephrase the label. -->
```text
flowchart TD
    A["Candidate cohort statistic\nfor measurement window"] --> B{">= 500 transactions?"}
    B -- no --> S["Suppress cohort\n(no rounding/approximation)"]
    B -- yes --> C{">= 20 distinct\noriginating clients?"}
    C -- no --> S
    C -- yes --> D{"largest single client\n<= 15% of cohort volume?"}
    D -- no --> S
    D -- yes --> E{"refreshed\nat least monthly?"}
    E -- no --> S
    E -- yes --> F{"wording/disclaimer approved\nby Disclosure Review Committee?"}
    F -- no --> S
    F -- yes --> G["May be displayed to clients"]
```

[`wire_corridor_stats_daily`](../datasets/wire-corridor-stats-daily.md)'s
catalog sample is a worked illustration of these gates applied to real
corridor cohorts: high-volume corridors such as EUR/DE (31,200 wires, 1,140
distinct clients, 4% largest-client share) pass every quantitative gate,
while the thin NGN/NG corridor (140 wires, 11 distinct clients, 38%
largest-client share) fails both the 500-transaction and 20-distinct-client
floors outright and would have to be suppressed entirely if ever surfaced
to a client. That table is currently Internal-classified and built only for
Payment Ops dashboards, so §5 does not yet constrain it operationally - but
any proposal to reuse it for a client-facing corridor insight would have to
pass this same gate row by row.

## Use of a client's own data (§6)

A client's own historical transactions may be used to generate insights
shown to that same client - for example, the typical time for that client's
past wires to a given beneficiary to complete. **Insights must be based on
at least 5 comparable transactions and must state the basis (count and
period).** This is a materially lower bar than the multi-client cohort
thresholds in §5 precisely because the insight only ever uses the client's
own data about itself, not information about any other client or
counterparty - it is still subject to §3 purpose limitation and §4
cross-client confidentiality, but not to the 500-transaction/20-client/15%
cohort gates.

The [TDIP Insights API](../interfaces/tdip-insights-api.md)'s only
generally available endpoint, `GET
/tdip/insights/v1/cash-forecast/{clientId}` (EP-TDIP-01), is scoped to a
single `{clientId}` per request, consistent with the §6 own-data pattern;
any future wire-history or corridor-insight endpoint would need to
determine, feature by feature, whether it is computing a §6 own-data
insight (5-comparable-transaction minimum) or a §5 cross-client cohort
statistic (500/20/15% thresholds), since the two paths carry different
evidentiary and approval requirements.

## Approvals (§7)

| Activity | Approval |
|---|---|
| Access to Restricted datasets | Data owner + Privacy Office (Collibra Data Access Request; 15 business days) |
| New client-facing use of client data | Privacy Impact Assessment (~4 weeks) |
| Use of financial-crimes data outside FCC purposes | Privacy Office + FCC; generally not approved |

These approval paths compose with, rather than replace, the gating logic in
§5 and §6: obtaining Collibra access to a Restricted dataset or clearing a
Privacy Impact Assessment does not itself certify that a specific
client-facing statistic meets the §5 cohort thresholds or the §6
comparable-transaction minimum - those tests must still be applied to the
actual measurement window at serving time.

## How DUS-07 gates client-facing analytics end to end

DUS-07 does not, by itself, authorize or build any analytic; it is one of
several controls that every new client-facing insight in the Payments
domain must clear, alongside Model Risk Management (MRM-POL-02) tiering and
Disclosure Review Committee sign-off on wording. The
[TDIP Insights API](../interfaces/tdip-insights-api.md) documents this
sequencing concretely:

1. **MRM inventory registration** (MRM-POL-02) - Model or End-User Analytic
   path, determining validation requirements.
2. **Data access approvals** (DUS-07 §7) - Collibra Data Access Request,
   plus the 15-business-day SLA for Restricted datasets.
3. **Serving endpoint build** on the TDIP Insights API itself (the only
   sanctioned serving layer for client-facing analytics, per ADR-PAY-026).
4. **Disclosure Review Committee approval** of client-facing wording and
   disclaimers - the same body referenced in DUS-07 §5(5).

Within that build, DUS-07 §3-§6 are the substantive tests applied to the
specific data and statistic being proposed: purpose limitation (§3) and
cross-client confidentiality (§4) determine whether the underlying data may
be used for the proposed client-facing purpose at all; §5 or §6 determine
the evidentiary threshold the resulting statistic must clear before display.
A dataset can fail this chain even after passing MRM and DRC review -
for example, `beneficiary_behavior_profile` is permanently excluded from
client-facing use by §3/§4 (and by MRM-POL-02's Tier 1 financial-crimes
restriction) regardless of any cohort size it might otherwise satisfy.

## Related pages

- [TDIP Insights API](../interfaces/tdip-insights-api.md) - the serving
  layer where every DUS-07-gated client-facing insight must be published.
- [`beneficiary_behavior_profile` feature table](../datasets/beneficiary-behavior-profile.md) -
  a Restricted - Client Confidential table permanently barred from
  client-facing use under §3/§4.
- [`wire_corridor_stats_daily` feature table](../datasets/wire-corridor-stats-daily.md) -
  worked example applying the §5 cohort thresholds to real corridor volumes.
- [POL-FCC-014](pol-fcc-014.md) - financial-crimes-control policy referenced
  as a related document and as the additional approval required for
  purpose changes involving financial-crimes data.
