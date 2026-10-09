# OpenWiki findings

Observations from testing OpenWiki 0.7.0 on the MHFC document corpus (Windows 11, Node 24.13.0).
Testing OpenWiki's capability is the point of the POC, so this log is a deliverable.

## Setup (verified 2026-10-04)

| Spec item (BUILD_SPEC Sections 3, 10) | Result on 0.7.0 |
|---|---|
| Launch as `node <npm root -g>/openwiki/dist/cli/cli.js` | Works. `npm install -g` under npm 11 warns that better-sqlite3's install script is not allowed, but the prebuilt `better_sqlite3.node` is shipped, so no build tools are needed. |
| `OPENWIKI_CONFIG_DIR` isolates state | Works. With it set, the banner shows the project's provider/model instead of the user's global `~/.openwiki` (which was OpenAI). |
| Anthropic model IDs | OpenWiki presets are `claude-sonnet-5` and `claude-haiku-4-5`. Custom IDs are accepted and checked against the provider. `claude-sonnet-5-5` and `claude-haiku-4-5-20251001` both work. |
| `mcp` subcommand | Present (`openwiki mcp`), although not listed in `--help`. |
| Non-interactive `--init --print` | Works without the interactive first run. Writing `<config dir>/onboarding.json` as `{version: 1, completedAt, modeId: "code", modeName: "Code", sourceInstances: [], sources: {}}` is enough; the wiki goal is read from the repo's `openwiki/INSTRUCTIONS.md`. Env vars cover provider, key and model; `LANGCHAIN_TRACING_V2=false` skips the LangSmith step. `scripts/build-semantic.ps1` does this. |
| Interactive onboarding and INSTRUCTIONS.md | Code-mode onboarding pre-fills the "wiki goal" box from the existing INSTRUCTIONS.md and writes the box back on confirm. Pressing Enter keeps the brief; editing the box replaces it. |
| Windows encoding | PowerShell 5.1 `Set-Content -Encoding utf8` writes a BOM, which would break `onboarding.json` and `.openwikiignore`. The scripts write UTF-8 without BOM. |
| Windows git | A global `core.autocrlf=true` treats the generated PDFs as text. The corpus repo sets `core.autocrlf false` locally. |

## How OpenWiki builds a wiki (from source, 0.7.0)

`--init` runs in phases: LangSmith ingest (skipped if not configured), **planning**, **generating**,
finalizing. The planning agent's only output is `submit_plan`, a list of pages; **page paths are final
once submitted**. Then one fresh worker writes each planned page, and `index.md` files are generated.
The planning prompt (`dist/agent/repository-prompts.js`) is written for codebases: it asks for "the
smallest complete repository-specific information architecture", requires `/openwiki/quickstart.md`,
and appends our INSTRUCTIONS.md at the end.

## Run 1: Haiku dry run, brief as provided (2026-10-04)

- Model `claude-haiku-4-5-20251001`, concurrency 3. Planning about 7 min; total about 15 min.
- **Plan: 1 page** (`/openwiki/quickstart.md` only, no seedPaths or relatedPages).
- Output: `quickstart.md` (28 KB, 15 headings, front-matter `type: overview`, Grounded Claims sources
  as `repo://sources/...`) and a generated `index.md`. `.claims/quickstart.json` present.
- quickstart.md contains 47 links to `.md` pages that were never planned (e.g. `apis/api-01-accounts-api.md`).
  The visualizer drops links to missing pages, so the graph is about 2 nodes.
- Conclusion: Haiku understood the target structure (it linked to it) but followed the planning
  prompt's "smallest" instruction over the brief's page catalogue. The brief describes page types but
  never lists the pages to plan.

## Change: explicit page list in the brief (2026-10-04)

Added a "Required pages (planning: submit ALL of these in the plan)" section to
`templates/semantic-INSTRUCTIONS.md`: about 80 page paths by folder and `type`, with seed paths, and an
explicit note that "smallest complete" means one page per entity for this corpus. Reason: Run 1 showed
the planner follows the code-oriented prompt over a brief that only describes page types.

## Run 2: Sonnet, strengthened brief (2026-10-04)

