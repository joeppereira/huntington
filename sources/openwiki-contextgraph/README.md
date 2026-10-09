# OpenWiki Semantic + Context Graph POC

A proof of concept that tests LangChain's **OpenWiki** CLI on two jobs:

1. **Semantic graph** - turn a set of financial documents (3 PDF reports, 3 Excel models, 1 API
   reference) about a fictional bank into a linked wiki and an interactive graph.
2. **Context graph** - a LangChain Q&A agent answers questions about those documents while every turn,
   tool call and decision is written to a second OpenWiki wiki that acts as the agent's memory and is
   shown live next to the chat.

All data is synthetic. "Meridian Harbor Financial Corp." is fictional and does not describe any real
company.

## Status

Built and working (milestones 1-8 of `BUILD_SPEC.md`). Findings about OpenWiki, including timings,
issues and workarounds, are in [`docs/openwiki-findings.md`](docs/openwiki-findings.md).

**Main limitation:** the agent answers in 6-17 s, but the memory (context) graph lags behind. Each
memory update is a full OpenWiki run: about **13-19 min the first time** after the app starts, then
**2-8 min per update**. The semantic graph is built once in advance and loads instantly.

## Quickstart (Windows)

### 1. One-time setup

Requirements: Node.js 22.22+, Git for Windows, Python 3.12 or 3.13 (3.14 lacks some package builds),
an Anthropic API key, and internet access (the OpenWiki graph viewer loads its libraries from a CDN).

Get the project folder (`git clone <repo url>`, or unzip a shared copy), then run setup **from inside
that folder** (about 5 minutes):

```powershell
cd C:\path\to\openwiki-graph-poc
powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
```

This checks the prerequisites, installs OpenWiki 0.7.0 with npm, creates `.venv` (or rebuilds one
copied from another machine), installs the Python and frontend packages, creates `.env` from
`.env.example`, and restores the **prebuilt semantic graph** from `prebuilt/semantic-corpus/` into
`semantic-corpus/` as its own git repository (OpenWiki requires that). Then put your own key in `.env`:

```dotenv
ANTHROPIC_API_KEY=sk-ant-...
```

### 2. Semantic graph: already built

The repository ships the finished semantic graph, so there is nothing to build. Rebuilding it from
`data/` is only needed if the documents change (about 45 min, roughly $25-35 of API use):

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build-semantic.ps1
```

It converts `data/` to Markdown in `semantic-corpus/` and runs `openwiki --init` with Sonnet; pages that
OpenWiki silently skips are rewritten automatically with a targeted `--update`.

### Sharing a copy (Google Drive, zip)

Leave out `.env` (your key), `.venv\`, `frontend\node_modules\`, `logs\` and `context-corpus\`; the
recipient's `setup.ps1` recreates them. Everything else, including `semantic-corpus\`, can be copied.

### 3. Run the app

```powershell
powershell -ExecutionPolicy Bypass -File scripts\dev.ps1
```

Open **http://127.0.0.1:5173**. Stop everything with **Ctrl+C** in that window (this also stops the
graph viewers and any running memory update).

- **Semantic Graph** tab: OpenWiki's graph of the bank documents (99 pages). Click nodes to read pages.
- **Agent & Memory** tab: chat on the right; the memory graph on the left. Each answer shows sources,
  follow-up chips and a collapsible decision trace. The pill above the graph shows the memory state
  (empty, syncing (N pending), up to date, failed). **Sync memory now** starts an update;
  **Reset demo** wipes the memory and starts a new chat.

A good test sequence (one session): "What was Meridian Harbor's CET1 ratio at year-end 2025, and what
is its requirement?", "Which APIs feed the CECL model, and who owns that model?", "How does that model
turn scenarios into an allowance?", "What happens to NII if rates drop 200 bp?", "What would the CET1
ratio be if buybacks doubled?". When the pill says up to date: "What have I asked so far, and where were
you least confident?"

### Settings worth knowing (`.env`)

| Setting | Default | Effect |
|---|---|---|
| `RESET_CONTEXT_ON_START` | `true` | Wipe the agent's memory on every start. Set `false` to keep memory between runs (avoids the long first update). |
| `MEMORY_SYNC_MODE` | `per_turn` | `per_turn`: update memory after every answer (turns that arrive mid-update are batched into one more update). `manual`: only when you press **Sync memory now** (cheapest). |
| `CONTEXT_OPENWIKI_MODEL_ID` | Haiku 4.5 | Model OpenWiki uses for memory updates. |
| `CONTEXT_OPENWIKI_PAGE_CONCURRENCY` | `6` | Parallel page writers per memory update (OpenWiki maximum 8). |
| `AGENT_MODEL_ID` / `OPENWIKI_MODEL_ID` | Sonnet 5.5 | Q&A agent / semantic graph build. |

To wipe memory without the UI: `powershell -ExecutionPolicy Bypass -File scripts\reset-context.ps1`
(works whether or not the app is running).

### API cost (estimates)

- Semantic graph build: one-time, roughly $25-35 (Sonnet).
- Each question: about $0.02-0.05 (Sonnet).
- Each memory update: roughly $0.20-1 (Haiku); the first after a start costs the most.

OpenWiki does not report its token usage; check the Anthropic console for actual spend.

## Tests

```powershell
# Backend: about 4 min, free (no model calls)
cd backend; ..\.venv\Scripts\python -m pytest -q

