---
type: System
entity_id: SYS-PRSP-SSC
title: "SanctionScreen (SYS-PRSP-SSC)"
description: OFAC and other sanctions-list screening system within the Payment Risk & Screening Platform (PRSP) at Crestline National Bank; its potential-match hits drive HRC-09 SANCTIONS_REVIEW holds and the BLOCKED/REJECTED dispositions that carry OFAC regulatory reporting obligations.
tags: [sanctionscreen, prsp, ofac, sanctions-screening, hold-management-service, hrc-09, financial-crimes, restricted, pol-fcc-014, regulatory-reporting]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-49303e801f124d97df9c3ea3
    resource: repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md
  - id: openwiki-source-1601c697250670250350a70c
    resource: repo://sources/estate/pol-fcc-014-v3.2-customer-communication-of-payment-status-holds-and-exceptions-standard.md
  - id: openwiki-source-19beabaf3acaad354d39ee1e
    resource: repo://sources/estate/pph-sys-ovw-9.2-prism-payments-hub-system-overview-and-lifecycle-state-model.md
  - id: openwiki-source-08ac07f04b390aa09d5edc51
    resource: repo://sources/estate/prsp-hms-3.4-hold-management-service-design-and-reason-taxonomy-restricted.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

SanctionScreen (system ID `SYS-PRSP-SSC`) is the sanctions-list screening
system within the **Payment Risk & Screening Platform (PRSP)**, alongside
**Sentinel Fraud Scoring** (a vendor fraud model, MRM ID `M-FCT-0021`) and
the **[Hold Management Service (HMS)](hold-management-service.md)** (the
system of record for payment holds). It screens outbound payments against
OFAC and other sanctions lists. SanctionScreen is owned end to end within
Financial Crimes Technology (FCT): Grace Mensah (Engineering Manager, FCT -
PRSP) is its sole accountable **technical owner**, and Michael Tran (SVP,
OFAC/Sanctions Officer) is its named **business owner** — a second-line
Financial Crimes Compliance (FCC) accountability distinct from the
engineering team that builds and runs it. It is classified Tier 1 (24x7
critical).

Unlike HMS, which has its own restricted design-of-record document
(`PRSP-HMS-3.4`), the source corpus does not include a dedicated
SanctionScreen design document, API catalog, or match-logic specification.
What is documented about SanctionScreen comes from its role in the
[PRISM Payments Hub (PPH)](prism-payments-hub.md) screening stage, its
hit-to-hold handoff into HMS, and the sanctions-communication rules
referenced below. Readers needing SanctionScreen's internal
matching algorithm, list-update cadence, or a formal API contract should
treat that as an open gap, not assume it is out of scope — raise it with FCT
(Grace Mensah / `#fct-prsp`) or the OFAC/Sanctions Officer function
(Michael Tran) rather than inferring it from downstream behavior.

## Responsibilities

- **Synchronous sanctions-list screening of outbound payments.** As part of
  PPH's processing pipeline, every outbound wire passes through a
  **Screening** stage that makes a synchronous call to PRSP (SanctionScreen
  and Sentinel together); PPH's canonical `SCREENING` lifecycle state has a
  typical duration of 1-20 seconds, after which the payment either proceeds
  or is held.
- **Producing sanctions hits that create HMS holds.** A SanctionScreen
  potential match does not itself block a payment; it creates a hold record
  in HMS, and PPH transitions the payment into its `HELD` state pending
  analyst review.
- **Feeding the HRC-09 SANCTIONS_REVIEW hold-reason code.** SanctionScreen
  hits are the sole upstream source of hold-reason code **HRC-09
  (SANCTIONS_REVIEW)** in HMS's taxonomy — about 7% of all HMS holds by
  volume, tier **R** (Restricted), pending L1/L2 Sanctions Operations
  analyst review, with a reported median time to disposition of roughly 3
  hours 20 minutes.
