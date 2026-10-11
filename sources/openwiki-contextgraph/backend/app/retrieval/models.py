"""Typed result contracts for the retrieval layer.

These models are the single source of truth for what retrieval returns: the in-process
tools return them directly, and any future MCP facade serializes the same objects as
structured output (outputSchema derives from these). Tools must never return bare strings.
"""

from pydantic import BaseModel, Field

# "2" (gap-fix round): ConfidenceSignals grew `second_pass`; everything in "1" is intact.
SCHEMA_VERSION = "2"


class PageInfo(BaseModel):
    """Identity of one wiki page as the retrieval layer sees it."""

    ref: str  # "openwiki/<folder>/<slug>.md"
    type: str  # frontmatter type (== folder, enforced by tools/validate_corpus.py)
    title: str
    entity_ids: list[str] = Field(default_factory=list)
    status: str | None = None
    tags: list[str] = Field(default_factory=list)


class SearchHit(BaseModel):
    page: PageInfo
    score: float
    matched: str  # "exact_id" | "fuzzy_id" | "exact_alias" | "exact_title" | "bm25" | "graph"
    snippet: str = ""  # best-scoring chunk text (enriched prefix stripped)


class ConfidenceSignals(BaseModel):
    """Intrinsic, query-time signals. Thresholds are corpus-specific and must be fitted
    on the golden set (ratchet R6) — never inherited from another corpus."""

    bm25_top1: float = 0.0
    bm25_margin: float = 0.0  # top1 - top2 at page level
    term_coverage: float = 0.0  # fraction of query tokens present in the corpus vocabulary
    exact_hit: bool = False
    second_pass: bool = False  # FusedRetriever ran the gated graph-anchored second pass


class SearchResult(BaseModel):
    schema_version: str = SCHEMA_VERSION
    query: str
    hits: list[SearchHit] = Field(default_factory=list)
    confidence: ConfidenceSignals = Field(default_factory=ConfidenceSignals)
