---
type: Team
entity_id: cbo-platform-entitlements
title: CBO Platform & Entitlements
description: Engineering team within Digital Treasury Channels Engineering that owns the CBO Status Projection Service (SPS) and the Commercial Entitlements Service (CES); engaged via Jira CBO (Platform) / #cbo-platform with a two-week triage cadence and ~70% committed capacity as of PI 27.1.
tags: [team, cbo-platform, ces, sps, entitlements, status-projection, payments, ptt, engagement, capacity-planning]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-95e454ddd82fc29fca46b0a9
    resource: repo://sources/estate/arb-pay-reg-2026q3-payments-arb-adr-register-and-minutes.md
  - id: openwiki-source-550c0e3f038aab7950cab477
    resource: repo://sources/estate/cbo-arch-wc-4.1-wire-center-current-state-architecture.md
  - id: openwiki-source-49303e801f124d97df9c3ea3
    resource: repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md
  - id: openwiki-source-4452149a3b4502b4c763a559
    resource: repo://sources/estate/jira-export-wt-discovery-2026-10-05.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

**CBO Platform & Entitlements** is one of the two engineering teams inside
**Digital Treasury Channels Engineering** at Crestline National Bank (CNB),
within Payments & Treasury Technology (PTT). Its sibling team is the
[CBO Wire Center squad](../systems/cbo-wire-center.md) (Tom Becker, EM;
Lucas Ferreira, Tech Lead; Marcus Chen, Product Owner), which owns the
client-facing Wire Center module itself. CBO Platform & Entitlements instead
owns the two shared platform systems that Wire Center (and, for SPS, other
Crestline Business Online channel surfaces) depend on: status projection and
authorization/entitlements.
<!-- openwiki: broken internal link [../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L41-L52] heading anchor "L41-L52" does not exist in "../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md". Fix the href or restore the target, then delete this comment. -->
[PTT organization, system ownership & engagement directory](../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L41-L52)

The team is led by **Nadia Haddad (Engineering Manager)**, with
**Arjun Mehta** as Tech Lead for both of the team's owned systems. Both
report into **Anjali Deshpande**, Director of Digital Treasury Channels
Engineering, who holds engineering delivery and on-call/support
accountability for CBO's channel-adjacent systems. Business/product
ownership for both of the team's systems sits with **Marcus Chen** (Director,
Digital Treasury Product; Product Owner, CBO Wire Center and Payments &
Transfers) — a deliberate separation between engineering-management and
product-ownership lines that is applied consistently across Digital Treasury
Channels Engineering.
<!-- openwiki: broken internal link [../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L28-L52] heading anchor "L28-L52" does not exist in "../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md". Fix the href or restore the target, then delete this comment. -->
[PTT organization, system ownership & engagement directory](../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L28-L52)

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: a semicolon inside a label breaks rendering; rephrase the label. -->
```text
graph TD
  AD["Anjali Deshpande<br/>Director, Digital Treasury Channels Eng."]
  NH["Nadia Haddad<br/>EM, CBO Platform &amp; Entitlements<br/>Technical owner: SYS-CES"]
  AM["Arjun Mehta<br/>Tech Lead: SPS, CES"]
  MC["Marcus Chen<br/>Director, Digital Treasury Product<br/>Business owner: SYS-CES, SYS-CBO-SPS"]
  SPS["SYS-CBO-SPS<br/>Status Projection Service (T2)"]
  CES["SYS-CES<br/>Commercial Entitlements Service (T1)"]

  AD --> NH
  NH --> AM
  MC -.->|business owner| SPS
  MC -.->|business owner| CES
  AM -->|technical owner + delivery| SPS
  AM -->|hands-on delivery| CES
  NH -->|technical owner of record| CES
```

## Systems owned

| System ID | System | Technical owner (register) | Hands-on delivery | Business owner | Support tier |
|---|---|---|---|---|---|
| SYS-CBO-SPS | [CBO Status Projection Service](../systems/cbo-status-projection-service.md) | Arjun Mehta | Arjun Mehta | Marcus Chen | T2 (business hours + on-call) |
| SYS-CES | [Commercial Entitlements Service](../systems/commercial-entitlements-service.md) | Nadia Haddad | Arjun Mehta (e.g. account-filter mapping) | Marcus Chen | T1 (24x7 critical) |

