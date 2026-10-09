---
type: Organization
entity_id: treasury-management-products
title: Treasury Management Products
description: Business line within Payments & Treasury Technology, led by EVP Danielle Okafor, that owns Crestline Business Online and the broader Treasury Management client product suite and acts as business sponsor for CBO features.
tags: [treasury-management-products, organization, business-line, crestline-business-online, cbo, treasury-management, payments-treasury-technology, product-ownership]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-550c0e3f038aab7950cab477
    resource: repo://sources/estate/cbo-arch-wc-4.1-wire-center-current-state-architecture.md
  - id: openwiki-source-49303e801f124d97df9c3ea3
    resource: repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

Treasury Management Products is the business line, within Payments &
Treasury Technology (PTT), that owns **Crestline Business Online (CBO)** —
Crestline National Bank's commercial digital banking portal — and the
broader suite of Treasury Management (TM) products sold to commercial
clients. It is led by **Danielle Okafor, EVP, Head of Treasury Management
Products**, who sits alongside Gregory Hall (MD, CIO Payments & Treasury
Technology) in PTT's leadership team and is the accountable business owner
for TM products including CBO. Treasury Management Products is a
business-side organization: it sets product strategy and sponsors
client-facing features, while the corresponding engineering delivery is
done by PTT engineering organizations such as
[Digital Treasury Channels](digital-treasury-channels.md). See
[Danielle Okafor](../people/danielle-okafor.md) for role and reporting
detail, and [Crestline National Bank](crestline-national-bank.md) for how
this business line fits into CNB's overall payments organization.

## Position within PTT leadership

| Role | Name | Scope |
|---|---|---|
| MD, CIO Payments & Treasury Technology | Gregory Hall | All PTT engineering: channels, payments hub, networks, data |
| **EVP, Head of Treasury Management Products** | **Danielle Okafor** | **Business owner, Treasury Management (TM) products incl. Crestline Business Online** |
| Director, Digital Treasury Product | Marcus Chen | Product Owner, CBO Wire Center and Payments & Transfers |

Danielle Okafor reports at EVP level and is the top-of-line business owner
for the entire TM product portfolio, of which CBO is the flagship client
channel. Beneath her, **Marcus Chen (Director, Digital Treasury Product)**
holds day-to-day product ownership for the CBO Wire Center module and the
broader Payments & Transfers product line — he is the named business owner
of record for the Wire Center and entitlements systems (see below) and the
Product Owner engaged by engineering for sprint-level prioritization. The
PTT organization directory (CNB-ORG-PTT-2026-06) records Okafor's scope as
business ownership of TM products "incl. Crestline Business Online," while
engineering delivery for those same systems is organized separately under
PTT's CIO line.

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: a semicolon inside a label breaks rendering; rephrase the label. -->
```text
graph TD
  GH["Gregory Hall<br/>MD, CIO Payments & Treasury Technology"]
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

## Business/engineering split

Treasury Management Products exemplifies PTT's general pattern of
separating business ownership from engineering ownership: the system
ownership register in CNB-ORG-PTT-2026-06 lists a distinct **technical
owner** (accountable engineering manager/lead) and **business owner**
(accountable product owner) for every system. For the CBO-related systems
sponsored by this business line, the split is:

| System ID | System | Owning engineering team | Technical owner | Business owner | Support tier |
|---|---|---|---|---|---|
| SYS-CBO | Crestline Business Online — Wire Center module | CBO Wire Center squad | Tom Becker / Lucas Ferreira | Marcus Chen | T1 (24x7 critical) |
| SYS-CBO-SPS | CBO Status Projection Service | CBO Platform & Entitlements | Arjun Mehta | Marcus Chen | T2 |
| SYS-CES | Commercial Entitlements Service | CBO Platform & Entitlements | Nadia Haddad | Marcus Chen | T1 (24x7 critical) |

In this model, Marcus Chen — acting for Treasury Management Products — is
the business sponsor who prioritizes the roadmap and accepts delivered
work, while engineering delivery, on-call accountability, and technical
design authority sit with [Digital Treasury Channels](digital-treasury-channels.md)
engineering under Director Anjali Deshpande. New client-facing features or
architecture changes to these systems (e.g. the Wire Center's current-state
architecture, CBO-ARCH-WC-4.1) require sign-off from the engineering side
(Deshpande, plus the Chief Architect for architecture review) but are
driven and sponsored from the business side by Treasury Management
Products.

## Role as business sponsor of CBO features

Because Treasury Management Products owns the commercial relationship and
P&L for CBO, it is the business sponsor that initiates and prioritizes
Wire Center and CBO platform feature work — for example, closing known
functional gaps such as milestone tracking, international (gpi) status
display, hold-reason explanations, or client self-service actions on held
wires, all of which are tracked as roadmap items against the underlying
PRISM Payments Hub (PPH) API's current limitations rather than CBO defects.
Any such feature that changes what CBO communicates to clients about
payment status must additionally clear enterprise governance gates that sit
outside Treasury Management Products' direct control — FCC Policy &
Advisory review and Disclosure Review Committee approval under
POL-FCC-014, and, for any predictive or estimated completion-time
statement, Model Risk Management registration — so business sponsorship
from this line is necessary but not sufficient to ship client-facing
payment-status changes.

## Relationship to other organizations

- [Crestline National Bank](crestline-national-bank.md) — top-level
  organization page describing CNB's lines of business and how Treasury
  Management Products and PTT engineering fit together.
- [Digital Treasury Channels](digital-treasury-channels.md) — the PTT
  engineering organization (CBO Wire Center squad and CBO Platform &
  Entitlements) that builds and operates the systems this business line
  sponsors.
- [Danielle Okafor](../people/danielle-okafor.md) — EVP and accountable
  leader of Treasury Management Products.

## Source

Leadership scope, product ownership, and system business-ownership
assignments on this page are drawn from the PTT organization directory,
**CNB-ORG-PTT-2026-06** (v2026.2, published 2026-06-15; refreshed
quarterly). Because the directory is only refreshed quarterly,
organizational announcements issued between refreshes take precedence over
the roles and assignments recorded here.
