# Project Context — Enterprise Semantic Graph Demo for Product Development

> **Read this first.** This file gives a new Claude / Claude Code session the full background of this project:
> - what I am trying to achieve;
> - what the demo is;
> - what every document in my corpus means, and how the documents connect;
> - which hidden findings the agent should uncover;
> - what is left to build.
>
> I already have all the documents. This file explains them. The demo story is set on **Thursday, 2026-10-08**.

---

## 1. What I'm trying to achieve

### 1.1 The problem

- Developers have mature **harnesses** on top of GitHub Copilot, Claude Code and Codex: custom agents, skills, hooks and pipelines.
- Product managers have far less, especially for the hardest part of feature work. That part is not ideation or writing a PRD. It is **gathering enterprise context**.
- When a PM wants to add a feature to an existing system in a large enterprise (here, a large US bank's payments business), they must find out:
  - which existing systems the feature depends on;
  - who owns each system: team, manager, product owner;
  - whether the endpoints, fields and events the feature needs already exist, or which team must build them;
  - what has been tried before, what failed, and what can be reused;
  - which compliance, privacy and model-risk rules constrain what can be shown to customers;
  - which approvals, forums, lead times and capacity constraints sit on the critical path.
- Today this takes **weeks of meetings and document hunting**, and important things are still missed.

### 1.2 The thesis

An **enterprise brain**, a **semantic graph** built over a business unit's IT-estate and compliance documents, can be queried by a PM's AI agent. The agent then gathers this context in **minutes** with sources. More importantly, it can find problems that **no single document reveals**, because the answer only exists in the **connections between documents** written by different teams at different times.

### 1.3 What the demo must prove

1. A PM can go from idea to an accurate, **BRD-grade** picture: dependencies, endpoints, owning teams and people, missing interfaces, prior work, compliance constraints, teams to engage, hours to allocate, critical path.
2. The agent catches **non-obvious pitfalls** that would otherwise surface late or in production:
   - a missing endpoint in a dependency system;
   - a stale owner after a re-org;
   - a compliance violation in the PM's own design;
   - a privacy violation hidden in an "insight";
   - a hard deadline nobody scheduled.
3. These catches **require a graph**, meaning multi-hop joins across documents. Keyword search or single-document retrieval would not find them.

The demo is one concrete instance of a broader point: **semantic graphs dramatically speed up enterprise context gathering across the product development lifecycle.**

---

## 2. The demo in one picture

```
 15 bank documents (PDF)                         PM uploads market research + feature concept
 (IT estate, APIs, policies, Jira, ADRs, ...)            (PM-WTC-MR-0.3, contains flawed assumptions)
          │                                                         │
          ▼                                                         ▼
 PDF → Markdown → git repo → OpenWiki (LangChain)        ┌──────────────────────────────────────┐
          │           + typed YAML frontmatter            │  PM Chat Agent                       │
          ▼                                               │  • Anthropic product-management      │
 Linked wiki pages + grounded claims ──────────────────▶ │    plugin skills (write-spec→BRD...) │
 Frontmatter parsed → in-memory graph (NetworkX) ──────▶ │  • custom "estate-discovery" skill   │
          (graph_query tool)                              │  • tools: wiki_read/grep, graph_query│
                                                          └──────────────────────────────────────┘
                                                                           │
                                                                           ▼
                                 10 questions → dependency map, missing endpoints, compliance catches,
                                 owners, effort (hours by team), phasing, critical path → BRD sections
```

**Persona:** Sarah Whitfield, Senior Product Manager, Wire Tracking.

**Feature:** a **"FedEx view" Wire Tracking Center** in an **existing** corporate banking portal. It covers:
- milestone tracking of domestic and international wires;
- held and returned wire views;
- notifications;
- **predictions based on how the same customer's similar past wires behaved**.

---

## 3. The story and its "aha" moments

The bank is **Crestline National Bank (CNB)**, a fictional large US bank. Its commercial portal **Crestline Business Online (CBO)** already has a **Wire Center** module for initiating, approving, releasing and listing wires.

Sarah's concept looks reasonable. She estimates it as **"mostly front-end work for the CBO squad, 1.5 PIs, GA Q1 2027."** The agent, grounded in the graph, shows otherwise:

| # | Headline | What Sarah assumed | What the graph reveals |
|---|---|---|---|
| 1 | **The tooltip that would tip off** | Show the exact hold reason from the risk system; Confirm/Reject on every held wire | Violates the bank's customer-communication standard and SAR confidentiality. A Jira story (**CBO-4388**) is **about to ship raw fraud/sanctions text to clients on 2026-10-22.** |
| 2 | **"Settled" is not a field** | "Settled" = the existing "Completed" label | "Completed" is already shown **at release**, before the Fed accepts the wire. That is a live compliance issue linked to a client complaint. A real "Settled" needs an unscheduled API migration with a **hard 2027-03-31 deadline**, rail-aware semantics and a backlog API change with no sponsor. |
| 3 | **The FedEx map has no live feed and a new owner** | Live SWIFT gpi route refreshed every minute; work with Raj Malhotra's team | gpi data is a 4-hourly batch with no API. Vendor quota blocks per-wire calls. The architecture board forbids direct exposure. The real-time service is a 2027 initiative. **Ownership moved to another team on 2026-10-01.** |
| 4 | **The insight that uses someone else's bank account** | "Beneficiary typically moves funds within 4 hours" | That figure can only come from **another client's deposit account activity**, held in a Restricted, fraud-only dataset. Showing it would be a cross-client confidentiality and model-use violation. |

**Closing before/after:**
- **Before:** "Front-end, 1.5 PIs."
- **After:** 16 teams/functions, **~1,900 hours** for Phases 1–2, a hard deadline on the critical path, one production compliance risk stopped two weeks before release, two design violations removed, and a three-phase plan with named owners and dates.

---

## 4. Background research and decisions (from earlier conversation)

### 4.1 PM "harnesses" that exist today (as of Oct 2026)

Same plumbing as developer harnesses, different payload:

| Building block | Developer payload | PM payload |
|---|---|---|
| CLAUDE.md / AGENTS.md | Repo, stack, conventions | Product, personas, strategy, OKRs |
| Skills | Test, refactor, review | OST, RICE, PRD, pre-mortem, pricing |
| Sub-agents | Code reviewer | Skeptic, exec, customer, engineer reviewers |
| Hooks | Lint / test gates | PRD quality gates |
| MCP connectors | GitHub, CI | Jira/Linear, Notion, PostHog/Amplitude, Slack |

The landscape has five layers:

1. **Framework skill libraries**
   - `phuryn/pm-skills`: 68 skills, 42 workflows, 9 plugins, MIT.
   - `deanpeters/Product-Manager-Skills`: ~70 skills in three tiers.
   - `RefoundAI/lenny-skills`: 76 skills.
   - `anthropics/knowledge-work-plugins/product-management`.
2. **PM operating systems** (context + memory + cadence)
   - `carlvellotti/carls-product-os`
   - `aakashg/pm-claude-code-setup`
   - `feamando/pmos`
   - `benhuds/pm-os`
   - `runtm-ai/claudecode-for-pms`
3. **Persona methods**
   - BMAD: Analyst "Mary" and PM "John"; the CIS brainstorming module.
   - BMAD is strong at the developer handoff and weak at launch and measurement.
4. **Research and validation tools**
   - Cookiy user-research skill
   - `usercall-mcp`
   - Microsoft TinyTroupe (synthetic personas)
   - n8n interview synthesizers
5. **Analytics MCPs:** official PostHog, Amplitude and Mixpanel MCP servers.

Gaps across all of them:
- mostly prompt packs, with no quality gates;
- **context is the moat**;
- skills collide when several libraries are installed;
- synthetic users are not real validation;
- the handoff to developer tooling is weak.

### 4.2 Anthropic's product-management plugin (used by the demo agent)

- **Packaging:** built for Cowork, works in Claude Code, Apache-2.0. Folder layout: `.claude-plugin/plugin.json`, `.mcp.json`, `CONNECTORS.md`, `commands/`, `skills/`.
- **Current skills (8):**
  - `write-spec`
  - `roadmap-update`
  - `stakeholder-update`
  - `synthesize-research`
  - `competitive-brief`
  - `metrics-review`
  - `sprint-planning`
  - `product-brainstorming`
- **Commands:** one, `/brainstorm`. Skills double as `/product-management:<skill>`.
- **Tool-agnostic placeholders:** for example `~~project tracker` and `~~product analytics`. When a tool isn't connected, the skill works from pasted input.
- **Pre-wired connectors:** Slack, Linear, Asana, Monday, ClickUp, Atlassian, Notion, Figma, Amplitude, Pendo, Intercom, Fireflies, Google Calendar, Gmail, Similarweb.
- **Gaps:**
  - no subagents, no hooks, no orchestration and no product-context layer;
  - `write-spec` outputs a PRD, so **we fork it into `write-brd`**.
- **History:** an older layout had 6 commands plus 6 knowledge skills. Community PR #55 (14 commands) was closed, not merged.

### 4.3 Running a Claude plugin outside Cowork / Claude Code

- **Claude Agent SDK** loads plugins natively from local directories: skills, agents, hooks and MCP servers. This is the preferred runtime, and it can sit inside a LangGraph node.
- **LangGraph Deep Agents** (`deepagents >= 1.7.0`) supports the Agent Skills `SKILL.md` spec. It can use the skills only; MCP wiring and `~~` placeholders must be adapted manually.

### 4.4 Knowledge layer: OpenWiki as a "soft" semantic graph

- **What it is:** LangChain **OpenWiki** (open-sourced July 2026) is a CLI that writes and maintains an **agent-oriented Markdown wiki**. It supports grounded **claims** (`.claims/`), Open Knowledge Format output and a visualizer, and is built on Deep Agents.
- **No PDF connector.** The plan is PDFs → Markdown → git repo → `openwiki personal --init` with the `git-repo` source (or code mode on that repo).
- **As a graph:** pages are nodes and links are edges. Its weaknesses are untyped links, no query engine and entity-name drift.
- **Fix:** enforce **typed YAML frontmatter** via `~/.openwiki/INSTRUCTIONS.md`, then parse it into NetworkX and expose a `graph_query` tool. Text stays the source of truth.

### 4.5 Demo design choices adopted

- **Generation:** the documents were generated from a hidden **ground-truth model**, so the agent can be scored.
- **Seeded traps:** missing endpoints, a stale owner, compliance violations, a privacy violation, a freshness trap and a deadline.
- **Every answer carries:** click-through **citations** (document ID + section), an **endpoint gap matrix**, auto-drafted asks to other teams, and hour estimates from planning factors.
- **Optional extras:**
  - a live "estate changed" moment, where a new memo triggers a wiki update and the BRD is regenerated;
  - reviewer subagents (Architect / Compliance / Ops);
  - an accuracy scorecard;
  - a Jira handoff.

### 4.6 My original inputs

- A draft PRD for a "Wire Tracking Center" covering:
  - dashboard metrics and a "Wire Insights Engine";
  - search and filters, and a fee breakdown;
  - a FedEx-style progress bar and a SWIFT gpi route;
  - held and returned wire workflows;
  - "explain delays", status sharing and subscriptions.
- Figma screenshots of such a portal from a real regional bank.
- **Scope decision:** assume the portal exists; focus on the tracker plus same-customer historical predictions; use a **fictional bank**.

---

## 5. The fictional bank's estate (reference facts)

### 5.1 Current architecture

```
[CBO Wire Center UI] → [cbo-wire-bff] ──sync REST v1──▶ [PRISM Payments Hub (PPH) – Volaris 9.4]
                           │  ├─▶ CES (entitlements)                     ├─▶ PRSP: Hold Mgmt (HMS), Sentinel fraud, SanctionScreen
                           │  ├─▶ CBO Auth step-up                       ├─▶ Core Deposit Platform (funds control)
                           │  └─▶ ENS notifications (TRS.WIRE.*)         ├─▶ PNG: Fedwire Funds Connector (FFC)
                           │                                             └─▶ PNG: Swift Alliance & gpi Connector (GPI-C)
 NOT used by Wire Center today: SPS read model (ACH only), PPH v2 APIs, pay.wire.lifecycle.v2 topic,
                                gpi data, HMS APIs, TDIP Insights API
 gpi: GPI-C batch pull every 4h → GPI_TRACKER_SNAPSHOT (Oracle) → Ops Investigations Workbench + TDIP load
```

### 5.2 Systems and owners (current, after the 2026-10-01 re-org)

| System | Owning team | People |
|---|---|---|
| CBO Wire Center (SYS-CBO) | CBO Wire Center squad | Anjali Deshpande (Director), Tom Becker (EM), Lucas Ferreira (Tech Lead), Jason Park (Eng), Mei Tanaka (QA); **Marcus Chen** (Product Owner) |
| Status Projection Service (SYS-CBO-SPS), Commercial Entitlements Service (SYS-CES) | CBO Platform & Entitlements | Nadia Haddad (EM), Arjun Mehta (Tech Lead) |
| PRISM Payments Hub (SYS-PPH) | Payments Hub Engineering | Raymond Ortiz (Director), Kevin O'Brien (EM), Sunita Rao (Principal Eng); **Laura Kim** (Product Owner and payment data owner) |
| Fedwire Funds Connector (SYS-PNG-FFC) | Payment Networks Engineering (PNE) | Raj Malhotra (Director), Brian Walsh (EM), Chen Wei (Tech Lead) |
| Swift Alliance & gpi Connector (SYS-PNG-GPI) | **GTSI** (moved from PNE, effective 2026-10-01) | Elena Vasquez (Director), Omar Siddiqui (EM), Hannah Lindqvist (Tech Lead), Tomasz Nowak (moved from PNE) |
| Hold Management (HMS), Sentinel fraud, SanctionScreen | Financial Crimes Technology (FCT) | Victor Petrov (Director), Grace Mensah (EM), Daniel Kowalski (Tech Lead) |
| Enterprise Notification Service (SYS-ENS) | Enterprise Notification Platform | Sanjay Iyer (Director), Melissa Grant (EM), Paul Henderson (onboarding) |
| Treasury Data & Insights Platform (SYS-TDIP) | Treasury Data & Analytics | Wei Zhang (Director), Carlos Mendes (EM), Dr. Aisha Rahman (Lead Data Scientist) |
| Core Deposit Platform, Investigations Workbench | Deposits / Payment Ops | Mark Sullivan (Deposits data owner), Luis Ramirez |

**Partner functions (approval gates):**

| Function | Accountable | Contacts |
|---|---|---|
| Financial Crimes Compliance (FCC) | Catherine Doyle (Chief BSA/AML Officer) | Jordan Ellis (Policy & Advisory, the day-to-day contact), Michael Tran (OFAC), Rebecca Stone (FIU) |
| Model Risk Management | Jonathan Price | Sophie Laurent (Validation Lead) |
| Privacy Office | Rachel Goldberg | Ethan Brooks (Data Governance) |
| Legal | Andrew Feldman | Patricia Moore (Chair, Disclosure Review Committee, DRC) |
| Enterprise Architecture / ARB | Nikhil Bose (Chair) | Jenna Ross (secretariat) |
| InfoSec | Farah Ali | |
| Payment Operations | Denise Carter | Luis Ramirez, Tanya Brooks |
| Treasury Support | Kim Nguyen | |

- **Executive sponsor / business:** Gregory Hall (CIO, Payments & Treasury Technology); Danielle Okafor (EVP, Treasury Management Products).

### 5.3 Interfaces: existing vs missing

**PPH v1 (deprecated; sunset 2027-03-31, no extension).** Rate limit 20 TPS shared.
- `GET /pph/v1/wires/{wireRef}/status` (EP-PPH-01) returns:
  - `status`: 7 coarse values;
  - `holdReasonDesc`: legacy free text synced from HMS;
  - `fedRef`: IMAD only.
- `GET /pph/v1/wires?...` (EP-PPH-02)
- `POST /pph/v1/wires` (EP-PPH-03)

**PPH v2 (GA 2025-10)**
- `GET /pph/v2/payments/{id}` returns:
  - identifiers: cboRef, IMAD, OMAD, **UETR**, endToEndId;
  - `hold{isHeld, holdId}` only;
  - charges.
  It has **no settlement object** (PPH-2207).
- Search (no beneficiary-name filter; PPH-2251), `/history`, POST.

**Event topics**

| Topic | Notes |
|---|---|
| `pay.wire.lifecycle.v2` | Consumer access control list (ACL) takes ~3 weeks |
| `pay.ach.lifecycle.v1` | Feeds SPS |
| `net.fedwire.ack.v1` | Fed pacs.002 with OMAD; consumers: PPH only; ACL owned by PNE |
| `risk.hold.events.v1` | Restricted; channels not allowed |

**Hold Management Service (HMS)**
- `GET /prsp/hms/v1/holds?paymentId=`: internal, Restricted; returns code, description and analyst notes.
- `POST .../disposition`: Ops only, maker-checker.

**Enterprise Notification Service (ENS)**
- Send: `POST /ens/v3/notifications`.
- Subscribe: `POST /ens/v3/subscriptions`, by event type + account only. **No per-wire subscriptions until ENS-1120 (2027-H1).**

**Treasury Data & Insights Platform (TDIP)**
- `GET /tdip/insights/v1/cash-forecast/{clientId}`: a reference pattern only, not wire-related.

**CBO**
- BFF list, detail and refresh (refresh throttled to 1 per 60 s per wire).
- `POST /cbo/auth/v2/step-up`.
- SPS timeline `GET /cbo/sps/v1/payments/{type}/{id}/timeline`, ACH only.

**Documented as DOES NOT EXIST**

| Missing interface | Ticket / status |
|---|---|
| `GET /png/gpi/v1/payments/{uetr}/tracker` | GTRS, GTSI-0107, 2027 |
| `GET /prsp/hms/v1/holds/{id}/client-view` | FCT-1893, 21 pts |
| `POST /prsp/hms/v1/holds/{id}/client-attestation` | None |
| `GET /tdip/insights/v1/wire-history/{clientId}` | None |
| `GET /tdip/insights/v1/corridor-stats` | None |

### 5.4 Status semantics

- **v1 status `PROCESSED`** collapses RELEASED, SENT_TO_NETWORK, NETWORK_ACCEPTED and COMPLETED. CBO labels it **"Completed"** (CBO-4402, Feb 2026), so "Completed" appears **at release**.
- **`NETWORK_ACCEPTED` differs by rail:**
  - **Fedwire:** Fed pacs.002 with OMAD means **final interbank settlement** (Reg J / UCC 4A). Beneficiary account credit is **not** reported.
  - **Swift:** only a SwiftNet ACK. Beneficiary credit is known only from gpi **ACCC**.
- **v2 history timestamps** are PPH processing times. The exact Fed timestamp needs **PPH-2207**.
- **gpi codes:**

| Code | Meaning |
|---|---|
| ACSP / G000 | Forwarded to the next gpi bank |
| ACSP / G001 | Forwarded to a non-gpi bank; **tracking ends** |
| ACSP / G002–G004 | Pending (credit not same day / awaiting documents / awaiting cover) |
| ACCC | Credited to beneficiary |
| RJCT | Rejected |

- **Observed gpi outcomes:**

| Outcome | Value |
|---|---|
| Reached ACCC | 88% |
| Tracking ended at G001 | 8% |
| Pending more than 24 h | 2.5% |
| Rejected | 1.5% |
| Median time to ACCC | 2 h 41 m |
| Wires with intermediary deductions reported | 34% |

### 5.5 Holds: reason codes and disclosure tiers

**Disclosure tiers:**
- **P** = public;
- **C** = client-actionable;
- **G** = generic "being reviewed";
- **R** = restricted. R must look **identical to G**, and there is **no ETA** for G or R.

| Code | Name | Tier | Share | What the client may do |
|---|---|---|---|---|
| HRC-01 | DUP_SUSPECT | C | 22% | Digital attestation with step-up authentication; up to $5M (CTRL-PAY-031) |
| HRC-02 | CALLBACK_REQUIRED | C | 18% | **Never confirmable in the portal** (CTRL-PAY-018); may request a callback |
| HRC-03 | LIMIT_EXCEEDED | C | 9% | Admin approval / RM |
| HRC-04 | CUTOFF_WAREHOUSED | P | 6% | Informational |
| HRC-05 | FUNDS_PENDING | C | 14% | Fund the account |
| HRC-06 | REPAIR_REQUIRED | C | 11% (rising to ~16% after Nov-2026 address rules) | Cancel and resubmit |
| HRC-07 | FRAUD_MODEL_HIGH | R | 8% | None |
| HRC-08 | ATO_SUSPECT | R | 1% | None |
| HRC-09 | SANCTIONS_REVIEW | R | 7% | None |
| HRC-10 | AML_REVIEW | R | 2% | None |
| HRC-11 | LEGAL_HOLD | R | <0.5% | None |
| HRC-12 | OPS_MANUAL_REVIEW | G | 1.5% | None |

- Holds run at about 410 per day. Median time to resolution for HRC-01 is 47 minutes.
- HMS descriptions are **Restricted**, for example `FRAUD_MODEL_HIGH sc=9xx L1 queue`.
- Controls:
  - CTRL-PAY-012: maker-checker;
  - CTRL-PAY-018: callback;
  - CTRL-PAY-031: duplicate attestation;
  - CTRL-PAY-040: no ETA for G/R holds.

### 5.6 Data and models

**TDIP datasets**

| Dataset | Notes |
|---|---|
| `pay_wire_txn_hist` | Hourly; 7 years |
| `gpi_tracker_events` | Nightly, moving to hourly via TDA-2188, but the source refreshes only every 4 h; history from 2025-03-01 |
| `fed_ack_events` | **Not ingested** (TDA-2210) |
| `dda_txn_history` | **Restricted** |
| `client_hierarchy` | |
| `cbo_wire_events` | |

**Feature tables**

| Feature table | Notes |
|---|---|
| `wire_corridor_stats_daily` | Cross-client; Internal / Ops use; no suppression flag |
| **`beneficiary_behavior_profile`** | Restricted. Derived from deposit activity of on-us beneficiaries. Permitted purpose: **fraud / money-mule detection only**. Input to model **M-FCT-0034**. Contains `bene_median_hours_to_outflow`. |
| `client_wire_history_features` | Unregistered prototype |

**Corridor sample (90 days)**

| Corridor | Wires | Distinct clients | Largest client share | Same-day ACCC | DUS-07 |
|---|---|---|---|---|---|
| EUR/DE | 31,200 | 1,140 | 4% | 92% | Passes |
| MXN/MX | 2,950 | 88 | 21% | | Fails (largest client >15%) |
| NGN/NG | 140 | 11 | | | Fails all |

**DUS-07 thresholds for cohort statistics:**
- at least 500 transactions and at least 20 distinct clients;
- no single client above 15%;
- refreshed at least monthly;
- wording approved by DRC.

Own-data insights need at least 5 comparable wires and must state their basis. **Cross-client use and purpose drift are prohibited.**

**MRM-POL-02 v7.0** (aligned to the **2026-04-17 interagency guidance** — SR 26-2 / OCC Bulletin 2026-13 / FDIC FIL-15-2026 — that rescinded SR 11-7):
- Descriptive statistics count as an **End-User Analytic (EUA)**, roughly two weeks to register.
- **Customer-facing estimates are Tier 2 at minimum:** 10–14 weeks of validation, 160–240 validator hours, plus a ~6-week queue.
- Financial-crimes model outputs must not be used for product features:
  - M-FCT-0021 (Sentinel fraud score);
  - M-FCT-0034 (beneficiary mule-risk features).

### 5.7 Architecture decisions (ADRs)

| ADR | Decision |
|---|---|
| ADR-PAY-017 | Kafka is the integration backbone |
| ADR-PAY-019 | Channel status must be **event-driven, no polling** (after incident INC-2024-1182) |
| ADR-PAY-021 | Hold reasons never leave the FCT boundary |
| ADR-PAY-023 | **UETR** is the canonical correlation ID (available in v2 only) |
| ADR-PAY-026 | Customer-facing insights must be served via the **TDIP Insights API**, not computed in BFFs |

**ARB minutes, 2026-09-08:**
- no extension of v1;
- GTRS not funded for 2026;
- direct exposure of the gpi snapshot table **not approved**;
- SPS is the reference pattern.

### 5.8 Numbers and calendar

**Volumes:**
- CBO: 9,800 clients, 41,000 users, 11,600 wires/day.
- PPH: 14,200 domestic and 2,900 international outgoing wires/day.

**Swift Tracker API quota:** 250k calls/month, ~61% used. Per-wire client lookups would need ~1.9M calls/month, about 7x the quota.

**Planning factors (hours per story point):**

| Team | Hours per point |
|---|---|
| CBO | 6.5 |
| PPH | 8 |
| PNE | 8 |
| GTSI | 7 |
| FCT | 8, plus 20% compliance testing |
| TDIP | 6 |

**Fixed efforts and lead times:**

| Item | Effort / lead time |
|---|---|
| New ENS event type | ~12 hours each; 6-week service level |
| InfoSec review | 3 weeks |
| Privacy Impact Assessment (PIA) | ~4 weeks |
| FCC review | ~10 business days |

**Capacity:** PPH is ~90% committed. FCT has a change freeze from Dec 15 to Jan 5.

**Calendar:**

| Date | Event |
|---|---|
| 2026-10-01 | Re-org effective |
| **2026-10-08** | Story "today" |
| 2026-10-21 | Demand Board |
| **2026-10-22** | CBO-4388 production release |
| 2026-10-27 | ARB submission deadline |
| 2026-11-06 | PI dependency asks due |
| 2026-11-10 | ARB |
| 2026-11-17 / 18 | PI planning |
| 2026-11-20 | ENS cutoff |
| 2026-12-01 → 2027-03-05 | PI 27.1 |
| 2026-12-15 | GTSI knowledge transfer ends |
| **2027-03-31** | PPH v1 sunset |
| 2027-04 | Volaris 9.6 |

### 5.9 Real-world facts embedded (accurate as of 2026)

- **Fedwire:** moved to ISO 20022 on **2025-07-14**. The Fed returns pacs.002 acknowledgments with OMAD.
- **Swift:** CBPR+ MT/MX coexistence ended **2025-11-22**. Structured-address enforcement starts in **Nov 2026**.
- **Confidentiality and sanctions:**
  - SAR confidentiality: 31 U.S.C. 5318(g)(2); 31 CFR 1020.320(e).
  - OFAC: 31 CFR Part 501 (501.603 / 501.604).
- **Funds transfer and authentication law:** UCC Article 4A and Regulation J; FFIEC authentication guidance (2021); FTC Act §5; GLBA (consumer data).
- **Model risk:** SR 11-7 was rescinded on **2026-04-17** (replaced by SR 26-2).

---

## 6. Document guide — what each document is and why it is there

The corpus has **15 documents**. They look like genuine bank documents: doc-control tables, classification banners, "Uncontrolled when printed" footers, and realistic authoring metadata (Word / Confluence / Jira). They contain no demo language.

**Design principle:** each document is internally consistent and **never states a pitfall's conclusion**. Pitfalls emerge only when documents are joined.

### 6.1 CNB-ORG-PTT-2026-06 — Organization, System Ownership & Engagement Directory

- **Basics:** published 2026-06-15.
- **Contents:**
  - leadership;
  - team directory and partner functions;
  - **system ownership register** (13 systems with tech owner, business owner, tier);
  - governance forums with cadence and lead times (ARB, Demand Board, FCT Change Advisory, DRC, MRM, PIA);
  - **planning factors** (story points → hours, capacity %);
  - PI calendar and escalation path.
- **Role in the demo:**
  - It is the "who owns what" baseline. It is **deliberately stale for gpi**: it shows the gpi Connector owned by PNE / Raj Malhotra / Tomasz Nowak.
  - It also supplies the planning factors behind every hour estimate.

### 6.2 CNB-MEMO-2026-09 — Realignment of Cross-Border Network Integration (CIO memo)

- **Basics:** issued 2026-09-02, effective **2026-10-01**.
- **Contents:**
  - The Swift Alliance Gateway, gpi Connector, gpi Tracker integration, Swift API gateway / PKI and the international-tracking roadmap move from **PNE → GTSI** (Elena Vasquez; Omar Siddiqui; Hannah Lindqvist; Tomasz Nowak transfers).
  - The Fedwire connector stays with PNE.
  - PNE remains secondary on-call until 2026-12-15 (GTSI-0112).
  - New gpi requests go to Jira GTSI.
  - GTRS (GTSI-0107) is unfunded for 2026; discovery is in 2027-Q2.
  - The Swift quota renewal is due 2027-01-31.
- **Role in the demo:** the **temporal override**. The graph must prefer it over the older directory and design doc.

### 6.3 CBO-ARCH-WC-4.1 — Wire Center Current-State Architecture

- **Basics:** last reviewed 2026-08-20.
- **Contents:** the existing portal.
  - Features in production, and what is **not** there (tracking, gpi, hold explanations, client actions on holds).
  - Usage metrics.
  - Integration inventory: all on **PPH v1**.
  - **Status-label mapping:** PROCESSED → "Completed".
  - Stored identifiers: no UETR or OMAD.
  - Notifications produced: TRS.WIRE.RELEASED via template TPL-WIRE-REL-02.
  - Entitlements and step-up authentication; external sharing is unsupported (SEC-STD-22).
  - Constraints: no polling, v1 sunset.
  - **Reusable assets:** the journey-timeline component and SPS from the ACH Tracker.
- **Role in the demo:** the "existing app" every question starts from.

### 6.4 PPH-SYS-OVW-9.2 — PRISM Payments Hub System Overview & Lifecycle State Model

- **Basics:** last reviewed 2026-05-30.
- **Contents:**
  - the 14 v2 lifecycle states with their v1 mapping, including the **PROCESSED collapse** callout;
  - **rail-specific meaning of NETWORK_ACCEPTED**;
  - identifiers;
  - the HMS integration, including the **legacy `holdReasonDesc` sync** into v1;
  - cutoffs and upcoming changes.
- **Role in the demo:** the semantics behind Cases 1–2.

### 6.5 PPH-API-CAT-2026.3 — PRISM Payments Hub API & Event Catalog

- **Basics:** published 2026-09-10.
- **Contents:**
  - **v1 deprecation notice** (no extensions);
  - consumer migration table: **cbo-wire-bff "Not started"**;
  - v1 and v2 endpoints with response excerpts. The `holdReasonDesc` note says only that it is "free text synced from HMS, not curated for external display";
  - v2 has no settlement object;
  - topics and onboarding;
  - SLAs;
  - backlog: PPH-2207, PPH-2251, PPH-2190.
- **Role in the demo:** endpoint truth and the hard deadline.

### 6.6 PNG-TDD-6.0 — Payment Network Gateway: Fedwire & gpi Technical Design

- **Basics:** dated 2025-11-14, with an addendum dated 2026-03-03. Ownership is shown as **PNE** (written before the re-org).
- **Contents:**
  - Fedwire: ISO 20022, pacs.002 acknowledgments with OMAD, and Reg J finality. The Fed does not report beneficiary credit. Includes acknowledgment metrics.
  - **gpi batch every 4 hours** into GPI_TRACKER_SNAPSHOT (columns include route and deducted charges); consumers are Ops and TDIP; **no API**; the table must not be exposed.
  - **Quota math:** about 7x over the contract for per-wire lookups.
  - gpi status table, including **G001**, and outcome statistics.
  - Addendum: the request to increase batch frequency was declined (PNG-1544).
- **Role in the demo:** network truth and the gpi constraints in Case 3.

### 6.7 PRSP-HMS-3.4 — Hold Management Service: Design & Hold Reason Taxonomy (RESTRICTED)

- **Basics:** last reviewed 2026-06-24.
- **Contents:**
  - hold lifecycle, including OFAC blocking and reporting;
  - the **12-code taxonomy** with tiers and shares;
  - volumes and resolution times;
  - **data handling:** descriptions are Restricted, with examples; the legacy sync to v1; open risk FCT-2004;
  - internal APIs only; no client-facing or attestation endpoints;
  - controls 012 / 018 / 031 / 040.
- **Role in the demo:** the risk-side truth behind Case 1.

### 6.8 ENS-INT-3.2 — Enterprise Notification Service Integration Guide

- **Basics:** published 2026-07-30.
- **Contents:**
  - channels and limits;
  - onboarding steps with a **6-week service level**; the year-end cutoff;
  - subscription model: **no per-entity subscriptions until ENS-1120**; a producer-resolved-recipients pattern is available;
  - Treasury event catalog, including **TPL-WIRE-REL-02 "Wire completed: …"** fired on v1 PROCESSED;
  - no events exist for Fed acceptance, ACCC, returns, gpi or hold actions.
- **Role in the demo:** the notification gaps, and a second "Completed" violation hidden in a template.

### 6.9 TDIP-CAT-2026.2 — Treasury Data & Insights Platform Data Catalog

- **Basics:** published 2026-09-18.
- **Contents:**
  - datasets with refresh, history, classification and owners;
  - feature tables, including **`beneficiary_behavior_profile`** (Restricted, fraud-only, M-FCT-0034 input);
  - corridor statistics sample;
  - Insights API pattern;
  - onboarding steps;
  - known gaps: Fed acks not ingested; gpi data nightly; no sub-minute serving.
- **Role in the demo:** data truth behind Case 4.

### 6.10 POL-FCC-014 v3.2 — Customer Communication of Payment Status, Holds & Exceptions Standard

- **Basics:** effective 2026-03-01; owner Catherine Doyle.
- **Contents:** this is the **"what we can and cannot show a customer" rulebook**.
  - Scope: all channels, including notifications, call-center scripts and third-party sharing.
  - Legal basis.
  - Disclosure tiers P/C/G/R.
  - **§5.1 hold rules:** no restricted reasons; indistinguishability; no ETA; client actions only per Appendix A; callback cannot be satisfied in-channel; sanctions handled by Sanctions Ops.
  - **§5.2 status terminology:** "Completed / Settled" only after Fed acceptance or gpi ACCC; "Credited" only on ACCC; "Tracking unavailable beyond [bank]" for G001.
  - §5.3 gpi data.
  - **§5.4 third-party sharing:** no accounts or fees; links expire within 7 days; InfoSec and Privacy review required.
  - **§5.5 insights:** own data or thresholded cohorts only; MRM; disclaimer; never on G/R holds.
  - Approvals.
  - Appendix A (code → tier → copy → action), Appendix B (approved copy library), Appendix C (prohibited terms).
- **Role in the demo:** the compliance backbone for Cases 1–3 and the share-link finding.

### 6.11 DUS-07 v2.1 — Data Use & Client Confidentiality Standard

- **Basics:** effective 2026-01-15; owner: Chief Privacy Officer.
- **Contents:**
  - GLBA (consumers) versus contractual confidentiality (commercial clients);
  - classification;
  - **§3 purpose limitation**: feature tables inherit the most restrictive purpose of their inputs;
  - **§4 cross-client prohibition**, including a counterparty's account activity after receiving funds;
  - **§5 cohort thresholds**;
  - §6 own-data rules;
  - approvals.
- **Role in the demo:** the privacy rules behind Case 4.

### 6.12 MRM-POL-02 v7.0 — Model Risk Management Policy (extract)

- **Basics:** effective 2026-07-01, aligned to the April 2026 interagency guidance.
- **Contents:**
  - definitions of Model, EUA and customer-facing estimate;
  - tiering, with **customer-facing estimates at Tier 2 minimum**;
  - use limitations on financial-crimes models;
  - inventory extract;
  - validation queue notice.
- **Role in the demo:** why "predicted delivery time" cannot be in the MVP, and why fraud features can't drive product insights.

### 6.13 JIRA-EXP-2026-10-05 — Jira Export, Wire Center & Dependency Backlog

- **Basics:** 29 issues across projects CBO, PPH, PNG, GTSI, FCT, ENS and TDA, with selected comments.
- **Key planted details:**
  - **CBO-4388** (hold-reason tooltip):
    - In Progress and merged; feature flag defaults ON; production **2026-10-22**;
    - its UAT comments quote fraud and sanctions text;
    - the Service Center praises it.
  - **CBO-4402:** the "Completed" label.
  - **CBO-4419 / CMP-2026-1189:** a client relied on "Completed" for a EUR 412,600 wire that was later rejected (AC04).
  - **CBO-4471:** the v2 migration, 34 points, unscheduled.
  - **CBO-4480:** the gpi spike, still pointing to Raj.
  - **CBO-3790 / 3802 / 3815:** the ACH Tracker's reusable assets.
  - **PPH-2207:** no sponsor.
  - **PPH-2190:** v1 sunset reminders.
  - **FCT-1893:** deprioritized with "no channel consumer committed".
  - **FCT-1951:** 82% of duplicate holds resolved in 30 minutes.
  - **FCT-2004:** the open leak risk.
  - **GTSI-0107:** Elena Vasquez wants channel requirements.
  - **TDA-2188:** hourly gpi load.
  - **TDA-2210:** blocked on an ACL.
  - Linked records: the complaint and incident INC-2024-1182.
- **Role in the demo:** what's in flight and what history exists. It supplies the **time-bound critical finding**.

### 6.14 ARB-PAY-REG-2026Q3 — Payments ARB ADR Register & Minutes

- **Basics:** published 2026-09-12.
- **Contents:**
  - ADR register and summaries: 017 / 019 / 021 / 023 / 026;
  - minutes of 2026-09-08: no v1 extension; GTRS unfunded; **no direct gpi snapshot exposure**; SPS is the reference pattern.
- **Role in the demo:** binding architecture constraints.

### 6.15 PIR-2024-07 — Post-Implementation Review: Wire Status Lite Pilot & INC-2024-1182

- **Basics:** dated 2024-07-15.
- **Contents:**
  - In 2024, a pilot polled v1 every 30 seconds. On a month-end it overloaded PPH:
    - 1,240 wires delayed by 47 minutes;
    - 312 missed the Fed cutoff;
    - 14 clients compensated, $41,800 in total.
  - Client learnings: 37% thought "Processed" meant the beneficiary had been paid.
  - Root causes and actions. One action remains **open: "validate status terminology with FCC and Legal"**.
- **Role in the demo:** institutional memory. It shows a lesson the organization forgot.

### 6.16 Files outside the corpus (never ingest into the graph)

- **PM-WTC-MR-0.3 — Market Research Summary & Feature Concept.** This is what Sarah uploads during the demo.
  - Research inputs:
    - 61,000 wire inquiries per year; 38% are "where is my wire", at 11.5 minutes each;
    - 24 client interviews;
    - a competitive scan.
  - Feature concept **FC-01..FC-07**, with deliberate flaws:

| Concept item | Flaw | Finding |
|---|---|---|
| FC-01 | "Settled = Completed" | F2–F4 |
| FC-02 | Live gpi every minute; "Expected delivery: Today"; engage Raj | F5–F8 |
| FC-03 | Exact risk reasons; Confirm/Reject on all holds; "released ~30 min after confirm" | F9, F1 |
| FC-04 | Beneficiary-behavior insight; cohort statistic; predicted delivery computed in the BFF | F10–F13 |
| FC-05 | Per-wire "notify me when settled" | F14 |
| FC-06 | Share link with fees and funding account | F15 |
| FC-07 | Returned wires | — |

  - Assumptions section: "status API already used", "Raj's team", "insights in BFF", "existing ENS events", "mostly front-end, 1.5 PIs" (→ F16).
- **Demo Pack (PDF):**
  - storyline and graph model (266 typed nodes);
  - the four cases with traversal paths;
  - run-of-show;
  - **10 questions with target answers and sources**;
  - effort plan;
  - Appendix A answer key (F1–F16);
  - Appendix B graph tips.
- **estate_ground_truth.json:** structured people, teams, systems, interfaces, Jira, hold codes and seeded findings, for **scoring** the agent.

---

## 7. The 16 seeded findings (answer key)

A strong agent surfaces **at least 12 of 16** with correct sources. "Docs" = the documents that must be joined.

| ID | Finding | Docs to join | Severity |
|---|---|---|---|
| F1 | CBO-4388 will expose Restricted HMS text via v1 `holdReasonDesc` on 2026-10-22 | JIRA, PPH-API-CAT, PPH-SYS-OVW, PRSP-HMS, POL-FCC-014, ARB | **Critical** |
| F2 | "Completed" shown at release; template TPL-WIRE-REL-02 "Wire completed"; complaint CMP-2026-1189 | CBO-ARCH, PPH-SYS-OVW, PPH-API-CAT, ENS-INT, POL-FCC-014, JIRA, PIR | High |
| F3 | True "Settled" needs v2, rail-aware mapping and PPH-2207 (no sponsor) | CBO-ARCH, PPH-SYS-OVW, PPH-API-CAT, PNG-TDD, POL-FCC-014, JIRA | High |
| F4 | v1 sunset 2027-03-31 (no extension) vs unscheduled CBO-4471 | PPH-API-CAT, JIRA, ARB, ORG | High |
| F5 | No gpi API; 4-hourly batch; quota ~7x; ARB forbids direct exposure; GTRS in 2027 | PNG-TDD, ARB, JIRA, MEMO | High |
| F6 | gpi ownership moved PNE → GTSI; concept and CBO-4480 are stale | ORG, MEMO, PNG-TDD, JIRA | Medium |
| F7 | 8% of wires end at G001, so a universal "Expected delivery" is not allowed | PNG-TDD, POL-FCC-014 | Medium |
| F8 | Hourly TDIP load can't beat the 4-hour source | TDIP-CAT, PNG-TDD | Low |
| F9 | Exact hold reasons and Confirm/Reject on all holds violate policy and controls | PRSP-HMS, POL-FCC-014, ARB, JIRA | **Critical** |
| F10 | Beneficiary-outflow insight = cross-client + purpose-limitation + Tier-1 model misuse | TDIP-CAT, DUS-07, MRM-POL-02 | **Critical** |
| F11 | Corridor statistics need DUS-07 suppression (MXN and NGN fail) | TDIP-CAT, DUS-07 | Medium |
| F12 | Predicted delivery is a Tier 2 model: ~16–20 weeks including the queue | MRM-POL-02, TDIP-CAT, ARB | High (timeline) |
| F13 | Domestic history is blocked because Fed acks are not ingested (TDA-2210) | TDIP-CAT, PNG-TDD, JIRA | Medium |
| F14 | Per-wire notifications unsupported until ENS-1120; 6-week onboarding; freeze | ENS-INT, JIRA, ORG | Medium |
| F15 | Share link must exclude accounts and fees, expire within 7 days, and pass InfoSec + PIA | POL-FCC-014, CBO-ARCH | Medium |
| F16 | Planning constraints: PPH 90% committed, FCT freeze, GTSI knowledge transfer, PI dates | ORG, MEMO, JIRA | Planning |

---

## 8. Demo flow and the 10 questions (with target answers)

**Run of show (~15 minutes):**
1. Context.
2. Upload + Q1.
3. Q4 / Q5: the "stop the release" moment.
4. Q2 / Q3.
5. Q6.
6. Q7 / Q10.
7. Before/after close.

### Q1 — Dependencies and owners

**Target answer:**
- **Six systems** outside the portal: PPH, FFC, GPI-C, HMS, ENS, TDIP.
- **Three CBO platform services:** SPS, CES, step-up authentication.
- **Eight partner functions** with gates: FCC, MRM, Privacy, DRC, ARB, InfoSec, Ops, Treasury Support.
- **Correction:** gpi is owned by **GTSI (Omar Siddiqui)**, not Raj.
- FCT, MRM, Privacy, FCC and ARB are missing from the concept.

### Q2 — Can "Completed" mean "Settled"?

**Target answer: no.**
- Today's "Completed" label and the "Wire completed" template are already non-compliant.
- A real milestone needs:
  - the v2 migration (CBO-4471, before 2027-03-31);
  - event-driven status via SPS (ADR-PAY-019);
  - rail-aware mapping;
  - PPH-2207 for the exact Fed timestamp.
- Domestic milestones end at **"Delivered to beneficiary's bank"** (Fed acceptance, show OMAD). Never "credited" for domestic wires.
- **Action:** sponsor PPH-2207 at the 2026-10-21 Demand Board.

### Q3 — Live gpi route like FedEx?

**Target answer: not as specified.**
- Phase 2: a 4-hour-fresh "as of" view via a GTSI read-only service (~21 points, ARB review), with G001 handling and deducted charges.
- Real-time depends on GTRS (2027).
- The UETR join needs v2.
- Give GTSI your requirements now so they shape GTRS discovery.

### Q4 — Review the held-wire design

**Target answer: four policy issues** (restricted reasons, indistinguishability, Confirm/Reject scope, ETA) **and two missing FCT endpoints** (FCT-1893 client view + attestation).

| Hold group | Compliant treatment |
|---|---|
| HRC-01 | Attestation only, with step-up authentication, up to $5M |
| HRC-02 | "Request callback" |
| R and G tiers | Identical generic copy, no ETA |

- FCT effort: ~326 hours.
- FCC review needed.
- Mind the FCT freeze.

### Q5 — Anything in flight that conflicts?

| Priority | Item | Action |
|---|---|---|
| **Critical** | CBO-4388 tooltip | Stop it before 2026-10-22; notify FCC (Jordan Ellis) and FCT |
| High | CBO-4402 label + TPL-WIRE-REL-02 | Relabel to "Sent"; template change via DRC; FCC complaint review |
| High | CBO-4471 | Commit in PI 27.1; ARB 2026-11-10 |
| Medium | CBO-4480 stale owner | Re-route to GTSI |
| Low | TDA-2188 freshness trap | Set expectations |

### Q6 — Insights and predictions

| Insight | Verdict | Why / how |
|---|---|---|
| "Beneficiary moves funds within 4 h" | **Not permitted** | Breaches DUS-07 §3 and §4 and MRM-POL-02 §4. Replace with "your last N wires to this beneficiary were credited in a median X h" (own data, N ≥ 5). |
| "92% of EUR wires same day" | Conditional | Only with DUS-07 suppression; counts as an EUA; DRC wording. |
| "Predicted delivery" | **Phase 3** | Tier 2 model. |

- Insights must be served via the TDIP Insights API; neither of the needed endpoints exists yet.
- Domestic history needs TDA-2210.

### Q7 — Missing endpoints and builders

Target answer: a table of 12 gaps.

| Gap | Ticket | Size |
|---|---|---|
| PPH v2 settlement object | PPH-2207 | 8 pts |
| SPS wire mapping + topic ACL | New | ~13 pts |
| v2 migration + CES account filter | CBO-4471, CBO-4473 | 34 + 8 pts |
| Beneficiary-name index | PPH-2251 | 13 pts |
| GTSI gpi service | New | ~21 pts |
| HMS client view | FCT-1893 | 21 pts |
| Client attestation | None | ~13 pts |
| TDIP wire-history endpoint | None | 13 pts |
| TDIP corridor endpoint | None | 8 pts |
| Fed ack ingestion | TDA-2210 | 8 pts |
| 5 ENS event types | None | 5 × ~12 hours |
| 2 CES entitlements | None | ~5 pts |

### Q8 — Notify me when this wire settles

**Target answer:** not supported natively until ENS-1120.
- Workaround: an SPS watch list plus producer-resolved recipients.
- New event types needed; 6-week service level; submit before 2026-11-20.
- A "notify when released" option is allowed only if offered identically for all hold tiers.

### Q9 — Prior attempts and reuse

**Target answer:**
- **Wire Status Lite** failure → ADR-PAY-019.
- An open PIR action was never closed; "Completed" was later reintroduced.
- **Reuse:**
  - the timeline component + SPS (~30 points saved);
  - FCT-1951 evidence;
  - the cash-forecast Insights pattern (note the model is being re-tiered to Tier 2).

### Q10 — Effort, engagement plan and critical path

**Target answer:** 16 teams/functions, **~1,900 hours for Phases 1–2**, plus 160–240 MRM hours in Phase 3.

| Team | Points | Hours |
|---|---|---|
| CBO Wire Center squad | 92 | 598 |
| CBO Platform | 26 | 169 |
| PPH | 21 | 192 |
| PNE | — | 16 |
| GTSI | 21 | 163 |
| FCT | 34 | 326 |
| ENS | — | 60 |
| TDIP | 29 | 174 |
| MRM | — | 16 |
| FCC | — | 40 |
| DRC | — | 16 |
| Privacy | — | 24 |
| InfoSec | — | 32 |
| ARB | — | 12 |
| Ops | — | 40 |
| Treasury Support | — | 24 |

**Critical path:**
1. v1 sunset;
2. topic ACL + SPS;
3. FCT freeze;
4. GTSI knowledge transfer;
5. MRM queue.

**Phases:**

| Phase | Window | Scope |
|---|---|---|
| 1 | PI 27.1 | Domestic milestones to Fed acceptance, compliant holds, HRC-01 attestation, fixed labels, category notifications, own-history EUA insight |
| 2 | PI 27.2 | International 4-hour view, corridor statistics, watch notifications |
| 3 | 2027-H2 | Tier 2 ETA, GTRS real-time, ENS-1120, share link |

**This week's actions:**
- stop CBO-4388;
- raise the "Completed" label with FCC;
- sponsor PPH-2207;
- re-route CBO-4480;
- book ARB;
- submit PI asks;
- file ENS onboarding.

---

## 9. What remains to build

```
1. Ingestion    PDF → Markdown (pdftotext/markitdown) → git repo
2. Wiki         openwiki personal --init (git-repo source) with INSTRUCTIONS.md enforcing typed frontmatter
3. Graph        parse frontmatter → NetworkX → graph_query(tool): owners, exposes/consumes, sourced_from,
                governed_by, status/sunset, missing-interface nodes, valid_from for ownership
4. Agent        Claude Agent SDK app:
                  • anthropics/knowledge-work-plugins/product-management (fork write-spec → write-brd)
                  • estate-discovery skill (below)
                  • tools: wiki_read, wiki_grep, graph_query; optional Jira MCP for epic handoff
                  • optional reviewer subagents: Architect, Compliance (FCC), Ops
5. Scoring      compare findings vs estate_ground_truth.json (recall of F1–F16, source accuracy)
6. Live moment  add/modify a document → openwiki --update → regenerate BRD on stage
```

**`estate-discovery` skill logic.** For each capability in the PM's concept, trace this chain:

```
data needed → producing system → interface (exists? missing?) → current owner (latest valid_from wins)
→ governing policy clauses → open Jira → prior incidents/PIRs
```

Then flag:
- conflicts and stale references;
- deadlines;
- tier/classification issues;
- in-flight work that conflicts.

**Graph conventions:**

- **Entity ID patterns:**

| Kind | Patterns |
|---|---|
| Systems, interfaces | `SYS-*`, `EP-*`, `EV-*`, `BT-*` |
| Hold codes | `HRC-\d\d` |
| Policies | `POL-*`, `DUS-*`, `MRM-*` |
| Architecture and controls | `ADR-PAY-\d+`, `CTRL-PAY-\d+` |
| Jira | `[A-Z]+-\d+` |
| Incidents, complaints, models | `INC-*`, `CMP-*`, `M-FCT-*`, `M-TRS-*` |

- **Frontmatter fields:** `type, id, owned_by, exposes, consumes, sourced_from, classification, permitted_purpose, governed_by, status, sunset_date, valid_from`.
- **Gap nodes:** "DOES NOT EXIST" interfaces become nodes linked to the capability and the proposal ticket.
- **Field-level lineage:** needed for Cases 1 and 4 (`holdReasonDesc`, `bene_median_hours_to_outflow`).

---

## 10. Guardrails for future sessions

- **Never ingest the market research, Demo Pack or ground-truth JSON into the graph.** They contain the answers.
- **Keep facts consistent with §5** when editing or adding documents. IDs, dates, percentages and point sizes are cross-referenced across documents and the Demo Pack.
- **Pitfalls must remain multi-hop.** Source documents must not state the conclusions; for example, the policy must never mention CBO-4388.
- **Keep the bank fictional:** Crestline National Bank / CBO / PRISM / PTT. Do not substitute a real bank's name. Corpus documents must contain no demo, synthetic or fictional language.
- **Answer style I prefer in chat:**
  - summary first, then a hierarchical, detailed answer;
  - simple English, technical terms where needed;
  - ASCII diagrams where helpful;
  - not overly long;
  - **"qq" prefix = quick, concise answer**.

---

## 11. Glossary

| Term | Meaning |
|---|---|
| BRD / PRD | Business / Product Requirements Document |
| WISMO | "Where is my wire/money" inquiries |
| IMAD / OMAD | Fedwire input / output message accountability data; OMAD = Fed acceptance reference |
| UETR | Unique end-to-end transaction reference (gpi tracking key) |
| ACSP / ACCC / RJCT | gpi statuses: in progress / credited / rejected |
| G001 | Forwarded to a non-gpi bank; tracking ends |
| CBPR+ | Swift's ISO 20022 cross-border usage guidelines |
| SPS | CBO Status Projection Service (event-driven read model) |
| CES | Commercial Entitlements Service |
| HMS / HRC | Hold Management Service / Hold Reason Code |
| P / C / G / R | Disclosure tiers (public / client-actionable / generic / restricted) |
| EUA | End-User Analytic (descriptive, not a model) |
| GTRS | gpi Tracker Real-Time Service (future, GTSI-0107) |
| PI | Program Increment (quarterly planning cycle) |
| ARB / DRC / PIA | Architecture Review Board / Disclosure Review Committee / Privacy Impact Assessment |
| FCC / FCT / FIU | Financial Crimes Compliance / Financial Crimes Technology / Financial Intelligence Unit |
| SAR | Suspicious Activity Report (confidential by law) |
| OKF | Open Knowledge Format (OpenWiki output) |
