"""In-process semantic tools (ratchet R7): the agent's query path to the knowledge wiki.

Replaces the OpenWiki MCP stdio hop for `semantic_search`/`semantic_read` with the
model-free retrieval layer (app/retrieval: FusedRetriever + WikiGraph), and adds the
typed graph tools (`graph_query`, `graph_neighbors`) that lexical retrieval measured
poorly on — inventory/aggregation and relationship questions.

The toolkit is built once at startup (lifespan) and reused across requests. Every call
is stateless and deterministic: the same query always returns the same results, which
structurally removes the MCP repeated-search decay bug. OpenWiki MCP remains in use for
build-time and the memory (context) wiki only — see app/mcp_tools.py.

Refs keep the "openwiki/<folder>/<slug>.md" shape the tracing layer expects; search and
graph outputs are the typed Pydantic contracts from app/retrieval/models.py serialized
as compact JSON.
"""

import json
import re
from pathlib import Path
from typing import Literal

from langchain_core.tools import BaseTool, StructuredTool
from pydantic import BaseModel, Field

from .retrieval import FusedRetriever, SearchHit, WikiGraph, load_corpus
from .retrieval.corpus import RELATION_FIELDS, STATUS_ENUM, _HEADING

GRAPH_HITS_LIMIT = 50  # graph_query can match the whole corpus; cap what the model sees
RELATIONS = (*RELATION_FIELDS, "links_to")


def _dumps(data: dict) -> str:
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False)


