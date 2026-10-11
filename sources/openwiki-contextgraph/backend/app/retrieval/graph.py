"""Typed wiki graph (ratchet R4): frontmatter + author-curated cross-links -> NetworkX.

The research verdict (docs/research/retrieval-architecture-2026-10-10.md §3) is to exploit
this hand-curated graph deterministically instead of building an LLM-extracted one:
typed lookups answer "find Interface where ..." directly, and expand() link-expands top
retrieval hits to capture multi-fact aggregation with zero query-time model calls.

Gap-fix round: the typed-relation frontmatter fields (docs/schema-relations.md) become
edges with relation=<field name> alongside the body-link "links_to" edges. A pair of pages
may be related in several ways, so each edge carries a `relations` set; `neighbors()` can
filter on one relation, and `find()` on the normalized status enum.
"""

import networkx as nx

from .corpus import RELATION_FIELDS, Page


class WikiGraph:
    def __init__(self, pages: list[Page]):
        self.g = nx.DiGraph()
        refs = {p.ref for p in pages}

        def add_edge(src: str, dst: str, relation: str):
            if dst not in refs or dst == src:
                return
            if self.g.has_edge(src, dst):
                self.g.edges[src, dst]["relations"].add(relation)
            else:
                self.g.add_edge(src, dst, relations={relation})

        for p in pages:
            self.g.add_node(
                p.ref, type=p.type, title=p.title, entity_ids=p.entity_ids,
                status=p.status, status_norm=p.status_norm, tags=p.tags,
                aliases=p.aliases,
            )
        for p in pages:
            for target in p.links:
                add_edge(p.ref, target, "links_to")
            for rel in RELATION_FIELDS:
                for target in getattr(p, rel):
                    add_edge(p.ref, target, rel)
        self._by_id = {eid: p.ref for p in pages for eid in p.entity_ids}

    def find(self, *, type: str | None = None, entity_id: str | None = None,
             title_contains: str | None = None, status: str | None = None) -> list[dict]:
        """Typed node lookup; every filter is optional and conjunctive. `status` matches
        the normalized enum (status_norm), falling back to the legacy free-text status."""
        if entity_id is not None:
            ref = self._by_id.get(entity_id)
            nodes = [ref] if ref else []
        else:
            nodes = list(self.g.nodes)
        out = []
        for ref in nodes:
            d = self.g.nodes[ref]
            if type is not None and d["type"].lower() != type.lower():
                continue
            if title_contains is not None and title_contains.lower() not in d["title"].lower():
                continue
            if status is not None:
                norm = d.get("status_norm") or str(d.get("status") or "").strip().lower()
                if norm != status.lower():
                    continue
            out.append({"ref": ref, **d})
        return out

    def neighbors(self, ref: str, *, type: str | None = None, direction: str = "both",
                  relation: str | None = None) -> list[dict]:
        """Pages linked from/to ref ('out' = this page cites them, 'in' = they cite it).
        `relation` keeps only edges carrying that relation (e.g. 'owned_by')."""
        if ref not in self.g:
            return []
        seen: list[str] = []
        if direction in ("out", "both"):
            seen += [r for r in self.g.successors(ref)
                     if relation is None or relation in self.g.edges[ref, r]["relations"]]
        if direction in ("in", "both"):
            seen += [r for r in self.g.predecessors(ref)
                     if r not in seen
                     and (relation is None or relation in self.g.edges[r, ref]["relations"])]
        out = []
        for r in seen:
            d = self.g.nodes[r]
            if type is None or d["type"].lower() == type.lower():
                out.append({"ref": r, **d})
        return out

    def expand(self, refs: list[str], *, limit: int = 10) -> list[str]:
        """Deterministic link-expansion of top retrieval hits: 1-hop neighbors ranked by
        how many seed pages link to/from them (multi-fact aggregation, experiment #3)."""
        votes: dict[str, int] = {}
        seeds = set(refs)
        for ref in refs:
            for n in self.neighbors(ref):
                if n["ref"] not in seeds:
                    votes[n["ref"]] = votes.get(n["ref"], 0) + 1
        return sorted(votes, key=lambda r: (-votes[r], r))[:limit]
