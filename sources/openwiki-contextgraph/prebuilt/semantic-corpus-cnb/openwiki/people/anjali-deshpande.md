---
type: Person
entity_id: anjali-deshpande
title: Anjali Deshpande
description: Director, Digital Treasury Channels Engineering at Crestline National Bank; accountable engineering leader for the CBO Wire Center squad and CBO Platform & Entitlements, and architecture/incident-review approver for Wire Center systems.
tags: [people, digital-treasury-channels, cbo, wire-center, director, payments-treasury-technology, architecture-approver, engineering-leadership]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-550c0e3f038aab7950cab477
    resource: repo://sources/estate/cbo-arch-wc-4.1-wire-center-current-state-architecture.md
  - id: openwiki-source-49303e801f124d97df9c3ea3
    resource: repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md
  - id: openwiki-source-3cc45df143c5eec31fe1f9f6
    resource: repo://sources/estate/pir-2024-07-wire-status-lite-pilot-inc-2024-1182-post-implementation-review.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

Anjali Deshpande is **Director, Digital Treasury Channels Engineering**
within Payments & Treasury Technology (PTT) at Crestline National Bank
(CNB). She is the accountable engineering leader for the two teams that
build and operate Crestline Business Online's (CBO) client-facing digital
channel — the **CBO Wire Center squad** and **CBO Platform &
Entitlements** — and is the named engineering approver of record for the
Wire Center's governing architecture document and for the post-incident
review of the 2024 Wire Status Lite pilot.

## Role and reporting line

Deshpande reports to **Gregory Hall**, MD and CIO of Payments & Treasury
Technology, and leads Digital Treasury Channels Engineering as one of the
engineering organizations under PTT's CIO line. She works alongside, but
is organizationally distinct from, **Marcus Chen**, Director of Digital
Treasury Product, who holds business/product ownership (Product Owner) of
the Wire Center and the broader Payments & Transfers product line. This
reflects PTT's general pattern of separating business ownership from
engineering ownership: Chen sets roadmap priorities and is the named
business owner in the system ownership register, while Deshpande owns
engineering delivery, technical design authority, and on-call/support
accountability for the underlying systems.

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: an unescaped angle bracket inside a label breaks rendering; rephrase the label. -->
```text
graph TD
  GH["Gregory Hall<br/>MD, CIO Payments & Treasury Technology"]
  MC["Marcus Chen<br/>Director, Digital Treasury Product<br/>(Product Owner: Wire Center)"]
  AD["Anjali Deshpande<br/>Director, Digital Treasury Channels Eng."]
  WC["CBO Wire Center squad<br/>Tom Becker (EM), Lucas Ferreira (Tech Lead)"]
  PE["CBO Platform & Entitlements<br/>Nadia Haddad (EM), Arjun Mehta (Tech Lead)"]

  GH --> AD
  AD --> WC
  AD --> PE
  MC -.->|Product Owner for Wire Center| WC
```

Within her organization, Deshpande's direct reports/teams are:

- **CBO Wire Center squad** — Tom Becker (Engineering Manager), Lucas
  Ferreira (Tech Lead), with Marcus Chen as Product Owner — owns the
  `cbo-wire-bff` and Wire Center micro-frontend (system `SYS-CBO`, Tier 1,
  24x7 critical support).
- **CBO Platform & Entitlements** — Nadia Haddad (Engineering Manager),
  Arjun Mehta (Tech Lead for the Status Projection Service and Commercial
  Entitlements Service) — owns `SYS-CBO-SPS` (Tier 2) and `SYS-CES`
  (Tier 1, 24x7 critical).

See [Digital Treasury Channels](../organizations/digital-treasury-channels.md)
for the full organization writeup, and
[CBO Wire Center squad](../teams/cbo-wire-center-squad.md) for the squad's
day-to-day engagement and planning details.

## Approval authority

### CBO-ARCH-WC-4.1 (Wire Center current-state architecture)