- Model `claude-sonnet-5-5`, concurrency 3. Planning about 12 min; generation about 30 min.
- **Plan: 87 pages**, matching the brief's list plus a few of its own (`apis/developer-platform-overview.md`,
  3 `workflows/` pages, `overview.md`). Every planned page had seedPaths and relatedPages.
- Page quality is good: front-matter `type` from the brief, quoted numbers with dates, and a
  "Relationships" section of labelled links (e.g. API-10: owned by Risk Analytics Engineering; feeds
  MDL-CR-007 and CECL lifetime PD).
- **11 pages were silently skipped.** They were left as stubs (`openwiki_generated: true`, `type: Reference`,
  no description), and the run still reported `complete` with exit 0. They included
  `metrics/allowance-for-credit-losses.md`, `reports/pillar3-disclosures-2025.md` and
  `scenarios/macro-scenarios-msc-2025q4.md`. Cause (from `dist/agent/repository-runner.js`): a page
  worker that throws, or ends without calling submit, is marked skipped. In `--print` mode the warning
  is not printed, and only the final "await enrichment on a later run" line mentions it.
- A plain `--update --print` **did nothing** (plan of 0 pages): with no source drift the planner may
  submit `pages: []`, even with stubs present.
- `--update --print "<message naming the 11 stub paths>"` **fixed all 11**, in about 10 min.
  `scripts/build-semantic.ps1` now does this automatically after `--init` when stubs remain.
- Grounded Claims work on Markdown sources: 760 claims in 87 `.claims/` files, all with line-range
  evidence such as `repo://sources/reports/mhfc-2025-annual-report.md#L166-L176`.

### Final semantic graph (`GET /api/graph`, after the stub fix)

- **99 nodes, 942 edges**, no isolated nodes.
- Types: API 19 (18 APIs + platform overview), Team 16, Section 12 (generated folder `index.md`
  pages), FinancialMetric 10, ModelComponent 10, RiskConcept 8, Organization 5, Person 5,
  FinancialModel 3, Scenario 3, Report 3 (one written as `report`), Workflow 3 (two as `workflow`),
  overview 1, quickstart 1.
- Acceptance (BUILD_SPEC Section 9, Stage 1): all 3 reports, 3 models, 18 APIs, the bank plus 4 segments and
  key metrics are typed nodes. `models/cecl-allowance-model` links to API-10, API-11, API-14,
  `metrics/allowance-for-credit-losses` and `reports/annual-report-2025` (27 neighbours in total).
- Minor: `type` casing is not enforced (`report`/`Report`, `workflow`/`Workflow`), so the visualizer
  colours them as separate types.

### Visualizer (verified)

`openwiki visualize semantic-corpus/openwiki --port 4321 --no-open` prints `open: http://127.0.0.1:4321`
(with ANSI colour codes around the URL; strip them when parsing). The CSP has no `frame-ancestors` and
there is no `X-Frame-Options`, so iframe embedding works. `/api/graph` returns `{nodes, edges}` with
edges as `{source, target}`.

## Backend process supervision (milestone 3, 2026-10-04)

- `openwiki visualize` **starts fine on a wiki folder holding only INSTRUCTIONS.md** (0 pages; `/api/graph`
  returns empty `nodes`/`edges`). The placeholder `index.md` fallback in BUILD_SPEC 8.1 is not needed.
- **Bug in OpenWiki 0.7.0: the banner reports the wrong port after an auto-increment.** When the
  preferred port is taken, `listen()` retries on port+1 but leaves the first attempt's callback
  attached (`dist/visualize/server.js`), so on success *both* callbacks fire: a stale banner
  `open: http://127.0.0.1:<taken port>` is printed first, then the real one (the initial scan and
  file watcher are also started twice). Reproduced 7 of 8 times on Windows. Requests to the stale URL
  reach the *other* visualizer. The backend therefore takes the port from the process's actual
  listening socket (psutil) instead of the banner; a regression test runs 5 times.
- A plain Python socket bound to a port does *not* block Node on Windows (no exclusive bind), so
  port-conflict tests must use a second visualizer.
