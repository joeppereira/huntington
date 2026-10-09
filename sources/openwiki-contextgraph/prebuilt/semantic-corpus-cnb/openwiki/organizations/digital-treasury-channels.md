---
type: Organization
entity_id: digital-treasury-channels
title: Digital Treasury Channels
description: Engineering organization led by Anjali Deshpande that owns Crestline Business Online's client-facing digital channel, comprising the CBO Wire Center squad and CBO Platform & Entitlements teams.
tags: [digital-treasury-channels, cbo, wire-center, organization, treasury-management, crestline-business-online, payments-treasury-technology]
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

Digital Treasury Channels is the engineering organization, led by Director
**Anjali Deshpande**, that builds and operates the client-facing digital
channel for Crestline Business Online (CBO) — Crestline National Bank's
commercial digital banking portal (web and mobile) serving Treasury
Management clients. The organization sits inside Payments & Treasury
Technology (PTT), under MD/CIO Gregory Hall, and partners closely with the
Treasury Management product line owned by EVP Danielle Okafor.

Digital Treasury Channels is made up of two engineering teams:

- [CBO Wire Center squad](../teams/cbo-wire-center-squad.md) — owns the
  Wire Center module (domestic Fedwire and international Swift wire
  initiation, templates, approvals, release, and activity/status display)
  inside CBO.
- [CBO Platform & Entitlements](../teams/cbo-platform-entitlements.md) —
  owns shared CBO platform capabilities consumed by Wire Center and other
  CBO modules, including the Commercial Entitlements Service (CES) and the
  Status Projection Service (SPS).

Anjali Deshpande is the accountable Director for both teams and is the
named approver of record for Wire Center architecture decisions (e.g.
CBO-ARCH-WC-4.1). See [Anjali Deshpande](../people/anjali-deshpande.md) for
role and reporting details.

## Position within Payments & Treasury Technology

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: an unescaped angle bracket inside a label breaks rendering; rephrase the label. -->
```text
graph TD
  GH["Gregory Hall<br/>MD, CIO Payments & Treasury Technology"]
  DO["Danielle Okafor<br/>EVP, Head of Treasury Management Products"]
  MC["Marcus Chen<br/>Director, Digital Treasury Product<br/>(Product Owner: Wire Center, Payments & Transfers)"]
  AD["Anjali Deshpande<br/>Director, Digital Treasury Channels Eng."]
  WC["CBO Wire Center squad<br/>Tom Becker (EM), Lucas Ferreira (Tech Lead)"]
  PE["CBO Platform & Entitlements<br/>Nadia Haddad (EM), Arjun Mehta (Tech Lead)"]

  GH --> AD
  DO --> MC
  AD --> WC
  AD --> PE
  MC -.->|Product Owner for Wire Center| WC
```

Digital Treasury Channels is an engineering-side organization: product
direction for its systems is set by Marcus Chen (Director, Digital
Treasury Product), who is Product Owner for both CBO Wire Center and the
broader Payments & Transfers product line, while Anjali Deshpande owns
engineering delivery and technical accountability. This engineering/product
split means roadmap prioritization flows through Marcus Chen while
technical design authority and on-call/support accountability sit with
Deshpande's organization.

## Owned systems

| System ID | System | Owning team | Technical owner | Business owner | Support tier |
|---|---|---|---|---|---|
| SYS-CBO | Crestline Business Online - Wire Center module | CBO Wire Center squad | Tom Becker / Lucas Ferreira | Marcus Chen | T1 (24x7 critical) |
| SYS-CBO-SPS | CBO Status Projection Service | CBO Platform & Entitlements | Arjun Mehta | Marcus Chen | T2 |
| SYS-CES | Commercial Entitlements Service | CBO Platform & Entitlements | Nadia Haddad | Marcus Chen | T1 (24x7 critical) |

Both SYS-CBO (Wire Center) and SYS-CES (entitlements) carry Tier-1, 24x7
support obligations because they gate client-facing money movement and
authorization; SYS-CBO-SPS is Tier-2 because it currently only backs ACH
status projection, not wires.

## CBO Wire Center squad responsibilities

The Wire Center squad owns the `cbo-wire-bff` (Java 21 / Spring Boot 3, on
OpenShift) and the Wire Center micro-frontend (React 18, Aurora DS v4).
Together these provide, for CBO clients:

- Domestic (Fedwire) and international (Swift) wire initiation
- Wire templates
- Dual approval and release with step-up authentication
- A wire activity list, wire detail view, CSV export, and confirmation PDF
  download

Wire Center explicitly does **not** currently provide milestone tracking,
international (gpi) status, hold-reason explanations, or client actions on
held wires — these are known architectural gaps tracked against the
PRISM Payments Hub (PPH) v1 API's limitations.

### Key integrations

`cbo-wire-bff` is the sole backend integration point for the Wire Center
MFE and calls out to:

- **PRISM Payments Hub (PPH) v1** — `POST /pph/v1/wires` to submit a wire,
  `GET /pph/v1/wires?clientId...` for the activity list (max 500 rows, no
  cursor), and `GET /pph/v1/wires/{ref}/status` for wire detail status
  (cached 60s, refresh throttled to 1 request/60s per wire).
- **Commercial Entitlements Service (CES)** — `GET
  /ces/v2/users/{id}/entitlements`, used to authorize users and filter
  activity-list results to their entitled accounts.
- **CBO Auth** — `POST /cbo/auth/v2/step-up`, used for step-up
  authentication (push or OTP) on wire release and reusable for other
  high-risk client actions.
