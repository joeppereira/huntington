# Demo answer cache - Wire Tracking Center

> **Not part of any graph.** This file sits outside `semantic-corpus-cnb/` and `context-corpus/`,
> so OpenWiki never indexes it. The backend reads it only when `DEMO_CACHE_ENABLED=true`.
>
> Each entry was recorded from a live run of the graph agent by `tools/record_demo_cache.py`:
> the answer, its sources and the full tool trace (every search / read the agent made over the
> semantic graph). When a question means the same as an entry's intent - any wording - the app
> serves the entry in seconds and labels it *Recorded*; anything else goes to the live graph agent.
>
> To change an answer, edit its `answer:` block or re-record it:
> `.venv/bin/python tools/record_demo_cache.py --only WTC-Q04`

## WTC-Q01 - Dependencies and owners

```yaml
id: WTC-Q01
title: Dependencies and owners
intent: Which existing systems, platform services and approval functions the Wire Tracking Center depends on, and
  who owns each of them today (including any recent ownership change).
example_questions:
- 'I''ve uploaded my market research and concept. Before I write the BRD: which existing systems does the Wire Tracking
  Center depend on, and who owns each today?'
- What are the dependencies for this feature and who are the owners?
- Map the systems and teams the wire tracker relies on.
- Who do I need to work with - which systems does this touch and who owns them now?
recorded_question: 'I''ve uploaded my market research and concept. Before I write the BRD: which existing systems
  does the Wire Tracking Center depend on, and who owns each today? Cover the core payment systems (payments hub,
  Fedwire and gpi connectors, hold management, notifications, the data and insights platform), the CBO platform
  services, and every partner or approval function that holds a gate (compliance, model risk, privacy, disclosure
  review, architecture, security, operations, support). Flag any owner in my concept that is out of date.'
recorded_at: '2026-10-12T05:46:54+00:00'
recorded_model: claude-sonnet-5
recorded_latency_ms: 106744
confidence: medium
answer: |-
  ## Verdict
  Wire Tracking Center sits on top of **9+ systems/services and 8 governance gates**, and the concept doc has **at least four outdated or incorrect ownership/architecture assumptions** that would block a BRD built on it as written — most critically the gpi owner, the "BFF computes insights" assumption, and the "mostly front-end, 1.5 PIs" sizing.

  ### Core payment systems & CBO platform
  | System/Interface | Owning team today | Technical/Business owner | Note |
  |---|---|---|---|
  | PRISM Payments Hub (SYS-PPH) | Payments Hub Engineering | Kevin O'Brien/Sunita Rao (tech), Laura Kim (biz) | Wire Center uses only **v1** (`/pph/v1/wires*`); v1 sunsets **2027-03-31**, no extensions (ARB 2026-09-08 minutes) |
  | Fedwire Funds Connector (SYS-PNG-FFC) | Payment Networks Engineering (PNE) | Brian Walsh/Chen Wei (tech), Laura Kim (biz) | Unchanged, stayed with PNE |
  | Swift Alliance & gpi Connector (SYS-PNG-GPI) | **GTSI**, not PNE | Elena Vasquez (Dir), Omar Siddiqui (EM), Hannah Lindqvist (TL) | Moved from PNE/Raj Malhotra on **2026-10-01** per CNB-MEMO-2026-09; batch-only (4-hr cadence), no real-time API; new requests go to Jira project **GTSI** |
  | Hold Management Service (SYS-PRSP-HMS) | Financial Crimes Technology (FCT) | Daniel Kowalski/Grace Mensah (tech), Victor Petrov (Dir) | No client-facing interface exists; FCT-1893 facade deprioritized 2025-Q3 |
  | Enterprise Notification Service (SYS-ENS) | Enterprise Notification Platform | Melissa Grant (tech), Sanjay Iyer (biz) | Only 3 of needed TRS.WIRE.* events exist; new types need ENS onboarding (6-wk SLA) + DRC |
  | Treasury Data & Insights Platform (SYS-TDIP) | Treasury Data & Analytics | Wei Zhang (Dir) | No Insights API endpoint for wire-history/corridor stats exists |
  | CBO Wire Center (SYS-CBO) / `cbo-wire-bff` | CBO Wire Center squad | Tom Becker (EM), Lucas Ferreira (TL) | Under Anjali Deshpande → Gregory Hall |
  | CES / CBO Auth / Status Projection Service | CBO Platform & Entitlements | Nadia Haddad (EM), Arjun Mehta (TL) | SPS is ACH-only today |
  | Investigations Workbench (SYS-IWB) | Payment Operations Tech | Luis Ramirez (biz) | Only internal consumer of gpi + hold detail |

  ### Approval/partner gates
  | Gate | Owner | Cadence/lead time |
  |---|---|---|
  | Architecture (ARB) | Nikhil Bose (Chair) | Monthly, 10 business days' lead; required for new client-facing payment integrations |
  | Financial Crimes Compliance (POL-FCC-014) | Catherine Doyle / Jordan Ellis | FCT Change Advisory bi-weekly, 5 days lead |
  | Model Risk Management (MRM-POL-02) | Jonathan Price / Sophie Laurent | Tier 2 customer-facing estimate: ~6-wk queue + 10-14 wks validation |
  | Privacy Office (DUS-07) | Rachel Goldberg | PIA ~4 weeks (OneTrust) |
  | Disclosure Review Committee (Legal) | Patricia Moore | Bi-weekly Thursdays, 5 days lead |
  | InfoSec (SEC-STD-22) | Farah Ali | 24-40 hrs, 3-week SLA |
  | Payment Operations readiness | Denise Carter | Ops Readiness Review, 4 weeks pre go-live |
  | Commercial Service Center | Kim Nguyen | Readiness checklist, 3 weeks pre go-live |

  ### Flags against your concept
  1. **FC-01/FC-02 gpi owner wrong**: concept says "Raj Malhotra/PNE, spike CBO-4480." gpi ownership moved to **GTSI** on 2026-10-01; CBO-4480 is an unscheduled CBO Wire Center discovery spike (owner Lucas Ferreira), not a PNE deliverable, and gpi has no real-time API — only a 4-hr batch (`GTSI-0107` real-time service not funded for 2026).
  2. **FC-04 insights-in-BFF is prohibited**: ADR-PAY-026 (2026-05-12) requires all client-facing predictions/statistics be computed in TDIP and served via the TDIP Insights API; no such endpoint exists for wire history today, and any new one needs MRM Tier-2 classification.
  3. **FC-03 "exact reason" + Confirm/Reject on all holds** conflicts with HMS controls: tier G/R holds (majority of volume) must show only an identical generic "being reviewed" message (`CTRL-PAY-040`); only HRC-01 supports digital self-service (`CTRL-PAY-031`, <$5M).
  4. **"Settled" ≡ CBO "Completed"** is the same conflation behind incident CMP-2026-1189 (wire shown Completed, then returned); PPH v1 `PROCESSED` doesn't mean settlement.
  5. **"Mostly front-end, 1.5 PIs"** ignores the PPH v1→v2 migration (CBO-4471, unscheduled), new ENS event types, TDIP build + MRM validation, and the gate lead times above (ARB, MRM, Privacy, Legal, InfoSec, Ops, TSC) — these alone push well past 1.5 PIs and likely past the Feb 2027 pilot date.
sources:
- ref: openwiki/systems/swift-gpi-connector.md
  why: Confirms gpi connector ownership moved to GTSI and batch-only architecture
- ref: openwiki/systems/cbo-wire-center.md
  why: CBO Wire Center squad ownership and CBO-4480/CBO-4471 spike details
- ref: openwiki/interfaces/ens-notification-api-trs-catalog.md
  why: ENS event catalog showing only 3 existing TRS.WIRE.* events and onboarding SLA
- ref: openwiki/decisions/adr-pay-026.md
  why: Architecture decision requiring insights computed in TDIP, not BFF
- ref: openwiki/systems/hold-management-service.md
  why: HMS ownership and hold tier/control constraints (CTRL-PAY-040, CTRL-PAY-031)
- ref: openwiki/teams/model-risk-management.md
  why: MRM gate ownership and Tier 2 validation timelines
- ref: openwiki/teams/payment-operations.md
  why: Payment Operations readiness gate owner and lead time
- ref: openwiki/teams/commercial-service-center.md
  why: Commercial Service Center readiness gate owner and lead time
- ref: openwiki/teams/legal-treasury-payments.md
  why: Disclosure Review Committee ownership and cadence
- ref: openwiki/teams/payments-arb-enterprise-architecture.md
  why: ARB gate ownership, cadence, and PPH v1 sunset decision
follow_up_questions:
- Should the BRD scope include the PPH v1→v2 migration (CBO-4471) as a prerequisite or dependency?
- Do you want a revised, realistic sizing/timeline estimate that accounts for the MRM, ARB, and ENS gate lead times?
- Should hold status messaging in the BRD be redesigned around the tiered generic-message control (CTRL-PAY-040)
  instead of exact-reason display?
reasoning_summary: Formatted the provided CNB Q&A agent answer into the structured schema, preserving the text verbatim
  and mapping the "Refs the agent read" list into the sources field with brief rationale for each.
trace:
  input_tokens: 193845
  output_tokens: 11105
  steps:
  - step: 1
    tool: semantic_search
    input: '"Payments Hub system owner"'
    result: '8 hits: openwiki/teams/payments-hub-engineering.md, openwiki/people/laura-kim.md, openwiki/people/kevin-obrien.md'
    ms: 784
    refs:
    - semantic:openwiki/teams/payments-hub-engineering.md
    - semantic:openwiki/people/laura-kim.md
    - semantic:openwiki/people/kevin-obrien.md
    - semantic:openwiki/people/sunita-rao.md
    - semantic:openwiki/people/raymond-ortiz.md
    - semantic:openwiki/organizations/payments-treasury-technology.md
    - semantic:openwiki/people/sanjay-iyer.md
    - semantic:openwiki/systems/core-deposit-platform.md
  - step: 2
    tool: semantic_search
    input: '"Wire Center CBO platform"'
    result: '8 hits: openwiki/people/anjali-deshpande.md, openwiki/teams/cbo-wire-center-squad.md, openwiki/teams/cbo-platform-entitlements.md'
    ms: 784
    refs:
    - semantic:openwiki/people/anjali-deshpande.md
    - semantic:openwiki/teams/cbo-wire-center-squad.md
    - semantic:openwiki/teams/cbo-platform-entitlements.md
    - semantic:openwiki/projects/cbo-3790-ach-payment-tracker.md
    - semantic:openwiki/people/tom-becker.md
    - semantic:openwiki/people/lucas-ferreira.md
    - semantic:openwiki/systems/commercial-entitlements-service.md
    - semantic:openwiki/organizations/digital-treasury-channels.md
  - step: 3
    tool: semantic_search
    input: '"Fedwire connector interface owner"'
    result: '8 hits: openwiki/people/raj-malhotra.md, openwiki/interfaces/fedwire-network-ack-topics.md, openwiki/teams/payment-networks-engineering.md'
    ms: 784
    refs:
    - semantic:openwiki/people/raj-malhotra.md
    - semantic:openwiki/interfaces/fedwire-network-ack-topics.md
    - semantic:openwiki/teams/payment-networks-engineering.md
    - semantic:openwiki/people/brian-walsh.md
    - semantic:openwiki/systems/fedwire-funds-connector.md
    - semantic:openwiki/systems/swift-gpi-connector.md
    - semantic:openwiki/interfaces/gpi-tracker-batch-feed.md
    - semantic:openwiki/people/chen-wei.md
  - step: 4
    tool: semantic_search
    input: '"Swift gpi connector interface"'
    result: '8 hits: openwiki/datasets/gpi-tracker-snapshot.md, openwiki/systems/swift-gpi-connector.md, openwiki/decisions/png-1544.md'
    ms: 784
    refs:
    - semantic:openwiki/datasets/gpi-tracker-snapshot.md
    - semantic:openwiki/systems/swift-gpi-connector.md
    - semantic:openwiki/decisions/png-1544.md
    - semantic:openwiki/systems/investigations-workbench.md
    - semantic:openwiki/interfaces/gpi-tracker-batch-feed.md
    - semantic:openwiki/teams/payment-networks-engineering.md
    - semantic:openwiki/teams/gtsi.md
    - semantic:openwiki/projects/gtsi-0112-gpi-knowledge-transfer.md
  - step: 5
    tool: semantic_search
    input: '"wire hold management system"'
    result: '8 hits: openwiki/systems/hold-management-service.md, openwiki/people/grace-mensah.md, openwiki/teams/payment-operations.md'
    ms: 784
    refs:
    - semantic:openwiki/systems/hold-management-service.md
    - semantic:openwiki/people/grace-mensah.md
    - semantic:openwiki/teams/payment-operations.md
    - semantic:openwiki/systems/prism-payments-hub.md
    - semantic:openwiki/teams/financial-crimes-compliance.md
    - semantic:openwiki/interfaces/hms-hold-api.md
    - semantic:openwiki/systems/sentinel-fraud-scoring.md
    - semantic:openwiki/systems/sanctionscreen.md
  - step: 6
    tool: semantic_search
    input: '"ENS notifications event system owner"'
    result: '8 hits: openwiki/people/sanjay-iyer.md, openwiki/people/melissa-grant.md, openwiki/teams/enterprise-notification-platform.md'
    ms: 784
    refs:
    - semantic:openwiki/people/sanjay-iyer.md
    - semantic:openwiki/people/melissa-grant.md
    - semantic:openwiki/teams/enterprise-notification-platform.md
    - semantic:openwiki/systems/cbo-wire-center.md
    - semantic:openwiki/interfaces/sps-read-model-api.md
    - semantic:openwiki/projects/cbo-3790-ach-payment-tracker.md
    - semantic:openwiki/projects/ens-1120-entity-level-subscriptions.md
    - semantic:openwiki/systems/enterprise-notification-service.md
  - step: 7
    tool: semantic_search
    input: '"data and insights platform payments analytics"'
    result: '8 hits: openwiki/people/wei-zhang.md, openwiki/systems/treasury-data-insights-platform.md, openwiki/teams/treasury-data-analytics.md'
    ms: 1432
    refs:
    - semantic:openwiki/people/wei-zhang.md
    - semantic:openwiki/systems/treasury-data-insights-platform.md
    - semantic:openwiki/teams/treasury-data-analytics.md
    - semantic:openwiki/interfaces/tdip-insights-api.md
    - semantic:openwiki/people/aisha-rahman.md
    - semantic:openwiki/decisions/adr-pay-026.md
    - semantic:openwiki/systems/core-deposit-platform.md
    - semantic:openwiki/policies/dus-07.md
  - step: 8
    tool: semantic_search
    input: '"model risk governance approval predictive insights"'
    result: '8 hits: openwiki/policies/mrm-pol-02.md, openwiki/systems/sentinel-fraud-scoring.md, openwiki/decisions/adr-pay-026.md'
    ms: 1432
    refs:
    - semantic:openwiki/policies/mrm-pol-02.md
    - semantic:openwiki/systems/sentinel-fraud-scoring.md
    - semantic:openwiki/decisions/adr-pay-026.md
    - semantic:openwiki/teams/model-risk-management.md
    - semantic:openwiki/systems/treasury-data-insights-platform.md
    - semantic:openwiki/people/jonathan-price.md
    - semantic:openwiki/interfaces/tdip-insights-api.md
    - semantic:openwiki/people/denise-carter.md
  - step: 9
    tool: semantic_search
    input: '"privacy review approval gate wire sharing"'
    result: '8 hits: openwiki/teams/information-security-digital-channels.md, openwiki/policies/sec-std-22.md, openwiki/policies/dus-07.md'
    ms: 1432
    refs:
    - semantic:openwiki/teams/information-security-digital-channels.md
    - semantic:openwiki/policies/sec-std-22.md
    - semantic:openwiki/policies/dus-07.md
    - semantic:openwiki/teams/payment-operations.md
    - semantic:openwiki/teams/commercial-service-center.md
    - semantic:openwiki/systems/enterprise-notification-service.md
    - semantic:openwiki/incidents/pir-2024-07.md
    - semantic:openwiki/documents/pir-2024-07.md
  - step: 10
    tool: semantic_search
    input: '"disclosure review compliance gate wire"'
    result: '8 hits: openwiki/teams/legal-treasury-payments.md, openwiki/teams/financial-crimes-compliance.md, openwiki/teams/payment-operations.md'
    ms: 1432
    refs:
    - semantic:openwiki/teams/legal-treasury-payments.md
    - semantic:openwiki/teams/financial-crimes-compliance.md
    - semantic:openwiki/teams/payment-operations.md
    - semantic:openwiki/policies/pol-fcc-014.md
    - semantic:openwiki/teams/commercial-service-center.md
    - semantic:openwiki/people/jordan-ellis.md
    - semantic:openwiki/concepts/settlement-release-completed-semantics.md
    - semantic:openwiki/people/andrew-feldman.md
  - step: 11
    tool: semantic_search
    input: '"architecture review board approval gate CBO"'
    result: '8 hits: openwiki/documents/pir-2024-07.md, openwiki/incidents/pir-2024-07.md, openwiki/people/lucas-ferreira.md'
    ms: 1432
    refs:
    - semantic:openwiki/documents/pir-2024-07.md
    - semantic:openwiki/incidents/pir-2024-07.md
    - semantic:openwiki/people/lucas-ferreira.md
    - semantic:openwiki/systems/cbo-wire-center.md
    - semantic:openwiki/people/nikhil-bose.md
    - semantic:openwiki/teams/information-security-digital-channels.md
    - semantic:openwiki/organizations/digital-treasury-channels.md
    - semantic:openwiki/organizations/payments-treasury-technology.md
  - step: 12
    tool: semantic_search
    input: '"security review gate wire tracking link external"'
    result: '8 hits: openwiki/teams/information-security-digital-channels.md, openwiki/policies/sec-std-22.md, openwiki/projects/pph-2190-v1-sunset-migration.md'
    ms: 1432
    refs:
    - semantic:openwiki/teams/information-security-digital-channels.md
    - semantic:openwiki/policies/sec-std-22.md
    - semantic:openwiki/projects/pph-2190-v1-sunset-migration.md
    - semantic:openwiki/interfaces/cbo-auth-step-up-api.md
    - semantic:openwiki/people/farah-ali.md
    - semantic:openwiki/teams/commercial-service-center.md
    - semantic:openwiki/teams/payment-operations.md
    - semantic:openwiki/incidents/pir-2024-07.md
  - step: 13
    tool: semantic_read
    input: openwiki/systems/swift-gpi-connector.md []
    result: 9 sections, 11556 chars
    ms: 1
    refs:
    - semantic:openwiki/systems/swift-gpi-connector.md
  - step: 14
    tool: semantic_read
    input: openwiki/systems/cbo-wire-center.md []
    result: 12 sections, 12317 chars
    ms: 1
    refs:
    - semantic:openwiki/systems/cbo-wire-center.md
  - step: 15
    tool: semantic_read
    input: openwiki/interfaces/ens-notification-api-trs-catalog.md []
    result: 9 sections, 8424 chars
    ms: 1
    refs:
    - semantic:openwiki/interfaces/ens-notification-api-trs-catalog.md
  - step: 16
    tool: semantic_read
    input: openwiki/decisions/adr-pay-026.md []
    result: 6 sections, 8843 chars
    ms: 1
    refs:
    - semantic:openwiki/decisions/adr-pay-026.md
  - step: 17
    tool: semantic_read
    input: openwiki/systems/hold-management-service.md []
    result: 8 sections, 14077 chars
    ms: 1
    refs:
    - semantic:openwiki/systems/hold-management-service.md
  - step: 18
    tool: semantic_read
    input: openwiki/teams/model-risk-management.md []
    result: 8 sections, 13274 chars
    ms: 8
    refs:
    - semantic:openwiki/teams/model-risk-management.md
  - step: 19
    tool: semantic_read
    input: openwiki/teams/payment-operations.md []
    result: 9 sections, 14858 chars
    ms: 8
    refs:
    - semantic:openwiki/teams/payment-operations.md
  - step: 20
    tool: semantic_read
    input: openwiki/teams/commercial-service-center.md []
    result: 4 sections, 8737 chars
    ms: 7
    refs:
    - semantic:openwiki/teams/commercial-service-center.md
  - step: 21
    tool: semantic_read
    input: openwiki/teams/legal-treasury-payments.md []
    result: 8 sections, 7841 chars
    ms: 7
    refs:
    - semantic:openwiki/teams/legal-treasury-payments.md
  - step: 22
    tool: semantic_read
    input: openwiki/teams/payments-arb-enterprise-architecture.md []
    result: 9 sections, 11141 chars
    ms: 7
    refs:
    - semantic:openwiki/teams/payments-arb-enterprise-architecture.md
  - step: 23
    tool: semantic_search
    input: '"CBO-4480 spike gpi status visible Investigations Workbench"'
    result: '8 hits: openwiki/people/lucas-ferreira.md, openwiki/systems/investigations-workbench.md, openwiki/projects/gtsi-0107-gpi-real-time-service.md'
    ms: 7
    refs:
    - semantic:openwiki/people/lucas-ferreira.md
    - semantic:openwiki/systems/investigations-workbench.md
    - semantic:openwiki/projects/gtsi-0107-gpi-real-time-service.md
    - semantic:openwiki/systems/cbo-wire-center.md
    - semantic:openwiki/teams/payment-operations.md
    - semantic:openwiki/projects/jira-backlog-registry.md
    - semantic:openwiki/systems/cbo-status-projection-service.md
    - semantic:openwiki/incidents/cmp-2026-1189.md
```

