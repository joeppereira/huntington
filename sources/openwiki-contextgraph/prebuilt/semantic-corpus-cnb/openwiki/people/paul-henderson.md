---
type: Person
entity_id: paul-henderson
title: Paul Henderson
description: Owner of the 'ENS Event Onboarding' ServiceNow catalog item, the required intake point for producers registering a new event type with the Enterprise Notification Service.
tags: [paul-henderson, ens, enterprise-notification-service, onboarding, servicenow, catalog-item, treasury]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-09T18:41:05.232Z
sources:
  - id: openwiki-source-d637e82ba742e8a4b8f0c799
    resource: repo://sources/estate/ens-int-3.2-enterprise-notification-service-integration-guide.md
generated: { by: "openwiki/0.7.0", at: "2026-10-09T18:41:05.232Z" }
---

## Overview

Paul Henderson is the designated owner of the **'ENS Event Onboarding'** ServiceNow catalog item, the formal intake mechanism for any producer team that wants to register a new event type with the [Enterprise Notification Service (ENS)](../systems/enterprise-notification-service.md). Per the ENS integration guide, submitting this catalog item is the mandatory first step of the ENS event-onboarding process.

## Responsibility: ENS Event Onboarding intake

The ENS onboarding workflow for a new event type is a five-step process, and Henderson's catalog item is the entry point that kicks it off:

1. **Submit ServiceNow catalog item 'ENS Event Onboarding'** (owner: Paul Henderson).
2. Define the payload schema and recipient resolution (subscription filters) for the new event type.
3. Draft templates per delivery channel and submit them to the Disclosure Review Committee (DRC), which meets bi-weekly.
4. ENS engineering configures and tests the new event type (approximately 12 engineering hours per event type).
5. The producer performs integration testing in UAT, followed by production enablement.

As the catalog item owner, Henderson's intake process is the entry point that a producer team (for example, CBO, CBO SPS, or CDP, the producers listed in the Treasury event catalog) must pass through before any new `TRS.*`-style event type can be defined, templated, and go live in ENS.

## Operational context

- The overall onboarding SLA is **6 weeks** from complete submission (via the catalog item) to production, inclusive of DRC review.
- Submissions made after **2026-11-20** are scheduled after the year-end change freeze, which affects planning for any producer intending to onboard a new event type before year end.
- Templates for financial-crimes-related states must use FCC-approved copy (POL-FCC-014, Appendix B), a content rule that onboarding submissions must satisfy before they can proceed through DRC review.

## Relationships

- **[Enterprise Notification Service](../systems/enterprise-notification-service.md)** — the platform for which Henderson's catalog item governs new event-type onboarding; ENS resolves recipients from subscriptions, renders approved templates, and delivers across email, SMS, mobile push, and the CBO in-app inbox.
- **Disclosure Review Committee (DRC)** — reviews channel templates drafted during step 3 of the onboarding flow that the catalog item initiates.
- **Producer teams (CBO, CBO SPS, CDP, etc.)** — the organizations that must file an 'ENS Event Onboarding' request through Henderson's catalog item to register any new Treasury (TRS) or other domain event type.

## Source

This page is derived from the ENS Integration Guide & Treasury Event Catalog (document ENS-INT-3.2, v3.2, owned by Melissa Grant, EM - Enterprise Notification Service; approved by Sanjay Iyer, Director, Enterprise Notification Platform), which names Paul Henderson as the owner of the 'ENS Event Onboarding' catalog item.