- **Enterprise Notification Service (ENS)** — `POST /ens/v3/notifications`,
  used to emit `TRS.WIRE.APPROVAL_REQUIRED`, `TRS.WIRE.RELEASED`, and
  `TRS.WIRE.REJECTED` notification events across email, push, in-app, and
  (for release) opt-in SMS.

Wire Center does **not** use the CBO Status Projection Service (SPS, which
is ACH-only today), PPH v2 APIs, `pay.wire.lifecycle.v2`, gpi data, or Hold
Management Service (HMS) APIs. gpi status visibility is restricted to
Payment Operations via the Investigations Workbench.

### Status model and identifiers

Wire Center derives its client-facing status labels from PPH v1 statuses,
with pre-submission states (Draft, Pending Approval, Approved) owned by
CBO itself:

| PPH v1 status | CBO label | Visual |
|---|---|---|
| DRAFT / PENDING_APPROVAL / APPROVED | Draft / Pending Approval / Approved | grey |
| RECEIVED | Submitted | blue |
| PENDING | In Process | blue |
| HELD | Pending Review | amber |
| PROCESSED | Completed (renamed from "Processed" in release R26.1) | green check |
| REJECTED | Rejected | red |
| CANCELLED | Cancelled | grey |
| RETURNED | Returned | red |

Held wires show a generic "Pending Review" / "This wire is being reviewed"
message; hold reasons are not surfaced to clients today.

Wire Center persists its own `cboRef` as primary key alongside the PPH
`pphId`; it displays but does not persist the Fedwire IMAD, and has no
access to OMAD or UETR values under the PPH v1 integration.

### Operating constraints

- **No status polling.** Per ADR-PAY-019 (issued following INC-2024-1182),
  Wire Center must not poll PPH for status; only throttled, user-initiated
  refresh (1 per 60s per wire) is permitted, and any new status capability
  must be event-driven rather than poll-based.
- **PPH v1 sunset 2027-03-31.** Migration to PPH v2 is tracked as CBO-4471
  and depends on CES account-filter mapping work (CBO-4473).
- **No international wire tracking.** Swift gpi status is not available to
  Wire Center or CBO clients; it is visible only to Payment Operations.
- **Activity list limits.** The v1 list API caps results at 500 rows with
  no cursor and no server-side beneficiary-name search.
- **External sharing is out of scope.** Sharing client transaction data
  with non-users (links/documents) is not supported and would require an
  InfoSec design review (SEC-STD-22) and a Privacy Impact Assessment
  before being built.

### Reusable platform assets

The squad can build on several existing assets rather than building new
primitives:

- `<cbo-journey-timeline>` Aurora DS v4 component (from the ACH Payment
  Tracker, CBO-3802) — a rail-agnostic milestone timeline with
  terminal/error styling.
- **Status Projection Service (SPS)** (CBO-3815, owned by CBO Platform &
  Entitlements) — a Kafka-consumer-backed Postgres read model exposed via
  `/cbo/sps/v1`; extending it to wires requires a new mapping module and a
  consumer ACL on `pay.wire.lifecycle.v2`.
- **Step-up authentication** (CBO Auth v2) — already used for wire
  release and reusable for other high-risk actions.
- **ENS producer library** (`cbo-commons` 3.x) — templated notification
  sends with masking helpers.

## CBO Platform & Entitlements responsibilities

CBO Platform & Entitlements, led by EM Nadia Haddad with Arjun Mehta as
Tech Lead for SPS and CES, owns the shared platform services that Wire
Center (and other CBO modules) depend on:

- **Commercial Entitlements Service (CES)** — authorization and
  account-level entitlement filtering for CBO users (`WIRE_VIEW`,
  `WIRE_INITIATE`, `WIRE_APPROVE`, `WIRE_RELEASE`,
  `WIRE_TEMPLATE_ADMIN` and other entitlement types).
- **CBO Status Projection Service (SPS)** — the Kafka-to-Postgres status
  read-model service, currently scoped to ACH payment status only.

Because CES sits in the authorization path for every wire action, its
Tier-1 support classification reflects that an outage blocks client wire
activity even if Wire Center itself is healthy.

## Engagement and planning

- **Intake:** Jira project `CBO` for Wire Center work, and the separate
  Jira `CBO (Platform)` board with a two-week triage cadence for platform
  work; Slack channels `#cbo-wire-center` and `#cbo-platform`.
- **Planning factors (PI 27.1 snapshot):** CBO Wire Center squad sizes at
  roughly 1 story point ≈ 6.5 engineering hours with a velocity around 42
  points/sprint, and was tracked at ~85% committed for Q4-2026. CBO
  Platform & Entitlements uses the same ~6.5 hr/point factor at roughly 30
  points/sprint and was ~70% committed.
- **Governance:** New client-facing integrations to payment systems
  require Payments Architecture Review Board (ARB) approval (monthly, 2nd
  Tuesday, 10 business days' lead time), chaired by Chief Architect Nikhil
  Bose. Client-facing copy, disclaimers, and notification templates (such
  as the `TRS.WIRE.*` notification templates Wire Center produces) require
  sign-off from the Disclosure Review Committee (bi-weekly, 5 business
  days' lead time).
- **Dependency escalation:** Unresolved cross-team dependency conflicts
  escalate from engineering managers to the respective Directors (e.g.
  Anjali Deshpande for Digital Treasury Channels systems), then to the PTT
  Leadership Team, which meets weekly on Mondays.

## Related pages

- [Anjali Deshpande](../people/anjali-deshpande.md)
- [CBO Wire Center squad](../teams/cbo-wire-center-squad.md)
- [CBO Platform & Entitlements](../teams/cbo-platform-entitlements.md)
