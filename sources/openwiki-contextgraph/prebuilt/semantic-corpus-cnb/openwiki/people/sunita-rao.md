---
type: Person
entity_id: sunita-rao
title: Sunita Rao
description: Principal Engineer on Payments Hub Engineering at Crestline National Bank; co-technical owner of PRISM Payments Hub (SYS-PPH), designer of the PPH v1 and v2 payments APIs, and document owner of PPH-API-CAT-2026.3.
tags: [people, principal-engineer, payments-hub-engineering, pph, prism-payments-hub, pph-api-cat-2026.3, api-design, system-ownership]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-49303e801f124d97df9c3ea3
    resource: repo://sources/estate/cnb-org-ptt-2026-06-ptt-organization-system-ownership-engagement-directory.md
  - id: openwiki-source-4452149a3b4502b4c763a559
    resource: repo://sources/estate/jira-export-wt-discovery-2026-10-05.md
  - id: openwiki-source-a4ee8b1dfcb7e3cec0a315e4
    resource: repo://sources/estate/pph-api-cat-2026.3-prism-payments-hub-api-and-event-catalog.md
  - id: openwiki-source-19beabaf3acaad354d39ee1e
    resource: repo://sources/estate/pph-sys-ovw-9.2-prism-payments-hub-system-overview-and-lifecycle-state-model.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

Sunita Rao is the Principal Engineer on the Payments Hub Engineering team within Payments & Treasury Technology (PTT) at Crestline National Bank. She is the named designer of record for both the deprecated [PPH v1 Wire Status API](../interfaces/pph-v1-wire-status-api.md) and the current [PPH v2 Payments API](../interfaces/pph-v2-payments-api.md), and she owns **PPH-API-CAT-2026.3**, the "PRISM Payments Hub - API & Event Catalog (v1/v2) incl. v1 Deprecation Notice," the consumer-facing reference document for every REST API and Kafka topic exposed by [PRISM Payments Hub](../systems/prism-payments-hub.md) (PPH).

Alongside Kevin O'Brien (Engineering Manager), she is listed as co-technical owner of `SYS-PPH` in the PTT system ownership register. She reports, along with Kevin O'Brien, into Raymond Ortiz (Director, Payments Hub Engineering), and works alongside Laura Kim (Director, Payments Platform Product), the business owner of PPH and Business Data Owner for payment datasets.

## Role and reporting line

| Attribute | Value |
|---|---|
| Team | Payments Hub Engineering |
| Title | Principal Engineer |
| Director | Raymond Ortiz |
| Peer technical contact | Kevin O'Brien (Engineering Manager) |
| Product Owner / business owner | Laura Kim (Director, Payments Platform Product) |
| Jira project / Slack | PPH / `#pph-support` |

Within the PTT engineering team directory, Payments Hub Engineering is the owning team for `SYS-PPH` (PRISM Payments Hub, running Volaris 9.4), a Tier 1 (24x7 critical) system. The directory records the "technical owner" as the accountable engineering manager/lead for a system, as distinct from its "business owner" (accountable product or data owner); Sunita Rao and Kevin O'Brien jointly hold that technical-owner role for `SYS-PPH`, with Laura Kim as business owner.

## Document ownership: PPH-API-CAT-2026.3

Sunita Rao is the document owner of **PPH-API-CAT-2026.3** ("PRISM Payments Hub - API & Event Catalog (v1/v2) incl. v1 Deprecation Notice"), version 2026.3, published 2026-09-10 and classified INTERNAL - CONFIDENTIAL. The catalog is approved by Kevin O'Brien (EM) and Raymond Ortiz (Director), and is the system of record consumer teams use to pick an API version, understand field semantics and limits, and track the mandatory migration off v1. See [PPH-API-CAT-2026.3](../documents/pph-api-cat-2026.3.md) for the document's full content record.

As document owner, she is listed as the "API design" contact at the end of the catalog, alongside Kevin O'Brien (scheduling via the Payments Platform Demand Board) and Laura Kim (product). The catalog cross-references PPH-SYS-OVW-9.2 (system overview), ADR-PAY-019, ADR-PAY-021, and ADR-PAY-023 — the architecture decisions underpinning the v2 API design — and the backlog tickets PPH-2190 (v1 sunset tracking) and PPH-2207 (proposed v2 settlement object).