def _slug(heading: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-")


def _hit(h: SearchHit) -> dict:
    return {
        "ref": h.page.ref,
        "type": h.page.type,
        "title": h.page.title,
        "entity_ids": h.page.entity_ids,
        "status": h.page.status,
        "score": h.score,
        "matched": h.matched,
        "snippet": h.snippet,
    }


def _node(n: dict) -> dict:
    return {
        "ref": n["ref"],
        "type": n["type"],
        "title": n["title"],
        "entity_ids": n["entity_ids"],
        "status": n["status"],
        "tags": n["tags"],
    }


def _sections(body: str) -> list[dict]:
    """Split a page body into [{"heading", "content"}] blocks on #/##/### headings."""
    sections: list[dict] = []
    heading = ""
    buf: list[str] = []

    def flush() -> None:
        content = "\n".join(buf).strip()
        if content or heading:
            sections.append({"heading": heading, "content": content})

    for line in body.split("\n"):
        m = _HEADING.match(line)
        if m:
            flush()
            heading, buf = m.group(2).strip(), []
        else:
            buf.append(line)
    flush()
    return sections


class SearchArgs(BaseModel):
    query: str = Field(min_length=1, max_length=2000, description="What to look for, in plain words.")
    limit: int = Field(default=8, ge=1, le=20, description="Maximum number of ranked results.")


class ReadArgs(BaseModel):
    ref: str = Field(
        min_length=1, max_length=1000,
        description='Page ref from a search or graph result, e.g. "openwiki/interfaces/pph-v1-wire-status-api.md".',
    )
    heading: str | None = Field(
        default=None, max_length=300,
        description="Optional section heading (as shown in snippets or a previous read) to read just that section.",
    )


class GraphQueryArgs(BaseModel):
    type: str | None = Field(default=None, description='Page type, e.g. "System", "Interface", "Team", "Decision".')
    entity_id: str | None = Field(default=None, description='Exact entity id, e.g. "EP-PPH-01".')
    title_contains: str | None = Field(default=None, description="Case-insensitive substring of the page title.")
    status: str | None = Field(
        default=None, description=f"Lifecycle status, one of: {', '.join(sorted(STATUS_ENUM))}."
    )


class GraphNeighborsArgs(BaseModel):
    ref: str = Field(min_length=1, max_length=1000, description='Page ref, e.g. "openwiki/systems/prism-payments-hub.md".')
    relation: str | None = Field(default=None, description=f"Keep only edges with this relation: {', '.join(RELATIONS)}.")
    type: str | None = Field(default=None, description="Keep only neighbors of this page type.")
    direction: Literal["out", "in", "both"] = Field(
        default="both", description='"out" = pages this page cites, "in" = pages citing it.'
    )


class SemanticToolkit:
    """Model-free retrieval over the semantic wiki, shared across requests.

    Holds the corpus (raw + enriched), the typed graph and the fused retriever in
    memory; all tool calls are pure reads of that state.
    """

    def __init__(self, openwiki_dir: str | Path) -> None:
        raw = load_corpus(openwiki_dir, enrich=False)
        enriched = load_corpus(openwiki_dir, enrich=True)
        self.graph = WikiGraph(enriched)
        # arm="fused" with the graph injected: the gated graph-anchored second pass is on.
        self.retriever = FusedRetriever(raw, enriched, graph=self.graph)
        self._pages = {p.ref: p for p in raw}

    async def search(self, query: str, limit: int = 8) -> str:
        result = self.retriever.search(query, k=limit)
        return _dumps({
            "query": result.query,
            "hits": [_hit(h) for h in result.hits],
            "confidence": result.confidence.model_dump(),
        })

    async def read(self, ref: str, heading: str | None = None) -> str:
        page = self._pages.get(ref.strip())
        if page is None:
            return f"Error: unknown page ref {ref!r}; use a ref returned by semantic_search or graph_query"
        sections = _sections(page.body)
        if heading:
            want = _slug(heading)
            kept = [s for s in sections if _slug(s["heading"]) == want]
            if not kept:
                known = ", ".join(s["heading"] for s in sections if s["heading"])
                return f"Error: unknown heading {heading!r} on {ref}; available: {known}"
            sections = kept
        return _dumps({
            "ref": page.ref,
            "type": page.type,
            "title": page.title,
            "entity_ids": page.entity_ids,
            "status": page.status,
            "tags": page.tags,
            "description": page.description,
            "sections": sections,
        })

    async def graph_query(
        self,
        type: str | None = None,
        entity_id: str | None = None,
        title_contains: str | None = None,
        status: str | None = None,
    ) -> str:
        nodes = self.graph.find(type=type, entity_id=entity_id, title_contains=title_contains, status=status)
        return _dumps({"count": len(nodes), "hits": [_node(n) for n in nodes[:GRAPH_HITS_LIMIT]]})

    async def graph_neighbors(
        self,
        ref: str,
        relation: str | None = None,
        type: str | None = None,
        direction: Literal["out", "in", "both"] = "both",
    ) -> str:
        ref = ref.strip()
        if ref not in self.graph.g:
            return f"Error: unknown page ref {ref!r}; use a ref returned by semantic_search or graph_query"
        nodes = self.graph.neighbors(ref, type=type, direction=direction, relation=relation)
        return _dumps({"ref": ref, "count": len(nodes), "hits": [_node(n) for n in nodes[:GRAPH_HITS_LIMIT]]})

    def as_langchain_tools(self) -> list[BaseTool]:
        return [
            StructuredTool.from_function(
                coroutine=self.search,
                name="semantic_search",
                description="Search the knowledge wiki (systems, interfaces, teams, policies, decisions, incidents, "
                "datasets). Returns ranked pages as JSON hits carrying explicit type, status and entity_ids, with a "
                "snippet and refs like openwiki/interfaces/pph-v1-wire-status-api.md, plus retrieval-confidence "
                "signals. Deterministic: repeating a query returns the same results, so vary the wording instead.",
                args_schema=SearchArgs,
            ),
            StructuredTool.from_function(
                coroutine=self.read,
                name="semantic_read",
                description="Read a knowledge-wiki page by ref — the whole page, or one section via `heading`. "
                "Returns the page's frontmatter summary (type, title, entity_ids, status, tags, description) "
                "and the section contents.",
                args_schema=ReadArgs,
            ),
            StructuredTool.from_function(
                coroutine=self.graph_query,
                name="graph_query",
                description="Typed lookup over the wiki graph: filter pages by type, exact entity_id, title "
                "substring and/or lifecycle status. Use this (not search) for inventory and aggregation questions "
                "like 'list all deprecated Interfaces' or 'which Systems are proposed'.",
                args_schema=GraphQueryArgs,
            ),
            StructuredTool.from_function(
                coroutine=self.graph_neighbors,
                name="graph_neighbors",
                description="Pages linked to/from a wiki page, with optional relation filter "
                f"({', '.join(RELATIONS)}), neighbor type and direction. Use for relationship questions: "
                "who owns X, what is X part of, what supersedes X, what depends on X.",
                args_schema=GraphNeighborsArgs,
            ),
        ]
