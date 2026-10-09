---
type: Team
entity_id: financial-crimes-compliance
title: Financial Crimes Compliance (FCC)
description: Second-line partner function (accountable leader Catherine Doyle, EVP Chief BSA/AML Officer) that owns POL-FCC-014, the enterprise standard controlling client-facing payment status/hold/exception communication, and whose Policy & Advisory review (Jordan Ellis) is a mandatory pre-build gate for any Payments & Treasury Technology engineering change in that space.
tags: [financial-crimes-compliance, fcc, second-line, partner-function, catherine-doyle, jordan-ellis, pol-fcc-014, disclosure-tiers, ptt, governance, hold-management-service, fct]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-49303e801f124d97df9c3ea3
    resource: repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md
  - id: openwiki-source-3cc45df143c5eec31fe1f9f6
    resource: repo://sources/estate/pir-2024-07-wire-status-lite-pilot-inc-2024-1182-post-implementation-review.md
  - id: openwiki-source-1601c697250670250350a70c
    resource: repo://sources/estate/pol-fcc-014-v3.2-customer-communication-of-payment-status-holds-and-exceptions-standard.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

**Financial Crimes Compliance (FCC)** is a second-line partner function in
Crestline National Bank's (CNB) Payments & Treasury Technology (PTT)
organization. It is listed in the PTT organization directory's
"Partner functions (first and second line)" table, not in the engineering
team directory or the system ownership register: FCC owns no system of
record and employs no engineering staff of its own. Instead, it is the
accountable second-line compliance function that **every** PTT engineering
or product team building a client-facing payment status, hold, or exception
experience must engage — for mandatory policy review, for interpretation of
what may be disclosed to a client, and for sign-off before committing a
build.
[Partner functions (first and second line)](repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L65-L77)

| Field | Value |
|---|---|
| Function | Financial Crimes Compliance (FCC) |
| Accountable | Catherine Doyle, EVP, Chief BSA/AML Officer |
| Line | Second line of defense |
| Policy owned | POL-FCC-014 (co-owned with Michael Tran, SVP OFAC/Sanctions) |
| Policy & Advisory contact | Jordan Ellis, VP, FCC Policy & Advisory |
| Other named contacts | Michael Tran (OFAC); Rebecca Stone (FIU) |
| Engineering counterpart | Financial Crimes Technology (FCT), led by Victor Petrov |
| Appears in engineering team directory (Sec. 3)? | No |
| Appears in system ownership register (Sec. 4)? | No |

## Accountable leadership and named contacts

Catherine Doyle, EVP and Chief BSA/AML Officer, is named in both the PTT
leadership roster and the partner-functions table as the accountable owner
of FCC and of "financial-crimes policies incl. POL-FCC-014." Day-to-day
product and design review work is delegated to three named specialists
under her, each covering a distinct slice of financial-crimes compliance:

- **Jordan Ellis, VP, FCC Policy & Advisory** — the policy contact for
  [POL-FCC-014](../policies/pol-fcc-014.md) and the reviewer of record for
  client-facing status/hold/exception designs; see
  [Jordan Ellis](../people/jordan-ellis.md).
- **Michael Tran, SVP, OFAC/Sanctions Officer** — co-owner of POL-FCC-014
  and business owner of SYS-PRSP-SSC (SanctionScreen).
- **Rebecca Stone, Financial Intelligence Unit (FIU)** — business owner of
  SYS-PRSP-HMS (Hold Management Service) and the escalation point for hold
  casework.

Engineering and product teams are explicitly directed to engage these named
contacts rather than Doyle directly for routine reviews; Doyle herself is
reserved for policy exceptions (see below).
[Leadership](repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L28-L39)

See [Catherine Doyle](../people/catherine-doyle.md) for her full role detail
and [POL-FCC-014](../policies/pol-fcc-014.md) for the policy record.

## Why FCC exists: the control it owns

