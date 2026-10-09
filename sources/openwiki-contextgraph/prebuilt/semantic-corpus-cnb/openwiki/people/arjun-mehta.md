---
type: Person
entity_id: arjun-mehta
title: Arjun Mehta
description: Tech Lead for the SPS and CES systems on the CBO Platform & Entitlements team; built the ACH Status Projection Service consumer (CBO-3815) and is the recognized source for extending status projection to wires.
tags: [people, tech-lead, cbo-platform, sps, ces, status-projection, entitlements, payments]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-4452149a3b4502b4c763a559
    resource: repo://sources/estate/jira-export-wt-discovery-2026-10-05.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Role

Arjun Mehta is the **Tech Lead for SPS and CES** on the **CBO Platform & Entitlements** team within Payments & Treasury Technology (PTT), reporting to EM Nadia Haddad. He is the named technical owner of record for two systems in the PTT system ownership register:

- **SYS-CBO-SPS** - CBO Status Projection Service (business owner: Marcus Chen; support tier T2)
- **SYS-CES** - Commercial Entitlements Service (technical owner of record is Nadia Haddad for CES overall, but Arjun does hands-on CES delivery work, e.g. account-filter mapping; business owner: Marcus Chen; support tier T1)

CBO Platform & Entitlements intake runs through Jira CBO (Platform) with a two-week triage cadence; the team's planning factor is roughly 1 story point ≈ 6.5 engineering hours at about 30 points per sprint, and it was running at roughly 70% committed capacity as of PI 27.1 planning.
[Org, system ownership, and planning factor table](../../sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md)

## Key work: ACH Status Projection Service consumer (CBO-3815)

Arjun built **CBO-3815**, the Status Projection Service (SPS) ACH lifecycle consumer, delivered in release R25.3 (21 story points, status Done). The story is a child of the ACH Payment Tracker epic (CBO-3790) and implements architecture decision **ADR-PAY-019** ("channel status integrations must be event-driven; no polling of PPH"), which was adopted after the Wire Status Lite pilot (CBO-3120) caused PPH v1 thread-pool exhaustion under polling load (INC-2024-1182).

SPS follows a simple, repeatable shape that Arjun designed to be payment-type agnostic:

```
Kafka lifecycle topic  -->  SPS consumer  -->  Postgres read model  -->  /cbo/sps/v1 API
```

For ACH, the consumer subscribes to the ACH lifecycle topic feeding CBO-3790's tracker UI and the reusable `<cbo-journey-timeline>` Aurora DS component (CBO-3802), and publishes the `TRS.ACH.STATUS_CHANGED` notification event. New payment types are intended to be added by configuration plus a dedicated mapping module, not by forking the consumer.
<!-- openwiki: broken internal link [../../sources/estate/jira-export-wt-discovery-2026-10-05.md#L28-L31] heading anchor "L28-L31" does not exist in "../../sources/estate/jira-export-wt-discovery-2026-10-05.md". Fix the href or restore the target, then delete this comment. -->
[CBO-3815 and related ACH tracker issues](../../sources/estate/jira-export-wt-discovery-2026-10-05.md#L28-L31)

See [CBO Status Projection Service](../systems/cbo-status-projection-service.md) for the system-level writeup of SPS's architecture and API.

## Guidance on extending SPS to wires

Arjun is the authoritative source, both in the CBO-3815 ticket history and in Payments Architecture Review Board (ARB) minutes, for how SPS should be extended beyond ACH:

- In a 2025-10-03 comment on CBO-3815, Arjun stated that SPS is payment-type agnostic and that adding wire support requires (a) a new Kafka topic subscription plus consumer ACL on `pay.wire.lifecycle.v2`, and (b) a new mapping module translating v2 `lifecycleState` values into client-facing milestones. This is the same extension path later recorded as a known limitation in the Wire Center current-state architecture (CBO-ARCH-WC-4.1 §7.5): "Status Projection Service (SPS, CBO-3815) is configured for ACH only; wire support requires a new mapping module and a consumer ACL on `pay.wire.lifecycle.v2`."
- At the 2026-09-08 ARB session, the board reaffirmed SPS as the **reference pattern for client-facing status of any payment type**, with Arjun named as owner of that agenda item - formalizing the Kafka-consumer/read-model/mapping-module pattern as the bank's preferred approach rather than a one-off ACH solution.

<!-- openwiki: broken internal link [../../sources/estate/jira-export-wt-discovery-2026-10-05.md#L123-L130] heading anchor "L123-L130" does not exist in "../../sources/estate/jira-export-wt-discovery-2026-10-05.md". Fix the href or restore the target, then delete this comment. -->
[CBO-3815 ticket comment](../../sources/estate/jira-export-wt-discovery-2026-10-05.md#L123-L130) ·
<!-- openwiki: broken internal link [../../sources/estate/cbo-arch-wc-4.1-wire-center-current-state-architecture.md#L143] heading anchor "L143" does not exist in "../../sources/estate/cbo-arch-wc-4.1-wire-center-current-state-architecture.md". Fix the href or restore the target, then delete this comment. -->
[Wire Center architecture, known limitation #5](../../sources/estate/cbo-arch-wc-4.1-wire-center-current-state-architecture.md#L143) ·
<!-- openwiki: broken internal link [../../sources/estate/arb-pay-reg-2026q3-payments-arb-adr-register-and-minutes.md#L65-L68] heading anchor "L65-L68" does not exist in "../../sources/estate/arb-pay-reg-2026q3-payments-arb-adr-register-and-minutes.md". Fix the href or restore the target, then delete this comment. -->
[ARB 2026-09-08 minutes, "Status projection reuse"](../../sources/estate/arb-pay-reg-2026q3-payments-arb-adr-register-and-minutes.md#L65-L68)

Because Wire Center currently calls PPH v1 synchronously for status (with throttled user-initiated refresh only, per ADR-PAY-019) and does not yet consume `pay.wire.lifecycle.v2` or run SPS for wires, any wire milestone-tracking feature (e.g., follow-on work to CBO-4480's international/gpi visibility spike) is expected to route through Arjun's extension pattern rather than through new polling or a bespoke wire-only service.

## Other current work

Arjun also owns **CBO-4473** ("CES: account-filter mapping for PPH v2 search (clientId + entitled accounts)"), an 8-point backlog story that blocks the larger **CBO-4471** epic (migrate Wire Center from PPH v1 to PPH v2 APIs, required before the PPH v1 sunset on 2027-03-31). CBO-4473 maps CES entitlement data (client ID plus the user's entitled accounts) into the account filter PPH v2 search requires, and as of the 2026-10-05 Jira export it was unscheduled in the backlog.
<!-- openwiki: broken internal link [../../sources/estate/jira-export-wt-discovery-2026-10-05.md#L37-L38] heading anchor "L37-L38" does not exist in "../../sources/estate/jira-export-wt-discovery-2026-10-05.md". Fix the href or restore the target, then delete this comment. -->
[CBO-4473 and CBO-4471](../../sources/estate/jira-export-wt-discovery-2026-10-05.md#L37-L38)

## Engagement

Arjun is reached through the CBO Platform & Entitlements team's Jira project (CBO, Platform component) and Slack channel `#cbo-platform`. Cross-team dependency requests for SPS or CES work should go through the team's two-week Jira triage rather than directly to Arjun, per the PTT engagement directory's standard intake routes.