- **Upstream accountability for BLOCKED/REJECTED sanctions dispositions and
  their regulatory reporting obligations.** Where a SanctionScreen-driven
  hold is ultimately dispositioned as an OFAC block, HMS enters its
  `BLOCKED` state, funds are moved to a blocked account, and the block is
  reported to OFAC within 10 business days under 31 CFR 501.603. Sanctions
  rejects carry a parallel reporting obligation under 31 CFR 501.604. These
  are executed by Sanctions Operations, not by SanctionScreen itself or by
  any engineering team, but the detections that trigger them originate in
  SanctionScreen.

## Control flow: screening to disposition

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: a semicolon inside a label breaks rendering; rephrase the label. -->
```text
flowchart LR
    PPH["PRISM Payments Hub\n(Screening stage, 1-20s)"] -- "synchronous call" --> PRSP["PRSP: SanctionScreen + Sentinel"]
    PRSP -- "no hit" --> Continue["PPH continues: funds control, release"]
    PRSP -- "sanctions potential match" --> HMS["Hold Management Service\ncreates hold, HRC-09 SANCTIONS_REVIEW (tier R)"]
    HMS -- "holdId" --> Held["PPH payment -> HELD"]
    HMS -- "IWB: L1/L2 analyst disposition\n(maker-checker, CTRL-PAY-012)" --> Disposition{Disposition}
    Disposition -- "release" --> Released["PPH resumes processing"]
    Disposition -- "reject" --> Rejected["PPH cancels payment\nOFAC reject report (31 CFR 501.604)\nSanctions Ops notifies client in writing"]
    Disposition -- "OFAC block" --> Blocked["HMS BLOCKED: funds moved to\nblocked account; OFAC report\nwithin 10 business days (31 CFR 501.603)\nSanctions Ops notifies client in writing"]
```
*SanctionScreen itself never discloses outcomes, assigns dispositions, or
notifies clients; it only produces the potential-match signal that creates
an HRC-09 hold. Disposition, blocking, rejection and client/regulator
notification are carried out by HMS, Investigations Workbench analysts, and
Sanctions Operations respectively.*

## State and lifecycle

SanctionScreen has no hold state of its own; a sanctions determination's
lifecycle is entirely the hold lifecycle owned by HMS. The states a
SanctionScreen-triggered hold can pass through are `OPEN` → `IN_REVIEW`
(Sanctions L1/L2 queue) → optionally `ESCALATED` (Sanctions L2) → exactly
one terminal state of `RELEASED`, `REJECTED`, `BLOCKED`, or `EXPIRED`. See
[Hold Management Service](hold-management-service.md#hold-lifecycle) for the
full state diagram and the maker-checker control (`CTRL-PAY-012`) that gates
every exit from `IN_REVIEW`/`ESCALATED`.

## Invariants and disclosure controls

These rules, defined by [POL-FCC-014](../policies/pol-fcc-014.md) and
`PRSP-HMS-3.4`, constrain anything built around SanctionScreen's output:

- **No client-facing channel may ever disclose a sanctions screening outcome.**
  This is stricter than the general tier-based disclosure model: even tier R
  holds in general are presented identically to tier G ("being reviewed")
  holds, but sanctions blocks and rejects specifically are communicated
  **only by Sanctions Operations per procedure** — never by Channels, APIs,
  notifications, or Commercial Service Center scripts (POL-FCC-014 §5.1.6).
- **Prohibited terms.** POL-FCC-014 Appendix C bars terms such as
  "sanctions," "OFAC," "watch list," and "screening hit" from any
  client-facing copy, operationalizing SanctionScreen's confidentiality at
  the vocabulary level.
- **No estimated release time for tier R holds**, including HRC-09, per
  `CTRL-PAY-040` — internal median-disposition-time figures (e.g., the ≈3 h
  20 min HRC-09 median) must never be surfaced to a client.
- **No client self-service resolution path exists for HRC-09.** The only
  production client-attestation flow is `CTRL-PAY-031`, scoped exclusively
  to HRC-01 (duplicate-suspect); it does not and cannot extend to sanctions
  holds. A proposed client-facing hold-status facade (`FCT-1893`) was
  deprioritized in 2025-Q3 and would, even if built, still be bound by the
  no-disclosure and prohibited-terms rules above for any sanctions-related
  hold.
- **Regulatory reporting timelines are fixed by rule, not by internal SLA.**
  Blocked funds must be reported to OFAC within 10 business days (31 CFR
  501.603); rejected payments are reported under 31 CFR 501.604. Both are
  independent of HMS's internal median-time-to-disposition metrics.

## Interfaces and data

No API catalog, event topic, or data schema specific to SanctionScreen
appears in the available source material — it is known to be invoked
synchronously by PPH's Screening stage and to communicate hits to HMS (which
creates the hold record and carries fields such as `hrcCode`, `description`,
and `analystNotes` for the case). Restricted investigative detail generated
from a sanctions hit — match confidence, list name, and analyst notes (for
example, the HMS hold-description pattern `SANCTIONS_REVIEW name match 0.91
L2`) — is classified Restricted and handled under the same HMS data-handling
rules and `ADR-PAY-021` trust boundary that govern all hold detail; it is
not a SanctionScreen-specific control. The legacy PPH v1 `holdReasonDesc`
sync (tracked risk `FCT-2004`) is therefore also a latent exposure path for
sanctions-hold descriptions specifically, since it long-predates
`ADR-PAY-021` and was not designed with sanctions confidentiality in mind.

