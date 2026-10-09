---
type: Person
entity_id: danielle-okafor
title: Danielle Okafor
description: EVP, Head of Treasury Management Products at Crestline National Bank; accountable business owner of the Treasury Management (TM) product portfolio, including Crestline Business Online (CBO).
tags: [people, treasury-management-products, cbo, crestline-business-online, business-owner, leadership, ptt, product-ownership]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-49303e801f124d97df9c3ea3
    resource: repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

Danielle Okafor is EVP, Head of Treasury Management Products at Crestline
National Bank (CNB). Within the Payments & Treasury Technology (PTT)
organization's leadership roster she is named as the **business owner of
the Treasury Management (TM) product portfolio, including Crestline
Business Online (CBO)** — CNB's commercial digital banking portal. She sits
at the top of PTT's business-side leadership line, alongside Gregory Hall
(MD, CIO Payments & Treasury Technology), who leads the corresponding
engineering organization. Okafor and Hall together represent the
business/engineering split that runs throughout PTT: she sets product
direction and commercial accountability for TM products, while Hall's
organization designs, builds and operates the underlying systems. She leads
the business line documented at
[Treasury Management Products](../organizations/treasury-management-products.md).

## Role and scope

- **Title**: EVP, Head of Treasury Management Products.
- **Scope of ownership**: PTT's leadership roster records her scope as
  "Business owner, Treasury Management (TM) products incl. Crestline
  Business Online," making her the top-of-line accountable business owner
  for the entire TM product portfolio — of which CBO is the flagship
  client-facing channel.
- **Peer in PTT leadership**: She is listed directly alongside Gregory Hall
  (MD, CIO Payments & Treasury Technology, scope: all PTT engineering —
  channels, payments hub, networks, data), reflecting that TM product
  ownership and PTT engineering delivery are organized as separate,
  parallel lines that must coordinate on roadmap and delivery rather than
  one reporting into the other.
- **Business-only accountability**: Okafor is not named as technical owner
  of any system in the PTT system ownership register; day-to-day product
  ownership and the business-owner-of-record role for individual CBO
  systems sit with her direct report, Marcus Chen (see below). Okafor's
  accountability is portfolio-level commercial ownership of TM products,
  not sprint-level prioritization.

## Reporting structure

Beneath Okafor, **Marcus Chen (Director, Digital Treasury Product)** holds
day-to-day product ownership for the CBO Wire Center module and the
broader Payments & Transfers product line. Chen is the named business
owner of record for the Wire Center and CBO platform/entitlements systems,
and is the Product Owner engineering teams engage for sprint-level
prioritization and backlog decisions. Okafor is the EVP-level business
sponsor above him; engineering delivery for the same systems is organized
separately, under Gregory Hall's CIO line, through
[Digital Treasury Channels](../organizations/digital-treasury-channels.md)
(CBO Wire Center squad and CBO Platform & Entitlements, led by Director
Anjali Deshpande).

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: a semicolon inside a label breaks rendering; rephrase the label. -->
```text
graph TD
  GH["Gregory Hall<br/>MD, CIO Payments &amp; Treasury Technology"]
  DO["Danielle Okafor<br/>EVP, Head of Treasury Management Products"]
  MC["Marcus Chen<br/>Director, Digital Treasury Product<br/>(PO: CBO Wire Center, Payments &amp; Transfers)"]
  AD["Anjali Deshpande<br/>Director, Digital Treasury Channels Eng."]
  WC["CBO Wire Center squad"]
  PE["CBO Platform &amp; Entitlements"]

  DO --> MC
  GH --> AD
  AD --> WC
  AD --> PE
  MC -.->|business sponsorship /<br/>product ownership| WC
  MC -.->|business sponsorship /<br/>product ownership| PE
```

## Business ownership of CBO systems

The PTT system ownership register separates a **technical owner**
(accountable engineering manager/lead) from a **business owner**
(accountable product owner) for every system. For the CBO-related systems
within Okafor's TM portfolio, business ownership is delegated to Marcus
Chen rather than held directly by Okafor:

| System ID | System | Owning engineering team | Technical owner | Business owner | Support tier |
|---|---|---|---|---|---|
| SYS-CBO | Crestline Business Online — Wire Center module | CBO Wire Center squad | Tom Becker / Lucas Ferreira | Marcus Chen | T1 (24x7 critical) |
| SYS-CBO-SPS | CBO Status Projection Service | CBO Platform & Entitlements | Arjun Mehta | Marcus Chen | T2 |
| SYS-CES | Commercial Entitlements Service | CBO Platform & Entitlements | Nadia Haddad | Marcus Chen | T1 (24x7 critical) |

Okafor's role above this table is commercial and strategic: she holds P&L
and portfolio accountability for Treasury Management products as a whole
(of which CBO is one part), while Chen executes product ownership
day-to-day and engineering delivery sits entirely with PTT's engineering
organizations under Gregory Hall.

## Role as business sponsor of CBO features

As the top-of-line accountable business owner, Okafor's organization is
the ultimate business sponsor that initiates and prioritizes investment in
Treasury Management products, including CBO Wire Center and CBO platform
feature work — for example, closing functional gaps such as milestone
tracking, international (gpi) status display, hold-reason explanations, or
client self-service actions on held wires. Any such feature that changes
what CBO communicates to clients about payment status must additionally
clear enterprise governance gates outside her organization's direct
control: FCC Policy & Advisory review and Disclosure Review Committee
approval under POL-FCC-014 (owned by Catherine Doyle, EVP, Chief BSA/AML
Officer), and, for predictive or estimated completion-time statements,
Model Risk Management registration (owned by Jonathan Price). Business
sponsorship from Okafor's line is therefore necessary but not sufficient
to ship client-facing payment-status changes.

## Relationships

- **Engineering peer**: Gregory Hall, MD, CIO Payments & Treasury
  Technology — leads the engineering organization that builds and
  operates the systems Okafor's business line sponsors.
- **Direct report**: Marcus Chen, Director, Digital Treasury Product —
  holds day-to-day product ownership and is the business owner of record
  for CBO Wire Center, CBO Status Projection Service and Commercial
  Entitlements Service.
- **Engineering counterpart for delivery**: Anjali Deshpande, Director,
  Digital Treasury Channels Engineering — leads the CBO Wire Center squad
  and CBO Platform & Entitlements team that implement features Okafor's
  organization sponsors.
- **Governance partners**: Catherine Doyle (EVP, Chief BSA/AML Officer;
  owner of POL-FCC-014) and Jonathan Price (Head of Model Risk Management;
  owner of MRM-POL-02) — second-line partners whose sign-off gates
  client-facing changes to payment-status communication that Okafor's
  organization proposes.

## Related pages

- [Treasury Management Products](../organizations/treasury-management-products.md) — the business line Okafor leads.
- [Digital Treasury Channels](../organizations/digital-treasury-channels.md) — the PTT engineering organization that builds and operates CBO.
- [Payments & Treasury Technology](../organizations/payments-treasury-technology.md) — the broader PTT organization in which Okafor's business line and Hall's engineering line both sit.
- [Catherine Doyle](catherine-doyle.md) — second-line governance partner for client-facing payment-status changes.

## Source

Role, scope and reporting information on this page is drawn from the PTT
organization directory, **CNB-ORG-PTT-2026-06** (v2026.2, published
2026-06-15; refreshed quarterly). Because the directory is only refreshed
quarterly, organizational announcements issued between refreshes take
precedence over the roles and assignments recorded here.
