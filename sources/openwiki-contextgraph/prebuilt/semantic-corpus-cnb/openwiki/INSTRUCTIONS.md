# OpenWiki brief: Crestline National Bank payments-estate semantic graph

<!-- Copy to semantic-corpus-cnb/openwiki/INSTRUCTIONS.md before running `openwiki --init`.
     OpenWiki reads this file for scope and priorities and never rewrites it. -->

## What this repository is

This repository is NOT a software codebase. It is a document corpus describing the payments IT
estate of a fictional large US bank, **Crestline National Bank ("CNB")**. Everything under
`sources/estate/` is Markdown converted from 15 internal PDF documents: architecture documents,
system overviews, API/event catalogs, an org & ownership directory, a re-org memo, compliance and
privacy policies, a model-risk policy extract, an ARB decision register, a Jira export, a data
catalog extract, and a post-implementation review of a failed pilot. Page markers look like
`<!-- page 2 -->`; each file's first line names its source PDF.

`raw/` holds the original PDFs and is ignored. Do not document `AGENTS.md`, `CLAUDE.md` or this brief.

## Goal

Build a **semantic knowledge graph** of CNB's payments estate as a linked wiki: one page per
important entity, with Markdown links for every real relationship stated in the sources. The wiki
is the context layer for a **product manager's AI agent** doing estate discovery for new features
in the commercial portal (Crestline Business Online, "CBO"). A reader (or an agent using
`openwiki_search` / `openwiki_read`) must be able to answer multi-hop questions such as:

- "Which systems and interfaces would a wire-tracking feature in CBO depend on, and what is each
  one's status (existing / deprecated / missing / planned)?"
- "Who owns the Swift gpi connector **today**, and when and why did ownership change?"
- "What may the bank show a client about a held or screened wire, and which policy says so?"
- "What was tried before for near-real-time wire status, and why did it fail?"
- "Which approvals, forums and deadlines constrain a change to the PPH v1 API?"
- "Which datasets could power payment-timing predictions, and what are their access restrictions?"

## Front-matter contract (so the wiki can be parsed into a typed graph)

Every page's YAML front matter MUST include:

- `type:` exactly one of the values below.
- `entity_id:` the stable identifier the sources use when one exists (e.g. `SYS-PPH`,
  `TEAM-FCT`, `POL-FCC-014`, `ADR-PAY-019`, `INC-2024-1182`, `PIR-2024-07`); otherwise a short
  kebab-case id you keep consistent everywhere.
- `status:` when the sources state one (e.g. `active`, `deprecated`, `sunset 2027-03-31`,
  `missing`, `planned`, `terminated`).

## Page types (use exactly these values in the front-matter `type` field)

