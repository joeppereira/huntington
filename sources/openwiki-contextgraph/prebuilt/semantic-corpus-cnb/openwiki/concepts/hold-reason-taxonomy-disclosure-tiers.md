---
type: Concept
entity_id: hold-reason-taxonomy-disclosure-tiers
title: "Hold Reason Taxonomy (HRC) and Disclosure Tiers"
description: "The 12 HRC hold-reason codes used by the Hold Management Service, their P/C/G/R client-disclosure tiers, and the POL-FCC-014 rules an agent must check any held-wire customer-communication design against before it ships."
tags: [hold-management-service, hold-reason-codes, disclosure-tiers, pol-fcc-014, prsp-hms, customer-communication, financial-crimes, restricted]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-1601c697250670250350a70c
    resource: repo://sources/estate/pol-fcc-014-v3.2-customer-communication-of-payment-status-holds-and-exceptions-standard.md
  - id: openwiki-source-08ac07f04b390aa09d5edc51
    resource: repo://sources/estate/prsp-hms-3.4-hold-management-service-design-and-reason-taxonomy-restricted.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

Every hold the Hold Management Service (HMS) places on an outbound payment carries one of twelve **Hold Reason Codes (HRC-01 through HRC-12)**. Each code is assigned a **disclosure tier** - P, C, G, or R - that governs what, if anything, a client-facing channel may say about the hold. The taxonomy is defined jointly by two documents that any agent designing or reviewing a held-wire customer experience must reconcile:

- **PRSP-HMS-3.4** (*Hold Management Service: Design & Hold Reason Taxonomy*, RESTRICTED - FINANCIAL CRIMES) - owns the HRC codes, their mnemonics, descriptions, tiers and observed share of hold volume. See [Hold Management Service](../systems/hold-management-service.md).
- **POL-FCC-014** (*Customer Communication of Payment Status, Holds & Exceptions Standard*, v3.2) - owns the disclosure-tier definitions, the Appendix A copy-key/permitted-action mapping per HRC code, and the communication rules that apply to each tier. See [POL-FCC-014](../policies/pol-fcc-014.md).

This page merges both sources into a single reference table plus the governing rules, so a reader does not have to cross-reference a RESTRICTED design document against a separate compliance standard to determine what is safe to show a customer.

**This page documents RESTRICTED-FINANCIAL-CRIMES-sourced material (PRSP-HMS-3.4) faithfully, including hold mnemonics, descriptions and queue-routing detail that the standard itself classifies as Restricted and that must never be displayed, transmitted or implied in any client-facing channel (POL-FCC-014 §5.1(1)).** Anyone building or reviewing a client-facing artifact must treat the mnemonic/description/tier columns below as internal-only inputs to a design, never as copy source.

## Disclosure tiers

POL-FCC-014 §4 defines four tiers that describe what a client-facing channel may ever surface for a hold:

| Tier | Name | Client may see | Example |
|---|---|---|---|
| **P** | Public status | Factual processing status and timing | "Scheduled for next business day (after cutoff)" |
| **C** | Client-actionable | Approved explanation and a permitted client action | "Possible duplicate"; "limit exceeded"; "funds pending" |
| **G** | Generic review | Generic "being reviewed" message only | "Operations manual review" |
| **R** | Restricted | Generic "being reviewed" message only - **identical to tier G** | Fraud, account takeover, sanctions, AML, legal holds |

### The R/G indistinguishability rule

POL-FCC-014 §5.1(2) states this as a hard requirement, and it is the single most important invariant on this page:

> **Tier R and tier G holds must be presented identically** - same label, icon, color, copy, actions and absence of timing information - so that a client cannot infer the nature of a review from the presentation.

Concretely, HRC-07 through HRC-11 (tier R: fraud, account takeover, sanctions, AML, legal hold) and HRC-12 (tier G: ops manual review) all map to the **same copy key, `COPY-HOLD-GEN-01`**, with **no** client action and **no** release-time estimate, per Appendix A and CTRL-PAY-040. A design that gives sanctions-review holds a different icon, color, wording, or "estimated release" treatment than an ordinary manual-review hold violates §5.1(2) even if no restricted term is ever displayed - the differentiation itself leaks information about the nature of the review.

POL-FCC-014 §5.1(1) and Appendix C additionally prohibit specific restricted content in any client-facing copy regardless of tier: HRC codes, scores, list names, match details, analyst notes, queue names, and prohibited terms such as *fraud, suspicious, sanctions, OFAC, watch list, screening hit, AML, compliance review, investigation, flagged, security alert, risk score, law enforcement*, and *blocked* (except Sanctions Operations correspondence).

