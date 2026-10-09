---
type: Person
entity_id: nadia-haddad
title: Nadia Haddad
description: Engineering Manager for CBO Platform & Entitlements at Crestline National Bank; named technical owner of record for the Commercial Entitlements Service (CES), the Tier 1 authorization system behind Crestline Business Online.
tags: [people, engineering-manager, cbo-platform, ces, entitlements, payments, ptt, technical-owner]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-550c0e3f038aab7950cab477
    resource: repo://sources/estate/cbo-arch-wc-4.1-wire-center-current-state-architecture.md
  - id: openwiki-source-49303e801f124d97df9c3ea3
    resource: repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md
  - id: openwiki-source-4452149a3b4502b4c763a559
    resource: repo://sources/estate/jira-export-wt-discovery-2026-10-05.md
  - id: openwiki-source-a8ab82acd285acae1ac9546d
    resource: repo://sources/estate/tdip-cat-2026.2-treasury-data-and-insights-platform-data-catalog-extract.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

Nadia Haddad is the **Engineering Manager (EM) of CBO Platform &
Entitlements**, one of the two engineering teams within Digital Treasury
Channels Engineering at Crestline National Bank (CNB), inside Payments &
Treasury Technology (PTT). She is the named **technical owner of record** for
**SYS-CES, the Commercial Entitlements Service**, a Tier 1 (24x7 critical)
system in the PTT system ownership register.
<!-- openwiki: broken internal link [../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L82-L97] heading anchor "L82-L97" does not exist in "../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md". Fix the href or restore the target, then delete this comment. -->
[PTT organization, system ownership & engagement directory](../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L82-L97)

## Role and reporting line

Haddad reports to **Anjali Deshpande**, Director of Digital Treasury Channels
Engineering, who also leads the [CBO Wire Center squad](../teams/cbo-wire-center-squad.md)
(Tom Becker, EM; Lucas Ferreira, Tech Lead). Deshpande's organization holds
engineering delivery, technical design authority, and on-call/support
accountability for CBO's client-facing channel systems, while **Marcus
Chen** (Director, Digital Treasury Product) holds business/product ownership
and roadmap prioritization as a separate, deliberately distinct line of
accountability — Chen is recorded as the business owner for both of CBO
Platform & Entitlements' systems.
<!-- openwiki: broken internal link [../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L46] heading anchor "L46" does not exist in "../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md". Fix the href or restore the target, then delete this comment. -->
[PTT organization, system ownership & engagement directory](../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L46)

Within CBO Platform & Entitlements, Haddad's direct technical counterpart is
**Arjun Mehta**, Tech Lead for the team's two owned systems. The two systems
split technical-owner and hands-on-delivery responsibility differently:

| System ID | System | Technical owner (register) | Hands-on delivery | Business owner | Tier |
|---|---|---|---|---|---|
| SYS-CBO-SPS | CBO Status Projection Service | Arjun Mehta | Arjun Mehta | Marcus Chen | T2 |
| SYS-CES | Commercial Entitlements Service | **Nadia Haddad** | Arjun Mehta (e.g. account-filter mapping work) | Marcus Chen | T1 (24x7 critical) |

For CES specifically, Haddad is the accountable technical owner named in the
system register even though day-to-day CES delivery stories (such as
account-filter mapping) are executed by Mehta — mirroring the same
business/engineering-ownership separation pattern used one level up between
Chen and Deshpande, but applied here between EM and Tech Lead on a single
system.
<!-- openwiki: broken internal link [../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L82-L97] heading anchor "L82-L97" does not exist in "../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md". Fix the href or restore the target, then delete this comment. -->
[PTT organization, system ownership & engagement directory](../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L82-L97)

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: a semicolon inside a label breaks rendering; rephrase the label. -->
```text
graph TD
  AD["Anjali Deshpande<br/>Director, Digital Treasury Channels Eng."]
  NH["Nadia Haddad<br/>EM, CBO Platform &amp; Entitlements<br/>Technical owner: SYS-CES"]
  AM["Arjun Mehta<br/>Tech Lead: SPS, CES"]
  MC["Marcus Chen<br/>Director, Digital Treasury Product<br/>Business owner: SYS-CES, SYS-CBO-SPS"]

  AD --> NH
  NH --> AM
  MC -.->|business owner| NH
```

See [CBO Platform & Entitlements](../teams/cbo-platform-entitlements.md) for
the team's full engagement and planning-factor writeup, and
[Commercial Entitlements Service](../systems/commercial-entitlements-service.md)
for the system-level architecture of CES.

## System ownership: Commercial Entitlements Service (CES)

