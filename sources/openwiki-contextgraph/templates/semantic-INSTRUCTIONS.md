# OpenWiki brief: Meridian Harbor semantic knowledge graph

<!-- Copy to semantic-corpus/openwiki/INSTRUCTIONS.md before running `openwiki --init`.
     OpenWiki reads this file for scope and priorities and never rewrites it. -->

## What this repository is

This repository is NOT a software codebase. It is a document corpus about a fictional bank,
Meridian Harbor Financial Corp. ("MHFC"). Everything under `sources/` is Markdown converted from:

- `sources/reports/` - three financial reports (2025 Annual Report, Q2 2026 Earnings Release and
  Financial Supplement, 2025 Pillar 3 Regulatory Capital Disclosures). Page markers look like
  `<!-- page 12 -->`.
- `sources/models/` - three Excel financial models rendered as text: value grids per sheet, then every
  formula with its cell address, row label and computed value. README sections describe each model.
- `sources/api_docs/` - the Developer Platform API Reference (18 APIs). `sources/api_docs/apis/` has one
  file per API.

`raw/` holds the original binary files and is ignored. Do not document `AGENTS.md`, `CLAUDE.md` or this
brief.

## Goal

Build a **semantic knowledge graph** of this corpus as a linked wiki: one concept page per important
entity, and Markdown links between pages for every real relationship found in the sources. A reader (and
a Q&A agent that uses `openwiki_search` / `openwiki_read`) should be able to answer questions such as
"which APIs feed the CECL model?", "how is the allowance calculated?", "what drove Q2 2026 net income?",
or "what happens to NII if rates fall 200 bp?" by following links.

## Page types (use exactly these values in the front-matter `type` field)

| type | one page per | examples |
|---|---|---|
| `Organization` | the bank and each legal entity / business segment | Meridian Harbor Financial Corp., Consumer & Community Banking, Commercial & Investment Bank, Asset & Wealth Management, Corporate (Treasury/CIO) |
| `Report` | each source report | 2025 Annual Report, Q2 2026 Earnings Supplement, Pillar 3 Disclosures |
| `FinancialMetric` | each important metric family | Net interest income, Net income & EPS, CET1 ratio, Allowance for credit losses, LCR, NSFR, SLR, RWA, Net charge-offs, VaR |
| `FinancialModel` | each Excel model | MDL-ALM-014 NII Sensitivity, MDL-CR-007 CECL Allowance, MDL-CAP-003 Capital Planning |
| `ModelComponent` | each model sheet or calculation step worth explaining | Scenario weighting, Lifetime PD, Deposit betas, Repricing factor, Stress projection, Indicative SCB |
| `API` | each of the 18 APIs | API-10 Credit Risk Scoring API, API-14 Macroeconomic Scenario API |
| `RiskConcept` | each risk or regulatory concept | CECL, IRRBB, EVE, Stress capital buffer, G-SIB surcharge, Basel III Pillar 3, BCBS 239, Model risk (SR 11-7) |
| `Scenario` | each macro / rate scenario set | Upside / Baseline / Downside (MSC-2025Q4), Internal severely adverse, Parallel rate shocks |
| `Person` | each named executive | CEO, CFO, CRO, CTO, Treasurer |
| `Team` | each owning team named in the sources | Corporate Treasury - ALM, Model Risk Governance & Review, Risk Analytics Engineering |

Also write an `overview` page for the bank and the reserved `index.md`.

## Required pages (planning: submit ALL of these in the plan)

This corpus is a knowledge graph, not a codebase: the goal is **many small linked pages, one per entity**.
"Smallest complete" here means one page per entity below; do **not** merge entities into the
quickstart or into a few long pages. Plan every path listed (under `/openwiki/`), give each the seed
paths shown, and fill `relatedPages` from the Relationships section. You may add pages; do not drop any.