She is also recorded, alongside Kevin O'Brien, as the day-to-day author/owner of **PPH-SYS-OVW-9.2** ("PRISM Payments Hub - System Overview & Wire Lifecycle State Model"), co-approved with Laura Kim and Raymond Ortiz, which defines the canonical v2 lifecycle state model, the v1-to-v2 status mapping, rail-specific settlement semantics, and identifier scoping (`pphId`, IMAD, OMAD, UETR, `EndToEndId`) that the API catalog builds on. See [PPH-SYS-OVW-9.2](../documents/pph-sys-ovw-9.2.md).

## Designer of record: PPH v1 and v2 APIs

### v1 (deprecated, sunset 2027-03-31)

Sunita Rao is the designer of record for PPH's original REST surface, three endpoints (`EP-PPH-01` status, `EP-PPH-02` list, `EP-PPH-03` submit) documented in detail on [PPH v1 Wire Status API](../interfaces/pph-v1-wire-status-api.md). The v1 adapter is not supported on the vendor's upcoming Volaris 9.6 upgrade (April 2027), and the Payments Architecture Review Board (ARB) confirmed on 2026-09-08 that no sunset extension beyond 2027-03-31 will be granted. The catalog she owns records the per-consumer migration tracking for this sunset (tracked as epic PPH-2190, owned by Kevin O'Brien):

| v1 consumer | Owner | Migration status |
|---|---|---|
| IVR wire status | Contact Center Tech | Migrated (2026-05) |
| Service Center CRM | CRM Engineering | In progress (target 2026-12) |
| `cbo-wire-bff` (Wire Center) | CBO Wire Center squad | Not started (CBO-4471, unscheduled) |
| Wire Room console | Payment Operations Tech | Migrated to IWB (2025) |

### v2 (GA 2025-10)

v2 (`EP-PPH-04`..`07`, documented on [PPH v2 Payments API](../interfaces/pph-v2-payments-api.md)) replaced v1's coarse `status` enum with a single `lifecycleState` field and added a richer, rail-aware `identifiers` object (including `uetr` and `omad`, neither available in v1) per [ADR-PAY-023](../decisions/adr-pay-023.md). v1's legacy `holdReasonDesc` free-text field was deliberately not carried into v2 per [ADR-PAY-021](../decisions/adr-pay-021.md) — v2 surfaces only hold presence (`isHeld`, `holdId`), not raw hold detail. v2 reached general availability in 2025-10 and is published at 99.95% availability / 180 ms p95 latency / T1 support, versus v1's 99.9% / 350 ms / best-effort-until-sunset.

Two open backlog items against v2, both tracked in the catalog she owns, remain relevant to API consumers:

- **PPH-2207** — a proposed v2 settlement object (`fedSettlementTs` sourced from pacs.002/OMAD, plus rail-specific `settlementStatus`); backlog, 8 points, awaiting a product sponsor.
- **PPH-2251** — v2 search does not index beneficiary name, only `clientId`; backlog.

## FCT-2004: hold-reason leak raised to Sunita Rao

Sunita Rao is the named PPH-side recipient of **FCT-2004** (Risk, Open), raised by Daniel Kowalski (Financial Crimes Technology) in 2026-05. The issue: PPH v1's `holdReasonDesc` field synchronizes free-text Hold Management Service (HMS) content — including Hold Reason Code (HRC) mnemonics and analyst casework notes, classified Restricted — into an API field with no access controls tailoring it for client-facing display. Daniel Kowalski raised the issue to both Sunita Rao (PPH) and Tom Becker (CBO Wire Center); remediation options under consideration are to stop the HMS-to-PPH field sync or to redact the field at the API gateway. As document owner, Sunita Rao's catalog records that `holdReasonDesc` content "is not curated for external display" and that the field has no v2 equivalent, consistent with the ADR-PAY-021 decision to exclude raw hold detail from v2. As of the catalog's 2026-09-10 publication and the broader estate record, no remediation has shipped, and the v1 sunset (2027-03-31) is noted as a possible path to mooting the issue by retiring the field's only consumer path (v1) rather than remediating it directly — a risk made more concrete by CBO-4388, an in-progress Wire Center feature that would surface `holdReasonDesc` as a client-visible tooltip.

## Related pages

- [PRISM Payments Hub](../systems/prism-payments-hub.md) — the system she co-technically owns (`SYS-PPH`).
- [PPH v1 Wire Status API](../interfaces/pph-v1-wire-status-api.md) — the deprecated API surface she designed.
- [PPH v2 Payments API](../interfaces/pph-v2-payments-api.md) — the current API surface she designed.
- [PPH-API-CAT-2026.3](../documents/pph-api-cat-2026.3.md) — the API/event catalog document she owns.
- [PPH-SYS-OVW-9.2](../documents/pph-sys-ovw-9.2.md) — the system overview document she co-owns with Kevin O'Brien.
