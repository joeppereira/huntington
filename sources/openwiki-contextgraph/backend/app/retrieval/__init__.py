"""Model-free retrieval over a typed Markdown wiki corpus.

Plan: docs/plan-retrieval-ratchets.md. Evidence: docs/research/retrieval-architecture-2026-10-10.md.
Query path uses no LLM; an optional local dense encoder can be injected (off by default).
"""

from .models import ConfidenceSignals, PageInfo, SearchHit, SearchResult
from .corpus import Page, load_corpus
from .retriever import FusedRetriever, RoutedRetriever, WikiRetriever, build_retriever
from .graph import WikiGraph
from .router import RoutedResult, Router

__all__ = [
    "ConfidenceSignals",
    "FusedRetriever",
    "Page",
    "PageInfo",
    "RoutedResult",
    "RoutedRetriever",
    "Router",
    "SearchHit",
    "SearchResult",
    "WikiGraph",
    "WikiRetriever",
    "build_retriever",
    "load_corpus",
]