## The 12 HRC codes

Merged from PRSP-HMS-3.4 §3 (code, mnemonic, description, tier, share of holds) and POL-FCC-014 Appendix A (copy key, permitted client action):

| Code | Mnemonic | Description | Tier | Share of holds | Copy key | Client action permitted |
|---|---|---|---|---|---|---|
| HRC-01 | DUP_SUSPECT | Possible duplicate of a recent wire (same beneficiary/amount/date window) | C | 22% | COPY-HOLD-DUP-01 | Yes - digital attestation (confirm/cancel) with step-up auth (CTRL-PAY-031) |
| HRC-02 | CALLBACK_REQUIRED | Out-of-band callback verification for new/changed beneficiary above threshold | C | 18% | COPY-HOLD-CB-01 | No in-channel confirmation. Client may request a callback; verification only via callback to a contact on file (CTRL-PAY-018) |
| HRC-03 | LIMIT_EXCEEDED | Client daily / per-transaction limit exceeded | C | 9% | COPY-HOLD-LIM-01 | Client admin secondary approval, or RM limit request |
| HRC-04 | CUTOFF_WAREHOUSED | Received after Fedwire customer cutoff (6:00 p.m. ET) or future-dated | P | 6% | COPY-STAT-WH-01 | None needed (informational) |
| HRC-05 | FUNDS_PENDING | Insufficient available balance at funds control | C | 14% | COPY-HOLD-FUND-01 | Fund account; auto-retry until 5:30 p.m. ET |
| HRC-06 | REPAIR_REQUIRED | Message repair (e.g., structured postal address, invalid routing/BIC) | C | 11% (forecast ~16% after Nov-2026 address enforcement) | COPY-HOLD-RPR-01 | Cancel and resubmit with corrected beneficiary data (no in-place edit) |
| HRC-07 | FRAUD_MODEL_HIGH | Sentinel fraud score above threshold | R | 8% | COPY-HOLD-GEN-01 | None |
| HRC-08 | ATO_SUSPECT | Session / device anomalies indicating possible account takeover | R | 1% | COPY-HOLD-GEN-01 | None |
| HRC-09 | SANCTIONS_REVIEW | SanctionScreen potential match pending L1/L2 review | R | 7% | COPY-HOLD-GEN-01 | None |
| HRC-10 | AML_REVIEW | Unusual activity review by FIU | R | 2% | COPY-HOLD-GEN-01 | None |
| HRC-11 | LEGAL_HOLD | Legal process / law enforcement request | R | <0.5% | COPY-HOLD-GEN-01 | None |
| HRC-12 | OPS_MANUAL_REVIEW | Large-value or exception manual review by Wire Room | G | 1.5% | COPY-HOLD-GEN-01 | None |

Volumes: roughly 410 holds per business day (~2.6% of outbound wires). Median time-to-disposition reported by HMS: HRC-01 ≈ 47 min; HRC-02 ≈ 2 h 10 min; HRC-07 ≈ 1 h 35 min; HRC-09 ≈ 3 h 20 min; HRC-10 1-5 business days - none of these durations may be surfaced to a client for tier G/R holds (CTRL-PAY-040; POL-FCC-014 §5.1(3)), and predictive/insight statements about typical completion time are separately barred from tier G/R payments under POL-FCC-014 §5.5(d).

## Reasons that may never be shown to a customer

- **All tier-R codes (HRC-07 FRAUD_MODEL_HIGH, HRC-08 ATO_SUSPECT, HRC-09 SANCTIONS_REVIEW, HRC-10 AML_REVIEW, HRC-11 LEGAL_HOLD)**: HRC mnemonic, description, score, list/match details, analyst notes and queue name are Restricted and must never be displayed, transmitted or implied in any client-facing channel (POL-FCC-014 §5.1(1); PRSP-HMS-3.4 §4). The client sees only the generic `COPY-HOLD-GEN-01` copy, with the same presentation as tier-G HRC-12.
- **Sanctions outcomes specifically**: where a payment is blocked or rejected for sanctions reasons, only Sanctions Operations may notify the client, in writing, per the Sanctions Operations Procedure (and must report to OFAC under 31 CFR 501.603/501.604); channels themselves must never communicate screening outcomes and continue to show only the tier G/R generic presentation (PRSP-HMS-3.4 §7; POL-FCC-014 §5.1(6)).
- **No release-time or likelihood language for tier G or R**: no estimated release time, likelihood of release, or "next steps" timing may be shown for a tier G or R hold, enforced by control CTRL-PAY-040 (PRSP-HMS-3.4 §6; POL-FCC-014 §5.1(3)).
- **Prohibited terms (Appendix C)**: *fraud, suspicious, sanctions, OFAC, watch list, screening hit, AML, compliance review, investigation, flagged, security alert, risk score, law enforcement, blocked* (except in Sanctions Operations correspondence) must never appear in client-facing copy for any hold, regardless of tier.
- **Underlying data classification**: the Hold `description` and `analystNotes` fields in HMS are themselves classified Restricted and are generated from rule templates that routinely embed HRC mnemonics and investigative context (e.g., "FRAUD_MODEL_HIGH sc=9xx L1 queue", "SANCTIONS_REVIEW name match 0.91 L2") - these fields must never be routed to a client-facing surface (PRSP-HMS-3.4 §4). The `risk.hold.events.v1` event topic that carries this data is restricted to FCT and Payment Operations tooling; channel applications are not authorized consumers.