| type | one page per | examples |
|---|---|---|
| `Organization` | the bank and each named org unit / business line | Crestline National Bank, Payments & Treasury Technology (PTT), Digital Treasury Channels, Treasury Management Products |
| `System` | each named system or major service | CBO Wire Center, Status Projection Service (SPS), Commercial Entitlements Service (CES), PRISM Payments Hub (PPH), Fedwire Funds Connector (FFC), Swift Alliance & gpi Connector (GPI-C), Hold Management Service (HMS), Sentinel, SanctionScreen, Enterprise Notification Service (ENS), Treasury Data & Insights Platform (TDIP), Core Deposit Platform, Investigations Workbench |
| `Interface` | each API surface, event topic family or data feed (list its endpoints/fields in a table inside the page, with each endpoint's `EP-...` id and status) | PPH v1 Wire Status API (deprecated), PPH v2 Payments API, `pay.wire.lifecycle` event topics, HMS Hold API, ENS `TRS.WIRE.*` notification topics, gpi 4-hourly batch snapshot feed, TDIP Insights API, SPS read model |
| `Team` | each engineering team or 2nd-line function named in the org directory | CBO Wire Center squad, Payments Hub Engineering, Payment Networks Engineering, GTSI, Financial Crimes Technology, Enterprise Notification Platform, Treasury Data & Analytics, Model Risk Management, Privacy Office, Payments ARB / Enterprise Architecture, Financial Crimes Compliance, Payment Operations, Legal / DRC, InfoSec |
| `Person` | each key contact: directors, engineering managers, tech leads, product owners, data owners, approvers and named policy/forum contacts (other names stay as text on their team's page) | Anjali Deshpande, Marcus Chen, Laura Kim, Raj Malhotra, Elena Vasquez, Catherine Doyle, Jordan Ellis, Nikhil Bose, ... |
| `Policy` | each policy / standard document's rules | POL-FCC-014 customer communication of holds, DUS-07 data use & client confidentiality, MRM-POL-02 model risk management |
| `Decision` | each ADR or architecture-board decision in the register | ADR-PAY-019 and every other ADR in ARB-PAY-REG-2026Q3, plus standing ARB rules from the minutes |
| `Project` | each epic / initiative / pilot in the Jira export or history | each epic in the WT-discovery Jira export (list its stories, owners, targets and statuses in a table inside the epic page), Wire Status Lite pilot (CBO-3120), the 2027 real-time gpi initiative |
| `Incident` | each incident or post-implementation review | INC-2024-1182 and PIR-2024-07 |
| `Dataset` | each data catalog entry / dataset with its classification and permitted uses | the TDIP catalog extract's datasets (e.g. wire history, gpi tracker snapshot, fraud/beneficiary-behaviour datasets), GPI_TRACKER_SNAPSHOT |
| `Concept` | each domain concept needed to read the rest | wire lifecycle state model (the exact PPH states and what "Completed" does and does not mean), hold reason taxonomy and tiers, UETR, IMAD/OMAD, Fedwire, SWIFT gpi, settlement vs release |
| `Document` | each of the 15 source documents (id, version, owner, approvers, what it covers, what pages cite it) | CBO-ARCH-WC-4.1, PPH-SYS-OVW-9.2, CNB-MEMO-2026-09, ... |

Also write an `overview.md` page for the estate and the reserved `index.md`, plus
`/openwiki/quickstart.md` as a short routing page that links into each folder.

Folder layout: `organizations/`, `systems/`, `interfaces/`, `teams/`, `people/`, `policies/`,
`decisions/`, `projects/`, `incidents/`, `datasets/`, `concepts/`, `documents/`.

This corpus is a knowledge graph, not a codebase: the goal is **many small linked pages, one per
entity**; do not merge entities into a few long pages. Plan one page per entity listed in the
sources for every type above. Endpoints and Jira stories are the two exceptions: they stay as
tables inside their `Interface` / `Project` parent pages.

Planning: submit the complete page list in a **single `submit_plan` tool call** — never write the
plan out as prose text. Keep each planned page's seed/notes short (a path and a few words) so the
full plan fits in one call.

## Relationships to capture as links (state the relationship in the sentence)

- System **depends on** system / interface (the current-state architecture is the map).
- Interface **belongs to** system; interface or endpoint **is consumed by** system; mark each
  endpoint or field **existing / deprecated / missing / planned** exactly as the sources do.
- Team **owns** system; person **belongs to** team and **is product owner / approver of** X.
- Ownership **changed**: say from which team to which team, the effective date, and which memo
  says so — and reflect the *current* owner on the system page.
- Policy **constrains** system / interface / feature behaviour (quote the controlling clause ids).
- Decision (ADR) **permits / forbids / requires** an integration pattern; link affected systems.
- Project **targets** system; project **is blocked by** missing interface or approval.
- Incident **was caused by** a pattern; decision or policy **resulted from** incident.
- Dataset **is produced by** system; dataset **has classification/restriction**; model or insight
  **would require** dataset.
- Deadlines and sunsets: every dated commitment (API sunsets, release dates, review cadences)
  must appear on the page of the thing it constrains, with the date and the source document id.

On every page, add a short "Relationships" section listing typed links, e.g.
`- owned by: [GTSI](../teams/gtsi.md) (since 2026-10-01, per [CNB-MEMO-2026-09](../documents/cnb-memo-2026-09.md))`.

## Rules

- Quote identifiers, dates, versions, rate limits, SLAs and clause numbers **exactly** as the
  sources state them (e.g. `EP-PPH-01`, `20 TPS shared`, `sunset 2027-03-31`). Always name the
  source document id (and page) for load-bearing facts.
- Where documents written by different teams touch the same entity, link them all from that
  entity's page — disagreements and gaps between documents are the most valuable content; state
  them neutrally ("X says A; Y says B") rather than resolving them silently.
- Restricted material: the corpus includes a RESTRICTED hold-reason taxonomy and policies about
  what may be shown to clients. Document the taxonomy and the rules faithfully — including tier
  labels and which reasons may never be shown to customers — because the graph's job is to let an
  agent *check* designs against these rules.
- Add Mermaid diagrams where useful: the CBO → PPH → network-connector flow; the wire lifecycle
  state machine; the gpi batch data path; org chart of PTT.
- The bank is fictional; do not add outside knowledge about real banks, Fedwire or SWIFT beyond
  what the sources state.
