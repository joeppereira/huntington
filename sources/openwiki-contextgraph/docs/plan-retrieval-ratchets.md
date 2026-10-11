# Retrieval build plan — ratchets

**Date:** 2026-10-10. Successor plan to Phase 0 (corpus repair + validation gate, done).
Evidence base: `docs/research/retrieval-architecture-2026-10-10.md` (verified findings) and
the gtm_cloud cascade components (treated as hypotheses, per the verify-per-corpus policy).
Eval data: `eval/golden_cnb.json` (60 items, 10 classes).

## Operating model: ratchets

Every milestone lands with (a) code + unit tests, (b) an eval run on the golden set, and
(c) updated metric **floors** in `eval/ratchet.json`. The ratchet check
(`python eval/ratchet.py check`) fails if any metric drops below its floor; floors only move
up (`update` raises them to current, never lowers). No component is "adopted" until it moves
a metric; no later change may silently regress one. Negative/unanswerable items are excluded
from recall metrics but their confidence signals are logged for R6.

**Metrics** (computed by `eval/run_eval.py`): `ref_hit@1/@5/@10` (any `expected_refs` page in
top-k), `id_coverage@10` (fraction of `expected_entity_ids` present in top-k pages),
per-class breakdowns, plus logged confidence signals per query.

Serving constraint throughout: **model-free query path** (local-embedding tier allowed only
behind a flag, off by default, pending R5's experiment).

## Ratchets

- **R0 — Baseline harness.** `backend/app/retrieval/` package skeleton (typed Pydantic
  results), corpus loader (frontmatter walker over `semantic-corpus-cnb/openwiki/`), naive
  BM25 over raw page text, eval runner + ratchet tooling. Record baseline floors. *This
  milestone's number is the floor everything else must beat.*
- **R1 — Lexical core.** Identifier-aware tokenizer (whole hyphenated ID + sub-tokens, same
  at index and query time); field/metadata boost from frontmatter (title, entity_id, type,
  tags, aliases). Expect the biggest lift here (research: boost was +27pp @1 on gtm corpus).
- **R2 — Exact-ID short-circuit.** Un-analyzed exact-match tier on `entity_id` (and exact
  title): an ID-shaped query token that exactly matches a page's id pins that page to rank 1.
  Kills the EP-PPH-01 class of failure outright (golden G-015/G-027/G-032 regressions).
- **R3 — Index-time deterministic enrichment.** Adapted HierarchicalChunker-F: heading
  breadcrumbs + frontmatter tags (type/status/ids) + co-entity injection from the page's own
  author-curated cross-links. No LLM — this is experiment #4 (how much of contextual
  retrieval's gain is achievable deterministically).
- **R4 — Typed graph + link expansion.** Frontmatter→NetworkX graph (nodes: pages with
  type/ids/status; edges: cross-links). `graph_query` (find by type/id, neighbors) as an
  in-process typed tool, and deterministic link-expansion of top results for multi-fact
  questions — experiment #3 (capture GraphRAG's aggregation edge with zero query-time LLM).
- **R5 — Fusion + optional dense stream.** RRF fusion over rank lists (query variants, and
  an injected local encoder behind `RETRIEVAL_DENSE=1`). Run experiment #1: does fused dense
  add recall on this corpus? Adopt only if the ratchet moves.
- **R6 — Confidence gating.** Log top-1 score, top1−top2 margin, query-term coverage,
  exact-tier hits per golden query; fit escalation thresholds on labeled hit/miss outcomes
  (experiment #2). Unanswerable items must trend low-confidence.
- **R7 — Serve-path switchover** (after R1–R4 hold): wire `WikiRetriever` + `graph_query`
  into the agent as in-process typed tools, retire the OpenWiki MCP hop from the query path
  (OpenWiki remains build-time only). MCP facade deferred until an external client needs it.

**This implementation pass delivers R0–R4** (basic code, tests, eval, floors). R5–R7 follow
once the user reviews the numbers (and possibly on a different model tier per their call).

### R0–R4 outcome (2026-10-10, measured on golden n=56)

| arm | ref_hit@1 | @5 | @10 | id_cov@10 | vocab-gap@10 |
|---|---|---|---|---|---|
| baseline (whole-page BM25) | .554 | .839 | .911 | .443 | 4/5 |
| enriched (chunker-F deterministic) | .500 | .821 | .929 | .463 | 5/5 |
| **fused (equal-weight RRF, shipped default)** | .536 | **.857** | .911 | .437 | 4/5 |
| enriched + 1-hop link-expand | .500 | .821 | .875 | .463 | — |

Decisions (recorded in eval/ratchet.json history): fused is the default (best @5 — the
agent's read window — and near-best @1); floors re-baselined to it explicitly. Weight sweep
showed no dominating config and 1–2-item deltas (noise at n=56) → equal weights, no tuning.
Link-expansion hurts single-answer recall → off by default; the graph serves typed
`graph_query` and multi-fact aggregation instead. Enrichment's measured value here is the
vocab-gap class and tail recall — smaller than the transplanted gtm_cloud numbers implied,
confirming the verify-per-corpus policy.

## Layout

```
backend/app/retrieval/
  __init__.py   models.py    (Pydantic result contracts, SCHEMA_VERSION)
  tokenize.py   (identifier-aware tokenizer)
  corpus.py     (frontmatter walker -> Page + enriched chunks; chunker adapted from
                 gtm_cloud tools/cascade/chunker.py)
  bm25.py       (Okapi BM25, lifted from gtm_cloud tools/cascade/hybrid_retriever.py)
  retriever.py  (exact tier -> BM25 over chunks -> page aggregation -> boost -> RRF hook;
                 confidence signals)
  graph.py      (NetworkX typed graph, graph_query, link expansion)
eval/
  run_eval.py   ratchet.py   ratchet.json   results/   golden_cnb.json  README.md
backend/tests/test_retrieval_core.py  test_retrieval_eval.py
```