CES is Crestline Business Online's central authorization service. It is
called synchronously by `cbo-wire-bff` — the Wire Center backend-for-frontend
— via `GET /ces/v2/users/{id}/entitlements` (endpoint ID `EP-CES-01`) to
determine, for a given authenticated user, which accounts and entitlement
types they hold. Wire Center uses CES's response for account-level filtering
of results before returning data to the client, and relies on CES-governed
entitlement types including `WIRE_VIEW`, `WIRE_INITIATE`, `WIRE_APPROVE`,
`WIRE_RELEASE`, and `WIRE_TEMPLATE_ADMIN`.
<!-- openwiki: broken internal link [../../sources/estate/cbo-arch-wc-4.1-wire-center-current-state-architecture.md#L39-L67] heading anchor "L39-L67" does not exist in "../../sources/estate/cbo-arch-wc-4.1-wire-center-current-state-architecture.md". Fix the href or restore the target, then delete this comment. -->
[Wire Center current-state architecture, logical architecture and security sections](../../sources/estate/cbo-arch-wc-4.1-wire-center-current-state-architecture.md#L39-L67)

Because CES sits on the authorization path for every wire-related action in
Wire Center — view, initiate, approve, release, and template administration
— and carries Tier 1 (24x7 critical) support status, an outage or
degradation of CES has the potential to block client access to Wire Center
functionality bank-wide, not merely degrade a single feature. This is the
basis for CES's Tier 1 classification in the system ownership register,
distinct from the Tier 2 classification of the team's other owned system,
SPS.
<!-- openwiki: broken internal link [../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L82-L97] heading anchor "L82-L97" does not exist in "../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md". Fix the href or restore the target, then delete this comment. -->
[PTT organization, system ownership & engagement directory](../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L82-L97)

CES client hierarchy data (CIF + CES) also feeds the Treasury Data &
Insights Platform (TDIP) as a daily-refreshed, Confidential-classified
dataset, with Marcus Chen and Carlos Mendes (TDIP Director, Data
Engineering) recorded as its data owners — making CES a source system for
downstream treasury analytics in addition to its real-time authorization
role.
<!-- openwiki: broken internal link [../../sources/estate/tdip-cat-2026.2-treasury-data-and-insights-platform-data-catalog-extract.md#L36] heading anchor "L36" does not exist in "../../sources/estate/tdip-cat-2026.2-treasury-data-and-insights-platform-data-catalog-extract.md". Fix the href or restore the target, then delete this comment. -->
[TDIP data catalog extract](../../sources/estate/tdip-cat-2026.2-treasury-data-and-insights-platform-data-catalog-extract.md#L36)

### CES in the PPH v2 migration

CES is also a dependency on Wire Center's planned migration from PPH v1 to
PPH v2 APIs (epic CBO-4471, 34 points, unscheduled as of the 2026-10-05 Jira
export), which must complete before the PPH v1 sunset on 2027-03-31.
CBO-4471 is blocked on **CBO-4473**, "CES: account-filter mapping for PPH v2
search (clientId + entitled accounts)," an 8-point backlog story owned by
Arjun Mehta that maps CES entitlement data into the account filter PPH v2
search requires. As CES's technical owner, Haddad is accountable for this
dependency being resolved on a timeline compatible with the v1 sunset, even
though Mehta performs the mapping work itself.
<!-- openwiki: broken internal link [../../sources/estate/jira-export-wt-discovery-2026-10-05.md#L37-L38] heading anchor "L37-L38" does not exist in "../../sources/estate/jira-export-wt-discovery-2026-10-05.md". Fix the href or restore the target, then delete this comment. -->
[CBO-4471 and CBO-4473](../../sources/estate/jira-export-wt-discovery-2026-10-05.md#L37-L38) ·
<!-- openwiki: broken internal link [../../sources/estate/cbo-arch-wc-4.1-wire-center-current-state-architecture.md#L137] heading anchor "L137" does not exist in "../../sources/estate/cbo-arch-wc-4.1-wire-center-current-state-architecture.md". Fix the href or restore the target, then delete this comment. -->
[Wire Center current-state architecture, known limitations](../../sources/estate/cbo-arch-wc-4.1-wire-center-current-state-architecture.md#L137)

## Team capacity and engagement

CBO Platform & Entitlements is engaged through Jira project `CBO` (Platform
component) and Slack channel `#cbo-platform`, with a two-week triage cadence
for intake. The team's planning factor is roughly 1 story point ≈ 6.5
engineering hours at about 30 points per sprint, and it was running at
roughly 70% committed capacity as of PI 27.1 planning (PI 27.1: 2026-12-01 to
2027-03-05) — lighter loading than the CBO Wire Center squad's ~85%
committed, which is a relevant factor when sizing cross-team CES or SPS
dependency requests against the team.
<!-- openwiki: broken internal link [../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L124-L146] heading anchor "L124-L146" does not exist in "../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md". Fix the href or restore the target, then delete this comment. -->
[PTT organization, system ownership & engagement directory](../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L124-L146)

Dependency conflicts that cannot be resolved between Haddad and a peer
engineering manager escalate to the respective Directors (Deshpande, for
CBO Platform & Entitlements), then to the PTT Leadership Team, which meets
weekly on Mondays.
<!-- openwiki: broken internal link [../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L148-L150] heading anchor "L148-L150" does not exist in "../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md". Fix the href or restore the target, then delete this comment. -->
[PTT organization, system ownership & engagement directory](../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L148-L150)