- Visualizers are started without `CREATE_NO_WINDOW` so they share the backend's console: closing the
  terminal or pressing Ctrl-C also ends them, and they cannot be orphaned when the terminal closes.
- uvicorn on Windows / Python 3.13 can hang forever after "Shutting down" (a reset client connection
  leaves `Server.wait_closed()` pending), which skips the lifespan shutdown. `scripts/dev.ps1` passes
  `--timeout-graceful-shutdown 5`; verified: Ctrl-Break gives "Application shutdown complete", exit in
  0.2 s, no `node.exe` left, ports 4321/4322 free.

## Frontend embedding (milestone 4, 2026-10-04)

- Both visualizers render inside the React app's iframes. Verified with Playwright (Chromium): the
  topbar and the force-graph `<canvas>` render, and `fetch('/api/graph')` from inside the semantic
  iframe returns the full graph.
- The iframes use `sandbox="allow-scripts allow-same-origin allow-popups allow-popups-to-escape-sandbox"`.
  The visualizer works under it: its scripts from cdn.jsdelivr.net, same-origin `/api/graph` and the
  SSE live reload all work, and it cannot navigate the parent tab.
- Pages stay mounted and are hidden with the `hidden` attribute; a Playwright test confirms the
  visualizer window survives a page switch (no reload).
- `scripts/dev.ps1` starts Vite with `Start-Process -NoNewWindow` (not `Start-Job`, whose hidden
  process does not receive Ctrl-C). Verified: Ctrl-Break stops all six processes and frees ports
  8000, 5173, 4321 and 4322.

## Agent over OpenWiki MCP (milestone 5, 2026-10-04)

### OpenWiki MCP server (verified)

- `node <cli.js> mcp --host poc-agent` works as a stdio MCP server on Windows. It exposes
  `openwiki_search`, `openwiki_read`, `openwiki_list_workspaces`, `openwiki_list_wikis` and the
  generation tools (`openwiki_begin`, `openwiki_submit_plan`, ...). `mcp` is not listed in `--help`.
- `openwiki_search` returns `{"results": [{"kind": "section", "ref": ["openwiki/<page>.md#<anchor>"], "content": ...}]}`
  (`ref` is a list). `openwiki_read` returns `{"page", "sections": [{"section", "content"}]}`.
- An unknown section anchor or a missing root returns `isError` with text such as
  `invalid_input: Unknown section: x`; the tool wrappers hand this back to the model as `Error: ...`.
- Searching a root whose `openwiki/` has no generated pages returns `{"results": []}` (not an error).
  `memory_*` add `"note": "memory not built yet"` until `context-corpus/openwiki/index.md` exists.
- **Repeated identical searches in one MCP session return fewer results** (8 hits, then 1 hit for the
  same query). That looks like session-level de-duplication of already-returned sections.
- One MCP session serves both wikis (different `root` per call). The anyio-based session must be
  opened and closed in the same asyncio task, so the backend keeps it in a dedicated owner task.

### Structured output with claude-sonnet-5-5 + LangChain 1.4 (important)

- `create_agent(..., response_format=AgentAnswer)` (auto strategy) and `ProviderStrategy(AgentAnswer)`
  **never finish**: the model keeps calling search/read (re-reading the same section 20+ times) until
  the recursion limit. One CET1 question used 384k input tokens and 51 s before giving up.
- `ToolStrategy(AgentAnswer)` fails immediately: `tool_choice: type "tool" and "any" are not supported
  for this model` (400).
- Without `response_format` the same agent answers after 1 search.
- **Fix used:** a normal `submit_answer` tool whose arguments are the `AgentAnswer` schema, with
  `return_direct=True`, plus a prompt line to call it when done. Fallback if the model replies in
  plain text: `model.with_structured_output(AgentAnswer, method="json_schema")` (native structured
  output, no forced tool choice). Recursion limit 40 caps a runaway loop.
- Result on the CET1 question: 1 tool call, 6,951 input tokens, 6.3 s (was 22+ calls, 384k tokens, 51 s).

### Acceptance (BUILD_SPEC Section 9, Stage 2 questions 1-4, one session, Sonnet 5.5)