| Folder (`type`) | Pages | Seed paths |
|---|---|---|
| `organizations/` (Organization) | `meridian-harbor-financial-corp.md`, `consumer-community-banking.md`, `commercial-investment-bank.md`, `asset-wealth-management.md`, `corporate.md` | `sources/reports/` |
| `reports/` (Report) | `annual-report-2025.md`, `q2-2026-earnings-supplement.md`, `pillar3-disclosures-2025.md` | the matching file in `sources/reports/` |
| `models/` (FinancialModel) | `nii-sensitivity-model.md` (MDL-ALM-014), `cecl-allowance-model.md` (MDL-CR-007), `capital-planning-model.md` (MDL-CAP-003) | the matching file in `sources/models/` |
| `models/components/` (ModelComponent) | `nii-repricing-and-deposit-betas.md`, `nii-rate-shock-projection.md`, `eve-modified-duration.md`, `cecl-scenario-weighting.md`, `cecl-lifetime-pd.md`, `cecl-lgd-and-ead.md`, `cecl-qualitative-overlay.md`, `capital-baseline-projection.md`, `capital-stress-projection.md`, `indicative-stress-capital-buffer.md` | the parent model's file in `sources/models/` |
| `apis/` (API) | one page per API, same file name as its source: `api-01-accounts-api.md` ... `api-18-webhooks-event-notifications-api.md` (all 18) | `sources/api_docs/apis/<same name>.md` |
| `metrics/` (FinancialMetric) | `net-interest-income.md`, `net-income-and-eps.md`, `cet1-ratio.md`, `allowance-for-credit-losses.md`, `liquidity-coverage-ratio.md`, `net-stable-funding-ratio.md`, `supplementary-leverage-ratio.md`, `risk-weighted-assets.md`, `net-charge-offs.md`, `value-at-risk.md` | `sources/reports/`, `sources/models/` |
| `concepts/` (RiskConcept) | `cecl.md`, `irrbb.md`, `economic-value-of-equity.md`, `stress-capital-buffer.md`, `gsib-surcharge.md`, `basel-iii-pillar-3.md`, `bcbs-239.md`, `model-risk-sr-11-7.md` | `sources/reports/` |
| `scenarios/` (Scenario) | `macro-scenarios-msc-2025q4.md`, `internal-severely-adverse.md`, `parallel-rate-shocks.md` | `sources/models/`, `sources/api_docs/apis/api-14-macroeconomic-scenario-api.md` |
| `people/` (Person) | `chief-executive-officer.md`, `chief-financial-officer.md`, `chief-risk-officer.md`, `chief-technology-officer.md`, `treasurer.md` (title each page with the person's name if the sources give it) | `sources/reports/mhfc-2025-annual-report.md` |
| `teams/` (Team) | one page per owning team named in the sources: the three model owners (Corporate Treasury - Asset & Liability Management, Consumer & Wholesale Credit Risk - Allowance Methodology, Corporate Treasury - Capital Management), Model Risk Governance & Review, and each API "Owning team" (e.g. Risk Analytics Engineering, Market Data Services, Treasury Technology) | `sources/models/`, `sources/api_docs/apis/` |

Plus `/openwiki/quickstart.md` (required by OpenWiki) as a short routing page that links into these folders.

## Relationships to capture as links (with the relationship stated in the sentence)

- Model **consumes** API (e.g. MDL-CR-007 consumes API-10, API-11, API-14).
- API **feeds** model / report / other API (use each API's "Data lineage" table).
- Model **produces** metric, and metric **is disclosed in** report (cite the report section and page).
- Metric **belongs to** segment; segment **is part of** the bank.
- Team **owns** model or API; person **leads** function.
- Model **uses** scenario; scenario **drives** metric.
- Concept **governs** model or metric (e.g. CECL governs the allowance; SR 11-7 governs all models).

On every page, add a short "Relationships" section listing typed links, e.g.
`- consumes: [API-10 Credit Risk Scoring API](../apis/api-10-credit-risk-scoring-api.md)`.

## Rules

- Quote numbers exactly as the sources state them, with units and as-of dates (e.g. "$15,920 million at
  Dec 31, 2025"). When the same number appears in a report and a model, link both and say they agree.
- For models, explain inputs -> calculation -> outputs in plain language, and name the sheets and key
  cells (e.g. `Allowance_Summary!G12`). Include the formula text for the core calculations.
- For APIs, record base path, version, owner, scopes, endpoints, consumers and the models they feed.
- Prefer many small, well-linked concept pages over a few long ones. Folder layout suggestion:
  `organizations/`, `reports/`, `metrics/`, `models/`, `apis/`, `concepts/`, `scenarios/`, `people/`, `teams/`.
- Add Mermaid diagrams where useful: API -> model -> report lineage flowchart; CECL calculation flow;
  capital stack.
- The bank is fictional; do not add outside knowledge about real banks.