FCC's reason for existence in the payments stack is a single enterprise
standard: **POL-FCC-014, "Customer Communication of Payment Status, Holds &
Exceptions Standard"** (v3.2, effective 2026-03-01, approved by the
Enterprise Policy Committee). The standard governs every client-facing
channel — Crestline Business Online, APIs and host-to-host status files,
notifications, Commercial Service Center scripts, relationship-manager
communications, downloadable reports, and anything shared with a third
party at a client's request — and exists to prevent three kinds of harm:
disclosure that would reveal a Suspicious Activity Report (SAR) or tip off
a client to a fraud/AML/sanctions/legal-process review; disclosure that aids
fraud or sanctions evasion; and misleading status language.
[Purpose](repo://sources/estate/pol-fcc-014-v3.2-customer-communication-of-payment-status-holds-and-exceptions-standard.md#L25-L27)

The standard's central mechanism is a four-tier disclosure model (P/C/G/R)
that determines what a client may ever see about a payment's status or
hold, with the deliberate invariant that tier **R (Restricted — fraud,
account takeover, sanctions, AML, legal holds)** must be presented
**identically** to tier **G (Generic review)** so that a client cannot infer
the nature of a review from the UI. It also gates specific status words
(e.g., "Sent," "Delivered," "Completed/Settled," "Credited") on concrete,
auditable payment-rail events such as Fedwire acceptance or SWIFT gpi ACCC,
limits what may be shared with third parties at a client's request, and
conditions any predictive/insight statement (e.g., estimated delivery
times) on Model Risk Management registration and a Disclosure Review
Committee (DRC)-approved disclaimer. Full policy detail, including the hold
rules, status-terminology table, and Appendix A hold-code-to-tier mapping,
is maintained on [POL-FCC-014](../policies/pol-fcc-014.md).

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: a semicolon inside a label breaks rendering; rephrase the label. -->
```text
flowchart TD
    Eng["PTT engineering / product team\n(client-facing status, hold or\nexception change)"] -->|mandatory review\nbefore build commitment| Ellis["Jordan Ellis\nFCC Policy & Advisory\n(~10 business days)"]
    Ellis -->|interprets/applies| Policy["POL-FCC-014\nDisclosure tiers P/C/G/R"]
    Ellis --> DRC["Disclosure Review Committee\n(bi-weekly; approves final copy)"]
    Ellis -.exception request.-> Doyle["Catherine Doyle\nEVP, Chief BSA/AML Officer\n(sole exception-approval authority)"]
    FCT["Financial Crimes Technology (FCT)\nHold Management Service, SanctionScreen"] -->|design review +\nsign-off required| Ellis
    FCT -->|FCT Change Advisory\n(bi-weekly)| CAB["FCT Change Advisory\nFCC sign-off required for\nhold/screening changes"]
```
*FCC's governance gates: Policy & Advisory review is a pre-build-commitment dependency; only Doyle can approve exceptions to POL-FCC-014.*

## Engagement routes and governance gates

FCC does not take engineering demand through a Jira project or Slack
channel like PTT's engineering teams; it is engaged through named
compliance intake routes and governance forums, each with its own lead
time:

| Route | Cadence / lead time | What it gates |
|---|---|---|
| FCC Policy & Advisory intake | ~10 business days per review | Required **before build commitment** for any new or changed client-facing status, hold, or exception experience (POL-FCC-014 Section 6) |
| FCT Change Advisory | Bi-weekly; 5 business days submission lead time; year-end freeze Dec-15–Jan-05 | FCC sign-off required for any hold or screening change in Financial Crimes Technology (FCT) systems |
| Disclosure Review Committee (DRC) | Bi-weekly, Thursday; 5 business days lead time | Approves final client-facing copy, disclaimers, and notification templates — the step after FCC Policy & Advisory review |

The PTT planning factors also price FCC's review burden into
cross-team estimation: Financial Crimes Technology (FCT) engineering work is
budgeted at roughly 1 story point ≈ 8 hours **plus an additional 20%** for
independent compliance testing, over and above the ~10-business-day FCC
Policy & Advisory review itself — making FCC review a scheduling dependency
distinct from, and in addition to, FCT's own engineering capacity.
[Engagement routes and planning factors](repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L120-L138)

## Approval authority and exceptions

POL-FCC-014 Section 6 sets a strict two-step approval sequence for any new
or changed client-facing status/hold/exception experience: **FCC Policy &
Advisory review before build commitment**, followed by **DRC approval of
final copy**. Neither step may be skipped or reordered — a design cannot
proceed to build on the strength of DRC copy approval alone, and copy
cannot ship without going through DRC after FCC sign-off.
[Approvals](repo://sources/estate/pol-fcc-014-v3.2-customer-communication-of-payment-status-holds-and-exceptions-standard.md#L100-L102)

**Exceptions to POL-FCC-014 require Catherine Doyle's (Chief BSA/AML
Officer) personal approval** — this is the one decision Jordan Ellis cannot
make on FCC's behalf, and it is the reason Doyle, not Ellis, is the named
escalation terminus for any request to deviate from the standard rather
than merely interpret it.

FCC's authority also extends beyond its own policy review gate into general
PTT dependency escalation: compliance or policy-interpretation questions
that arise anywhere in PTT engineering route directly to **FCC Policy &
Advisory (Jordan Ellis)** — bypassing the normal engineering-manager →
director → PTT Leadership Team escalation chain used for capacity or
sequencing conflicts — because such questions are "not decided by
engineering teams."
[Escalation](repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md#L148-L150)

## Engineering counterpart: Financial Crimes Technology (FCT)

FCC is a compliance/policy function, not an engineering organization; the
systems that implement the controls FCC's policy mandates are built by
**Financial Crimes Technology (FCT)**, a distinct engineering team led by
Victor Petrov (Director), with Grace Mensah (EM) and Daniel Kowalski (Tech
Lead, Hold Management Service). FCT owns:

- **[Hold Management Service (HMS)](../systems/hold-management-service.md)**
  (`SYS-PRSP-HMS`) — the system of record for payment holds, the Hold
  Reason Code (HRC-01–HRC-12) taxonomy, and the disclosure-tier assignment
  POL-FCC-014 defines; business owner Rebecca Stone (FIU).
- **[SanctionScreen](../systems/sanctionscreen.md)** (`SYS-PRSP-SSC`) — OFAC
  and sanctions-list screening; business owner Michael Tran.
- **[Sentinel Fraud Scoring](../systems/sentinel-fraud-scoring.md)**
  (`SYS-PRSP-SEN`) — vendor fraud model; business owner "Fraud Strategy
  (FCC)."

FCT's design documents are reviewed, not owned, by FCC: `PRSP-HMS-3.4`
(Hold Management Service design and hold-reason taxonomy) is approved by
Victor Petrov but reviewed by Jordan Ellis, who confirms the HRC-to-tier
mapping is consistent with POL-FCC-014 before the design proceeds. This
review relationship — FCT builds and owns the systems, FCC owns the
policy those systems must satisfy and reviews FCT's designs against it — is
the structural pattern that recurs across every hold- or
sanctions-adjacent change in PTT.

## Why this matters operationally

Two documented incidents make FCC's gate concrete rather than theoretical:

- **[PIR-2024-07](../incidents/pir-2024-07.md)** (Wire Status Lite pilot
  post-implementation review) found that Treasury Support (the Commercial
  Service Center) could not explain held wires to clients without FCC
  guidance, and left open an action — still unresolved — to validate
  client-facing status terminology with FCC and Legal before any future
  tracking feature.
- **[CMP-2026-1189](../incidents/cmp-2026-1189.md)** is the direct
  recurrence of that gap: a client released goods after Crestline Business
  Online displayed "Completed" on a wire that was later returned/rejected,
  because the status label did not satisfy POL-FCC-014 Section 5.2's gate
  on specific, auditable payment-rail events.

Both incidents are the evidentiary basis for why POL-FCC-014's pre-build
Policy & Advisory review exists as a mandatory gate rather than a
best-practice suggestion: client-facing status wording that has not cleared
FCC (and subsequently DRC) review has already caused a regulatory
complaint and a prior operational incident at CNB.

## Relationships

- **[Catherine Doyle](../people/catherine-doyle.md)** — accountable leader
  of FCC; document owner of POL-FCC-014; sole approver of exceptions to the
  standard.
- **[Jordan Ellis](../people/jordan-ellis.md)** — VP, FCC Policy & Advisory;
  day-to-day policy contact and the named pre-build reviewer for
  client-facing status/hold/exception designs; also the first escalation
  point for compliance/policy-interpretation questions PTT-wide.
- **[POL-FCC-014](../policies/pol-fcc-014.md)** — the enterprise standard
  FCC owns and enforces.
- **Financial Crimes Technology (FCT)** (Victor Petrov, Director) —
  engineering counterpart that builds and owns Hold Management Service,
  SanctionScreen, and Sentinel Fraud Scoring, subject to FCT Change
  Advisory sign-off from FCC.
- **[Hold Management Service](../systems/hold-management-service.md)** —
  the system that originates hold state and HRC codes against the
  disclosure tiers POL-FCC-014 defines.
- **Disclosure Review Committee (DRC)** (chaired by Patricia Moore) — the
  governance forum that approves final client-facing copy after FCC Policy
  & Advisory review.
- **[Commercial Service Center](commercial-service-center.md)** — first-line
  partner function whose phone scripts depend on wording that has cleared
  FCC and DRC review.
- **[PIR-2024-07](../incidents/pir-2024-07.md)** /
  **[CMP-2026-1189](../incidents/cmp-2026-1189.md)** — the incident and
  complaint record demonstrating the operational cost of bypassing FCC's
  review gate.