| # | Expected | Result | Tool calls | Latency |
|---|---|---|---|---|
| 1 | CET1 15.1% (15.08%) vs 10.2%, target 13.0% | correct, cites capital pages | 1 | 6.3 s |
| 2 | API-10/11/14; Allowance Methodology | correct | 3 | 9.8 s |
| 3 | PD elasticity, lifetime PD, LGD, EAD, 20/50/30, overlay $681mm | correct; "that model" resolved from history | 3 | 11.6 s |
| 4 | NII about -$3.0bn (-6.0%), within 7% | -$3,016.89mm (-6.01%), within 7.0% | 2 | 8.5 s |

Log: `logs/live-agent-q1-4.log`. The agent sometimes answers from search snippets alone without a
`semantic_read`, even though the prompt asks for a read; the answers were still exact.

## Turn trace files (milestone 6, 2026-10-05)

- After each answer the backend writes `context-corpus/sessions/<session_id>/turn-NNNN.md` in the
  BUILD_SPEC 8.2 format, rewrites `session.md` (`type: SessionLog`, `started_at`, `turn_count`, linked
  turn list) and commits `turn <session>/<n>`. `session.md` is only created on a session's first turn, so
  page loads do not leave empty sessions in the memory graph. `GET /api/sessions/{id}` reads the files back.
- Front matter is written with PyYAML in block style. A first version used flow style for all-scalar
  mappings (`{type: SessionLog, ...}`): valid YAML but unusual for Markdown front matter.
- Free text (question, answer, reasoning) has `#`/`##` headings pushed down to `###`, so an answer
  cannot fake a trace section.
- **Added field `semantic_refs_seen`**: every semantic ref the tools returned (all search hits plus
  reads). The agent often cites pages it saw only as search snippets: `semantic_pages_read` was empty
  for a turn that cited 4 pages. A cited source outside `semantic_refs_seen` is marked
  `[not seen in tool results]` under "Sources cited", in keeping with the brief's "never invent
  sources" rule. In the live check every citation was in the seen set.
- **Bug found and fixed (from milestone 5):** when `submit_answer` arguments failed validation (the
  model sent 4 follow-up questions; the schema allows 3), `return_direct` ended the run on the error
  message and the request returned 502. The tool's input schema is now lenient (follow-ups trimmed to 3),
  and any other failed submission falls back to structuring the attempted answer text.
- A trace write failure never loses the answer: the response carries `trace_file: null` and the error
  is logged.

## Memory sync and context graph (milestone 7, 2026-10-05)

### Sync timing (Haiku 4.5, real runs on Windows)

| Run | Turns covered | Page concurrency | Duration | Result |
|---|---|---|---|---|
| `--init` (scratch test) | 3 | 3 | 1,118 s (18.6 min) | 28 pages, 170 links; 3 pages skipped, 2 stubs |
| `--update` (scratch test) | +1 | 6 | 294 s | 7 pages rewritten (new Turn, Session, 2 SourceReferences, Topic, timeline, quickstart) |
| `--init` (live app, Q1 only) | 1 | 6 | 810 s (13.5 min) | |
| `--update` (live app, coalesced Q2-Q5) | +4 | 6 | 464 s (7.7 min) | 33 pages incl. 4 Decision pages |
| `--update` (live app, one Q6 turn) | +1 | 6 | 144 s | graph 32 -> 33 nodes, 138 -> 148 edges |

Memory therefore lags the chat by minutes: the first sync takes 13-19 min, later updates 2-8 min. Coalescing
works as designed: the first `--init` started with turn 1 only, turns 2-5 arrived during it, and exactly one
`--update` followed. `CONTEXT_OPENWIKI_PAGE_CONCURRENCY` (default 6) is separate from the semantic build's 3.

### The context brief works better than the semantic one did

Haiku planned 23 pages for 3 turns (all types except Decision) on the first try. The brief's per-entity
rules ("one Turn page per turn file") gave the planner enough to go on. A later live run did produce Decision
pages ("Decision to Decline Model Re-run", "Decision to Search for NII ..."). Like the semantic run, page
workers sometimes exit without submitting; those pages are restored as stubs ("Reference" type) and retried
on the next update.