<!-- openwiki: broken internal link [../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L78-L97] heading anchor "L78-L97" does not exist in "../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md". Fix the href or restore the target, then delete this comment. -->
[PTT system ownership register](../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L78-L97)

The two systems are organizationally adjacent but functionally distinct, and
they carry different support tiers for a specific reason:

- **SPS** (`SYS-CBO-SPS`) is the Kafka-consumer-to-Postgres-read-model system
  that materializes Prism Payments Hub (PPH) payment-lifecycle events into a
  queryable status feed for Crestline Business Online channel UIs, exposed at
  `/cbo/sps/v1`. It was built under story CBO-3815 as the platform half of
  the ACH Payment Tracker epic (CBO-3790) and implements
  [ADR-PAY-019](../decisions/adr-pay-019.md) ("channel status integrations
  must be event-driven; no polling of PPH"). It is rated **T2** because, as
  configured today, an outage degrades status visibility for one feature
  (ACH tracking) rather than blocking a critical client workflow outright.
- **CES** (`SYS-CES`) is Crestline Business Online's central authorization
  and entitlements service, called synchronously by `cbo-wire-bff` via
  `GET /ces/v2/users/{id}/entitlements` to determine which accounts and
  entitlement types (e.g. `WIRE_VIEW`, `WIRE_INITIATE`, `WIRE_APPROVE`,
  `WIRE_RELEASE`, `WIRE_TEMPLATE_ADMIN`) an authenticated user holds. It is
  rated **T1 (24x7 critical)** — the same tier as the Wire Center module
  itself and PRISM Payments Hub — because a CES outage or degradation can
  block wire authorization and release bank-wide, not merely degrade a
  single feature.

For CES specifically, Haddad is the accountable technical owner named in the
system register even though day-to-day CES delivery stories (such as
account-filter mapping for the PPH v1→v2 migration, CBO-4473) are executed
by Mehta — the same business/engineering-ownership separation pattern used
one level up between Chen and Deshpande, applied here between EM and Tech
Lead on a single system.

### Cross-team dependency: CBO-4473 and the PPH v2 migration

CES is the named blocking dependency for **CBO-4471**, the epic to migrate
Wire Center off deprecated PPH v1 APIs onto PPH v2 ahead of the
2027-03-31 PPH v1 sunset. CBO-4471 is blocked on **CBO-4473**
("CES: account-filter mapping for PPH v2 search (clientId + entitled
accounts)"), an 8-point backlog story owned by Arjun Mehta that maps CES
entitlement data into the account filter PPH v2 search requires; as of the
2026-10-05 Jira export it was unscheduled in the backlog. As CES's technical
owner, Haddad is accountable for this dependency being resolved on a
timeline compatible with the v1 sunset, even though Mehta performs the
mapping work.
<!-- openwiki: broken internal link [../../sources/estate/jira-export-wt-discovery-2026-10-05.md#L37-L38] heading anchor "L37-L38" does not exist in "../../sources/estate/jira-export-wt-discovery-2026-10-05.md". Fix the href or restore the target, then delete this comment. -->
[CBO-4471 and CBO-4473](../../sources/estate/jira-export-wt-discovery-2026-10-05.md#L37-L38) ·
<!-- openwiki: broken internal link [../../sources/estate/cbo-arch-wc-4.1-wire-center-current-state-architecture.md#L137-L143] heading anchor "L137-L143" does not exist in "../../sources/estate/cbo-arch-wc-4.1-wire-center-current-state-architecture.md". Fix the href or restore the target, then delete this comment. -->
[Wire Center current-state architecture, known limitations](../../sources/estate/cbo-arch-wc-4.1-wire-center-current-state-architecture.md#L137-L143)

Separately, SPS is currently configured for ACH only: it consumes
`pay.ach.lifecycle.v1` but has no subscription to `pay.wire.lifecycle.v2` and
no wire mapping module, so Wire Center still derives status labels from
synchronous, throttled calls to the deprecated PPH v1 status API rather than
from SPS. Extending SPS to wires is a known, bounded piece of work
(a new Kafka consumer ACL plus a mapping module) rather than a redesign, and
Arjun Mehta is the named owner of that extension pattern in both the
CBO-3815 ticket history and Payments Architecture Review Board (ARB)
minutes (2026-09-08 session, "Status projection reuse").
<!-- openwiki: broken internal link [../../sources/estate/jira-export-wt-discovery-2026-10-05.md#L123-L130] heading anchor "L123-L130" does not exist in "../../sources/estate/jira-export-wt-discovery-2026-10-05.md". Fix the href or restore the target, then delete this comment. -->
[CBO-3815 ticket comment](../../sources/estate/jira-export-wt-discovery-2026-10-05.md#L123-L130) ·
<!-- openwiki: broken internal link [../../sources/estate/arb-pay-reg-2026q3-payments-arb-adr-register-and-minutes.md#L65-L68] heading anchor "L65-L68" does not exist in "../../sources/estate/arb-pay-reg-2026q3-payments-arb-adr-register-and-minutes.md". Fix the href or restore the target, then delete this comment. -->
[ARB 2026-09-08 minutes](../../sources/estate/arb-pay-reg-2026q3-payments-arb-adr-register-and-minutes.md#L65-L68)

## Engagement route

Cross-team work for either SPS or CES is raised through **Jira project
`CBO`, Platform component**, and discussed in Slack channel `#cbo-platform`.
Intake runs on a **two-week triage cadence** — teams should not route
dependency requests directly to Haddad or Mehta outside this process.
<!-- openwiki: broken internal link [../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L41-L52] heading anchor "L41-L52" does not exist in "../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md". Fix the href or restore the target, then delete this comment. -->
[PTT engineering team directory](../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L41-L52)

New client-facing integrations that touch either system (for example, a new
Wire Center consumer of SPS, or a new CES entitlement type) also need review
at the monthly **Payments Architecture Review Board (ARB)** (2nd Tuesday,
10 business days' submission lead time), since ARB governs new client-facing
integrations to payment systems bank-wide.
<!-- openwiki: broken internal link [../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L98-L104] heading anchor "L98-L104" does not exist in "../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md". Fix the href or restore the target, then delete this comment. -->
[Governance forums](../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L98-L104)

## Capacity and planning factors

As of PI 27.1 planning, CBO Platform & Entitlements uses the following
planning factor for first-pass sizing of cross-team dependency work:

| Planning factor | Intake route / lead time | Capacity note (PI 27.1) |
|---|---|---|
| 1 story point ≈ 6.5 engineering hours; velocity ≈ 30 points/sprint | Jira CBO (Platform); 2-week triage | ~70% committed |

<!-- openwiki: broken internal link [../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L120-L138] heading anchor "L120-L138" does not exist in "../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md". Fix the href or restore the target, then delete this comment. -->
[Engagement routes and planning factors](../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L120-L138)

This is notably lighter loading than the sibling CBO Wire Center squad,
which was running at ~85% committed for the same period — a relevant factor
when a requesting team is deciding whether to route a dependency ask to CBO
Platform & Entitlements versus absorbing the work elsewhere. Planning
factors are calibrated from the last four program increments (PIs) and are
refreshed quarterly by the PTT Business Management Office; the directory
entry reflects version 2026.2, published 2026-06-15, with the next refresh
due 2026-12 (Q4). Dependency asks for **PI 27.1** (2026-12-01 to
2027-03-05) were due 2026-11-06, ahead of PI planning on 2026-11-17/18.
<!-- openwiki: broken internal link [../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L120-L146] heading anchor "L120-L146" does not exist in "../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md". Fix the href or restore the target, then delete this comment. -->
[PTT organization, system ownership & engagement directory](../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L120-L146)

## Escalation

Dependency conflicts that cannot be resolved between Haddad and a peer
engineering manager (for example, the EM of the CBO Wire Center squad)
escalate first to the respective Directors — Anjali Deshpande for CBO
Platform & Entitlements — and then, if still unresolved, to the PTT
Leadership Team, which meets weekly on Mondays. Compliance or policy
interpretation questions are routed to FCC Policy & Advisory or the Privacy
Office instead and are not decided within the engineering escalation chain.
<!-- openwiki: broken internal link [../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L148-L150] heading anchor "L148-L150" does not exist in "../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md". Fix the href or restore the target, then delete this comment. -->
[Escalation](../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L148-L150)

## Related pages

- [Arjun Mehta](../people/arjun-mehta.md) — Tech Lead, SPS and CES
- [Nadia Haddad](../people/nadia-haddad.md) — Engineering Manager; technical owner of record for CES
- [CBO Status Projection Service](../systems/cbo-status-projection-service.md)
- [Commercial Entitlements Service](../systems/commercial-entitlements-service.md)