## WTC-Q02 - 'Settled' vs 'Completed' for domestic wires

```yaml
id: WTC-Q02
title: '''Settled'' vs ''Completed'' for domestic wires'
intent: Whether today's 'Completed' status can be used as the 'Settled' step of the domestic wire timeline, and
  what a true settled milestone would need.
example_questions:
- My timeline ends in 'Settled'. Wire Center already shows 'Completed' - can we just use that?
- Can 'Completed' be our 'Settled' status?
- Is the existing Completed label good enough to show a wire as settled?
- What do we need to show 'Settled' on the timeline?
recorded_question: My timeline ends in 'Settled'. Wire Center already shows 'Completed' - can we just use that?
  If not, what would a true 'Settled' milestone need (APIs, fields, tickets, deadlines, rail differences between
  Fedwire and Swift), and what should the domestic milestones be?
recorded_at: '2026-10-12T05:51:18+00:00'
recorded_model: claude-sonnet-5
recorded_latency_ms: 66959
confidence: medium
answer: |-
  ## Verdict
  No — don't reuse "Completed." It maps to v1's `PROCESSED`, which collapses four different lifecycle events and has already caused a regulatory complaint (CMP-2026-1189) for exactly this reason. A true "Settled" milestone needs a different data source, a backlog item that doesn't exist yet, and a migration that's stalled and unscheduled.

  ## Why "Completed" ≠ "Settled"
  Per `openwiki/concepts/settlement-release-completed-semantics.md`, three groups disagree on what "Completed" means:
  - **PPH engineering**: `COMPLETED` = internal accounting close (end of day) — an engineering concept, not client disclosure.
  - **POL-FCC-014 §5.2** (the controlling rule): "Completed/Settled" may be shown **only** on Domestic = Fedwire acceptance (`pacs.002` with OMAD); International = gpi `ACCC`. Not permitted on release, transmission, or network ACK.
  - **CBO today**: shows "Completed" at v1 `PROCESSED`, i.e., anywhere across `RELEASED`/`SENT_TO_NETWORK`/`NETWORK_ACCEPTED`/`COMPLETED` — none of which is guaranteed to be Fedwire acceptance.

  This exact gap produced CMP-2026-1189 (EUR 412,600 wire shown "Completed" on 2026‑09‑16, rejected `RJCT AC04` next day, returned 2026‑09‑21).

  ## What a real "Settled" milestone needs

  | Need | Detail | Owner/Status |
  |---|---|---|
  | Lifecycle data | v2 `lifecycleState` via `GET /pph/v2/payments/{paymentId}` (EP-PPH-04) + `/history` (EP-PPH-06) — distinguishes `NETWORK_ACCEPTED` from `COMPLETED`, unlike v1's collapsed `status` (EP-PPH-01, deprecated) | SYS-PPH |
  | Fed proof (OMAD) | OMAD + authoritative Fed timestamp exist only on `net.fedwire.ack.v1` (Kafka) or v2 `identifiers.omad`; v2's `stateHistory` timestamp is PPH's processing time, **not** the Fed's own `pacs.002` timestamp | not in v1 at all |
  | Combined settlement field | **PPH-2207** (backlog): proposes a `settlement` object (`fedSettlementTs` + rail-specific `settlementStatus`) — **no product sponsor, parked**, doesn't exist today | PPH Engineering, unsponsored |
  | BFF migration off v1 | **CBO-4471** (34-pt epic, Backlog/unscheduled, owner Tom Becker) must move `cbo-wire-bff` to v2 before deadline **2027‑03‑31** (ARB-confirmed, no extensions). Blocked by **CBO-4473** (CES account-filter mapping, 8 pts, owner Arjun Mehta, also unscheduled). Scope explicitly **excludes new tracking features** — so even post-migration, a settlement milestone is separate work | CBO Wire Center squad |
  | Compliance sign-off | POL-FCC-014 §6: any new/changed client-facing status experience requires FCC Policy & Advisory review + DRC copy approval **before build commitment** — never done for the current "Completed" label | FCC (Jordan Ellis contact) |

  ## Rail differences
  - **Fedwire**: `NETWORK_ACCEPTED` (OMAD via `pacs.002`) = final, irrevocable interbank settlement (Reg J/UCC 4A) — but does **not** confirm beneficiary credit. No domestic "credited" milestone exists.
  - **Swift**: `NETWORK_ACCEPTED`/ACK = mere network delivery acknowledgment, no settlement meaning at all. True delivery/credit only via gpi `ACCC`.

  ## Suggested domestic milestones (POL-FCC-014-aligned)
  Submitted → Approved → **Sent/In transit** (released, transmitted) → **Delivered to beneficiary's bank** (Fedwire acceptance/OMAD) → **Settled** (same Fedwire-acceptance trigger — domestic has no further "credited" state) → Returned (+ISO reason, if applicable). Both "Delivered" and "Settled" fire off the *same* Fedwire-acceptance event per §5.2 — don't imply a later, separate credit confirmation domestically.
sources:
- ref: openwiki/concepts/wire-lifecycle-state-model.md
  why: Defines lifecycle states like NETWORK_ACCEPTED, RELEASED, SENT_TO_NETWORK, COMPLETED used in the analysis
- ref: openwiki/concepts/settlement-release-completed-semantics.md
  why: Source of the three-way disagreement on 'Completed' semantics and the CMP-2026-1189 incident
- ref: openwiki/concepts/imad-omad.md
  why: Explains OMAD as Fed proof of settlement and its relation to pacs.002
- ref: openwiki/projects/cbo-4471-pph-v1-to-v2-migration.md
  why: Details on CBO-4471 migration epic, CBO-4473 blocker, deadline, and scope exclusions
- ref: openwiki/policies/pol-fcc-014.md#5.2 Status terminology
  why: Controlling policy defining when 'Completed/Settled' may be shown for domestic vs international wires
follow_up_questions:
- Who would need to sponsor PPH-2207 to get the combined settlement field built?
- Can CBO-4471's 2027-03-31 deadline be met given it and its blocker CBO-4473 are both unscheduled?
- Should a new backlog item be opened specifically for the 'Settled' milestone UI work, separate from CBO-4471?
reasoning_summary: Transcribed the CNB Q&A agent's answer verbatim into structured format, citing only the refs
  the agent reported having read.
trace:
  input_tokens: 197008
  output_tokens: 6947
  steps:
  - step: 1
    tool: semantic_search
    input: '"Payments Hub wire status API Completed status field"'
    result: '8 hits: openwiki/concepts/wire-lifecycle-state-model.md, openwiki/systems/prism-payments-hub.md, openwiki/interfaces/pph-v1-wire-status-api.md'
    ms: 598
    refs:
    - semantic:openwiki/concepts/wire-lifecycle-state-model.md
    - semantic:openwiki/systems/prism-payments-hub.md
    - semantic:openwiki/interfaces/pph-v1-wire-status-api.md
    - semantic:openwiki/interfaces/pph-v2-payments-api.md
    - semantic:openwiki/projects/cbo-4471-pph-v1-to-v2-migration.md
    - semantic:openwiki/concepts/imad-omad.md
    - semantic:openwiki/projects/pph-2190-v1-sunset-migration.md
    - semantic:openwiki/people/sunita-rao.md
  - step: 2
    tool: semantic_search
    input: '"Wire Center wire status definitions Settled Completed"'
    result: '8 hits: openwiki/systems/cbo-wire-center.md, openwiki/teams/commercial-service-center.md, openwiki/concepts/wire-lifecycle-state-model.md'
    ms: 598
    refs:
    - semantic:openwiki/systems/cbo-wire-center.md
    - semantic:openwiki/teams/commercial-service-center.md
    - semantic:openwiki/concepts/wire-lifecycle-state-model.md
    - semantic:openwiki/systems/cbo-status-projection-service.md
    - semantic:openwiki/interfaces/sps-read-model-api.md
    - semantic:openwiki/people/tom-becker.md
    - semantic:openwiki/projects/cbo-3120-wire-status-lite-pilot.md
    - semantic:openwiki/incidents/cmp-2026-1189.md
  - step: 3
    tool: semantic_search
    input: '"Settlement Release Completed status semantics three definitions"'
    result: '8 hits: openwiki/incidents/cmp-2026-1189.md, openwiki/concepts/settlement-release-completed-semantics.md,
      openwiki/concepts/wire-lifecycle-state-model.md'
    ms: 400
    refs:
    - semantic:openwiki/incidents/cmp-2026-1189.md
    - semantic:openwiki/concepts/settlement-release-completed-semantics.md
    - semantic:openwiki/concepts/wire-lifecycle-state-model.md
    - semantic:openwiki/concepts/imad-omad.md
    - semantic:openwiki/incidents/inc-2024-1182.md
    - semantic:openwiki/incidents/pir-2024-07.md
    - semantic:openwiki/concepts/fedwire-funds-service.md
    - semantic:openwiki/teams/commercial-service-center.md
  - step: 4
    tool: semantic_read
    input: openwiki/concepts/wire-lifecycle-state-model.md []
    result: 7 sections, 10601 chars
    ms: 400
    refs:
    - semantic:openwiki/concepts/wire-lifecycle-state-model.md
  - step: 5
    tool: semantic_read
    input: openwiki/concepts/settlement-release-completed-semantics.md []
    result: 8 sections, 11541 chars
    ms: 2
    refs:
    - semantic:openwiki/concepts/settlement-release-completed-semantics.md
  - step: 6
    tool: semantic_read
    input: openwiki/concepts/imad-omad.md []
    result: 7 sections, 7194 chars
    ms: 1
    refs:
    - semantic:openwiki/concepts/imad-omad.md
  - step: 7
    tool: semantic_read
    input: openwiki/systems/cbo-wire-center.md [Capabilities Wire Center does not provide]
    result: 'Error: unknown heading ''Capabilities Wire Center does not provide'' on openwiki/systems/cbo-wire-center.md;
      available: Overview, Usage (trailing 90 days to 2026-07-31), What Wire Center does NOT suppor'
    ms: 2
    refs: []
  - step: 8
    tool: semantic_read
    input: openwiki/projects/cbo-4471-pph-v1-to-v2-migration.md []
    result: 8 sections, 13925 chars
    ms: 1
    refs:
    - semantic:openwiki/projects/cbo-4471-pph-v1-to-v2-migration.md
  - step: 9
    tool: semantic_search
    input: '"POL-FCC-014 Section 5.2 Completed Settled terminology table"'
    result: '8 hits: openwiki/policies/pol-fcc-014.md, openwiki/concepts/settlement-release-completed-semantics.md,
      openwiki/incidents/cmp-2026-1189.md'
    ms: 15
    refs:
    - semantic:openwiki/policies/pol-fcc-014.md
    - semantic:openwiki/concepts/settlement-release-completed-semantics.md
    - semantic:openwiki/incidents/cmp-2026-1189.md
    - semantic:openwiki/teams/financial-crimes-compliance.md
    - semantic:openwiki/systems/sanctionscreen.md
    - semantic:openwiki/people/catherine-doyle.md
    - semantic:openwiki/concepts/hold-reason-taxonomy-disclosure-tiers.md
    - semantic:openwiki/people/jordan-ellis.md
  - step: 10
    tool: semantic_read
    input: openwiki/policies/pol-fcc-014.md [Section 5.2]
    result: 'Error: unknown heading ''Section 5.2'' on openwiki/policies/pol-fcc-014.md; available: Why this policy
      exists, Scope, Regulatory and legal basis, Disclosure tiers (Section 4), Requirements (Section 5), '
    ms: 1
    refs: []
  - step: 11
    tool: semantic_read
    input: openwiki/policies/pol-fcc-014.md [5.2 Status terminology]
    result: 1 section, 1842 chars
    ms: 0
    refs:
    - semantic:openwiki/policies/pol-fcc-014.md#5.2 Status terminology
```

## WTC-Q03 - Live international gpi route