### Visualizer live reload does not survive `--init` (OpenWiki limitation)

`openwiki --init` deletes and recreates `openwiki/` (folder creation time 13 s after the visualizer
started; INSTRUCTIONS.md carried over). The visualizer's recursive `fs.watch` stays bound to the deleted
folder, so the graph stays at 0 nodes forever. **Fix:** after each successful sync the backend restarts the
context visualizer (same port; ~1 s) before publishing `last_success_at`, and the frontend remounts the
iframe when `last_success_at` changes. Verified live: graph refreshed from 32 to 33 nodes without a reload.

### Agent behaviour fixes found by the live run

- **Q5 (new scenario):** the agent said it could not run the model and then gave a "rough hand estimate"
  (~12.5%). The prompt now forbids any calculated or approximate result for new scenarios and asks for the
  input sheet/cell and affected outputs instead. Live: it cites `Assumptions!B13`, lists the affected cells,
  notes the stress path hard-codes buybacks at 0, and sets confidence to low.
- **Q6 (conversation questions):** the agent answered "what have I asked so far" from chat history only,
  with no tool calls. The prompt now requires `memory_search` first for questions about the conversation.
  Live, same session: `memory_search` returned 10 hits and Turn, Decision, Intent and timeline pages were
  cited. Live, new session (no history): it listed all 5 earlier questions with their confidence from memory.
- **Citation check:** memory citations seen only in `memory_search` hits were wrongly marked
  `[not seen in tool results]`; `context_refs_seen` now tracks them (0 flags in the live run).

### Test safety

- Live pytest tests run with `MEMORY_SYNC_MODE=manual`: one live turn had started a real ~20 min `--init`.
- Playwright's backend uses its own `logs/e2e-context-corpus` and manual sync. An earlier e2e run reset the
  user's `context-corpus/` because the backend wipes its corpus on start.
- Once, a live pytest run waited ~5 min at shutdown for a running OpenWiki sync. Not reproduced in three
  targeted attempts (direct `stop()`, app shutdown with a real Node process, real agent + real sync: all exit
  in 0.1-0.7 s). Both paths now have regression tests.

### Known gaps

- After a new session, the update added the new Turn but no second Session page (1 Session node for 2 sessions).
- Some page types come out under different names (`Entry Point`, `Reference`, `Section`), and stubs stay
  `Reference` until a later update fills them.

## Polish (milestone 8, 2026-10-05)

- **Reset demo** (`POST /api/demo/reset`, UI button with inline confirmation, `scripts/reset-context.ps1`):
  stops a running memory update (kills the OpenWiki process tree), stops the context visualizer (Windows
  will not delete a folder another process watches), recreates `context-corpus/`, restarts the
  visualizer, clears sessions and returns a new one. Verified live: reset during a real `--init` left no
  OpenWiki process, one "context corpus" commit, the old session returned 404, and the viewer was serving.
- Backend INFO logs now appear in the console (uvicorn only configures its own loggers).
- The memory pill shows "status unavailable" when the backend does not answer; reset failures are shown
  with the backend's reason.
- `pytest-asyncio` was missing from `backend/requirements.txt` (async tests would fail on a fresh setup).
  Verified with a fresh venv built only from the requirements: 71/71 tests passed.

## How the agent uses the semantic graph (retrieval path, 2026-10-05)

- `openwiki_search` does **not** traverse graph edges. It ranks every `##` section of every page with SQLite
  FTS5 BM25 (weights: title 8, heading 6, description 4, identifiers 3, body 1; "Related pages"/"See also"
  sections excluded), ordered first by how many query terms a section covers. `openwiki_read` returns whole
  sections. Links between pages play no part in retrieval.
- Each answer now carries a `retrieval` object (and the UI a "How the answer was found" panel): every semantic
  node (page) the tools returned, in order of discovery, with type, step and rank, sections, whether it was
  opened and whether it was cited, plus the graph's own edges between those nodes (from the visualizer's
  `/api/graph`). Built only from observed tool calls.
- Live example ("Which APIs feed the CECL model, and who owns that model?"): 2 searches reached 9 nodes;
  0 were opened (the agent answered from search excerpts) and 4 were cited.
