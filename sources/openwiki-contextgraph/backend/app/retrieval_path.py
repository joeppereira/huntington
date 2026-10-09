"""Which semantic-graph nodes the agent used to answer: found by search, opened, cited.

OpenWiki's search does not walk graph edges: it ranks every page section by keyword (SQLite FTS5,
BM25; title x8, heading x6, description x4, identifiers x3, body x1). A node here is one wiki page,
the same node the visualizer draws. Links are the graph's own edges between the nodes the agent
visited, to show where its evidence sits in the graph.
"""

import json
import logging
import threading
import urllib.request
from collections.abc import Iterable, Sequence
from dataclasses import dataclass

from pydantic import BaseModel

from .tracing import TraceStep

logger = logging.getLogger("openwiki_poc")

SEMANTIC_TOOLS = {"semantic_search", "semantic_read"}
WIKI_PREFIX = "openwiki/"


@dataclass(frozen=True)
class GraphIndex:
    nodes: dict[str, tuple[str, str | None]]  # id -> (title, type)
    edges: set[tuple[str, str]]


class RetrievalNode(BaseModel):
    id: str
    title: str
    type: str | None
    sections: list[str]
    found_in_step: int | None  # first search/read that returned it; None if only cited
    best_rank: int | None  # best position in any search result list (1 = top)
    opened: bool
    cited: bool


class RetrievalStep(BaseModel):
    step: int
    tool: str
    input: str
    node_ids: list[str]


class RetrievalLink(BaseModel):
    source: str
    target: str


class RetrievalPath(BaseModel):
    graph_available: bool
    steps: list[RetrievalStep]
    nodes: list[RetrievalNode]
    links: list[RetrievalLink]


def node_id_from_ref(ref: str) -> tuple[str, str | None] | None:
    """`openwiki/metrics/x.md#sec` -> (`metrics/x`, `sec`): the visualizer's node id plus section."""
    page, _, section = ref.partition("#")
    if not page.startswith(WIKI_PREFIX) or not page.endswith(".md"):
        return None
    return page[len(WIKI_PREFIX):-len(".md")], section or None


class _NodeBuilder:
    def __init__(self, node_id: str) -> None:
        self.id = node_id
        self.sections: list[str] = []
        self.found_in_step: int | None = None
        self.best_rank: int | None = None
        self.opened = False
        self.cited = False

    def add_section(self, section: str | None) -> None:
        if section and section not in self.sections:
            self.sections.append(section)

    def build(self, graph: GraphIndex | None) -> RetrievalNode:
        title, node_type = graph.nodes.get(self.id, (self.id, None)) if graph else (self.id, None)
        return RetrievalNode(
            id=self.id, title=title, type=node_type, sections=self.sections, found_in_step=self.found_in_step,
            best_rank=self.best_rank, opened=self.opened, cited=self.cited,
        )


def build_retrieval_path(
    steps: Sequence[TraceStep], cited_refs: Iterable[str], graph: GraphIndex | None
) -> RetrievalPath:
    builders: dict[str, _NodeBuilder] = {}

    def node(node_id: str) -> _NodeBuilder:
        return builders.setdefault(node_id, _NodeBuilder(node_id))

    path_steps: list[RetrievalStep] = []
    for step in steps:
        if step.tool not in SEMANTIC_TOOLS:
            continue
        touched: list[str] = []
        for rank, ref in enumerate(step.refs, start=1):
            parsed = node_id_from_ref(ref)
            if parsed is None:
                continue
            b = node(parsed[0])
            b.add_section(parsed[1])
            if b.found_in_step is None:
                b.found_in_step = step.step
            if step.tool == "semantic_search":
                b.best_rank = rank if b.best_rank is None else min(b.best_rank, rank)
            else:
                b.opened = True
            if b.id not in touched:
                touched.append(b.id)
        path_steps.append(RetrievalStep(step=step.step, tool=step.tool, input=step.input, node_ids=touched))

    for ref in cited_refs:
        parsed = node_id_from_ref(ref)
        # Memory refs share the openwiki/ prefix; only nodes known to the semantic path or graph count.
        if parsed is None or (parsed[0] not in builders and not (graph and parsed[0] in graph.nodes)):
            continue
        b = node(parsed[0])
        b.add_section(parsed[1])
        b.cited = True

    order = list(builders)
    links = [
        RetrievalLink(source=s, target=t)
        for s in order
        for t in order
        if graph and (s, t) in graph.edges
    ]
    return RetrievalPath(
        graph_available=graph is not None,
        steps=path_steps,
        nodes=[builders[i].build(graph) for i in order],
        links=links,
    )


class SemanticGraphCache:
    """Loads the semantic graph once from the visualizer's /api/graph (it does not change at runtime)."""

    def __init__(self, url_getter) -> None:
        self._url_getter = url_getter
        self._graph: GraphIndex | None = None
        self._lock = threading.Lock()

    def get(self, timeout: float = 3.0) -> GraphIndex | None:
        with self._lock:
            if self._graph is not None:
                return self._graph
            url = self._url_getter()
            if not url:
                return None
            try:
                with urllib.request.urlopen(url + "/api/graph", timeout=timeout) as resp:
                    data = json.load(resp)
            except (OSError, ValueError):
                logger.warning("could not load the semantic graph from %s", url, exc_info=True)
                return None
            self._graph = GraphIndex(
                nodes={n["id"]: (n.get("title") or n["id"], n.get("type")) for n in data.get("nodes", [])},
                edges={(e["source"], e["target"]) for e in data.get("edges", [])},
            )
            return self._graph
