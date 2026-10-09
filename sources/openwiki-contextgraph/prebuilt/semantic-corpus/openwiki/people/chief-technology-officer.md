---
type: Person
title: Marcus O. Lindqvist, Chief Technology Officer
description: Profile of Marcus O. Lindqvist, Chief Technology Officer of Meridian Harbor Financial Corp., who oversees the single Developer Platform exposing eighteen production APIs to internal applications, clients and approved third parties.
tags: [person, chief-technology-officer, developer-platform, apis, meridian-harbor, technology-leadership]
verified:
  - by: openwiki/0.7.0
    at: 2026-10-05T01:46:21.335Z
sources:
  - id: openwiki-source-eb14da62fbec45aad876fb64
    resource: repo://sources/reports/mhfc-2025-annual-report.md
  - id: openwiki-source-9da334bbfcfb68cd7514ff33
    resource: repo://sources/reports/mhfc-q2-2026-earnings-supplement.md
generated: { by: "openwiki/0.7.0", at: "2026-10-05T01:46:21.335Z" }
---

# Marcus O. Lindqvist, Chief Technology Officer

Marcus O. Lindqvist is the Chief Technology Officer (CTO) of Meridian Harbor Financial Corp. (MHFC), a fictional institution used in a synthetic proof-of-concept corpus. The sources name him in one role: the executive under whose oversight the Firm runs its [Developer Platform](../apis/developer-platform-overview.md). Both documents that mention him are corporate disclosures, so the facts below come from the 2025 Annual Report and one analyst Q&A in the Q2 2026 earnings supplement.

## What the sources say about the role

The 2025 Annual Report's *Operational, Technology and Cybersecurity Risk* section states: "Under the oversight of Chief Technology Officer Marcus O. Lindqvist, the Firm operates a single Developer Platform that exposes eighteen production APIs to internal applications, clients and approved third parties."

The sources do not give his reporting line, tenure, organization chart, or any other title. They do not say who runs the platform day to day. See [Developer Platform Engineering](../teams/developer-platform-engineering.md) for the team view. The CEO page notes the same gap, saying the report does not state who the CTO reports to ([Chief Executive Officer](chief-executive-officer.md)).

## Responsibilities: the Developer Platform

The annual report describes the platform he oversees as follows:

- **One platform, eighteen production APIs.** The glossary identifies them as API-01 to API-18. The Letter to Shareholders says they cover accounts, payments, cards, credit, market data and regulatory reporting.
- **Audiences.** Internal applications, clients and approved third parties. The report also says the APIs are not only client products: they are governed data feeds for the Firm's most important risk models.
- **Standard controls.** APIs are versioned, authenticated with OAuth 2.0 (with mutual TLS for server-to-server traffic), rate-limited, and monitored against published service-level objectives.
- **Scale and reliability (2025).** The platform handled an average of 4.0 billion calls per month with 99.97% availability.
- **Critical data services.** APIs that feed Tier 1 models or regulatory reports are classified as critical data services, with enhanced change management and data-quality controls. The report names six:
  - [Credit Risk Scoring API (API-10)](../apis/api-10-credit-risk-scoring-api.md)
  - [Loan Servicing API (API-11)](../apis/api-11-loan-servicing-api.md)
  - [Market Data API (API-12)](../apis/api-12-market-data-api.md)
  - [Macroeconomic Scenario API (API-14)](../apis/api-14-macroeconomic-scenario-api.md)
  - [Treasury Liquidity Positions API (API-15)](../apis/api-15-treasury-liquidity-positions-api.md)
  - [Regulatory Reporting API (API-16)](../apis/api-16-regulatory-reporting-api.md)

## Why the platform matters beyond client products

Two disclosures tie the CTO's remit to the Firm's risk and capital processes.

1. **Shared pipes for clients and regulators.** The CEO's letter says the APIs are the governed data feeds for the models that set the allowance for credit losses, measure interest rate risk and project capital under stress. It calls building one well-controlled set of data pipes for both clients and regulators one of the year's most important accomplishments. The annual report's model inventory lists upstream APIs for three Tier 1 models:

   | Model | Upstream APIs |
   |---|---|
   | MDL-ALM-014, Net Interest Income Sensitivity Model | API-12, API-15, API-11 |
   | MDL-CR-007, CECL Lifetime Expected Credit Loss Model | API-10, API-11, API-14 |
   | MDL-CAP-003, Capital Planning & Stress Projection Model | API-16, API-14, API-15 |

2. **Quoted benefit (Q2 2026 call).** Asked about the payoff of the API platform beyond client products, Lindqvist said the same governed APIs sold to clients feed the risk models. As an example, he said that moving the Macroeconomic Scenario API to the "strategic platform" cut the scenario load for the CECL and capital models from six hours to forty minutes. He said this lets the Firm run more scenarios and close the quarter faster with better controls.

## Investment context

The annual report says the Firm spent $16.8 billion on technology in 2025, roughly half of it on new capabilities. Technology, communications and equipment expense rose 7.3% to $7.96 billion. The report attributes the rise to migrating more applications to public and private cloud, expanding the Developer Platform, and retiring 1,140 legacy applications. It does not attribute these figures to Lindqvist personally.

## Relationships to other leaders

- **Chief Executive Officer.** Eleanor V. Ashcombe, Chairman and CEO, signs the shareholder letter that describes the Developer Platform ([Chief Executive Officer](chief-executive-officer.md)).
- **Chief Risk Officer.** Dana K. Whitfield is a separate role. Her organization sets model-risk and data-risk expectations that the Tier 1 feeds must meet ([Chief Risk Officer](chief-risk-officer.md)). The CTO oversees the platform that supplies the data, not the models or their validation.
- **Model owners.** The three Tier 1 models are owned by Treasury and Credit Risk groups, not by technology, according to the model inventory.

## Open questions

The sources leave several things unstated: his reporting line, appointment date, direct reports, platform budget, and whether he sits on any governance committee. This page does not infer them.

## Sources

- 2025 Annual Report, *Letter to Shareholders*, *Management's Discussion and Analysis* (expense discussion), model inventory, and *Operational, Technology and Cybersecurity Risk* (`sources/reports/mhfc-2025-annual-report.md`).
- Q2 2026 earnings supplement, *Technology and APIs* Q&A (`sources/reports/mhfc-q2-2026-earnings-supplement.md`).
