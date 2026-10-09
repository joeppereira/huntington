---
type: Person
entity_id: catherine-doyle
title: Catherine Doyle
description: EVP, Chief BSA/AML Officer at Crestline National Bank; second-line accountable owner of the Financial Crimes Compliance (FCC) partner function and document owner of POL-FCC-014, the enterprise standard governing client-facing communication of payment status, holds and exceptions.
tags: [people, financial-crimes-compliance, bsa-aml, second-line, policy-owner, pol-fcc-014, ptt, partner-function, governance]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-49303e801f124d97df9c3ea3
    resource: repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md
  - id: openwiki-source-1601c697250670250350a70c
    resource: repo://sources/estate/pol-fcc-014-v3.2-customer-communication-of-payment-status-holds-and-exceptions-standard.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

Catherine Doyle is EVP and Chief BSA/AML Officer at Crestline National Bank
(CNB). In the Payments & Treasury Technology (PTT) organization's engagement
directory she is named as the second-line owner of financial-crimes policies,
including **POL-FCC-014**, and as the accountable leader of the **Financial
Crimes Compliance (FCC)** partner function that PTT engineering and product
teams must engage for payment-status, hold and exception work. She is not a
member of an engineering team; she and her delegates are an accountable
second-line compliance partner whom engineering and product teams must route
demand and policy questions to, rather than a system owner.

## Role and scope

- **Title**: EVP, Chief BSA/AML Officer.
- **Second-line ownership**: Named in PTT's leadership roster as "2nd line owner of financial-crimes policies incl. POL-FCC-014."
- **Partner function accountable owner**: Named as the accountable leader for Financial Crimes Compliance (FCC) in the directory's partner-functions table, alongside Model Risk Management (Jonathan Price), Payment Operations (Denise Carter), Information Security (Farah Ali), and other first-/second-line functions that PTT engineering teams engage rather than own.
- **Delegated contacts**: For day-to-day product and design reviews, teams are directed to named specialists under her function rather than to Doyle directly: Jordan Ellis (FCC Policy & Advisory), Michael Tran (OFAC/Sanctions), and Rebecca Stone (Financial Intelligence Unit, FIU).
- **Escalation route**: Compliance or policy interpretation questions are explicitly routed to FCC Policy & Advisory (Jordan Ellis) — not decided unilaterally by engineering teams — reflecting Doyle's second-line accountability for financial-crimes policy interpretation.

## Document ownership: POL-FCC-014

Doyle is the named **document owner** of POL-FCC-014 v3.2, "Customer
Communication of Payment Status, Holds & Exceptions Standard," co-owned with
Michael Tran, SVP, OFAC/Sanctions Officer. The standard was approved by the
Enterprise Policy Committee on 2026-02-12, is effective 2026-03-01, and is
next due for review 2027-03-01. Jordan Ellis, VP, FCC Policy & Advisory, is
listed as the policy's day-to-day contact.

As document owner, Doyle's organization sets enterprise-wide rules that
engineering and product teams building client-facing payment experiences
(e.g., Crestline Business Online, host-to-host status files, notifications,
Commercial Service Center scripts) must follow, including:

- **Disclosure tiers (P/C/G/R)**: a four-tier model controlling what payment-status information may reach a client, from fully public factual status (P) down to restricted reviews (R) that must be presented identically to generic reviews (G) so a client cannot infer the nature of a hold.
- **Hold presentation rules**: restricted reasons, hold codes, scores, list names, match details, analyst notes and queue names must never be displayed or implied in any client-facing channel; no estimated release time or "next steps" may be shown for tier G/R holds; sanctions blocks/rejects are communicated only by Sanctions Operations.
- **Status terminology rules**: strict mapping between network-confirmed events (e.g., Fedwire acceptance, gpi ACCC) and permitted client-facing terms such as "Sent," "Delivered," "Completed/Settled," and "Credited," preventing premature or misleading status claims.
- **Third-party sharing limits**: data shared with a beneficiary or other third party at a client's request is restricted to amount, currency, value date, status milestones and a reference; account numbers, fees, internal references and hold information must be excluded, and sharing links must expire within 7 days with InfoSec and Privacy design approval.
- **Predictive/insight statements**: client-facing completion-time estimates must use only the client's own data or MRM/DUS-07-compliant aggregates, carry a DRC-approved disclaimer, and never be shown for tier G or R holds.
- **Approvals**: new or changed client-facing status/hold/exception experiences require FCC Policy & Advisory review before build commitment and Disclosure Review Committee (DRC) approval of final copy; **exceptions to the standard require Chief BSA/AML Officer (Doyle) approval**, making her the ultimate sign-off authority for deviations.

See [POL-FCC-014](../policies/pol-fcc-014.md) for the full policy record.

## Engagement routes into Doyle's organization

PTT engineering teams reach Doyle's function through defined governance
forums and intake routes rather than direct escalation:

- **FCT Change Advisory** (bi-weekly; 5 business days' submission lead time): FCC sign-off is required here for any hold or screening change; there is a year-end change freeze from December 15 to January 5.
- **FCC Policy & Advisory intake** (Jordan Ellis): approximately 10 business days per review; required before build commitment for new or changed client-facing status/hold/exception experiences.
- **Disclosure Review Committee (DRC)**: bi-weekly Thursdays, 5 business days' lead time; approves final client-facing copy, disclaimers and notification templates touching payment status.
- **Financial Crimes Technology (FCT) planning factor**: cross-team sizing guidance in the PTT directory budgets roughly 1 point ≈ 8 engineering hours **plus 20% independent compliance testing** for FCT work, reflecting the additional verification burden Doyle's second-line function imposes on financial-crimes-adjacent changes.

## Relationships

- **Peer second-line/partner-function leaders**: Jonathan Price (Model Risk Management, owner of MRM-POL-02), Rachel Goldberg (Chief Privacy Officer, owner of DUS-07), Denise Carter (Payment Operations), Andrew Feldman (Legal - Treasury & Payments), Farah Ali (Information Security - Digital Channels), Kim Nguyen (Commercial Service Center), and Mark Sullivan (Deposits Data Ownership).
- **Direct reports / delegated contacts**: Jordan Ellis (FCC Policy & Advisory), Michael Tran (OFAC/Sanctions, POL-FCC-014 co-owner), Rebecca Stone (FIU).
- **Engineering counterpart**: Financial Crimes Technology (FCT), led by Victor Petrov (Director), with Grace Mensah (EM) and Daniel Kowalski (Tech Lead, Hold Management Service) building the systems — notably PRSP Hold Management Service (SYS-PRSP-HMS) and PRSP SanctionScreen (SYS-PRSP-SSC) — that implement the hold-tier and sanctions-screening behavior Doyle's policies constrain.
- **Business owner counterpart**: Rebecca Stone (FIU) is the business owner of the Hold Management Service; Michael Tran is the business owner of SanctionScreen — both operating under Doyle's second-line financial-crimes policy framework.

## Related pages

- [POL-FCC-014](../policies/pol-fcc-014.md)
- [Financial Crimes Compliance](../teams/financial-crimes-compliance.md)
