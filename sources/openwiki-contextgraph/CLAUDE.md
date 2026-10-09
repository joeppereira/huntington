# Instructions for Claude Code

This project is a two-stage proof of concept that tests LangChain's OpenWiki CLI for building and
visualizing (1) a semantic knowledge graph of mock bank documents and (2) a context graph (agent memory)
for a LangChain Q&A agent.

- Follow `BUILD_SPEC.md`. It is the source of truth for architecture, file layout, APIs and milestones.
- The target machine is **Windows**; write PowerShell scripts and test process handling on Windows.
- Use OpenWiki for both graph generation and both visualizations; do not swap in another graph tool.
- The mock data in `data/` is final. Do not regenerate it unless asked (`generators/` can rebuild it).
- `tools/convert_corpus.py` is working; reuse it.
- Re-verify the items listed in BUILD_SPEC.md Section 10 on the installed OpenWiki version before
  relying on them, and record findings in `docs/openwiki-findings.md`.
- Work milestone by milestone (Section 12) and run each one before starting the next.

## Model selection (added 2026-10-09)

- Models for wiki builds and memory syncs are chosen from the ranked list in
  `config/model-selection.json` by `tools/select_model.py --apply` (probes availability on the
  provider in `.env`, prefers the cheap tier — Haiku — when enabled). Don't hardcode model ids.
- `build_history` in that file records which model/provider ran each build **and each later
  `--update`** (append one entry per run). Different runs may legitimately use different models —
  the corpus is plain Markdown and carries no dependency on whichever model wrote it; pick the
  best-available model per run via `tools/select_model.py`.
- When `selected_at` is older than `review_after_days` (4 months) the script exits with code 3:
  **research the current model landscape first** (pricing + quality — web search / claude-api
  skill), update the candidate ranking and `selected_at`, then re-run. Do not just pass
  --allow-stale in normal use.
- Vertex quirk: Claude via `gemini-enterprise` needs `OPENWIKI_MAX_OUTPUT_TOKENS=60000` and the
  `streaming: true` patch in the global openwiki install (large submit_plan calls truncate at the
  16K default, and the Anthropic SDK rejects long non-streaming calls).