```yaml
id: WTC-Q03
title: Live international gpi route
intent: 'Whether a live, minute-by-minute SWIFT gpi route with ''Expected delivery: Today'' for international wires
  is feasible (for Q1 2027), and what is realistic instead.'
example_questions:
- 'For international wires I want the live SWIFT gpi route, refreshed every minute, with ''Expected delivery: Today''.
  Feasible for Q1 2027?'
- Can we show a live FedEx-style map for international wires?
- Is real-time gpi tracking possible for the Q1 2027 launch?
- How fresh can the international wire route be?
recorded_question: ''
recorded_at: '2026-10-12T05:33:36+00:00'
recorded_model: claude-sonnet-5
recorded_latency_ms: 35662
confidence: medium
answer: |-
  **Verdict: Not feasible for Q1 2027 — this is a hard "No," not a scoping gap. Both the 1-minute refresh and "Expected delivery: Today" require infrastructure that is explicitly unfunded and architecturally blocked, not just undesigned.

  **Why "every minute" can't happen**

  | Constraint | Detail | Source |
  |---|---|---|
  | Current gpi data freshness | Swift Alliance & gpi Connector (GPI‑C, `SYS-PNG-GPI`) pulls Swift Tracker updates in a **4‑hour batch** (00:00/04:00/08:00/12:00/16:00/20:00 ET) into Oracle table `GPI_TRACKER_SNAPSHOT`. No live feed exists. | `openwiki/systems/swift-gpi-connector.md`, `openwiki/interfaces/gpi-tracker-batch-feed.md` |
  | Faster polling was already asked for and declined | **PNG-1544** (2026-03-03, Won't Do): request to double cadence to 2h was rejected because Swift Tracker API is capped at **250,000 calls/month**; per-payment client lookups were projected at **~1.9M calls/month (~7x quota)**. | `openwiki/decisions/png-1544.md` |
  | No interim workaround approved | Payments ARB (2026-09-08) explicitly ruled **direct exposure of `GPI_TRACKER_SNAPSHOT` to channels is not approved**, and even a quota-isolated read-only facade "would require ARB review" in its own right. | `openwiki/projects/gtsi-0107-gpi-real-time-service.md` |
  | The only sanctioned path | **GTSI-0107 (gpi Tracker Real-Time Service, GTRS)** — a change-feed-based internal REST+event API, status **proposed**, **not funded for 2026**, discovery **2027-Q2**, build **2027-Q3/Q4**, "subject to 2027 portfolio review." Owner: GTSI / Elena Vasquez. | same |
  | Ownership | gpi roadmap moved from PNE (Raj Malhotra) to **GTSI** (Elena Vasquez, Omar Siddiqui, Hannah Lindqvist) effective 2026-10-01; PNE is now secondary on-call only. | `openwiki/people/elena-vasquez.md`, `openwiki/teams/gtsi.md` |

  Since GTRS's earliest possible build window (2027‑Q3/Q4) is after your pilot (Feb 2027) and GA target (Q1 2027), **live minute-by-minute gpi tracking cannot exist by then under any currently approved plan** — this isn't a build-it-faster problem, it's a funding/quota/ARB-approval gap.

  **Why "Expected delivery: Today" also fails**
  - No endpoint or data source produces a forward-looking delivery estimate today. The closest asset, TDIP's `client_wire_history_features`, is a **prototype**, unregistered in MRM, with **no serving endpoint** — and it's a backward-looking median/p90 "release-to-ACCC" stat, not a delivery prediction.
  - Any forward-looking, customer-facing estimate is a **Tier 2 model minimum under MRM-POL-02**, requiring independent validation (**10–14 weeks, 160–240 validator hours, ~6‑week queue** currently) — vs. the lighter End-User-Analytic path for purely descriptive stats.
  - ADR-PAY-026 requires such insights be served via the TDIP Insights API, not computed in a channel BFF (contradicting the PM's assumption that insights can be calculated in the CBO wire BFF) — and no wire-insights endpoint exists yet (catalog literally states "not available").
  - This data also only covers international/gpi corridors (UETR-tracked), not domestic wires (`TDA-2210` not ingested).

  **Bottom line:** Recommend descoping FC-02's "live every-minute" claim and FC-04 for international wires out of the Q1 2027 release, and routing the real need (CBO-4480) into the GTSI-0107 roadmap discussion with Elena Vasquez's team — plus an MRM/DRC track for any future delivery-estimate feature.
sources:
- ref: openwiki/projects/gtsi-0107-gpi-real-time-service.md
  why: Details GTRS project status, funding, timeline, and ARB ruling on direct snapshot exposure
- ref: openwiki/decisions/png-1544.md
  why: Documents the rejected request to increase polling cadence due to Swift Tracker API quota limits
- ref: openwiki/datasets/client-wire-history-features.md
  why: Describes the prototype client_wire_history_features dataset, its lack of a serving endpoint, and its backward-looking
    nature
follow_up_questions:
- What is the status and timeline of the ADR-PAY-026-compliant TDIP Insights API for wire data?
- 'Can a lighter-weight ''last updated: X hours ago'' disclosure be substituted for live tracking in the Q1 2027
  release?'
- What would it take to get GTSI-0107 prioritized or accelerated in the 2027 portfolio review?
reasoning_summary: ''
trace:
  input_tokens: 50820
  output_tokens: 4069
  steps:
  - step: 1
    tool: semantic_search
    input: '"Swift gpi tracker snapshot refresh interval quota"'
    result: '8 hits: openwiki/datasets/gpi-tracker-snapshot.md, openwiki/concepts/uetr.md, openwiki/interfaces/gpi-tracker-batch-feed.md'
    ms: 510
    refs:
    - semantic:openwiki/datasets/gpi-tracker-snapshot.md
    - semantic:openwiki/concepts/uetr.md
    - semantic:openwiki/interfaces/gpi-tracker-batch-feed.md
    - semantic:openwiki/datasets/gpi-tracker-events.md
    - semantic:openwiki/decisions/png-1544.md
    - semantic:openwiki/systems/swift-gpi-connector.md
    - semantic:openwiki/teams/gtsi.md
    - semantic:openwiki/people/elena-vasquez.md
  - step: 2
    tool: semantic_search
    input: '"GTSI-0107 real-time gpi tracking project"'
    result: '8 hits: openwiki/projects/gtsi-0107-gpi-real-time-service.md, openwiki/people/elena-vasquez.md, openwiki/teams/gtsi.md'
    ms: 510
    refs:
    - semantic:openwiki/projects/gtsi-0107-gpi-real-time-service.md
    - semantic:openwiki/people/elena-vasquez.md
    - semantic:openwiki/teams/gtsi.md
    - semantic:openwiki/decisions/png-1544.md
    - semantic:openwiki/people/omar-siddiqui.md
    - semantic:openwiki/systems/swift-gpi-connector.md
    - semantic:openwiki/projects/gtsi-0112-gpi-knowledge-transfer.md
    - semantic:openwiki/people/tomasz-nowak.md
  - step: 3
    tool: semantic_search
    input: '"expected delivery date estimate gpi wire SLA"'
    result: '8 hits: openwiki/teams/gtsi.md, openwiki/projects/gtsi-0107-gpi-real-time-service.md, openwiki/datasets/gpi-tracker-events.md'
    ms: 510
    refs:
    - semantic:openwiki/teams/gtsi.md
    - semantic:openwiki/projects/gtsi-0107-gpi-real-time-service.md
    - semantic:openwiki/datasets/gpi-tracker-events.md
    - semantic:openwiki/policies/mrm-pol-02.md
    - semantic:openwiki/datasets/wire-corridor-stats-daily.md
    - semantic:openwiki/concepts/swift-gpi-cbpr.md
    - semantic:openwiki/datasets/gpi-tracker-snapshot.md
    - semantic:openwiki/datasets/client-wire-history-features.md
  - step: 4
    tool: semantic_read
    input: openwiki/projects/gtsi-0107-gpi-real-time-service.md []
    result: 7 sections, 10056 chars
    ms: 0
    refs:
    - semantic:openwiki/projects/gtsi-0107-gpi-real-time-service.md
  - step: 5
    tool: semantic_read
    input: openwiki/decisions/png-1544.md []
    result: 7 sections, 6443 chars
    ms: 0
    refs:
    - semantic:openwiki/decisions/png-1544.md
  - step: 6
    tool: semantic_read
    input: openwiki/datasets/client-wire-history-features.md []
    result: 8 sections, 12180 chars
    ms: 0
    refs:
    - semantic:openwiki/datasets/client-wire-history-features.md
```

## WTC-Q04 - Held-wire design review

```yaml
id: WTC-Q04
title: Held-wire design review
intent: 'A review of the held-wire design (FC-03: showing the hold reason, Confirm/Reject self-service, release
  time estimate) for policy, control and missing-interface issues.'
example_questions:
- Review FC-03. Clients want to know why a wire is held and to fix it themselves. Any issues?
- Any problems with showing clients why their wire is held?
- Can clients confirm or reject held wires themselves?
- Check my held wire self-service design.
recorded_question: ''
recorded_at: '2026-10-12T05:34:43+00:00'
recorded_model: claude-sonnet-5
recorded_latency_ms: 66425
confidence: medium
answer: |-
  **Verdict: FC-03 as written cannot ship — it directly violates POL-FCC-014's disclosure-tier rules on two of its three example reasons, proposes a self-service action (Confirm/Reject) that doesn't exist as a system capability beyond one narrow case, and would repeat a leak that CNB has already shipped once (unremediated) and is still an open risk.**

  **1. "Show the exact review reason" — fails for 2 of 3 example reasons**

  | FC-03 example text | Actual HRC code / tier | Allowed? |
  |---|---|---|
  | "Potential duplicate" | HRC-01 `DUP_SUSPECT`, tier **C** | OK in spirit, but must use the exact DRC-approved copy `COPY-HOLD-DUP-01`: *"This wire appears similar to another recent wire. Please confirm whether you intend to send both."* — not free text. |
  | "Unusual activity detected" | HRC-10 `AML_REVIEW`, tier **R** | **Prohibited.** Tier R must render identical to tier G — only generic `COPY-HOLD-GEN-01` ("This wire is being reviewed...") may be shown. |
  | "Sanctions screening in progress" | HRC-09 `SANCTIONS_REVIEW`, tier **R** | **Prohibited twice over**: "sanctions"/"screening" are Appendix C denylisted terms, and sanctions outcomes may only ever be communicated by Sanctions Operations, never a channel (POL-FCC-014 §5.1(6); ADR-PAY-021). |

  This isn't a copy-polish issue — showing differentiated reasons for R-tier vs G-tier holds violates the core §5.1(2) "indistinguishability" rule even if no banned word appears, because differentiation itself leaks the nature of the review.

  **This exact failure already happened:** CBO-4388 ("hold reason tooltip," flag `WC_HOLD_TOOLTIP`, shipped `release/26.21`, targeted prod 2026-10-22) populated a client tooltip straight from PPH v1's `holdReasonDesc`, and UAT samples captured literal restricted strings like `FRAUD_MODEL_HIGH sc=9xx L1 queue` and `SANCTIONS_REVIEW name match 0.91 L2`. This is the open, unremediated risk **FCT-2004** (owner Daniel Kowalski, FCT), flagged to both PPH (Sunita Rao) and CBO Wire Center (Tom Becker) in 2026-05 with no fix yet — only the v1 sunset (2027-03-31) may close it by retiring the field.

  **2. "Confirm/Reject on all held wires" — no such capability exists**
  - HMS has **no generalized client-facing interface**: `GET/POST /prsp/hms/v1/holds...` is restricted to the Investigations Workbench; a client attestation endpoint "does not exist" (PRSP-HMS-3.4).
  - The only sanctioned client action is **digital attestation for HRC-01 only** (confirm/cancel, not "reject"), under `CTRL-PAY-031`, requiring step-up auth, capped at **$5,000,000** (above that, Wire Room release is mandatory regardless of attestation).
  - Even that has **never been built digitally** — FCT-1951 only piloted phone-based attestation via Service Center; the proposed facade `FCT-1893` (21 pts) was deprioritized 2025-Q3.
  - HRC-02/03/05/06 have different, non-confirm/reject actions (callback, admin approval, fund account, cancel-and-resubmit); HRC-07–12 permit **no client action at all**.

  **3. "Released ~30 min after confirm" — needs governance FC-03 hasn't scoped**
  Any such predictive statement must satisfy §5.5: client's-own-data or DUS-07 cohort, MRM-POL-02 classification, DRC-approved disclaimer, served via TDIP Insights API (ADR-PAY-026) — not computed ad hoc in the CBO BFF as the PM assumed, and no such model/endpoint exists today.

  **Owners to engage before BRD:** Financial Crimes Technology (Victor Petrov/Grace Mensah/Daniel Kowalski — HMS, FCT-1893, FCT-2004), FCC Policy & Advisory (Jordan Ellis) and DRC (Patricia Moore) for any copy/action change under POL-FCC-014 §6, before build commitment.
sources:
- ref: openwiki/concepts/hold-reason-taxonomy-disclosure-tiers.md
  why: Defines HRC codes, disclosure tiers (C/R/G), and allowed copy per code
- ref: openwiki/decisions/adr-pay-021.md
  why: Governs sanctions communication restrictions and TDIP Insights API requirement
- ref: openwiki/projects/fct-1951-duplicate-suspect-attestation-pilot.md
  why: Details the only existing client attestation capability (HRC-01 phone pilot) and deprioritized facade FCT-1893
- ref: openwiki/policies/pol-fcc-014.md
  why: Source of disclosure-tier indistinguishability rules (§5.1), denylisted terms (Appendix C), and predictive
    statement governance (§5.5, §6)
- ref: openwiki/people/daniel-kowalski.md
  why: Identifies FCT-2004 risk owner and context for CBO-4388 leak
follow_up_questions:
- What would it take to extend digital attestation (CTRL-PAY-031) beyond HRC-01 to other hold reason codes?
- What is the remediation plan and timeline for closing FCT-2004 before the PPH v1 sunset in 2027-03-31?
- What governance steps (MRM-POL-02 classification, DRC approval) are needed to build a release-time prediction
  feature via the TDIP Insights API?
reasoning_summary: ''
trace:
  input_tokens: 113514
  output_tokens: 7106
  steps:
  - step: 1
    tool: semantic_search
    input: '"held wire review reason client self-service confirm reject"'
    result: '8 hits: openwiki/projects/fct-1951-duplicate-suspect-attestation-pilot.md, openwiki/teams/payment-operations.md,
      openwiki/decisions/adr-pay-021.md'
    ms: 237
    refs:
    - semantic:openwiki/projects/fct-1951-duplicate-suspect-attestation-pilot.md
    - semantic:openwiki/teams/payment-operations.md
    - semantic:openwiki/decisions/adr-pay-021.md
    - semantic:openwiki/systems/hold-management-service.md
    - semantic:openwiki/concepts/hold-reason-taxonomy-disclosure-tiers.md
    - semantic:openwiki/systems/investigations-workbench.md
    - semantic:openwiki/projects/ens-1120-entity-level-subscriptions.md
    - semantic:openwiki/teams/commercial-service-center.md
  - step: 2
    tool: semantic_search
    input: '"sanctions screening disclosure prohibited client-facing"'
    result: '8 hits: openwiki/systems/sanctionscreen.md, openwiki/policies/pol-fcc-014.md, openwiki/documents/pol-fcc-014.md'
    ms: 236
    refs:
    - semantic:openwiki/systems/sanctionscreen.md
    - semantic:openwiki/policies/pol-fcc-014.md
    - semantic:openwiki/documents/pol-fcc-014.md
    - semantic:openwiki/systems/hold-management-service.md
    - semantic:openwiki/teams/legal-treasury-payments.md
    - semantic:openwiki/people/patricia-moore.md
    - semantic:openwiki/policies/dus-07.md
    - semantic:openwiki/decisions/adr-pay-026.md
  - step: 3
    tool: semantic_search
    input: '"hold management service HRC reason codes"'
    result: '8 hits: openwiki/projects/fct-1951-duplicate-suspect-attestation-pilot.md, openwiki/systems/sentinel-fraud-scoring.md,
      openwiki/people/victor-petrov.md'
    ms: 236
    refs:
    - semantic:openwiki/projects/fct-1951-duplicate-suspect-attestation-pilot.md
    - semantic:openwiki/systems/sentinel-fraud-scoring.md
    - semantic:openwiki/people/victor-petrov.md
    - semantic:openwiki/systems/sanctionscreen.md
    - semantic:openwiki/interfaces/hms-hold-api.md
    - semantic:openwiki/people/rebecca-stone.md
    - semantic:openwiki/teams/financial-crimes-compliance.md
    - semantic:openwiki/people/daniel-kowalski.md
  - step: 4
    tool: semantic_search
    input: '"FCT-2004 leak risk hold reason exposure"'
    result: '8 hits: openwiki/systems/sentinel-fraud-scoring.md, openwiki/people/daniel-kowalski.md, openwiki/systems/sanctionscreen.md'
    ms: 236
    refs:
    - semantic:openwiki/systems/sentinel-fraud-scoring.md
    - semantic:openwiki/people/daniel-kowalski.md
    - semantic:openwiki/systems/sanctionscreen.md
    - semantic:openwiki/decisions/adr-pay-021.md
    - semantic:openwiki/interfaces/hms-hold-api.md
    - semantic:openwiki/people/victor-petrov.md
    - semantic:openwiki/people/grace-mensah.md
    - semantic:openwiki/concepts/hold-reason-taxonomy-disclosure-tiers.md
  - step: 5
    tool: semantic_read
    input: openwiki/concepts/hold-reason-taxonomy-disclosure-tiers.md []
    result: 8 sections, 11780 chars
    ms: 1
    refs:
    - semantic:openwiki/concepts/hold-reason-taxonomy-disclosure-tiers.md
  - step: 6
    tool: semantic_read
    input: openwiki/decisions/adr-pay-021.md []
    result: 7 sections, 9516 chars
    ms: 1
    refs:
    - semantic:openwiki/decisions/adr-pay-021.md
  - step: 7
    tool: semantic_read
    input: openwiki/projects/fct-1951-duplicate-suspect-attestation-pilot.md []
    result: 6 sections, 8652 chars
    ms: 1
    refs:
    - semantic:openwiki/projects/fct-1951-duplicate-suspect-attestation-pilot.md
  - step: 8
    tool: semantic_read
    input: openwiki/policies/pol-fcc-014.md []
    result: 16 sections, 17143 chars
    ms: 1
    refs:
    - semantic:openwiki/policies/pol-fcc-014.md
  - step: 9
    tool: semantic_read
    input: openwiki/people/daniel-kowalski.md []
    result: 5 sections, 3797 chars
    ms: 0
    refs:
    - semantic:openwiki/people/daniel-kowalski.md
```