## Governance and change management

Because SanctionScreen sits directly behind sanctions-review holds, any
change to its screening logic, thresholds, or list handling is treated as a
hold/screening change under FCT's governance: it must go through the
bi-weekly **FCT Change Advisory** forum (planning factor ~1 story point ≈ 8
engineering hours **plus a 20% allowance for independent compliance
testing**) with required FCC sign-off, and observes a year-end change freeze
from December 15 to January 5. Policy or compliance-interpretation
questions about how a sanctions hold should route or be disclosed are
explicitly out of engineering's decision scope and route to FCC Policy &
Advisory (Jordan Ellis) or, for exceptions to POL-FCC-014, the Chief
BSA/AML Officer (Catherine Doyle) — not to Michael Tran, whose co-ownership
of POL-FCC-014 covers the standard's content and maintenance rather than
exception sign-off.

## Relationships

- **[Hold Management Service](hold-management-service.md)** is the system
  of record that a SanctionScreen hit populates: it creates the HRC-09
  SANCTIONS_REVIEW hold, enforces the hold lifecycle and maker-checker
  disposition control (`CTRL-PAY-012`), and is the sole channel (via the
  Investigations Workbench) through which a sanctions hold is released,
  rejected, blocked, or escalated.
- **PRISM Payments Hub (PPH)** calls PRSP (SanctionScreen and Sentinel)
  synchronously during its Screening processing stage and transitions a
  payment to `HELD` on a hit; it has no visibility into SanctionScreen's
  internal match logic or confidence scoring, only the resulting hold.
- **[Michael Tran](../people/michael-tran.md)** is SanctionScreen's named
  business owner and, separately, co-owner of
  [POL-FCC-014](../policies/pol-fcc-014.md), the policy that defines the
  client-disclosure rules SanctionScreen's output is subject to.
- **Grace Mensah** is the accountable technical owner of SanctionScreen, the
  Hold Management Service, and Sentinel Fraud Scoring alike, all under
  Victor Petrov (Director, Financial Crimes Technology - PRSP).
- **Sentinel Fraud Scoring** (`SYS-PRSP-SEN`) is SanctionScreen's sibling
  system within PRSP, invoked in the same synchronous Screening call but
  feeding a separate hold-reason code (HRC-07, FRAUD_MODEL_HIGH) rather than
  HRC-09.
- **[POL-FCC-014](../policies/pol-fcc-014.md)** governs what any
  client-facing channel may ever communicate about a SanctionScreen-driven
  hold, block, or reject — including the absolute prohibition on Channels
  communicating sanctions screening outcomes under any circumstance.
