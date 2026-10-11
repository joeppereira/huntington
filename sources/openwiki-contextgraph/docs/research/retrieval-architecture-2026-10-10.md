# Retrieval architecture research — small typed Markdown corpus

**Date:** 2026-10-10 · **Method:** deep-research harness (5 angles, 22 sources fetched,
107 claims extracted, 25 verified via 3-vote adversarial verification, 23 confirmed /
2 refuted). Re-check landscape if consumed >4 months after this date (see
[[verify-retrieval-choices-per-corpus]] memory policy).

**Question:** retrieval for QA over a 100–500 page typed Markdown wiki (one page per entity:
system/team/person/interface/incident/policy; YAML frontmatter: type, stable entity_id,
status, tags; type folders; dense author-curated cross-links). Constraint: query path must be
model-free or at most a small LOCAL embedding model — LLMs only at index/build time.

## Headline recommendations (first build)

- **Lexical + metadata is the backbone.** Field-boosted BM25 (title, entity_id, type).
  Dense-*alone* loses to BM25 on terminology-dense corpora across 3 independent benchmarks.
- **Include a fused local-dense stream, but gate it behind our own eval.** Fusion added
  +5–8pp Recall@5 in the one in-domain benchmark, but the crossover was never measured below
  ~1.7M tokens — so whether it pays on our ~150 pages is **experiment #1**. RRF as the
  no-tuning fusion default; convex combination (tuned/equal weights) if we tune.
- **Exclude GraphRAG from the first build.** On single-hop fact lookup (our dominant query
  type) plain RAG matches/beats GraphRAG; graph wins only on multi-hop aggregation;
  build+query costs are disqualifying (190M build tokens / 10.6M corpus; up to 331k
  tokens/query — incompatible with model-free serving); published wins were inflated by
  biased LLM-judge protocols (LightRAG 66.7%→39% win rate under unbiased eval).
  **Crucial nuance:** every GraphRAG failure mode is lossy *LLM graph extraction* — which
  does NOT apply to us because our graph is author-curated. Exploit the existing links
  **deterministically** (link-expansion, co-entity injection, NetworkX typed `graph_query`).
- **Enrich at index time; drop query-time generative expansion.** Contextual-retrieval-style
  enrichment (prepend context before BOTH embedding and BM25 indexing) cut retrieval failure
  49%, build-time only. HyDE/query-time generative expansion was a measured *negative* on
  identifier/numeric corpora and violates model-free serving. Confirms chunker-F
  (hierarchy + co-entity). Keep only deterministic offline alias/synonym tables at query time.
- **Exact-ID lookups:** identifier-aware tokenization in BM25 (emit whole hyphenated ID +
  sub-tokens, consistently at index and query time) + a dedicated exact-match entity_id field
  tier that short-circuits ranking on a hit. Dense smears rare ID tokens — this is the
  EP-PPH-01 failure.
- **Confidence gating is purely empirical.** No gating-signal evidence survived verification;
  BM25 scores are not comparable across corpora or boost configs. The gtm_cloud report's
  18/14 bm25max thresholds do NOT transfer. Log top-1 score, top1−top2 margin, coverage,
  stream-agreement per query; fit thresholds on our labeled golden set.

## Four experiments for the golden set (eval/golden_cnb.json, 60 items)

1. Does a fused local-dense stream add measurable recall on ~150 pages? (crossover unmeasured)
2. Which failure signals predict wrong answers here, and what thresholds? (no evidence exists)
3. Can deterministic link-expansion / co-entity injection capture GraphRAG's multi-fact edge
   with zero query-time LLM?
4. How much of the 49% enrichment benefit survives when context is generated *deterministically*
   from frontmatter + heading breadcrumbs rather than by a build-time LLM?

## Refuted (do NOT cite)

- "For KBs under ~1,000 entries BM25 beats dense outright" — refuted 0-3. Cannot justify
  dropping dense on smallness alone.
- "Dense only starts paying beyond ~10³ entries" — refuted 0-3.

## Key sources

- BM25 Wins at Scale (arXiv 2607.26497) · T2-RAGBench financial QA (arXiv 2604.01733) ·
  code-RAG (arXiv 2410.09662) — lexical vs dense.
- RAG vs GraphRAG systematic eval (arXiv 2502.11371) · GraphRAG-Bench (arXiv 2506.05690) ·
  WildGraphBench (arXiv 2602.02053) · unbiased-eval (arXiv 2506.06331) — GraphRAG.
- Anthropic Contextual Retrieval (anthropic.com/engineering/contextual-retrieval) +
  independent reproduction — index-time enrichment.
- Bruch et al. fusion functions (arXiv 2210.11934) — RRF vs convex combination.

Full verified findings + caveats: this run's workflow result (journal.jsonl in the session
subagents dir).