## WTC-Q05 - In-flight conflicts

```yaml
id: WTC-Q05
title: In-flight conflicts
intent: Whether anything already in flight (backlog, upcoming release or production) conflicts with policy or with
  the Wire Tracking Center.
example_questions:
- Before I go further - is anything already in the Wire Center backlog or in production that conflicts with policy
  or with this feature?
- Is there anything in progress that clashes with this?
- Any existing Jira work or live features that conflict with policy?
- What in the current backlog could block or contradict this feature?
recorded_question: 'Before I go further - is anything already in the Wire Center backlog or in production that conflicts
  with policy or with this feature? Check across the whole concept (FC-01 to FC-07): status labels and templates,
  holds, gpi, migrations and data loads - and rank them by urgency.'
recorded_at: '2026-10-12T05:53:08+00:00'
recorded_model: claude-sonnet-5
recorded_latency_ms: 110329
confidence: high
answer: |-
  ## Verdict
  Yes — multiple live conflicts, one of them shipping to production in about two weeks. Ranked most urgent first:

  | Rank | FC | Conflict | Owner/Ticket | Date |
  |---|---|---|---|---|
  | 1 🔴 | FC-03 | **CBO-4388** ("hold reason tooltip") is *In Progress*, merged to `release/26.21` behind flag `WC_HOLD_TOOLTIP` (**default ON**), targeting production. It renders PPH v1's raw `holdReasonDesc` — HMS free-text like `"SANCTIONS_REVIEW name match 0.91 L2"` — truncated to 120 chars. This is the open risk **FCT-2004** (owner Daniel Kowalski) and violates ADR-PAY-021 and POL-FCC-014 §5.1(1)/(2) (tier R/G must be presented identically, generic-only, no mnemonic/score leakage). | Jason Park / Daniel Kowalski | Prod target **2026-10-22** |
  | 2 🔴 | FC-01 | "Completed" label (CBO-4402, shipped R26.1) is the subject of open complaint **CMP-2026-1189** (EUR 412,600 wire shown "Completed," then returned) and bug **CBO-4419**, `Open`/root-cause-TBD, **unscheduled**. Your FC-01 "Settled = Completed" reuse is the exact mechanism that caused this. | Tom Becker | Complaint filed 2026-09; fix unscheduled |
  | 3 🔴 | FC-03 | Confirm/Reject "on all held wires" conflicts with the HRC taxonomy: digital attestation only exists for **HRC-01 DUP_SUSPECT** (22% of holds, via CTRL-PAY-031/FCT-1951 pilot). The other 78% (tiers G/R: fraud, ATO, sanctions, AML, legal, ops-review) permit **no client action and no release-time estimate**. No generalized hold API exists — the client-safe facade **FCT-1893** was deprioritized 2025-Q3. | Daniel Kowalski (FCT-1893) | Not built |
  | 4 🟠 | FC-02 | GTSI-0107 (the only route to live/change-feed gpi data) is **not funded for 2026**; discovery 2027-Q2, build 2027-Q3/Q4. PNG-1544 already declined doubling the 4-hour batch poll (quota: 250k calls/mo, ~61% used; per-payment lookups would need ~1.9M/mo, ~7x quota). ARB (2026-09-08) also barred direct exposure of `GPI_TRACKER_SNAPSHOT` to channels. There is **no technical path** to a "live map refreshed every minute" by your Feb 2027 pilot. | GTSI (Tomasz Nowak) | Not funded for 2026 |
  | 5 🟠 | FC-04 | Your assumption "insights calculated in CBO wire BFF" is wrong: any forward-looking customer-facing estimate is **Tier 2 minimum under MRM-POL-02**, needing independent validation (10-14 wks + ~6-wk intake queue ≈ 4 months) plus DRC approval, and must go through the **TDIP Insights API** per ADR-PAY-026 — channels can't compute locally. Data freshness floor is hourly (no sub-minute); `gpi_tracker_events` is nightly until TDA-2188 (targeted 2026-11). | Sophie Laurent (MRM) / TDIP | ~4-month lead time alone |
  | 6 🟠 | FC-05 | ENS catalog has **no event types** for network acceptance, gpi ACCC, wire returns, gpi milestones, or held-wire action — explicitly listed as gaps (ENS-INT-3.2 §4). New-event onboarding has a 6-week SLA, and requests after **2026-11-20** fall behind the year-end freeze — a real threat to a Feb 2027 pilot. | ENS / CBO Wire Center squad | Cutoff 2026-11-20 |
  | 7 🟡 | all | Everything above sits on **PPH v1**, sunsetting **2027-03-31, no extensions**. Migration **CBO-4471** (34 pts) is Backlog/unscheduled, blocked by **CBO-4473** (8 pts, Arjun Mehta, also unscheduled). v1 has no OMAD/UETR, and ISO return reasons only exist on v2 (`pay.wire.lifecycle.v2`, since PPH-2266, 2026-08). | Tom Becker | 2027-03-31 hard deadline |
  | 8 🟡 | FC-06 | External sharing of transaction data is "not supported" today; requires an **InfoSec design review under SEC-STD-22** plus a **Privacy Impact Assessment** before any build. No ticket exists yet. | InfoSec | Pre-build gate, no ticket |
  | 9 🟡 | FC-07 | No `RETURNED` ENS event exists even though PPH v1 surfaces `RETURNED` status; "resend" workflow isn't documented anywhere. | CBO Wire Center squad | Gap, no ticket |

  **Capacity note:** squad velocity is ~42 pts/sprint, PI 27.1 already ~85% committed; CBO-4471 alone (34 pts) plus its CBO-4473 dependency likely consumes most of that — "1.5 PIs, mostly front-end" doesn't account for this backlog.
sources:
- ref: 'openwiki/interfaces/pph-v1-wire-status-api.md#FCT-2004: holdReasonDesc leaks HMS free-text'
  why: Source of the CBO-4388/FCT-2004 hold tooltip leakage risk and PPH v1 sunset/migration details
- ref: openwiki/concepts/hold-reason-taxonomy-disclosure-tiers.md
  why: Basis for HRC tier taxonomy, DUP_SUSPECT attestation pilot, and disclosure policy conflicts
- ref: openwiki/policies/sec-std-22.md
  why: Basis for FC-06 InfoSec design review requirement
- ref: openwiki/concepts/swift-gpi-cbpr.md
  why: Background on gpi data and GTSI-0107 funding status
- ref: openwiki/decisions/png-1544.md
  why: Decision declining increased gpi polling quota
- ref: openwiki/policies/mrm-pol-02.md
  why: Basis for Tier 2 model risk management requirement on FC-04 insights
- ref: openwiki/people/jason-park.md
  why: Ownership context for CBO-4388 production release
- ref: openwiki/interfaces/ens-notification-api-trs-catalog.md
  why: Basis for FC-05/FC-07 ENS event gaps and onboarding SLA
- ref: openwiki/systems/cbo-wire-center.md
  why: Backlog and capacity context for CBO-4471/CBO-4473 migration and squad velocity
follow_up_questions:
- Can CBO-4388's WC_HOLD_TOOLTIP flag be forced OFF before the 2026-10-22 release to avoid shipping the policy violation?
- What would it take to get FCT-1893 (client-safe hold facade) reprioritized given the FC-03 feature's dependency
  on it?
- Should FC-02's gpi live-map scope be reduced to match the existing 4-hour batch poll given GTSI-0107 is unfunded?
reasoning_summary: Compiled a cross-FC review of in-flight tickets, policies, and decisions already documented in
  the wiki, ranking conflicts by production urgency, legal/compliance risk, and deadline proximity.
trace:
  input_tokens: 262646
  output_tokens: 11231
  steps:
  - step: 1
    tool: semantic_search
    input: '"held wire review reason risk system disclosure policy"'
    result: '8 hits: openwiki/policies/pol-fcc-014.md, openwiki/teams/payment-operations.md, openwiki/concepts/hold-reason-taxonomy-disclosure-tiers.md'
    ms: 1158
    refs:
    - semantic:openwiki/policies/pol-fcc-014.md
    - semantic:openwiki/teams/payment-operations.md
    - semantic:openwiki/concepts/hold-reason-taxonomy-disclosure-tiers.md
    - semantic:openwiki/policies/mrm-pol-02.md
    - semantic:openwiki/systems/hold-management-service.md
    - semantic:openwiki/systems/prism-payments-hub.md
    - semantic:openwiki/systems/sanctionscreen.md
    - semantic:openwiki/systems/sentinel-fraud-scoring.md
  - step: 2
    tool: semantic_search
    input: '"share wire status with recipient beneficiary link full wire details"'
    result: '8 hits: openwiki/policies/sec-std-22.md, openwiki/systems/cbo-wire-center.md, openwiki/teams/commercial-service-center.md'
    ms: 1157
    refs:
    - semantic:openwiki/policies/sec-std-22.md
    - semantic:openwiki/systems/cbo-wire-center.md
    - semantic:openwiki/teams/commercial-service-center.md
    - semantic:openwiki/incidents/pir-2024-07.md
    - semantic:openwiki/interfaces/pph-v1-wire-status-api.md
    - semantic:openwiki/concepts/settlement-release-completed-semantics.md
    - semantic:openwiki/concepts/wire-lifecycle-state-model.md
    - semantic:openwiki/incidents/cmp-2026-1189.md
  - step: 3
    tool: semantic_search
    input: '"Swift gpi tracker intermediary bank status feed"'
    result: '8 hits: openwiki/projects/gtsi-0107-gpi-real-time-service.md, openwiki/concepts/swift-gpi-cbpr.md,
      openwiki/decisions/png-1544.md'
    ms: 1157
    refs:
    - semantic:openwiki/projects/gtsi-0107-gpi-real-time-service.md
    - semantic:openwiki/concepts/swift-gpi-cbpr.md
    - semantic:openwiki/decisions/png-1544.md
    - semantic:openwiki/systems/investigations-workbench.md
    - semantic:openwiki/interfaces/gpi-tracker-batch-feed.md
    - semantic:openwiki/teams/gtsi.md
    - semantic:openwiki/datasets/gpi-tracker-events.md
    - semantic:openwiki/projects/gtsi-0112-gpi-knowledge-transfer.md
  - step: 4
    tool: semantic_search
    input: '"returned wire reason code ISO 20022 root cause"'
    result: '8 hits: openwiki/concepts/iso20022-payment-messages.md, openwiki/systems/fedwire-funds-connector.md,
      openwiki/incidents/cmp-2026-1189.md'
    ms: 1157
    refs:
    - semantic:openwiki/concepts/iso20022-payment-messages.md
    - semantic:openwiki/systems/fedwire-funds-connector.md
    - semantic:openwiki/incidents/cmp-2026-1189.md
    - semantic:openwiki/people/tom-becker.md
    - semantic:openwiki/systems/cbo-status-projection-service.md
    - semantic:openwiki/interfaces/pph-lifecycle-event-topics.md
    - semantic:openwiki/incidents/inc-2024-1182.md
    - semantic:openwiki/concepts/fedwire-funds-service.md
  - step: 5
    tool: semantic_read
    input: openwiki/concepts/hold-reason-taxonomy-disclosure-tiers.md []
    result: 8 sections, 11780 chars
    ms: 2
    refs:
    - semantic:openwiki/concepts/hold-reason-taxonomy-disclosure-tiers.md
  - step: 6
    tool: semantic_read
    input: openwiki/policies/sec-std-22.md []
    result: 1 section, 748 chars
    ms: 2
    refs:
    - semantic:openwiki/policies/sec-std-22.md
  - step: 7
    tool: semantic_read
    input: openwiki/concepts/swift-gpi-cbpr.md []
    result: 8 sections, 7570 chars
    ms: 2
    refs:
    - semantic:openwiki/concepts/swift-gpi-cbpr.md
  - step: 8
    tool: semantic_read
    input: openwiki/decisions/png-1544.md []
    result: 7 sections, 6443 chars
    ms: 1
    refs:
    - semantic:openwiki/decisions/png-1544.md
  - step: 9
    tool: semantic_read
    input: openwiki/policies/mrm-pol-02.md []
    result: 8 sections, 9995 chars
    ms: 1
    refs:
    - semantic:openwiki/policies/mrm-pol-02.md
  - step: 10
    tool: semantic_search
    input: '"ADR-PAY-019 channel polling prohibited event-driven status"'
    result: '8 hits: openwiki/decisions/adr-pay-019.md, openwiki/incidents/inc-2024-1182.md, openwiki/interfaces/pph-lifecycle-event-topics.md'
    ms: 1096
    refs:
    - semantic:openwiki/decisions/adr-pay-019.md
    - semantic:openwiki/incidents/inc-2024-1182.md
    - semantic:openwiki/interfaces/pph-lifecycle-event-topics.md
    - semantic:openwiki/projects/cbo-3790-ach-payment-tracker.md
    - semantic:openwiki/projects/cbo-3120-wire-status-lite-pilot.md
    - semantic:openwiki/interfaces/sps-read-model-api.md
    - semantic:openwiki/projects/pph-2190-v1-sunset-migration.md
    - semantic:openwiki/decisions/adr-pay-023.md
  - step: 11
    tool: semantic_search
    input: '"ENS wire event notifications settle released returned"'
    result: '8 hits: openwiki/systems/cbo-wire-center.md, openwiki/interfaces/ens-notification-api-trs-catalog.md,
      openwiki/systems/cbo-status-projection-service.md'
    ms: 1095
    refs:
    - semantic:openwiki/systems/cbo-wire-center.md
    - semantic:openwiki/interfaces/ens-notification-api-trs-catalog.md
    - semantic:openwiki/systems/cbo-status-projection-service.md
    - semantic:openwiki/projects/ens-1120-entity-level-subscriptions.md
    - semantic:openwiki/interfaces/sps-read-model-api.md
    - semantic:openwiki/systems/enterprise-notification-service.md
    - semantic:openwiki/projects/cbo-3790-ach-payment-tracker.md
    - semantic:openwiki/systems/core-deposit-platform.md
  - step: 12
    tool: semantic_search
    input: '"TDIP Insights API predicted delivery time beneficiary typically moves funds"'
    result: '8 hits: openwiki/interfaces/tdip-insights-api.md, openwiki/systems/treasury-data-insights-platform.md,
      openwiki/decisions/adr-pay-026.md'
    ms: 1095
    refs:
    - semantic:openwiki/interfaces/tdip-insights-api.md
    - semantic:openwiki/systems/treasury-data-insights-platform.md
    - semantic:openwiki/decisions/adr-pay-026.md
    - semantic:openwiki/datasets/client-wire-history-features.md
    - semantic:openwiki/datasets/beneficiary-behavior-profile.md
    - semantic:openwiki/datasets/client-hierarchy.md
    - semantic:openwiki/systems/core-deposit-platform.md
    - semantic:openwiki/datasets/cbo-wire-events.md
  - step: 13
    tool: semantic_search
    input: '"CBO Wire Center squad capacity current sprint backlog PI"'
    result: '8 hits: openwiki/teams/cbo-wire-center-squad.md, openwiki/systems/cbo-wire-center.md, openwiki/people/marcus-chen.md'
    ms: 1094
    refs:
    - semantic:openwiki/teams/cbo-wire-center-squad.md
    - semantic:openwiki/systems/cbo-wire-center.md
    - semantic:openwiki/people/marcus-chen.md
    - semantic:openwiki/people/tom-becker.md
    - semantic:openwiki/teams/cbo-platform-entitlements.md
    - semantic:openwiki/people/jason-park.md
    - semantic:openwiki/projects/cbo-4471-pph-v1-to-v2-migration.md
    - semantic:openwiki/organizations/digital-treasury-channels.md
  - step: 14
    tool: semantic_read
    input: openwiki/people/jason-park.md []
    result: 2 sections, 1372 chars
    ms: 1
    refs:
    - semantic:openwiki/people/jason-park.md
  - step: 15
    tool: semantic_read
    input: openwiki/interfaces/ens-notification-api-trs-catalog.md []
    result: 9 sections, 8424 chars
    ms: 1
    refs:
    - semantic:openwiki/interfaces/ens-notification-api-trs-catalog.md
  - step: 16
    tool: semantic_read
    input: openwiki/systems/cbo-wire-center.md []
    result: 12 sections, 12317 chars
    ms: 1
    refs:
    - semantic:openwiki/systems/cbo-wire-center.md
  - step: 17
    tool: semantic_read
    input: openwiki/interfaces/pph-v1-wire-status-api.md [holdReasonDesc]
    result: 'Error: unknown heading ''holdReasonDesc'' on openwiki/interfaces/pph-v1-wire-status-api.md; available:
      Overview, Endpoint inventory (EP-PPH-01/02/03), EP-PPH-01 response shape, The PROCESSED collapse, F'
    ms: 10
    refs: []
  - step: 18
    tool: semantic_search
    input: '"FCT-2004 holdReasonDesc leak risk client-facing"'
    result: '8 hits: openwiki/interfaces/pph-v1-wire-status-api.md, openwiki/interfaces/hms-hold-api.md, openwiki/people/daniel-kowalski.md'
    ms: 10
    refs:
    - semantic:openwiki/interfaces/pph-v1-wire-status-api.md
    - semantic:openwiki/interfaces/hms-hold-api.md
    - semantic:openwiki/people/daniel-kowalski.md
    - semantic:openwiki/systems/sentinel-fraud-scoring.md
    - semantic:openwiki/projects/jira-backlog-registry.md
    - semantic:openwiki/policies/mrm-pol-02.md
    - semantic:openwiki/teams/commercial-service-center.md
    - semantic:openwiki/decisions/adr-pay-026.md
  - step: 19
    tool: semantic_read
    input: 'openwiki/interfaces/pph-v1-wire-status-api.md [FCT-2004: holdReasonDesc leaks HMS free-text]'
    result: 1 section, 2068 chars
    ms: 0
    refs:
    - 'semantic:openwiki/interfaces/pph-v1-wire-status-api.md#FCT-2004: holdReasonDesc leaks HMS free-text'
```