Deshpande is one of two named approvers — alongside **Nikhil Bose**, Chief
Architect for Payments & Treasury — of **CBO-ARCH-WC-4.1**, "Crestline
Business Online - Wire Center: Current-State Architecture," version 4.1,
status Approved, last reviewed 2026-08-20. This document is the
authoritative current-state record of Wire Center's integrations, status
model, identifiers, security/entitlements model, and known constraints
(including the no-polling rule from ADR-PAY-019 and the planned PPH v1
sunset). As an approver rather than the document owner (document owner is
Lucas Ferreira, Tech Lead), Deshpande's sign-off gives the document
standing as an approved architecture record rather than a draft, and marks
engineering-leadership acceptance of the documented constraints and
reuse plan. See
[CBO-ARCH-WC-4.1](../documents/cbo-arch-wc-4.1.md) for the full document
summary.

### PIR-2024-07 (Wire Status Lite post-implementation review)

Deshpande is also one of three named approvers — alongside **Raymond
Ortiz** (Director, Payments Hub Engineering) and **Denise Carter**
(accountable owner, Payment Operations) — of **PIR-2024-07**, the
post-implementation review of the **Wire Status Lite** pilot (CBO-3120)
and the resulting incident **INC-2024-1182**. That pilot auto-refreshed
wire status in CBO by polling the PPH v1 status API from the browser every
30 seconds for 60 clients between January and May 2024; on 2024-05-31
(month-end), combined pilot and production refresh traffic drove roughly
85 TPS against the v1 status API, exhausting its thread pool and delaying
wire release for 47 minutes (1,240 wires delayed, 312 released after the
Fedwire customer cutoff, 14 clients compensated $41,800 total). The pilot
was terminated and its epic closed. Deshpande's approval of the final
(1.1) revision closes the review across the three accountable leadership
areas it touched — Wire Center engineering (her own organization),
Payments Hub engineering (Ortiz), and Payment Operations (Carter) — and
endorses its root-cause findings and remediation actions, including the
adoption of an event-driven (non-polling) status pattern that became
[ADR-PAY-019](../decisions/adr-pay-019.md). See
[PIR-2024-07](../documents/pir-2024-07.md) for the document record and the
[incident page](../incidents/pir-2024-07.md) for the full narrative.

Because the Wire Status Lite incident directly produced the no-polling
constraint documented in CBO-ARCH-WC-4.1 (which Deshpande also approved),
her approver role spans both the incident that established the
architectural guardrail and the current-state document that encodes it —
making her the single engineering-leadership accountability point across
that cause-and-effect chain for Wire Center status handling.

## Relationships

- **Gregory Hall** — MD, CIO Payments & Treasury Technology; Deshpande's
  reporting line.
- **Marcus Chen** — Director, Digital Treasury Product; Product Owner for
  Wire Center and Payments & Transfers; business/product counterpart to
  Deshpande's engineering accountability.
- **Tom Becker** — Engineering Manager, CBO Wire Center squad; document
  owner of PIR-2024-07, reporting into Deshpande's organization.
- **Lucas Ferreira** — Tech Lead, CBO Wire Center squad; document owner of
  CBO-ARCH-WC-4.1, reporting into Deshpande's organization.
- **Nadia Haddad** — Engineering Manager, CBO Platform & Entitlements,
  reporting into Deshpande's organization.
- **Nikhil Bose** — Chief Architect, Payments & Treasury; co-approver of
  CBO-ARCH-WC-4.1.
- **Raymond Ortiz** and **Denise Carter** — co-approvers of PIR-2024-07,
  representing Payments Hub Engineering and Payment Operations
  respectively.

## Related pages

- [Digital Treasury Channels](../organizations/digital-treasury-channels.md)
- [CBO Wire Center squad](../teams/cbo-wire-center-squad.md)
- [CBO-ARCH-WC-4.1](../documents/cbo-arch-wc-4.1.md)
- [PIR-2024-07](../documents/pir-2024-07.md)
