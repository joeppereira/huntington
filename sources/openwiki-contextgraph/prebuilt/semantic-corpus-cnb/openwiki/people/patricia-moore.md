---
type: Person
entity_id: patricia-moore
title: Patricia Moore
description: Chair of the Disclosure Review Committee (DRC), approving client-facing copy, disclaimers, and notification templates on a bi-weekly cadence for Payments & Treasury Technology (PTT) initiatives.
tags: [governance, legal, disclosure-review-committee, client-communications, payments-treasury-technology, compliance]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-49303e801f124d97df9c3ea3
    resource: repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

Patricia Moore chairs the **Disclosure Review Committee (DRC)**, the governance forum responsible for approving client-facing copy, disclaimers, and notification templates produced by teams across Payments & Treasury Technology (PTT). She is the named engagement contact for the **Legal - Treasury & Payments** partner function for product and design reviews that touch client communications.

## Organizational placement

Patricia Moore sits within the Legal - Treasury & Payments function, which is accountable to Andrew Feldman. Within this function she is the specific point of contact engineering and product teams should reach for reviews of client-facing language, rather than Andrew Feldman directly, when the review concerns disclosure content. See [Legal - Treasury & Payments](../teams/legal-treasury-payments.md) for the broader function and its other contacts.

## Disclosure Review Committee (DRC)

As Chair of the DRC, Patricia Moore oversees the forum that signs off on:

- Client-facing copy
- Disclaimers
- Notification templates

The DRC is one of several governance forums that PTT product and engineering teams must route work through before client-facing changes ship. Its operating parameters are:

| Attribute | Value |
|---|---|
| Cadence | Bi-weekly, Thursdays |
| Submission lead time | 5 business days before the session |
| Scope | Client-facing copy, disclaimers, notification templates |

Teams building or changing anything a customer sees or receives - for example notification content routed through the Enterprise Notification Service, or in-product disclaimers in Crestline Business Online - should plan DRC submission into their timelines alongside other sign-offs such as the Payments Architecture Review Board or FCT Change Advisory. Missing the 5-business-day submission window pushes a launch to the next bi-weekly session.

```mermaid
flowchart LR
    Team[Product / engineering team] -->|Submit copy, disclaimers,\nor notification template\n(5 business days lead time)| DRC[Disclosure Review Committee\nChair: Patricia Moore]
    DRC -->|Bi-weekly, Thursday| Decision{Approved?}
    Decision -->|Yes| Ship[Client-facing release proceeds]
    Decision -->|No / revise| Team
```

## Relationship to policy and compliance escalation

The DRC's approval authority is limited to review and sign-off of disclosure content itself. Compliance or policy interpretation questions - for example how a disclaimer should reflect obligations under financial-crimes or privacy policy such as [POL-FCC-014](../policies/pol-fcc-014.md) - are not decided by the DRC or by engineering teams; they route instead to FCC Policy & Advisory or the Privacy Office. Patricia Moore's committee therefore operates downstream of, and in coordination with, those policy-owning functions rather than substituting for them.

## How to engage

Teams needing DRC sign-off should submit the relevant copy, disclaimer, or notification template at least 5 business days ahead of the next bi-weekly Thursday session. For broader Legal - Treasury & Payments questions outside the scope of disclosure review, engage Andrew Feldman's function directly.
