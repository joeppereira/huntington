"""Deterministic intent router (gap-fix round): typed queries answered from the graph.

route(query) returns a RoutedResult (a SearchResult; hits matched="graph") when one of the
rules below fires, else None — the caller falls back to FusedRetriever. No model calls,
no body text: everything resolves through frontmatter (ids/titles/aliases) and the typed
WikiGraph (docs/schema-relations.md).

Rules:
  1. ownership — "who owns <X>" / "owner of <X>": resolve X by exact id/title/alias;
     answer = the page followed by its owned_by/owner target page(s).
  2. typed listing — list|enumerate|which ... interfaces|endpoints|systems|teams|
     policies|datasets, optionally faceted by proposed|deprecated|live status;
     answer = graph.find(type=..., status=...), ordered by ref.
  3. supersession — the query contains an id whose page has supersedes/superseded_by;
     answer = both pages, current-first.
"""

import re

from .corpus import Page
from .graph import WikiGraph
from .models import ConfidenceSignals, PageInfo, SearchHit, SearchResult
from .tokenize import id_tokens

_OWNS = re.compile(r"\bwho\s+owns\s+(.+)|\bowner\s+of\s+(.+)", re.I)
_LIST_VERB = re.compile(r"\b(list|enumerate|which)\b", re.I)
_LIST_TYPE = re.compile(r"\b(interfaces?|endpoints?|systems?|teams?|policies|policy|datasets?)\b", re.I)
_LIST_STATUS = re.compile(r"\b(proposed|deprecated|live)\b", re.I)
_TYPE_MAP = {
    "interface": "Interface", "endpoint": "Interface", "system": "System",
    "team": "Team", "policy": "Policy", "dataset": "Dataset",
}


class RoutedResult(SearchResult):
    """SearchResult the eval consumes uniformly, plus which rule produced it."""

    rule: str = ""


class Router:
    def __init__(self, pages: list[Page], graph: WikiGraph):
        self.pages = pages
        self.graph = graph
        self._by_ref = {p.ref: p for p in pages}
        self._by_id = {eid.lower(): p for p in pages for eid in p.entity_ids}
        self._by_title = {p.title.lower(): p for p in pages}
        self._by_alias = {a.lower(): p for p in pages for a in p.aliases if a.strip()}

    # -- helpers --------------------------------------------------------------

    def _resolve(self, phrase: str) -> Page | None:
        """Exact id/title/alias resolution of a query-extracted entity phrase."""
        phrase = phrase.strip().strip("\"'").rstrip("?.!").strip().lower()
        if not phrase:
            return None
        for t in id_tokens(phrase):
            if t in self._by_id:
                return self._by_id[t]
        candidates = [phrase]
        article = re.match(r"(?:the|a|an)\s+(.+)", phrase)
        if article:
            candidates.append(article.group(1))
        for c in candidates:
            page = self._by_title.get(c) or self._by_alias.get(c)
            if page is not None:
                return page
        return None

    def _hit(self, page: Page, snippet: str | None = None) -> SearchHit:
        return SearchHit(
            page=PageInfo(ref=page.ref, type=page.type, title=page.title,
                          entity_ids=page.entity_ids, status=page.status, tags=page.tags),
            score=1.0,
            matched="graph",
            snippet=(snippet if snippet is not None else page.description)[:300],
        )

    def _result(self, query: str, hits: list[SearchHit], rule: str) -> RoutedResult:
        return RoutedResult(
            query=query, hits=hits, rule=rule,
            confidence=ConfidenceSignals(exact_hit=True, term_coverage=1.0),
        )

    # -- rules ----------------------------------------------------------------

    def _route_ownership(self, query: str) -> RoutedResult | None:
        m = _OWNS.search(query)
        if not m:
            return None
        page = self._resolve(m.group(1) or m.group(2))
        if page is None:
            return None
        hits = [self._hit(page)]
        for ref in [*page.owned_by, *page.owner]:
            target = self._by_ref.get(ref)
            if target is not None:
                hits.append(self._hit(target))
        return self._result(query, hits, "ownership")

    def _route_listing(self, query: str) -> RoutedResult | None:
        tm = _LIST_TYPE.search(query)
        vm = _LIST_VERB.search(query)
        if not (vm and tm):
            return None
        sm = _LIST_STATUS.search(query)
        # Precision guard: a bare "which ..." question with no status facet is usually about
        # one entity, not an enumeration — leave it to the fused retriever.
        if vm.group(1).lower() == "which" and not sm:
            return None
        noun = tm.group(1).lower()
        wiki_type = _TYPE_MAP["policy" if noun.startswith("polic") else noun.rstrip("s")]
        found = self.graph.find(type=wiki_type, status=sm.group(1).lower() if sm else None)
        if not found:
            return None
        hits = []
        for node in sorted(found, key=lambda n: n["ref"]):
            page = self._by_ref.get(node["ref"])
            if page is not None:
                hits.append(self._hit(page))
        return self._result(query, hits, "listing")

    def _route_supersession(self, query: str) -> RoutedResult | None:
        for t in id_tokens(query):
            page = self._by_id.get(t)
            if page is None or not (page.supersedes or page.superseded_by):
                continue
            # current-first: a superseded page yields its successor on top.
            pair = ([self._by_ref.get(r) for r in page.superseded_by] + [page]
                    if page.superseded_by
                    else [page] + [self._by_ref.get(r) for r in page.supersedes])
            hits = [self._hit(p) for p in pair if p is not None]
            if len(hits) >= 2:
                return self._result(query, hits, "supersession")
        return None

    # -- api ------------------------------------------------------------------

    def route(self, query: str) -> RoutedResult | None:
        """First matching rule wins; None means no rule fired (caller falls back)."""
        return (
            self._route_ownership(query)
            or self._route_listing(query)
            or self._route_supersession(query)
        )