## WTC-Q06 - Insights and predictions

```yaml
id: WTC-Q06
title: Insights and predictions
intent: Whether the FC-04 wire insights (beneficiary moves funds within N hours, share of similar wires completing
  same day, predicted delivery time) can be shown to clients, and compliant alternatives.
example_questions:
- 'FC-04: can we show ''Beneficiary typically moves funds within 4 hours'', ''92% of similar EUR wires complete
  same day'', and a predicted delivery time based on the client''s similar past wires?'
- Are the wire insights in FC-04 allowed?
- Can we predict delivery time from past wires?
- Can we tell clients how fast the beneficiary usually moves the money?
recorded_question: ''
recorded_at: '2026-10-12T05:36:23+00:00'
recorded_model: claude-sonnet-5
recorded_latency_ms: 59985
confidence: high
answer: |-
  **Verdict: All three FC-04 claims are blocked today — one is flatly prohibited by policy (not just undeveloped), and the other two have no governed path to production inside the Q1 2027 timeline.**

  | Claim | Status | Why |
  |---|---|---|
  | **"Beneficiary typically moves funds within 4 hours"** | **Prohibited, not just unbuilt** | This is counterparty (beneficiary) behavior shown to a *different* client — the exact pattern DUS-07 §4 bans ("information about one client... as a counterparty... must not be used to generate content shown to another client... even presented as a pattern or typical value"). The only matching feature, `bene_median_hours_to_outflow` on `beneficiary_behavior_profile`, is additionally **Restricted – Client Confidential** and a registered input to Tier 1 model **M-FCT-0034** (fraud/mule detection); MRM-POL-02 §4 states Tier 1 financial-crimes outputs **"may not be used for product, marketing, or client-facing purposes."** Two independent, hard blocks — this claim cannot ship under any current governance path. |
  | **"92% of similar EUR wires complete same day"** | **Data may qualify, but no serving path exists** | This is a cross-client cohort stat, gated by DUS-07 §5: ≥500 transactions, ≥20 distinct clients, no client >15% of volume, ≥monthly refresh, **DRC-approved wording** — all five must hold simultaneously or the cohort must be suppressed outright. The closest asset, `wire_corridor_stats_daily`, shows high-volume corridors (e.g. EUR/DE: 31,200 wires, 1,140 clients, 4% share) would likely pass, but thin corridors (e.g. NGN/NG: 140 wires, 11 clients, 38% share) must be suppressed — so "similar EUR wires" can't be promised as a blanket feature. More fundamentally: this table is **Internal-classified, built only for Payment Ops dashboards, not MRM-registered, and has no TDIP Insights API endpoint** — the catalog explicitly lists wire/corridor insights as **"Not available."** |
  | **"Predicted delivery time based on client's similar past wires"** | **Closest to feasible, but still blocked** | This matches DUS-07 §6 (client's own data, ≥5 comparable transactions, state basis) — the easier bar. The matching asset, `client_wire_history_features`, exists but is an **unproductionized prototype, unregistered in MRM**, scoped **only to Swift/gpi corridors** (no domestic Fedwire equivalent — `net.fedwire.ack.v1` not ingested, tracked as backlog TDA-2210). A genuine *forward-looking* "predicted delivery time" is a **Tier 2 model minimum** under MRM-POL-02 (independent validation 10–14 weeks, 160–240 validator hours, ~6-week queue as of Q4-2026) — not the lighter EUA path, since EUA covers only backward-looking descriptive stats (count/median/p90), not a prediction. |

  **Cross-cutting blockers for all three (per ADR-PAY-026):**
  - Insights **must be computed in TDIP and served via the versioned TDIP Insights API** — never locally in `cbo-wire-bff`, directly contradicting the PM's stated assumption ("insights calculated in the CBO wire BFF from wire history").
  - Only one Insights API endpoint is GA today (`EP-TDIP-01`, cash-forecast); wire-history/corridor insights are explicitly "not available." Standing up a new endpoint is ~13–21 story points of build *after* MRM/DUS-07/DRC clearance — none of that governance work has started.
  - DRC approval (biweekly, 5-day submission lead) is required for any cohort or predictive wording regardless of data readiness.

  **Recommendation:** Drop the beneficiary-behavior stat entirely (policy-barred). Descope the cohort % and predicted-delivery-time from Q1 2027; route both through TDIP (Dr. Aisha Rahman / Treasury Data & Analytics) and MRM for Tier/EUA classification now, with DRC wording review, as a post-GA phase.
sources:
- ref: openwiki/policies/dus-07.md#Section-4
  why: Prohibits using counterparty/beneficiary behavior data from one client to generate content shown to another
    client, blocking the 'beneficiary moves funds within 4 hours' claim.
- ref: openwiki/policies/dus-07.md#Section-5
  why: Defines the cross-client cohort statistics gating criteria (volume, client count, concentration cap, refresh
    cadence, DRC approval) relevant to the '92% of similar EUR wires' claim.
- ref: openwiki/policies/dus-07.md#Section-6
  why: Defines criteria for using a client's own historical data (>=5 comparable transactions) relevant to the predicted-delivery-time
    claim.
- ref: openwiki/datasets/beneficiary-behavior-profile.md
  why: Describes bene_median_hours_to_outflow feature, its Restricted-Client Confidential classification, and its
    role as an input to Tier 1 fraud model M-FCT-0034.
- ref: openwiki/datasets/client-wire-history-features.md
  why: Describes the client_wire_history_features prototype, its MRM registration status, Swift/gpi-only scope,
    and lack of Fedwire coverage.
- ref: openwiki/interfaces/tdip-insights-api.md
  why: Documents ADR-PAY-026 requirement that insights be computed in TDIP and served via the Insights API, and
    that only EP-TDIP-01 (cash-forecast) is GA while wire/corridor insights are not available.
follow_up_questions:
- What would it take to get beneficiary behavior data cleared for cross-client use, or is it permanently barred
  under DUS-07?
- What is the roadmap and resourcing to register wire_corridor_stats_daily and client_wire_history_features in MRM
  and expose them via a new TDIP Insights API endpoint?
- Should FC-04 be rescoped to only backward-looking descriptive stats (count/median/p90) to stay within the lighter
  EUA path instead of pursuing a Tier 2 predictive model?
reasoning_summary: 'Mapped the agent''s three-claim analysis against DUS-07 (counterparty-data prohibition §4, cross-client
  cohort rules §5, client-own-history rules §6), MRM-POL-02 (Tier 1 restriction on financial-crimes outputs, Tier
  2 validation requirements for predictive models), the client-wire-history-features and beneficiary-behavior-profile
  dataset specs, and the TDIP Insights API catalog (ADR-PAY-026 requirement that insights be served via TDIP API,
  with only EP-TDIP-01 GA today). Conclusion: all three claims are blocked, one by outright policy prohibition and
  two by lack of governed data/serving infrastructure within the Q1 2027 timeline.'
trace:
  input_tokens: 73836
  output_tokens: 6347
  steps:
  - step: 1
    tool: semantic_search
    input: '"beneficiary typically moves funds within hours insight"'
    result: '8 hits: openwiki/decisions/adr-pay-026.md, openwiki/policies/dus-07.md, openwiki/systems/prism-payments-hub.md'
    ms: 1329
    refs:
    - semantic:openwiki/decisions/adr-pay-026.md
    - semantic:openwiki/policies/dus-07.md
    - semantic:openwiki/systems/prism-payments-hub.md
    - semantic:openwiki/datasets/wire-corridor-stats-daily.md
    - semantic:openwiki/datasets/client-wire-history-features.md
    - semantic:openwiki/interfaces/tdip-insights-api.md
    - semantic:openwiki/datasets/gpi-tracker-events.md
    - semantic:openwiki/policies/mrm-pol-02.md
  - step: 2
    tool: semantic_search
    input: '"percent of similar wires complete same day statistic cohort"'
    result: '8 hits: openwiki/people/andrew-feldman.md, openwiki/policies/dus-07.md, openwiki/datasets/wire-corridor-stats-daily.md'
    ms: 1329
    refs:
    - semantic:openwiki/people/andrew-feldman.md
    - semantic:openwiki/policies/dus-07.md
    - semantic:openwiki/datasets/wire-corridor-stats-daily.md
    - semantic:openwiki/datasets/gpi-tracker-events.md
    - semantic:openwiki/teams/legal-treasury-payments.md
    - semantic:openwiki/teams/privacy-office-data-governance.md
    - semantic:openwiki/interfaces/proposed-interfaces-registry.md
    - semantic:openwiki/datasets/client-wire-history-features.md
  - step: 3
    tool: semantic_search
    input: '"predicted delivery time client wire history model"'
    result: '8 hits: openwiki/datasets/client-wire-history-features.md, openwiki/datasets/pay-wire-txn-hist.md,
      openwiki/concepts/wire-lifecycle-state-model.md'
    ms: 1329
    refs:
    - semantic:openwiki/datasets/client-wire-history-features.md
    - semantic:openwiki/datasets/pay-wire-txn-hist.md
    - semantic:openwiki/concepts/wire-lifecycle-state-model.md
    - semantic:openwiki/systems/prism-payments-hub.md
    - semantic:openwiki/incidents/cmp-2026-1189.md
    - semantic:openwiki/teams/commercial-service-center.md
    - semantic:openwiki/documents/pph-sys-ovw-9.2.md
    - semantic:openwiki/policies/frs-02.md
  - step: 4
    tool: semantic_search
    input: '"TDIP insights API wire predictive model governance disclaimer"'
    result: '8 hits: openwiki/interfaces/tdip-insights-api.md, openwiki/policies/mrm-pol-02.md, openwiki/documents/mrm-pol-02.md'
    ms: 1329
    refs:
    - semantic:openwiki/interfaces/tdip-insights-api.md
    - semantic:openwiki/policies/mrm-pol-02.md
    - semantic:openwiki/documents/mrm-pol-02.md
    - semantic:openwiki/decisions/adr-pay-026.md
    - semantic:openwiki/datasets/client-wire-history-features.md
    - semantic:openwiki/systems/treasury-data-insights-platform.md
    - semantic:openwiki/people/aisha-rahman.md
    - semantic:openwiki/teams/treasury-data-analytics.md
  - step: 5
    tool: semantic_read
    input: openwiki/interfaces/tdip-insights-api.md []
    result: 8 sections, 11505 chars
    ms: 1
    refs:
    - semantic:openwiki/interfaces/tdip-insights-api.md
  - step: 6
    tool: semantic_read
    input: openwiki/policies/dus-07.md []
    result: 9 sections, 10281 chars
    ms: 0
    refs:
    - semantic:openwiki/policies/dus-07.md
  - step: 7
    tool: semantic_read
    input: openwiki/datasets/client-wire-history-features.md []
    result: 8 sections, 12180 chars
    ms: 0
    refs:
    - semantic:openwiki/datasets/client-wire-history-features.md
  - step: 8
    tool: semantic_read
    input: openwiki/datasets/beneficiary-behavior-profile.md []
    result: 7 sections, 6716 chars
    ms: 0
    refs:
    - semantic:openwiki/datasets/beneficiary-behavior-profile.md
```

## WTC-Q07 - Missing endpoints and builders

```yaml
id: WTC-Q07
title: Missing endpoints and builders
intent: The full list of endpoints, fields, events or data the feature needs that do not exist yet, with the owning
  team and any existing ticket.
example_questions:
- List every endpoint, field or event we need that doesn't exist yet, the owning team, and any existing ticket.
- What APIs are missing and who builds them?
- Give me the gap list of interfaces we need.
- Which endpoints don't exist yet for this feature?
recorded_question: ''
recorded_at: '2026-10-12T05:36:56+00:00'
recorded_model: claude-sonnet-5
recorded_latency_ms: 32839
confidence: medium
answer: |-
  **Verdict:** Across FC-01–FC-05/FC-07, at least 9 distinct endpoints/fields/events needed for the Wire Tracking Center do not exist today. None has a committed delivery date inside Q1 2027.

  | # | Missing endpoint / field / event | Needed for | Owning team | Existing ticket / status |
  |---|---|---|---|---|
  | 1 | **PPH v2 `lifecycleState` wired into `cbo-wire-bff`** (replacing v1's collapsed `PROCESSED`) | FC-01 accurate timeline, compliant "Settled" | Payments Hub Engineering (Sunita Rao) / CBO Wire Center (Tom Becker) | **CBO-4471** — Migrate Wire Center PPH v1→v2, 34 pts, proposed/unscheduled, blocked on **CBO-4473**; must land before v1 sunset 2027-03-31 (**PPH-2190**) |
  | 2 | **PPH v2 settlement object** (`fedSettlementTs`, `settlementStatus`) distinguishing network-accepted vs. true accounting completion | FC-01 "Settled" semantics per POL-FCC-014 §5.2 | Payments Hub Engineering | **PPH-2207** — backlog, **no sponsor** |
  | 3 | **gpi Tracker Real-Time Service (GTRS)** — change-feed/event API replacing the 4-hour `GPI_TRACKER_SNAPSHOT` batch | FC-02 live map, FC-02 "Expected delivery: Today" | GTSI (Elena Vasquez) | **GTSI-0107** — proposed, not funded for 2026; discovery 2027-Q2, build 2027-Q3/Q4; spike **CBO-4480** (To Do) is the Wire Center-side ask |
  | 4 | **Client-Safe Hold Status Facade** `GET /prsp/hms/v1/holds/{holdId}/client-view` (disclosure tier + approved copy key only, no raw reason) | FC-03 hold-reason display without leaking restricted detail | Financial Crimes Technology (Daniel Kowalski / Grace Mensah) | **FCT-1893** — 21 pts, backlog, **deprioritized 2025-Q3** |
  | 5 | **Remediation of PPH v1 `holdReasonDesc` leak** (stop sync or redact at gateway) | Prerequisite before FC-03 can safely show any reason | PPH (Sunita Rao) + CBO (Tom Becker), tracked by FCT | **FCT-2004** — open risk, no fix date; may only close via v1 sunset |
  | 6 | **Digital client attestation (Confirm/Cancel) for HRC-01 holds** | FC-03 self-service action | Financial Crimes Technology | Piloted phone-only via **FCT-1951** (closed); digital facade is same unbuilt **FCT-1893** |
  | 7 | **ENS entity-level subscription** (subscribe by `paymentId`/`caseId`, not just event-type) | FC-05 "notify me when this wire settles" | Enterprise Notification Platform (Melissa Grant) | **ENS-1120** — proposed/Planned, target 2027-H1 |
  | 8 | **TDIP wire-history / corridor Insights API endpoint(s)** (serving layer per ADR-PAY-026; e.g. predicted delivery time, % same-day completion) | FC-04 all three insight claims | Treasury Data & Insights Platform (Dr. Aisha Rahman) | None filed yet — catalog states "not available"; `client_wire_history_features` and `wire_corridor_stats_daily` exist as datasets (TDA-2140 done) but have no serving endpoint or MRM/DRC clearance |
  | 9 | **Domestic Fedwire acknowledgment ingestion** (`net.fedwire.ack.v1`) into TDIP | FC-04 predicted delivery for domestic wires (currently gpi/Swift-corridor only) | Treasury Data & Insights Platform | **TDA-2210** — backlog |

  **Not a missing endpoint but a hard blocker regardless of build:** the beneficiary-behavior stat ("Beneficiary typically moves funds within 4 hours") uses `bene_median_hours_to_outflow`, a Tier 1 MRM field barred from client-facing use (MRM-POL-02 §4) and a DUS-07 §4 violation — no ticket would make this buildable; it requires a policy exception, not an engineering gap.

  **Also note:** item 1's blocker, **CBO-4473**, and item 2's **PPH-2207** both lack assigned owners/sponsors in the registry — these need sponsorship decisions before CBO-4471 can even be scheduled.

  **Net for BRD:** every FC that depends on real-time gpi (FC-02), predictive/cohort insight (FC-04), differentiated hold reasons or self-service action (FC-03), or per-wire notification (FC-05) requires work items that are either unfunded, unscheduled, or policy-blocked — none currently projects completion by Q1 2027.
sources:
- ref: openwiki/projects/cbo-4471-pph-v1-to-v2-migration.md
  why: PPH v1->v2 migration ticket, status, blocker CBO-4473, 34pts
- ref: openwiki/interfaces/cbo-wire-bff-api.md
  why: confirms CBO-4471 unscheduled, sunset deadline linkage
- ref: openwiki/projects/jira-backlog-registry.md
  why: authoritative list of ticket IDs/owners/status including PPH-2207, FCT-1893, FCT-2004, TDA-2210
- ref: openwiki/interfaces/tdip-insights-api.md
  why: confirms only EP-TDIP-01 live, no wire-history/corridor insights endpoint exists
- ref: openwiki/decisions/adr-pay-026.md
  why: confirms TDIP-only computation rule and that coverage gaps block launches
- ref: openwiki/datasets/client-wire-history-features.md
  why: prototype status, gpi-only scope for predicted delivery feature
- ref: openwiki/projects/gtsi-0107-gpi-real-time-service.md
  why: gpi real-time service funding/timeline status
- ref: openwiki/projects/ens-1120-entity-level-subscriptions.md
  why: entity-level subscription ticket, owner, target date
- ref: openwiki/projects/fct-1951-duplicate-suspect-attestation-pilot.md
  why: confirms FCT-1893 facade details and FCT-1951 phone-only pilot closure
- ref: openwiki/people/daniel-kowalski.md
  why: confirms FCT-1893/FCT-2004 blocking relationship and ownership
follow_up_questions: []
reasoning_summary: ''
trace:
  input_tokens: 54369
  output_tokens: 3318
  steps:
  - step: 1
    tool: semantic_search
    input: '"PPH v2 wire lifecycle endpoint lifecycleState field migration CBO-4471"'
    result: '8 hits: openwiki/projects/cbo-4471-pph-v1-to-v2-migration.md, openwiki/projects/pph-2190-v1-sunset-migration.md,
      openwiki/systems/commercial-entitlements-service.md'
    ms: 453
    refs:
    - semantic:openwiki/projects/cbo-4471-pph-v1-to-v2-migration.md
    - semantic:openwiki/projects/pph-2190-v1-sunset-migration.md
    - semantic:openwiki/systems/commercial-entitlements-service.md
    - semantic:openwiki/interfaces/pph-v1-wire-status-api.md
    - semantic:openwiki/interfaces/pph-v2-payments-api.md
    - semantic:openwiki/interfaces/cbo-wire-bff-api.md
    - semantic:openwiki/interfaces/ces-entitlements-api.md
    - semantic:openwiki/people/tom-becker.md
  - step: 2
    tool: semantic_search
    input: '"TDIP Insights API endpoint naming convention new endpoint wire corridor"'
    result: '8 hits: openwiki/interfaces/tdip-insights-api.md, openwiki/datasets/client-wire-history-features.md,
      openwiki/decisions/adr-pay-026.md'
    ms: 452
    refs:
    - semantic:openwiki/interfaces/tdip-insights-api.md
    - semantic:openwiki/datasets/client-wire-history-features.md
    - semantic:openwiki/decisions/adr-pay-026.md
    - semantic:openwiki/datasets/pay-wire-txn-hist.md
    - semantic:openwiki/datasets/cbo-wire-events.md
    - semantic:openwiki/people/aisha-rahman.md
    - semantic:openwiki/systems/treasury-data-insights-platform.md
    - semantic:openwiki/policies/dus-07.md
  - step: 3
    tool: semantic_search
    input: '"ENS entity-level subscription per-payment ENS-1120"'
    result: '8 hits: openwiki/projects/ens-1120-entity-level-subscriptions.md, openwiki/projects/cbo-3790-ach-payment-tracker.md,
      openwiki/people/melissa-grant.md'
    ms: 20
    refs:
    - semantic:openwiki/projects/ens-1120-entity-level-subscriptions.md
    - semantic:openwiki/projects/cbo-3790-ach-payment-tracker.md
    - semantic:openwiki/people/melissa-grant.md
    - semantic:openwiki/systems/enterprise-notification-service.md
    - semantic:openwiki/teams/enterprise-notification-platform.md
    - semantic:openwiki/interfaces/ens-notification-api-trs-catalog.md
    - semantic:openwiki/interfaces/sps-read-model-api.md
    - semantic:openwiki/people/sanjay-iyer.md
  - step: 4
    tool: semantic_search
    input: '"FCT-1893 client-safe hold status facade endpoint"'
    result: '8 hits: openwiki/people/daniel-kowalski.md, openwiki/interfaces/hms-hold-api.md, openwiki/systems/sentinel-fraud-scoring.md'
    ms: 20
    refs:
    - semantic:openwiki/people/daniel-kowalski.md
    - semantic:openwiki/interfaces/hms-hold-api.md
    - semantic:openwiki/systems/sentinel-fraud-scoring.md
    - semantic:openwiki/projects/jira-backlog-registry.md
    - semantic:openwiki/interfaces/pph-v1-wire-status-api.md
    - semantic:openwiki/projects/fct-1951-duplicate-suspect-attestation-pilot.md
    - semantic:openwiki/people/grace-mensah.md
    - semantic:openwiki/people/victor-petrov.md
```