# Live agent tests: spec questions 1-5 against the real model (a few cents)
$env:RUN_LIVE = "1"; ..\.venv\Scripts\python -m pytest -m live -s -q; Remove-Item Env:RUN_LIVE

# Frontend unit tests (seconds) and browser tests (start their own app; stop dev.ps1 first)
cd ..\frontend; npm test; npm run e2e
```

Browser tests use their own memory folder (`logs/e2e-context-corpus`) and manual sync, so they never
touch `context-corpus/` or start a paid memory update.

## How it fits together

- `backend/` (FastAPI) is the one process you start. It runs two `openwiki visualize` processes
  (semantic on 4321, context on 4322), one `openwiki mcp` server for the agent's search/read tools, and
  the memory update engine. API: `/api/health`, `/api/config`, `/api/sessions`, `/api/chat`,
  `/api/memory/status`, `/api/memory/sync`, `/api/demo/reset`.
- `frontend/` (Vite + React) embeds the two OpenWiki viewers in iframes and hosts the chat.
- After each answer the backend writes `context-corpus/sessions/<session>/turn-NNNN.md` (question,
  answer, decision trace, sources), commits it, and runs `openwiki --update` over that folder.

## Contents

| Path | What it is |
|---|---|
| `BUILD_SPEC.md` | Architecture, setup, implementation plan, acceptance tests, extensions |
| `CLAUDE.md` | Short instructions for Claude Code |
| `docs/openwiki-findings.md` | Measured OpenWiki behaviour, timings, issues and workarounds |
| `backend/` | FastAPI app, agent, OpenWiki process supervision, memory updates, tests |
| `frontend/` | React app, unit tests (`src/**/*.test.tsx`), browser tests (`e2e/`) |
| `scripts/` | `setup.ps1`, `build-semantic.ps1`, `dev.ps1`, `reset-context.ps1` |
| `data/reports/` | 2025 Annual Report (27 pp), Q2 2026 Earnings Supplement (21 pp), 2025 Pillar 3 Disclosures (22 pp) |
| `data/models/` | NII Sensitivity, CECL Allowance and Capital Planning Excel models (live formulas) |
| `data/api_docs/` | Developer Platform API Reference, 18 APIs (Word) |
| `prebuilt/semantic-corpus/` | The finished semantic graph (OpenWiki output + its Markdown sources), restored by `setup.ps1` |
| `semantic-corpus-preview/` | The Markdown corpus produced from `data/` by the converter, for inspection |
| `templates/` | OpenWiki `INSTRUCTIONS.md` briefs for the semantic and context wikis |
| `tools/convert_corpus.py` | PDF / XLSX / DOCX to Markdown converter |
| `generators/` | Scripts that generated the mock data (only needed to regenerate it) |

Generated at runtime and kept out of git: `semantic-corpus/`, `context-corpus/`, `.openwiki-state/`
(OpenWiki settings), `logs/`, `.venv/`, `node_modules/`, `.env`.

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| Semantic tab says the wiki is not built | Run `scripts\build-semantic.ps1`, then restart `dev.ps1`. |
| Memory pill stuck on "syncing" for many minutes | Normal: the first update after a start takes 13-19 min. Check `logs\context-sync-*.log`. |
| Memory pill says "sync failed" | Hover for the reason; the full log is the newest `logs\context-sync-*.log`. The next question or **Sync memory now** retries. |
| "Backend not reachable" banner | The backend is still starting or stopped; check the `dev.ps1` window. |
| Port already in use | Another copy of the app is running; stop it with Ctrl+C. The backend finds the real ports of the graph viewers itself. |

## Tested versions (5 Oct 2026, Windows 11)

Node 24.13.0, npm 11.16.0, Git 2.46.0, Python 3.13.9, OpenWiki 0.7.0. Python packages are pinned in
`backend/requirements.txt` (FastAPI 0.142, LangChain 1.4.3, langchain-anthropic 1.7.5,
langchain-mcp-adapters 0.3.2). Frontend: React 19.3, React Router 8.4, Vite 8.3, TypeScript 6.0,
Vitest 5.0, Playwright 1.63. Models: Claude Sonnet 5.5 (agent, semantic graph), Claude Haiku 4.5
(memory updates).

## Regenerating the mock data (optional)

```powershell
cd generators
pip install reportlab openpyxl matplotlib pypdf
python build_models.py ../data/models      # then recalculate the workbooks in Excel or LibreOffice
python extract_outputs.py                  # reads model outputs used by the reports
python build_annual.py; python build_q2.py; python build_pillar3.py
python api_catalog.py; node build_api_doc.js ../data/api_docs/MHFC_Developer_Platform_API_Reference.docx   # needs: npm install docx
```

## Converting the corpus by hand (optional)

`scripts\build-semantic.ps1` does this for you.

```powershell
.venv\Scripts\python tools/convert_corpus.py --data data --out semantic-corpus
```