## Client-actionable (tier C) exceptions and their guardrails

Tier C holds (HRC-01, -02, -03, -05, -06) are the only ones where the client may be told an approved explanation and offered a permitted action, but each comes with its own control:

- **HRC-01 DUP_SUSPECT**: since the FCT-1951 pilot, a client may resolve a duplicate-suspect hold via digital attestation (confirm/cancel) with step-up authentication of an entitled user, under control CTRL-PAY-031. Attestation above $5,000,000 still requires Wire Room release, and CTRL-PAY-031 applies to HRC-01 only - it does not extend attestation-based resolution to any other HRC code. See [FCT-1951 Duplicate-Suspect Attestation Pilot](../projects/fct-1951-duplicate-suspect-attestation-pilot.md).
- **HRC-02 CALLBACK_REQUIRED**: callback verification can never be satisfied by an in-channel confirmation received through the same channel that initiated the payment; it requires an out-of-band callback to a contact on file obtained independently of the payment instruction or session (CTRL-PAY-018). The channel may display that a callback is pending and let the client request one.
- **HRC-03 LIMIT_EXCEEDED**: resolved by client-admin secondary approval or a relationship-manager limit request.
- **HRC-05 FUNDS_PENDING**: client can fund the account; HMS auto-retries until 5:30 p.m. ET.
- **HRC-06 REPAIR_REQUIRED**: client must cancel and resubmit with corrected beneficiary data - there is no in-place edit path.

HRC-04 (CUTOFF_WAREHOUSED) is tier P and purely informational; it needs no client action and is the only HRC code that is not a "hold" in the restricted sense - it is simply scheduled processing.

## No client-facing hold status/attestation API exists

There is currently no generalized client-facing interface into HMS. HMS exposes `GET /prsp/hms/v1/holds` and `POST /prsp/hms/v1/holds/{holdId}/disposition` only to the Investigations Workbench (and a legacy read-only sync to PPH v1), gated by the `HOLD_RELEASER` role and maker-checker control CTRL-PAY-012. A proposal, **FCT-1893** (Client-Safe Hold Status Facade), would add a `GET /prsp/hms/v1/holds/{holdId}/client-view` endpoint returning only disclosure tier, approved copy key and permitted client actions, but it was deprioritized in 2025-Q3 and does not exist. The only client-facing resolution path that does exist today is the narrow HRC-01 digital-attestation flow delivered by the FCT-1951 pilot under CTRL-PAY-031; any other "customer self-service on a hold" design is building against an interface that is not there yet, and must still be checked against this taxonomy and POL-FCC-014 §5.1 before build commitment, with FCC Policy & Advisory review and DRC approval of final copy (POL-FCC-014 §6).

## How to use this taxonomy when reviewing a design

1. Identify every HRC code the design's scenario can produce.
2. Look up each code's tier in the table above.
3. For tier P: confirm only factual status/timing is shown, consistent with POL-FCC-014 §5.2 terminology rules.
4. For tier C: confirm the copy matches the approved copy key (Appendix B) and the only action offered is the one Appendix A permits for that code, with the right control (CTRL-PAY-012/018/031) wired in.
5. For tier G or R: confirm the presentation is the generic `COPY-HOLD-GEN-01` treatment, with **no** differentiation between any G and R code, no restricted terms, no mnemonic/score/queue leakage, and no timing or likelihood language.
6. If sanctions are involved (HRC-09, or any blocked/rejected sanctions outcome), confirm the channel is not the one communicating the outcome at all.