## WTC-Q08 - Per-wire notifications

```yaml
id: WTC-Q08
title: Per-wire notifications
intent: Whether a client can subscribe to notifications for one specific wire (for example 'notify me when it settles'),
  and the workaround and lead times.
example_questions:
- Can a client subscribe to a single wire - 'notify me when it settles'?
- Can we notify a client when one particular wire settles?
- Do per-wire alerts work with the notification service?
- Is 'notify me when this wire settles' possible?
recorded_question: ''
recorded_at: '2026-10-12T05:37:30+00:00'
recorded_model: claude-sonnet-5
recorded_latency_ms: 33823
confidence: medium
answer: |-
  **Verdict: No — not for a single wire today, and not even for "settled" in any form. ENS subscriptions are per-user/per-event-type only, with no concept of an individual `paymentId`, and there is no "settled" event in the catalog at all — the closest live event is actually mislabeled "completed" and fires at release, repeating the same semantics problem already flagged for FC-01.**

  **Why "subscribe to this one wire" can't be built as-is**

  | Constraint | Detail | Source |
  |---|---|---|
  | Subscription granularity | ENS subscriptions (`POST /ens/v3/subscriptions`) are created **per user, per event type**, with only `accountId` and amount-threshold filters — "this is the entire granularity ENS supports today... there is no field for an individual entity identifier such as a specific `paymentId`." | `openwiki/interfaces/ens-notification-api-trs-catalog.md` |
  | What's planned to fix it | **ENS-1120** — entity-level subscriptions (subscribe to a specific `paymentId`/`caseId`) — status **Planned**, owner **Melissa Grant**, target **2027-H1** | `openwiki/projects/ens-1120-entity-level-subscriptions.md` |
  | Interim workaround | "Producer-resolved recipients" pattern: the producer (`cbo-wire-bff`) itself would track the subscription intent and call `POST /ens/v3/notifications` directly for a named user, bypassing ENS matching — a custom build inside Wire Center, not an ENS capability | `openwiki/systems/enterprise-notification-service.md` |

  **Why "settles" specifically has no event to hook into**
  - The TRS catalog (ENS-INT-3.2 §4) explicitly states: **"no event types are registered for wire network acceptance, beneficiary credit (gpi ACCC), wire returns, gpi milestones, or client action required on held wires."**
  - Wire Center today produces only 3 live events, all driven off coarse **PPH v1** status: `TRS.WIRE.APPROVAL_REQUIRED`, `TRS.WIRE.RELEASED` (fires when PPH v1 status → `PROCESSED`, template literally titled *"Wire completed: {amount} to {beneficiary}"*), and `TRS.WIRE.REJECTED`. There is no `TRS.WIRE.SETTLED` or equivalent.
  - This is the same root cause as the FC-01 "Completed" problem: `TRS.WIRE.RELEASED`'s own template already overclaims "completed" at release, so even per-user subscription today would notify at the wrong (too-early) point, not true settlement.
  - A genuine "settled" event requires PPH v2 lifecycle data or gpi ACCC, neither of which feeds ENS yet — same dependency chain as FC-01/FC-02 (`CBO-4471`, `GTSI-0107`).

  **What it would take to build FC-05 as specified:**
  1. **ENS-1120** shipped (2027-H1 target — after Q1 2027 GA) for per-wire subscription granularity, owned by Melissa Grant/Enterprise Notification Platform.
  2. A new **TRS event type** for true settlement, which requires the 6-week ENS onboarding SLA (ServiceNow "ENS Event Onboarding," payload/recipient design, DRC template review, ~12 eng hours) — and that event can only be *accurate* once Wire Center consumes PPH v2 or gpi data (same `CBO-4471`/`GTSI-0107` dependency already identified).
  3. Any new event submitted after **2026-11-20** falls behind the year-end change freeze, further squeezing the Q1 2027 timeline.

  **Net:** per-wire "notify me when it settles" is blocked on two unshipped items (ENS-1120 and a correctly-timed settlement event) plus the standard 6-week onboarding SLA — none of which can land before Q1 2027 GA under current roadmaps.
sources:
- ref: openwiki/interfaces/ens-notification-api-trs-catalog.md
  why: Documents ENS subscription granularity (per-user/per-event-type, no per-paymentId support) and the explicit
    statement that no event types are registered for settlement-related wire events.
follow_up_questions:
- What is the current status and timeline of ENS-1120 (entity-level subscriptions)?
- Is there a workaround using the producer-resolved recipients pattern that could approximate per-wire notification
  before ENS-1120 ships?
- When will Wire Center begin consuming PPH v2 or gpi ACCC data needed for a true 'settled' event?
reasoning_summary: Formatted the provided answer into structured output, citing only the ref confirmed as read by
  the agent (ens-notification-api-trs-catalog.md). Other referenced documents (ens-1120 project page, enterprise-notification-service.md)
  were not in the confirmed read list, so they are omitted from sources per instructions.
trace:
  input_tokens: 57157
  output_tokens: 3709
  steps:
  - step: 1
    tool: semantic_search
    input: '"ENS subscription by paymentId entity-level notification wire"'
    result: '8 hits: openwiki/systems/enterprise-notification-service.md, openwiki/projects/ens-1120-entity-level-subscriptions.md,
      openwiki/people/melissa-grant.md'
    ms: 474
    refs:
    - semantic:openwiki/systems/enterprise-notification-service.md
    - semantic:openwiki/projects/ens-1120-entity-level-subscriptions.md
    - semantic:openwiki/people/melissa-grant.md
    - semantic:openwiki/interfaces/ens-notification-api-trs-catalog.md
    - semantic:openwiki/teams/enterprise-notification-platform.md
    - semantic:openwiki/people/sanjay-iyer.md
    - semantic:openwiki/interfaces/hms-hold-api.md
    - semantic:openwiki/interfaces/sps-read-model-api.md
  - step: 2
    tool: semantic_search
    input: '"Enterprise Notification Service subscription model user event type today"'
    result: '8 hits: openwiki/teams/enterprise-notification-platform.md, openwiki/people/melissa-grant.md, openwiki/interfaces/sps-read-model-api.md'
    ms: 474
    refs:
    - semantic:openwiki/teams/enterprise-notification-platform.md
    - semantic:openwiki/people/melissa-grant.md
    - semantic:openwiki/interfaces/sps-read-model-api.md
    - semantic:openwiki/people/sanjay-iyer.md
    - semantic:openwiki/people/paul-henderson.md
    - semantic:openwiki/systems/cbo-status-projection-service.md
    - semantic:openwiki/systems/enterprise-notification-service.md
    - semantic:openwiki/projects/cbo-3790-ach-payment-tracker.md
  - step: 3
    tool: semantic_read
    input: openwiki/interfaces/ens-notification-api-trs-catalog.md []
    result: 9 sections, 8424 chars
    ms: 0
    refs:
    - semantic:openwiki/interfaces/ens-notification-api-trs-catalog.md
  - step: 4
    tool: semantic_read
    input: openwiki/systems/enterprise-notification-service.md [producer-resolved recipients]
    result: 'Error: unknown heading ''producer-resolved recipients'' on openwiki/systems/enterprise-notification-service.md;
      available: Overview, Responsibilities and platform limits, Event onboarding process, Subsc'
    ms: 0
    refs: []
```

## WTC-Q09 - Prior attempts and reuse

```yaml
id: WTC-Q09
title: Prior attempts and reuse
intent: Whether wire tracking was attempted before, what went wrong, what to avoid and what can be reused.
example_questions:
- Has anyone attempted wire tracking before? What should we avoid, and what can we reuse?
- Was this tried before?
- Any lessons learned from earlier wire status projects?
- What existing components can we reuse for the tracker?
recorded_question: ''
recorded_at: '2026-10-12T05:38:12+00:00'
recorded_model: claude-sonnet-5
recorded_latency_ms: 42446
confidence: high
answer: |-
  **Verdict: Yes — two prior attempts exist, one a cautionary tale (avoid repeating it) and one a near-complete reusable blueprint (reuse it directly). Both are directly on point for Wire Tracking Center.**

  **1. What to avoid — Wire Status Lite (CBO-3120, 2024)**

  | Fact | Detail |
  |---|---|
  | What it did | Browser auto-refreshed every visible wire's status from PPH v1 (`GET /pph/v1/wires/{ref}/status`) every 30 seconds, piloted with 60 clients, Jan–May 2024 |
  | What happened | 2024-05-31 (month-end): pilot + production refreshes drove ~85 TPS against PPH's shared synchronous API, exhausting its thread pool — **INC-2024-1182** |
  | Quantified damage (PIR-2024-07) | 1,240 wires delayed; 312 missed the 6:00 p.m. ET Fedwire cutoff (value pushed next day); **14 clients compensated, $41,800** in interest claims; no regulatory notification required (delay, not data exposure) |
  | Root causes | (1) fixed-interval polling with no backoff against a shared sync API; (2) never load-tested at month-end volumes; (3) **status semantics not validated with Compliance/Legal before exposure** |
  | Client-understanding finding | **37% of surveyed pilot users believed "Processed" meant the beneficiary had received funds** — it actually collapsed release/transmission/network-ack/EOD-close into one label. Users valued three things most: confirmation the wire left CNB, the Fed IMAD/OMAD reference, and international credit timing — not granular lifecycle detail |
  | Held-wire gap already seen | Treasury Support couldn't explain holds to clients without FCC guidance — the exact FC-03 problem, first surfaced here in 2024 |
  | Resulting rules | **ADR-PAY-019** (no PPH polling, event-driven only) — directly governs why FC-01/FC-02's refresh design must not poll |
  | **Still-open action** | "Validate client-facing status terminology with FCC and Legal **before any future tracking feature**" — owner CBO Product, never closed. CBO's later unilateral rename to "Completed" (R26.1) skipped this gate and caused **CMP-2026-1189**, the complaint ticket already linked to your FC-01 discussion. **This gate must be satisfied before FC-01 ships, not after.** |

  **2. What to reuse — ACH Payment Tracker (CBO-3790, Done R25.4/2025-11)**

  Built *because of* the Wire Status Lite failure, as the PIR's "build a reusable status projection service" action:

  | Reusable asset | What it is | Reuse status for wires |
  |---|---|---|
  | `<cbo-journey-timeline>` (CBO-3802, Aurora DS v4) | Rail-agnostic milestone timeline UI, terminal/error styling | Explicitly designed to be reused as-is — "front-end half of a future wire-tracking feature" per architecture docs |
  | **CBO Status Projection Service (SPS, CBO-3815)** | Kafka consumer → Postgres read model → `GET /cbo/sps/v1`, decouples CBO from any synchronous PPH call | **Configured for ACH only today.** Reusable storage/API layer, but wire support needs net-new work: (1) a consumer ACL on `pay.wire.lifecycle.v2` (~3 weeks via PPH, incl. Confluent schema-registry access), (2) a **new mapping module** from PPH v2's 13 lifecycle states to client milestones (not reusable from ACH — different state machine) |
  | ADR-PAY-019 (reaffirmed by ARB 2026-09-08 as "the reference pattern for client-facing status of any payment type") | Governance mandate | Confirms SPS is the sanctioned architecture Wire Tracking Center must build on, not an alternative polling design |

  **Constraints that carry over even once wire is onboarded to SPS:**
  - **No hold reasons via this path either** — ADR-PAY-021 means `pay.wire.lifecycle.v2` carries only hold *presence* + `holdId`, never reason/score/notes, so SPS would show a wire is held but not why — same FC-03 gap already flagged, not solved by this reuse.
  - Return reasons only available since PPH-2266 (2026-08).
  - **No Jira story currently exists** requesting the ACL or mapping module — it's referenced only in CBO-3815's closing comment and architecture docs, not a scheduled backlog item.
  - Cross-team build: SPS owned by **CBO Platform & Entitlements** (Arjun Mehta/Marcus Chen), separate from **CBO Wire Center squad** (Tom Becker/Lucas Ferreira) — not a Wire Center-only estimate, contradicting the PM's "mostly front-end, 1.5 PIs" assumption.

  **Net:** Reuse the timeline component and SPS pattern as the Q1 2027 architecture target; but budget for the ACL + mapping module as new, unscheduled cross-team work, and treat the FCC/Legal terminology validation as a hard precondition before any status label ships — it's the one PIR-2024-07 action still open two years later.
sources:
- ref: openwiki/incidents/pir-2024-07.md
  why: Source for Wire Status Lite incident details, root causes, damages, client-understanding survey, and the
    still-open terminology validation action
- ref: openwiki/projects/cbo-3790-ach-payment-tracker.md
  why: Source for the ACH Payment Tracker project built in response to PIR-2024-07, including the reusable timeline
    component and SPS build
- ref: openwiki/systems/cbo-status-projection-service.md
  why: Source for SPS architecture, current ACH-only configuration, ownership, and constraints (ADR-PAY-019/021,
    hold reason limitations) relevant to reusing it for wires
follow_up_questions:
- Has a Jira story been created yet for the pay.wire.lifecycle.v2 consumer ACL and mapping module work?
- What is the current status of the FCC/Legal terminology validation gate from PIR-2024-07?
- Can PPH-2266's return reason data be incorporated into the wire lifecycle mapping module from the start?
reasoning_summary: Compiled findings from the Wire Status Lite post-incident review (PIR-2024-07), the ACH Payment
  Tracker project doc (CBO-3790), and the CBO Status Projection Service system doc to answer whether prior wire
  tracking attempts exist, what to avoid, and what can be reused.
trace:
  input_tokens: 70715
  output_tokens: 4777
  steps:
  - step: 1
    tool: semantic_search
    input: '"previous wire tracking project attempt history lessons learned"'
    result: '8 hits: openwiki/incidents/pir-2024-07.md, openwiki/teams/gtsi.md, openwiki/projects/cbo-3790-ach-payment-tracker.md'
    ms: 677
    refs:
    - semantic:openwiki/incidents/pir-2024-07.md
    - semantic:openwiki/teams/gtsi.md
    - semantic:openwiki/projects/cbo-3790-ach-payment-tracker.md
    - semantic:openwiki/projects/cbo-4471-pph-v1-to-v2-migration.md
    - semantic:openwiki/projects/pph-2190-v1-sunset-migration.md
    - semantic:openwiki/projects/jira-backlog-registry.md
    - semantic:openwiki/datasets/pay-wire-txn-hist.md
    - semantic:openwiki/datasets/client-wire-history-features.md
  - step: 2
    tool: semantic_search
    input: '"Wire Status Lite polling pilot CBO-3120 incident post-incident review"'
    result: '8 hits: openwiki/projects/cbo-3120-wire-status-lite-pilot.md, openwiki/incidents/inc-2024-1182.md,
      openwiki/interfaces/pph-v1-wire-status-api.md'
    ms: 677
    refs:
    - semantic:openwiki/projects/cbo-3120-wire-status-lite-pilot.md
    - semantic:openwiki/incidents/inc-2024-1182.md
    - semantic:openwiki/interfaces/pph-v1-wire-status-api.md
    - semantic:openwiki/incidents/pir-2024-07.md
    - semantic:openwiki/people/anjali-deshpande.md
    - semantic:openwiki/people/tom-becker.md
    - semantic:openwiki/decisions/adr-pay-019.md
    - semantic:openwiki/systems/cbo-status-projection-service.md
  - step: 3
    tool: semantic_search
    input: '"wire tracker prototype deprecated discontinued"'
    result: '8 hits: openwiki/datasets/client-wire-history-features.md, openwiki/systems/investigations-workbench.md,
      openwiki/interfaces/pph-v1-wire-status-api.md'
    ms: 677
    refs:
    - semantic:openwiki/datasets/client-wire-history-features.md
    - semantic:openwiki/systems/investigations-workbench.md
    - semantic:openwiki/interfaces/pph-v1-wire-status-api.md
    - semantic:openwiki/projects/gtsi-0107-gpi-real-time-service.md
    - semantic:openwiki/datasets/gpi-tracker-events.md
    - semantic:openwiki/projects/cbo-3790-ach-payment-tracker.md
    - semantic:openwiki/systems/treasury-data-insights-platform.md
    - semantic:openwiki/datasets/pay-wire-txn-hist.md
  - step: 4
    tool: semantic_read
    input: openwiki/incidents/pir-2024-07.md []
    result: 7 sections, 8610 chars
    ms: 2
    refs:
    - semantic:openwiki/incidents/pir-2024-07.md
  - step: 5
    tool: semantic_read
    input: openwiki/projects/cbo-3790-ach-payment-tracker.md []
    result: 9 sections, 8604 chars
    ms: 1
    refs:
    - semantic:openwiki/projects/cbo-3790-ach-payment-tracker.md
  - step: 6
    tool: semantic_read
    input: openwiki/systems/cbo-status-projection-service.md []
    result: 7 sections, 12727 chars
    ms: 1
    refs:
    - semantic:openwiki/systems/cbo-status-projection-service.md
```

## WTC-Q10 - Effort, engagement plan and critical path

```yaml
id: WTC-Q10
title: Effort, engagement plan and critical path
intent: 'The BRD dependency, effort and engagement plan: teams to engage, hours per team, approvals, lead times,
  phasing and the critical path.'
example_questions:
- 'Draft the dependency, effort and engagement section of the BRD: which teams to talk to, how many hours to allocate,
  approvals, lead times and the critical path.'
- How many hours and which teams will this take?
- Give me the effort estimate and critical path.
- Write the engagement plan for the BRD.
recorded_question: 'Draft the dependency, effort and engagement section of the BRD. For every engineering team and
  approval function: scope, size in story points from the tickets, hours (apply the planning factors from the engagement
  directory to those sizes), lead time or gate, and contact. Then give the total hours, the critical path, a phased
  plan, and the actions for this week.'
recorded_at: '2026-10-12T05:49:43+00:00'
recorded_model: claude-sonnet-5
recorded_latency_ms: 168290
confidence: medium
answer: |-
  ## Verdict
  Current ticket-sized, estate-documented dependency work totals **~717 engineering/ops/compliance hours** (plus a separate **160–240 MRM validator-hour** block), but several critical-path items (PPH v1→v2, the hold facade, gpi real-time, Insights) are **unscheduled, deprioritized, unsponsored or unfunded** — the Feb 2027 pilot date is not achievable against the wiki's own lead times.

  ### Engineering teams

  | Team (contact) | Scope (ticket) | Points | Hours (planning factor) | Lead time / gate |
  |---|---|---|---|---|
  | CBO Wire Center squad — Tom Becker (EM), Lucas Ferreira (TL), Marcus Chen (PO); Jira CBO | CBO-4471: migrate `cbo-wire-bff` PPH v1→v2 (prereq for v2 `lifecycleState`, UETR/OMAD) | 34 pts | 221 hrs (1pt≈6.5h) | Unscheduled; deadline 2027-03-31 (no extension, ARB 2026-09-08); ~85% committed PI27.1 |
  | CBO Wire Center squad | CBO-4480: gpi visibility discovery spike only | 3 pts | 19.5 hrs | Unscheduled, To Do |
  | CBO Platform & Entitlements — Nadia Haddad (EM), Arjun Mehta (TL); Jira CBO (Platform), 2-wk triage | CBO-4473: CES account-filter mapping for PPH v2 search (blocks CBO-4471) | 8 pts | 52 hrs | Backlog; ~70% committed |
  | CBO Platform & Entitlements | SPS wire extension (new `pay.wire.lifecycle.v2` ACL + mapping module) — prerequisite for event-driven FC-01/05 | **not sized** | n/a | No ticket filed |
  | Payments Hub Engineering — Kevin O'Brien, Sunita Rao; Demand Board | PPH-2207: v2 settlement object (fedSettlementTs) | **not sized, no sponsor** | n/a | 6–8 wk scheduling lead; ~90% committed (heaviest) |
  | GTSI — Elena Vasquez (Dir), Omar Siddiqui (EM); Jira GTSI | GTSI-0115: Swift gpi contract renewal (due 2027-01-31) | **not sized** | n/a | Quarterly roadmap intake; ~75% committed |
  | GTSI | GTSI-0107: real-time gpi tracker service (needed for FC-02's "live map, refreshed every minute") | **not sized, unfunded 2026** | n/a | Discovery 2027-Q2, build 2027-Q3/Q4 |
  | Financial Crimes Technology — Victor Petrov (Dir), Grace Mensah (EM), Daniel Kowalski (TL); FCT Change Advisory | FCT-1893: client-safe hold facade (needed for FC-03 reasons/Confirm-Reject) | 21 pts | 168 + 20% compliance testing = **202 hrs** | Deprioritized 2025-Q3; bi-weekly advisory, 5-day lead, FCC sign-off; year-end freeze Dec15–Jan5 |
  | Enterprise Notification Platform — Melissa Grant (EM), Sanjay Iyer | 4 missing TRS.WIRE.* event types (network acceptance, gpi milestones, returns, held-wire action) | n/a | ~12 hrs/event = **48 hrs** | ServiceNow onboarding, 6-wk SLA each; submit before 2026-11-20 freeze |
  | Enterprise Notification Platform | ENS-1120: entity-level subscriptions (needed for FC-05 per-wire "notify me") | **not sized** | n/a | Planned, target 2027-H1 |
  | Treasury Data & Analytics (TDIP) — Wei Zhang (Dir), Carlos Mendes | TDA-2210: ingest fed_ack_events; TDA-2188: gpi_tracker_events hourly | 8 + 5 pts | 48 + 30 = **78 hrs** | TDA-2210 blocked on PNE Kafka ACL, no sponsor; TDA-2188 in progress, target 2026-11 |
  | TDIP | New Insights API endpoint for FC-04 (required by ADR-PAY-026) | **not sized, no ticket** | n/a | n/a |

  ### Approval/partner gates

  | Gate (contact) | Scope | Hours | Lead time |
  |---|---|---|---|
  | MRM — Sophie Laurent/Jonathan Price | FC-04 is a customer-facing estimate → Tier 2 minimum | 160–240 validator hrs | 6-wk queue + 10–14 wk validation; register in Archer *before dev starts* |
  | Privacy Office — Rachel Goldberg/Ethan Brooks | PIA for FC-06 share link (external client data) | not stated | ~4 weeks (OneTrust) |
  | InfoSec (SECREV) — Farah Ali | SEC-STD-22 review for external sharing + step-up (FC-06) | 24–40 hrs | 3-week SLA |
  | Disclosure Review Committee — Patricia Moore | Approves all new client-facing copy (FC-01/03/04/05/07) | not stated | Bi-weekly, 5-day lead |
  | FCC Policy & Advisory — Jordan Ellis/Catherine Doyle | Hold-reason copy, FC-03 | not stated | ~10 business days; via FCT Change Advisory |
  | ARB — Nikhil Bose/Jenna Ross | New client-facing payment integrations (gpi real-time, Insights API, SPS wire extension, share-link) | not stated | Monthly, 10-day lead |
  | Payment Operations — Denise Carter/Luis Ramirez/Tanya Brooks | Ops Readiness Review, SOPs for any new client-facing workflow | **40 hrs** | 4 weeks pre go-live |
  | Commercial Service Center — Kim Nguyen | Readiness checklist, scripts/training | **24 hrs** | 3 weeks pre go-live |

  ### Totals, critical path, phasing
  - **Sized total: ~717 hrs** (221+19.5+52+202+48+78+40+24=684.5, +InfoSec midpoint 32 ≈ **717 hrs**), **plus 160–240 MRM validator hours**, **plus unsized work** (SPS extension, PPH-2207, GTSI-0115/0107, ENS-1120, TDIP Insights API) and the WTC front-end build itself — none of which the wiki sizes.
  - **Critical path:** CBO-4473 (8pt) → CBO-4471 (34pt) → PPH v1 sunset 2027-03-31 (no extension). This chain is unscheduled today, against ~90% committed PPH capacity and ~85% committed Wire Center capacity, and alone makes a Feb-2027 pilot infeasible without PI27.1 prioritization (dependency asks due **2026-11-06**).
  - **Phasing:** Phase 1 (PI27.1) — CBO-4473→CBO-4471, ENS new events (submit before 2026-11-20 freeze), TDA-2210/2188. Phase 2 — SPS wire extension, FCT-1893 re-prioritization, Ops/CSC readiness. Phase 3 — FC-02 real gpi (blocked on unfunded GTSI-0107, earliest 2027-Q3/Q4). Phase 4 — FC-04 Insights (MRM Tier 2, ~20-week total lead) and FC-06 (PIA+InfoSec+DRC).
  - **This week:** file PI27.1 dependency asks for CBO-4473/CBO-4471/SPS extension and PPH-2207 sponsorship; push FCT Change Advisory to re-prioritize FCT-1893 and resolve FCT-2004; register a candidate Wire Insights model with MRM (Sophie Laurent) before any build; submit ENS Event Onboarding tickets before 2026-11-20; open ARB intake for the architecture pattern; engage Privacy/InfoSec for FC-06 scoping; notify Payment Operations and CSC given their 4-/3-week readiness leads.
sources:
- ref: openwiki/projects/jira-backlog-registry.md
  why: Source of ticket sizes (story points) and team/ticket scope details
- ref: openwiki/documents/cnb-org-ptt-2026-06.md
  why: Team contacts, capacity commitments, and planning factors
- ref: openwiki/documents/jira-export-wt-discovery-2026-10-05.md
  why: Ticket status, lead times, and discovery details for dependency tickets
- ref: openwiki/projects/cbo-4471-pph-v1-to-v2-migration.md
  why: Critical-path PPH v1 to v2 migration details and deadline
- ref: openwiki/teams/payment-operations.md
  why: Ops Readiness Review hours and lead time
- ref: openwiki/interfaces/ens-notification-api-trs-catalog.md
  why: ENS event onboarding hours and SLA/freeze dates
- ref: openwiki/teams/model-risk-management.md
  why: MRM validator hours and Tier 2 validation lead time
follow_up_questions:
- Should we request formal sizing/ticket creation for the currently unsized items (SPS extension, PPH-2207, GTSI-0107,
  ENS-1120, TDIP Insights API) before the PI27.1 planning deadline?
- Who owns escalation to secure PPH-2207 sponsorship given Payments Hub Engineering is already ~90% committed?
- What is the fallback plan or revised pilot date if the CBO-4473 to CBO-4471 critical path cannot be prioritized
  in PI27.1?
reasoning_summary: Reformatted the agent's prior answer into the structured submission schema without altering content,
  pulling citations from the list of refs the agent actually read.
trace:
  input_tokens: 355484
  output_tokens: 17496
  steps:
  - step: 1
    tool: semantic_search
    input: '"engagement directory planning factor hours per story point"'
    result: '8 hits: openwiki/teams/treasury-data-analytics.md, openwiki/documents/cnb-org-ptt-2026-06.md, openwiki/teams/cbo-platform-entitlements.md'
    ms: 362
    refs:
    - semantic:openwiki/teams/treasury-data-analytics.md
    - semantic:openwiki/documents/cnb-org-ptt-2026-06.md
    - semantic:openwiki/teams/cbo-platform-entitlements.md
    - semantic:openwiki/teams/cbo-wire-center-squad.md
    - semantic:openwiki/people/arjun-mehta.md
    - semantic:openwiki/people/nadia-haddad.md
    - semantic:openwiki/people/wei-zhang.md
    - semantic:openwiki/people/marcus-chen.md
  - step: 2
    tool: semantic_search
    input: '"CBO-4480 gpi spike story points ticket"'
    result: '8 hits: openwiki/people/lucas-ferreira.md, openwiki/projects/jira-backlog-registry.md, openwiki/projects/gtsi-0107-gpi-real-time-service.md'
    ms: 361
    refs:
    - semantic:openwiki/people/lucas-ferreira.md
    - semantic:openwiki/projects/jira-backlog-registry.md
    - semantic:openwiki/projects/gtsi-0107-gpi-real-time-service.md
    - semantic:openwiki/systems/investigations-workbench.md
    - semantic:openwiki/people/arjun-mehta.md
    - semantic:openwiki/systems/cbo-status-projection-service.md
    - semantic:openwiki/incidents/cmp-2026-1189.md
    - semantic:openwiki/decisions/png-1544.md
  - step: 3
    tool: semantic_read
    input: openwiki/projects/jira-backlog-registry.md []
    result: 1 section, 2325 chars
    ms: 0
    refs:
    - semantic:openwiki/projects/jira-backlog-registry.md
  - step: 4
    tool: semantic_read
    input: openwiki/documents/cnb-org-ptt-2026-06.md []
    result: 12 sections, 11146 chars
    ms: 0
    refs:
    - semantic:openwiki/documents/cnb-org-ptt-2026-06.md
  - step: 5
    tool: semantic_search
    input: '"story points estimate PPH-2207 GTSI-0115 FCT-1893 TDA-2210"'
    result: '8 hits: openwiki/projects/jira-backlog-registry.md, openwiki/interfaces/hms-hold-api.md, openwiki/interfaces/pph-v1-wire-status-api.md'
    ms: 4088
    refs:
    - semantic:openwiki/projects/jira-backlog-registry.md
    - semantic:openwiki/interfaces/hms-hold-api.md
    - semantic:openwiki/interfaces/pph-v1-wire-status-api.md
    - semantic:openwiki/documents/jira-export-wt-discovery-2026-10-05.md
    - semantic:openwiki/datasets/fed-ack-events.md
    - semantic:openwiki/interfaces/fedwire-network-ack-topics.md
    - semantic:openwiki/people/carlos-mendes.md
    - semantic:openwiki/datasets/gpi-tracker-events.md
  - step: 6
    tool: semantic_search
    input: '"Payments Hub Engineering team contact planning factor lead time"'
    result: '8 hits: openwiki/teams/payments-hub-engineering.md, openwiki/teams/payment-operations.md, openwiki/people/raymond-ortiz.md'
    ms: 4088
    refs:
    - semantic:openwiki/teams/payments-hub-engineering.md
    - semantic:openwiki/teams/payment-operations.md
    - semantic:openwiki/people/raymond-ortiz.md
    - semantic:openwiki/organizations/payments-treasury-technology.md
    - semantic:openwiki/teams/cbo-platform-entitlements.md
    - semantic:openwiki/teams/treasury-data-analytics.md
    - semantic:openwiki/documents/cnb-org-ptt-2026-06.md
    - semantic:openwiki/teams/financial-crimes-technology.md
  - step: 7
    tool: semantic_search
    input: '"GTSI team contact planning factor lead time engagement"'
    result: '8 hits: openwiki/teams/payments-hub-engineering.md, openwiki/people/hannah-lindqvist.md, openwiki/projects/gtsi-0107-gpi-real-time-service.md'
    ms: 4087
    refs:
    - semantic:openwiki/teams/payments-hub-engineering.md
    - semantic:openwiki/people/hannah-lindqvist.md
    - semantic:openwiki/projects/gtsi-0107-gpi-real-time-service.md
    - semantic:openwiki/organizations/payments-treasury-technology.md
    - semantic:openwiki/people/elena-vasquez.md
    - semantic:openwiki/teams/gtsi.md
    - semantic:openwiki/teams/treasury-data-analytics.md
    - semantic:openwiki/documents/cnb-org-ptt-2026-06.md
  - step: 8
    tool: semantic_search
    input: '"Financial Crimes Technology FCT team contact planning factor"'
    result: '8 hits: openwiki/teams/financial-crimes-technology.md, openwiki/people/catherine-doyle.md, openwiki/teams/payment-operations.md'
    ms: 4087
    refs:
    - semantic:openwiki/teams/financial-crimes-technology.md
    - semantic:openwiki/people/catherine-doyle.md
    - semantic:openwiki/teams/payment-operations.md
    - semantic:openwiki/teams/financial-crimes-compliance.md
    - semantic:openwiki/people/grace-mensah.md
    - semantic:openwiki/people/victor-petrov.md
    - semantic:openwiki/people/jordan-ellis.md
    - semantic:openwiki/people/rebecca-stone.md
  - step: 9
    tool: semantic_search
    input: '"Enterprise Notification Platform team contact planning factor"'
    result: '8 hits: openwiki/teams/enterprise-notification-platform.md, openwiki/people/sanjay-iyer.md, openwiki/teams/cbo-wire-center-squad.md'
    ms: 4087
    refs:
    - semantic:openwiki/teams/enterprise-notification-platform.md
    - semantic:openwiki/people/sanjay-iyer.md
    - semantic:openwiki/teams/cbo-wire-center-squad.md
    - semantic:openwiki/teams/cbo-platform-entitlements.md
    - semantic:openwiki/teams/deposits-data-ownership.md
    - semantic:openwiki/teams/payments-hub-engineering.md
    - semantic:openwiki/systems/enterprise-notification-service.md
    - semantic:openwiki/people/melissa-grant.md
  - step: 10
    tool: semantic_search
    input: '"Model Risk Management contact review Tier 2 EUA registration"'
    result: '8 hits: openwiki/teams/model-risk-management.md, openwiki/policies/mrm-pol-02.md, openwiki/people/sophie-laurent.md'
    ms: 4087
    refs:
    - semantic:openwiki/teams/model-risk-management.md
    - semantic:openwiki/policies/mrm-pol-02.md
    - semantic:openwiki/people/sophie-laurent.md
    - semantic:openwiki/people/jonathan-price.md
    - semantic:openwiki/systems/sentinel-fraud-scoring.md
    - semantic:openwiki/people/denise-carter.md
    - semantic:openwiki/documents/mrm-pol-02.md
    - semantic:openwiki/people/victor-petrov.md
  - step: 11
    tool: semantic_search
    input: '"Privacy Office contact Privacy Impact Assessment Rachel Goldberg Ethan Brooks"'
    result: '8 hits: openwiki/people/rachel-goldberg.md, openwiki/people/ethan-brooks.md, openwiki/teams/privacy-office-data-governance.md'
    ms: 4086
    refs:
    - semantic:openwiki/people/rachel-goldberg.md
    - semantic:openwiki/people/ethan-brooks.md
    - semantic:openwiki/teams/privacy-office-data-governance.md
    - semantic:openwiki/policies/dus-07.md
    - semantic:openwiki/people/tanya-brooks.md
    - semantic:openwiki/teams/information-security-digital-channels.md
    - semantic:openwiki/organizations/payments-treasury-technology.md
    - semantic:openwiki/teams/deposits-data-ownership.md
  - step: 12
    tool: semantic_search
    input: '"Disclosure Review Committee Legal Patricia Moore contact lead time"'
    result: '8 hits: openwiki/teams/legal-treasury-payments.md, openwiki/people/patricia-moore.md, openwiki/people/andrew-feldman.md'
    ms: 4086
    refs:
    - semantic:openwiki/teams/legal-treasury-payments.md
    - semantic:openwiki/people/patricia-moore.md
    - semantic:openwiki/people/andrew-feldman.md
    - semantic:openwiki/people/jordan-ellis.md
    - semantic:openwiki/teams/commercial-service-center.md
    - semantic:openwiki/policies/dus-07.md
    - semantic:openwiki/systems/enterprise-notification-service.md
    - semantic:openwiki/teams/privacy-office-data-governance.md
  - step: 13
    tool: semantic_search
    input: '"Information Security InfoSec review contact hours SLA"'
    result: '8 hits: openwiki/teams/information-security-digital-channels.md, openwiki/people/farah-ali.md, openwiki/interfaces/ces-entitlement-type-registration.md'
    ms: 4086
    refs:
    - semantic:openwiki/teams/information-security-digital-channels.md
    - semantic:openwiki/people/farah-ali.md
    - semantic:openwiki/interfaces/ces-entitlement-type-registration.md
    - semantic:openwiki/policies/sec-std-22.md
    - semantic:openwiki/people/andrew-feldman.md
    - semantic:openwiki/teams/deposits-data-ownership.md
    - semantic:openwiki/teams/legal-treasury-payments.md
    - semantic:openwiki/people/jonathan-price.md
  - step: 14
    tool: semantic_search
    input: '"Payment Operations readiness review contact Denise Carter weeks"'
    result: '8 hits: openwiki/teams/payment-operations.md, openwiki/people/denise-carter.md, openwiki/teams/commercial-service-center.md'
    ms: 4086
    refs:
    - semantic:openwiki/teams/payment-operations.md
    - semantic:openwiki/people/denise-carter.md
    - semantic:openwiki/teams/commercial-service-center.md
    - semantic:openwiki/people/luis-ramirez.md
    - semantic:openwiki/systems/investigations-workbench.md
    - semantic:openwiki/documents/pir-2024-07.md
    - semantic:openwiki/organizations/payments-treasury-technology.md
    - semantic:openwiki/policies/mrm-pol-02.md
  - step: 15
    tool: semantic_search
    input: '"Commercial Service Center readiness checklist contact Kim Nguyen"'
    result: '8 hits: openwiki/teams/commercial-service-center.md, openwiki/people/kim-nguyen.md, openwiki/teams/payment-operations.md'
    ms: 4086
    refs:
    - semantic:openwiki/teams/commercial-service-center.md
    - semantic:openwiki/people/kim-nguyen.md
    - semantic:openwiki/teams/payment-operations.md
    - semantic:openwiki/people/ethan-brooks.md
    - semantic:openwiki/systems/commercial-entitlements-service.md
    - semantic:openwiki/projects/gtsi-0107-gpi-real-time-service.md
    - semantic:openwiki/people/andrew-feldman.md
    - semantic:openwiki/teams/legal-treasury-payments.md
  - step: 16
    tool: semantic_search
    input: '"Architecture Review Board ARB contact Nikhil Bose submission"'
    result: '8 hits: openwiki/people/nikhil-bose.md, openwiki/people/jenna-ross.md, openwiki/organizations/payments-treasury-technology.md'
    ms: 4086
    refs:
    - semantic:openwiki/people/nikhil-bose.md
    - semantic:openwiki/people/jenna-ross.md
    - semantic:openwiki/organizations/payments-treasury-technology.md
    - semantic:openwiki/documents/cbo-arch-wc-4.1.md
    - semantic:openwiki/teams/payments-arb-enterprise-architecture.md
    - semantic:openwiki/documents/arb-pay-reg-2026q3.md
    - semantic:openwiki/teams/information-security-digital-channels.md
    - semantic:openwiki/people/laura-kim.md
  - step: 17
    tool: semantic_read
    input: openwiki/organizations/payments-treasury-technology.md [Cross-team dependency sizing in PTT uses story-point-hour
      planning factors]
    result: 'Error: unknown heading ''Cross-team dependency sizing in PTT uses story-point-hour planning factors''
      on openwiki/organizations/payments-treasury-technology.md; available: Payments & Treasury Technology'
    ms: 0
    refs: []
  - step: 18
    tool: semantic_read
    input: openwiki/documents/jira-export-wt-discovery-2026-10-05.md []
    result: 8 sections, 10534 chars
    ms: 0
    refs:
    - semantic:openwiki/documents/jira-export-wt-discovery-2026-10-05.md
  - step: 19
    tool: semantic_read
    input: openwiki/projects/cbo-4471-pph-v1-to-v2-migration.md []
    result: 8 sections, 13925 chars
    ms: 18
    refs:
    - semantic:openwiki/projects/cbo-4471-pph-v1-to-v2-migration.md
  - step: 20
    tool: semantic_search
    input: '"CBO-4473 points CES account-filter mapping PPH v2 search"'
    result: '8 hits: openwiki/systems/commercial-entitlements-service.md, openwiki/projects/cbo-4471-pph-v1-to-v2-migration.md,
      openwiki/interfaces/ces-entitlements-api.md'
    ms: 18
    refs:
    - semantic:openwiki/systems/commercial-entitlements-service.md
    - semantic:openwiki/projects/cbo-4471-pph-v1-to-v2-migration.md
    - semantic:openwiki/interfaces/ces-entitlements-api.md
    - semantic:openwiki/people/arjun-mehta.md
    - semantic:openwiki/people/nadia-haddad.md
    - semantic:openwiki/projects/pph-2190-v1-sunset-migration.md
    - semantic:openwiki/teams/cbo-platform-entitlements.md
    - semantic:openwiki/projects/jira-backlog-registry.md
  - step: 21
    tool: semantic_search
    input: '"GTSI-0115 points Swift gpi Tracker API contract renewal"'
    result: '8 hits: openwiki/teams/gtsi.md, openwiki/people/omar-siddiqui.md, openwiki/people/elena-vasquez.md'
    ms: 18
    refs:
    - semantic:openwiki/teams/gtsi.md
    - semantic:openwiki/people/omar-siddiqui.md
    - semantic:openwiki/people/elena-vasquez.md
    - semantic:openwiki/systems/swift-gpi-connector.md
    - semantic:openwiki/projects/gtsi-0112-gpi-knowledge-transfer.md
    - semantic:openwiki/people/hannah-lindqvist.md
    - semantic:openwiki/decisions/png-1544.md
    - semantic:openwiki/people/tomasz-nowak.md
  - step: 22
    tool: semantic_search
    input: '"ENS-1120 points entity-level event subscriptions paymentId caseId"'
    result: '8 hits: openwiki/projects/ens-1120-entity-level-subscriptions.md, openwiki/people/melissa-grant.md,
      openwiki/systems/enterprise-notification-service.md'
    ms: 18
    refs:
    - semantic:openwiki/projects/ens-1120-entity-level-subscriptions.md
    - semantic:openwiki/people/melissa-grant.md
    - semantic:openwiki/systems/enterprise-notification-service.md
    - semantic:openwiki/interfaces/ens-notification-api-trs-catalog.md
    - semantic:openwiki/teams/enterprise-notification-platform.md
    - semantic:openwiki/people/sanjay-iyer.md
    - semantic:openwiki/interfaces/hms-hold-api.md
    - semantic:openwiki/people/paul-henderson.md
  - step: 23
    tool: semantic_search
    input: '"PPH-2207 points estimate story settlement object sponsor"'
    result: '8 hits: openwiki/interfaces/fedwire-network-ack-topics.md, openwiki/projects/jira-backlog-registry.md,
      openwiki/concepts/wire-lifecycle-state-model.md'
    ms: 441
    refs:
    - semantic:openwiki/interfaces/fedwire-network-ack-topics.md
    - semantic:openwiki/projects/jira-backlog-registry.md
    - semantic:openwiki/concepts/wire-lifecycle-state-model.md
    - semantic:openwiki/interfaces/pph-v2-payments-api.md
    - semantic:openwiki/datasets/fed-ack-events.md
    - semantic:openwiki/systems/prism-payments-hub.md
    - semantic:openwiki/projects/cbo-4471-pph-v1-to-v2-migration.md
    - semantic:openwiki/people/carlos-mendes.md
  - step: 24
    tool: semantic_search
    input: '"TDA-2188 points gpi_tracker_events nightly hourly load"'
    result: '8 hits: openwiki/people/carlos-mendes.md, openwiki/datasets/gpi-tracker-events.md, openwiki/decisions/png-1544.md'
    ms: 441
    refs:
    - semantic:openwiki/people/carlos-mendes.md
    - semantic:openwiki/datasets/gpi-tracker-events.md
    - semantic:openwiki/decisions/png-1544.md
    - semantic:openwiki/projects/jira-backlog-registry.md
    - semantic:openwiki/systems/investigations-workbench.md
    - semantic:openwiki/datasets/gpi-tracker-snapshot.md
    - semantic:openwiki/concepts/swift-gpi-cbpr.md
    - semantic:openwiki/interfaces/gpi-tracker-batch-feed.md
  - step: 25
    tool: semantic_search
    input: '"ENS-1120 effort hours estimate entity-level subscription scope"'
    result: '8 hits: openwiki/projects/ens-1120-entity-level-subscriptions.md, openwiki/people/melissa-grant.md,
      openwiki/systems/enterprise-notification-service.md'
    ms: 441
    refs:
    - semantic:openwiki/projects/ens-1120-entity-level-subscriptions.md
    - semantic:openwiki/people/melissa-grant.md
    - semantic:openwiki/systems/enterprise-notification-service.md
    - semantic:openwiki/teams/enterprise-notification-platform.md
    - semantic:openwiki/interfaces/ens-notification-api-trs-catalog.md
    - semantic:openwiki/documents/ens-int-3.2.md
    - semantic:openwiki/people/sanjay-iyer.md
    - semantic:openwiki/interfaces/hms-hold-api.md
  - step: 26
    tool: semantic_search
    input: '"extend Status Projection Service SPS to wires ACL mapping module effort"'
    result: '8 hits: openwiki/interfaces/sps-read-model-api.md, openwiki/people/arjun-mehta.md, openwiki/systems/cbo-status-projection-service.md'
    ms: 441
    refs:
    - semantic:openwiki/interfaces/sps-read-model-api.md
    - semantic:openwiki/people/arjun-mehta.md
    - semantic:openwiki/systems/cbo-status-projection-service.md
    - semantic:openwiki/projects/cbo-3790-ach-payment-tracker.md
    - semantic:openwiki/decisions/adr-pay-019.md
    - semantic:openwiki/teams/cbo-platform-entitlements.md
    - semantic:openwiki/interfaces/pph-lifecycle-event-topics.md
    - semantic:openwiki/projects/cbo-3120-wire-status-lite-pilot.md
  - step: 27
    tool: semantic_search
    input: '"GTSI-0115 contract renewal effort points scope"'
    result: '8 hits: openwiki/projects/jira-backlog-registry.md, openwiki/teams/gtsi.md, openwiki/people/elena-vasquez.md'
    ms: 441
    refs:
    - semantic:openwiki/projects/jira-backlog-registry.md
    - semantic:openwiki/teams/gtsi.md
    - semantic:openwiki/people/elena-vasquez.md
    - semantic:openwiki/systems/swift-gpi-connector.md
    - semantic:openwiki/people/omar-siddiqui.md
    - semantic:openwiki/projects/gtsi-0112-gpi-knowledge-transfer.md
    - semantic:openwiki/people/hannah-lindqvist.md
    - semantic:openwiki/people/tomasz-nowak.md
  - step: 28
    tool: semantic_read
    input: openwiki/teams/payment-operations.md []
    result: 9 sections, 14858 chars
    ms: 2
    refs:
    - semantic:openwiki/teams/payment-operations.md
  - step: 29
    tool: semantic_read
    input: openwiki/interfaces/ens-notification-api-trs-catalog.md []
    result: 9 sections, 8424 chars
    ms: 2
    refs:
    - semantic:openwiki/interfaces/ens-notification-api-trs-catalog.md
  - step: 30
    tool: semantic_read
    input: openwiki/teams/model-risk-management.md []
    result: 8 sections, 13274 chars
    ms: 1
    refs:
    - semantic:openwiki/teams/model-risk-management.md
```
