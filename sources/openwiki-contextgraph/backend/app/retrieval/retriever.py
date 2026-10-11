"""WikiRetriever: exact tier -> BM25 over enriched chunks -> page aggregation -> boost.

Pipeline per query (all deterministic, no model calls):
  1. Exact tier: an identifier token in the query that exactly matches a page's entity_id
     (or the full query matching a title) pins that page to rank 1 (research §5: short-circuit).
     Gap-fix round: an alias phrase contained in the query pins its page too (after id/title
     hits), and a full page title (>=2 words) contained in the query gets exact-tier-adjacent
     promotion (matched="exact_title").
  2. BM25 over chunks with identifier-aware tokens; page score = max of its chunk scores.
  3. Field boost: additive bump for query-token overlap with the page's title/ids/tags/type/
     aliases (the gtm_cloud "+title/metadata boost" — their single biggest measured lift;
     re-verified here by the ratchet eval, not assumed).
  4. RRF hook: extra rank lists (query variants, optional injected local dense encoder) fuse
     via reciprocal rank fusion. Default is lexical-only.
  5. Document demotion: a type-Document page never outranks an entity page that lists it in
     described_by (swap-style, applied after fusion within the top pool).

FusedRetriever adds a gated second pass (graph-anchored, frontmatter-only re-rank of the
1-hop neighborhood of the round-1 top-3) that fires only on low-confidence round-1 results.

Confidence signals are returned with every result and logged by the eval runner; thresholds
are fitted on the golden set (ratchet R6), never inherited from another corpus.
"""

import re

from .bm25 import BM25
from .corpus import Page, load_corpus
from .graph import WikiGraph
from .models import ConfidenceSignals, PageInfo, SearchHit, SearchResult
from .tokenize import id_tokens, tokenize

RRF_K0 = 60
REGISTRY_ID_LIMIT = 6  # pages with more ids than this are registries: boost, never pin
_EXACT_KINDS = {"exact_id", "fuzzy_id", "exact_alias", "exact_title"}


def _page_info(p: Page) -> PageInfo:
    return PageInfo(
        ref=p.ref, type=p.type, title=p.title, entity_ids=p.entity_ids,
        status=p.status, tags=p.tags,
    )


def _phrase_in(phrase: str, query_lc: str) -> bool:
    """Full-phrase containment on word boundaries (both sides already lowercased)."""
    return re.search(rf"(?<![a-z0-9]){re.escape(phrase)}(?![a-z0-9])", query_lc) is not None


def _norm_id(eid: str) -> str:
    """Lowercase an identifier and strip leading zeros from its numeric segments
    ("EP-PPH-01" -> "ep-pph-1") so zero-padding differences still resolve."""
    return re.sub(r"(?<![0-9])0+([0-9])", r"\1", eid.lower())


def _edit_budget(token: str) -> int:
    """Length-scaled edit tolerance for ID intent-matching: the longer the id, the more
    typos can still mean the same id. Short codes stay strict (one wrong char in 'EP-X'
    is a different id; one wrong char in 'CNB-MEMO-2026-09' is a typo)."""
    n = len(token)
    return 1 if n < 8 else 2 if n < 14 else 3


def _edit_within(a: str, b: str, k: int) -> bool:
    """True if Damerau-Levenshtein(a, b) <= k (adjacent transposition counts as ONE
    error — the most common human typo). Banded DP with early exit."""
    la, lb = len(a), len(b)
    if abs(la - lb) > k:
        return False
    if la > lb:
        a, b, la, lb = b, a, lb, la
    prev2: list[int] | None = None
    prev = list(range(lb + 1))
    for i in range(1, la + 1):
        cur = [i] + [0] * lb
        row_min = i
        for j in range(1, lb + 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] != b[j - 1]))
            if (prev2 is not None and i > 1 and j > 1
                    and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]):
                cur[j] = min(cur[j], prev2[j - 2] + 1)
            row_min = min(row_min, cur[j])
        if row_min > k:
            return False
        prev2, prev = prev, cur
    return prev[lb] <= k


def _demote_documents(order: list, page_of, *, start: int = 0, window: int = 20) -> list:
    """Swap-style Document demotion within the top pool: if a type-Document page ranks above
    a non-document page that lists it in described_by, swap them (entity above document).
    `order` is any ranked list; `page_of(item) -> Page`. Pinned exact hits (< start) are
    never touched."""
    order = list(order)
    end = min(len(order), start + window)
    for i in range(start, end):
        p = page_of(order[i])
        if p is None or p.type.lower() != "document":
            continue
        for j in range(i + 1, end):
            q = page_of(order[j])
            if q is not None and q.type.lower() != "document" and p.ref in q.described_by:
                order[i], order[j] = order[j], order[i]
                break
    return order


class WikiRetriever:
    def __init__(self, pages: list[Page], *, encoder=None):
        """pages: from load_corpus(). encoder: optional local .encode(list[str])->ndarray
        (normalized); None keeps the query path fully model-free."""
        self.pages = pages
        self.chunk_page: list[int] = []  # chunk index -> page index
        chunk_tokens: list[list[str]] = []
        for pi, p in enumerate(pages):
            for c in p.chunks:
                chunk_tokens.append(tokenize(c.text))
                self.chunk_page.append(pi)
        self._bm25 = BM25(chunk_tokens)
        self._by_id = {eid.lower(): pi for pi, p in enumerate(pages) for eid in p.entity_ids}
        # Fuzzy ID resolution map: numeric segments normalized (leading zeros stripped),
        # so "EP-PPH-1" resolves to EP-PPH-01. Only used when the exact lookup misses.
        self._by_id_norm = {_norm_id(eid): pi for eid, pi in self._by_id.items()}
        # Moving-pattern ID index (DNA-trie design: patterns match at any offset of the
        # separator-normalized stream). CODE ids only — must contain a digit and be >=6
        # normalized chars. Word-like ids (slugs, TEAM-EA) are excluded: sliding fuzz
        # over prose matches ordinary words ("team at" ~ "teamea"), which is a name-tier
        # job (aliases/titles), not an id-intent job (eval-measured false pins).
        self._moving_ids = [
            (re.sub(r"[^a-z0-9]", "", eid), pi)
            for eid, pi in self._by_id.items()
            if len(re.sub(r"[^a-z0-9]", "", eid)) >= 6 and re.search(r"[0-9]", eid)
        ]
        # Titles are matched with any trailing parenthetical stripped — "PRISM Payments
        # Hub (SYS-PPH)" must match a query saying "PRISM Payments Hub".
        bare = [re.sub(r"\s*\([^)]*\)\s*$", "", p.title).lower() for p in pages]
        self._by_title = {t: pi for pi, t in enumerate(bare)}
        self._by_title.update({p.title.lower(): pi for pi, p in enumerate(pages)})
        # alias -> page, longest alias first so the most specific phrase wins containment
        self._aliases = sorted(
            ((a.lower(), pi) for pi, p in enumerate(pages) for a in p.aliases if a.strip()),
            key=lambda t: (-len(t[0]), t[0]),
        )
        # (page, lowercased >=2-word bare title) for title-containment promotion, longest first
        self._multi_titles = sorted(
            ((pi, t) for pi, t in enumerate(bare) if len(t.split()) >= 2),
            key=lambda t: (-len(t[1]), t[1]),
        )
        self._field_terms = [
            set(tokenize(" ".join([p.title, p.type, *p.entity_ids, *p.tags, *p.aliases])))
            for p in pages
        ]
        self.encoder = encoder
        self._C = None
        if encoder is not None:
            self._C = encoder.encode([c.text for p in pages for c in p.chunks])

    # -- scoring ------------------------------------------------------------

    def _page_scores(self, q_tokens: list[str]) -> tuple[list[float], list[int]]:
        """Max-aggregate chunk BM25 to pages; also return each page's best chunk index."""
        scores = self._bm25.get_scores(q_tokens)
        page_score = [0.0] * len(self.pages)
        best_chunk = [-1] * len(self.pages)
        for ci, s in enumerate(scores):
            pi = self.chunk_page[ci]
            if s > page_score[pi]:
                page_score[pi] = s
                best_chunk[pi] = ci
        return page_score, best_chunk

    def _exact(self, query: str) -> list[tuple[int, str]]:
        """Exact-tier candidates as (page index, matched kind), ids/title before aliases."""
        hits: list[tuple[int, str]] = []
        seen: set[int] = set()

        def add(pi: int | None, kind: str):
            if pi is not None and pi not in seen:
                hits.append((pi, kind))
                seen.add(pi)

        saw_id_token = False
        for t in id_tokens(query):
            saw_id_token = True
            pi = self._by_id.get(t)
            kind = "exact_id"
            if pi is None:
                # Fuzzy ID tier (deterministic, ID-shaped tokens only): zero-padding
                # normalization first, then the UNIQUE minimum-Damerau-distance code id
                # within the token's length-scaled budget. No positional anchor — errors
                # may sit anywhere in the id, including its head ("PE-PPH-01" ->
                # EP-PPH-01). The WHOLE token is compared (the user typed a complete
                # id; its boundaries carry intent). Distance ties -> no match.
                pi = self._by_id_norm.get(_norm_id(t))
                if pi is None:
                    tn = re.sub(r"[^a-z0-9]", "", t)
                    k = _edit_budget(tn)
                    best_d, best_pi, tie = k + 1, None, False
                    for nid, p in self._moving_ids:
                        # band must INCLUDE best_d, or the tie branch below is dead
                        # code and equal-distance candidates silently lose to index
                        # order (caught by golden G-069).
                        for d in range(0, min(k, best_d) + 1):
                            if _edit_within(nid, tn, d):
                                if d < best_d:
                                    best_d, best_pi, tie = d, p, False
                                elif d == best_d and p != best_pi:
                                    tie = True
                                break
                    pi = best_pi if (best_pi is not None and not tie) else None
                kind = "fuzzy_id"
            # Registry rule: on a many-id page, only the PRIMARY (first) id is specific
            # enough to pin; a secondary id among dozens ranks via BM25/boost instead.
            if pi is not None and len(self.pages[pi].entity_ids) > REGISTRY_ID_LIMIT \
                    and t != self.pages[pi].entity_ids[0].lower():
                continue
            add(pi, kind)
        if not hits and not saw_id_token:
            # Moving-pattern tier (DNA-trie design): slide each normalized id over the
            # separator-stripped query stream, so "EP PPH 01" or an id embedded in a
            # slug still resolves when tokenization yields no ID token at all. Unique
            # best match only. (When an ID token exists, the whole-token comparison
            # above already carries the intent; free windows would slice it.)
            pi = self._moving_id_match(query)
            add(pi, "fuzzy_id")
        ql = query.strip().lower()
        add(self._by_title.get(ql), "exact_id")
        for alias, pi in self._aliases:
            if _phrase_in(alias, ql):
                add(pi, "exact_alias")
        return hits

    def _moving_id_match(self, query: str) -> int | None:
        """Best unique page whose normalized id matches ANY offset of the normalized
        query within its length-scaled edit budget. True moving-pattern semantics: no
        anchor — errors are tolerated anywhere in the id, including its head. Distance
        ties across different pages -> None (ambiguous: id intent not verifiable)."""
        qn = re.sub(r"[^a-z0-9]", "", query.lower())
        if len(qn) < 6:
            return None
        best: tuple[int, int] | None = None  # (distance, page) of the single best match
        ambiguous = False
        for nid, pi in self._moving_ids:
            k = _edit_budget(nid)
            d_id = None
            w_lo, w_hi = max(1, len(nid) - k), len(nid) + k
            for start in range(0, len(qn) - w_lo + 1):
                for w in range(w_lo, min(w_hi, len(qn) - start) + 1):
                    window = qn[start:start + w]
                    for d in range(0, (d_id if d_id is not None else k + 1)):
                        if _edit_within(nid, window, d):
                            d_id = d
                            break
                if d_id == 0:
                    break
            if d_id is None:
                continue
            if best is None or d_id < best[0]:
                best, ambiguous = (d_id, pi), False
            elif d_id == best[0] and pi != best[1]:
                ambiguous = True
        if best is None or ambiguous:
            return None
        pi = best[1]
        if len(self.pages[pi].entity_ids) > REGISTRY_ID_LIMIT:
            return None
        return pi

    def _title_promos(self, query: str, exclude: set[int]) -> list[int]:
        """Pages whose full (>=2-word) title is contained in the query: exact-tier-adjacent
        promotion — after true exact hits, before BM25 order."""
        ql = query.lower()
        return [pi for pi, tl in self._multi_titles if pi not in exclude and tl in ql]

    @staticmethod
    def _rrf(rank_lists: list[list[int]]) -> dict[int, float]:
        fused: dict[int, float] = {}
        for rl in rank_lists:
            for rank, pi in enumerate(rl):
                fused[pi] = fused.get(pi, 0.0) + 1.0 / (RRF_K0 + rank)
        return fused

    def _dense_rank(self, query: str) -> list[int] | None:
        if self.encoder is None or self._C is None:
            return None
        import numpy as np

        qv = self.encoder.encode([query])[0]
        order = np.argsort(-(self._C @ qv))
        page_rank: list[int] = []
        for ci in order:
            pi = self.chunk_page[int(ci)]
            if pi not in page_rank:
                page_rank.append(pi)
        return page_rank

    # -- api ----------------------------------------------------------------

    def search(self, query: str, k: int = 10, *, variants: list[str] | None = None) -> SearchResult:
        q_tokens = tokenize(query)
        page_score, best_chunk = self._page_scores(q_tokens)
        bm25_rank = sorted(range(len(self.pages)), key=lambda pi: -page_score[pi])

        rank_lists = [bm25_rank]
        for v in variants or []:
            vs, _ = self._page_scores(tokenize(v))
            rank_lists.append(sorted(range(len(self.pages)), key=lambda pi: -vs[pi]))
        dr = self._dense_rank(query)
        if dr is not None:
            rank_lists.append(dr)
        fused = self._rrf(rank_lists)

        qt = set(q_tokens)
        for pi in list(fused):
            overlap = len(qt & self._field_terms[pi])
            if overlap >= 2:
                fused[pi] += 0.5 / RRF_K0  # ~one extra top-rank vote (gtm_cloud boost)

        exact = self._exact(query)
        kind = dict(exact)
        promos = self._title_promos(query, exclude=set(kind))
        kind.update({pi: "exact_title" for pi in promos})
        pinned = [pi for pi, _ in exact] + promos
        order = pinned + [pi for pi in sorted(fused, key=lambda pi: -fused[pi]) if pi not in kind]
        order = _demote_documents(order, lambda pi: self.pages[pi], start=len(pinned))

        hits: list[SearchHit] = []
        all_chunks = [c for p in self.pages for c in p.chunks]
        for pi in order[:k]:
            if not pinned and page_score[pi] <= 0 and fused.get(pi, 0.0) <= 0:
                break
            ci = best_chunk[pi]
            hits.append(
                SearchHit(
                    page=_page_info(self.pages[pi]),
                    score=round(fused.get(pi, 0.0), 6),
                    matched=kind.get(pi, "bm25"),
                    snippet=(all_chunks[ci].body[:300] if ci >= 0 else self.pages[pi].description[:300]),
                )
            )

        top = sorted(page_score, reverse=True)[:2]
        covered = sum(1 for t in qt if t in self._bm25.vocab)
        return SearchResult(
            query=query,
            hits=hits,
            confidence=ConfidenceSignals(
                bm25_top1=round(top[0], 4) if top else 0.0,
                bm25_margin=round(top[0] - top[1], 4) if len(top) > 1 else 0.0,
                term_coverage=round(covered / len(qt), 4) if qt else 0.0,
                exact_hit=any(kd != "exact_title" for kd in kind.values()),
            ),
        )


class FusedRetriever:
    """RRF fusion of the whole-page and enriched-chunk arms (eval-measured on the CNB
    golden set: whole-page wins @1/@5 precision, enriched wins tail recall and the
    hard-vocab-gap class; fusion takes the best @5 of all arms). Same SearchResult
    contract as WikiRetriever.

    Gap-fix round: optional gated second pass. When round 1 produced no exact-tier hit AND
    looks low-confidence — bm25_margin below `second_pass_margin` (stand-in for the 25th
    percentile of the margin's own distribution, to be re-fitted from eval logs) OR the two
    arms' top-5 overlap <= 2 — the 1-hop typed-graph neighborhood of the round-1 top-3 is
    re-ranked on frontmatter terms only (ids/titles/tags — never body) and RRF-fused into
    the pool at weight 0.5. Requires an injected WikiGraph; without one the pass is off."""

    def __init__(self, pages_raw: list[Page], pages_enriched: list[Page], *, encoder=None,
                 graph: WikiGraph | None = None, second_pass_margin: float = 0.5):
        self.base = WikiRetriever(pages_raw, encoder=None)
        self.enriched = WikiRetriever(pages_enriched, encoder=encoder)
        self.graph = graph
        self.second_pass_margin = second_pass_margin
        self._page_by_ref = {p.ref: p for p in pages_raw}

    def _second_pass_rank(self, query: str, top_refs: list[str]) -> list[str]:
        """Frontmatter-only re-rank of the 1-hop graph neighborhood of the round-1 top-3."""
        anchor_terms: set[str] = set()
        for ref in top_refs:
            p = self._page_by_ref.get(ref)
            if p is not None:
                anchor_terms |= set(tokenize(" ".join([p.title, *p.entity_ids, *p.tags])))
        seeds = set(top_refs)
        neigh: list[str] = []
        for ref in top_refs:
            for n in self.graph.neighbors(ref):
                if n["ref"] not in seeds and n["ref"] not in neigh:
                    neigh.append(n["ref"])
        qt = set(tokenize(query))

        def key(ref: str):
            p = self._page_by_ref.get(ref)
            terms = set() if p is None else set(
                tokenize(" ".join([p.title, p.type, *p.entity_ids, *p.tags, *p.aliases]))
            )
            return (-len(terms & qt), -len(terms & anchor_terms), ref)

        return sorted(neigh, key=key)

    def search(self, query: str, k: int = 10, *, variants: list[str] | None = None) -> SearchResult:
        pool = max(2 * k, 20)
        ra = self.base.search(query, k=pool, variants=variants)
        rb = self.enriched.search(query, k=pool, variants=variants)

        # Exact-tier pins: enriched arm's order first, then any the base arm adds.
        kind: dict[str, str] = {}
        for res in (rb, ra):
            for h in res.hits:
                if h.matched in _EXACT_KINDS and h.page.ref not in kind:
                    kind[h.page.ref] = h.matched
        pinned = [r for r in kind if kind[r] != "exact_title"] + \
                 [r for r in kind if kind[r] == "exact_title"]
        exact = [r for r in pinned if kind[r] != "exact_title"]

        fused: dict[str, float] = {}
        for res in (ra, rb):
            for rank, h in enumerate(res.hits):
                fused[h.page.ref] = fused.get(h.page.ref, 0.0) + 1.0 / (RRF_K0 + rank)

        strong = ra.confidence if ra.confidence.bm25_top1 >= rb.confidence.bm25_top1 else rb.confidence
        overlap5 = len({h.page.ref for h in ra.hits[:5]} & {h.page.ref for h in rb.hits[:5]})
        second_pass = (
            self.graph is not None
            and not exact
            and (strong.bm25_margin < self.second_pass_margin or overlap5 <= 2)
        )

        def ordered() -> list[str]:
            o = pinned + [r for r in sorted(fused, key=lambda r: -fused[r]) if r not in kind]
            return _demote_documents(o, self._page_by_ref.get, start=len(pinned), window=pool)

        order = ordered()
        injected: set[str] = set()
        if second_pass:
            for rank, ref in enumerate(self._second_pass_rank(query, order[:3])):
                if ref not in fused:
                    injected.add(ref)
                fused[ref] = fused.get(ref, 0.0) + 0.5 / (RRF_K0 + rank)
            order = ordered()

        by_ref: dict[str, SearchHit] = {}
        for h in [*rb.hits, *ra.hits]:  # prefer the enriched arm's snippet
            by_ref.setdefault(h.page.ref, h)
        hits: list[SearchHit] = []
        for r in order[:k]:
            h = by_ref.get(r)
            page = h.page if h is not None else _page_info(self._page_by_ref[r])
            snippet = h.snippet if h is not None else self._page_by_ref[r].description[:300]
            hits.append(
                SearchHit(page=page, score=round(fused.get(r, 0.0), 6),
                          matched=kind.get(r, "graph" if r in injected else "bm25"),
                          snippet=snippet)
            )
        return SearchResult(
            query=query,
            hits=hits,
            confidence=ConfidenceSignals(
                bm25_top1=strong.bm25_top1,
                bm25_margin=strong.bm25_margin,
                term_coverage=ra.confidence.term_coverage,  # raw-text vocab: purer signal
                exact_hit=bool(exact),
                second_pass=second_pass,
            ),
        )


class RoutedRetriever:
    """Deterministic intent router fused WITH FusedRetriever: the router's graph-derived
    list is one more RRF voice, never a pre-emptor. Eval-measured rationale: replacing the
    lexical answer with the routed list cost @5 .857->.768 (router misfires bury good hits),
    while fusing keeps the router's wins (ownership/governed_by: rank 5-6 -> 2) without the
    losses. Candidate default arm — adopted only when the ratchet moves."""

    ROUTER_WEIGHT = 1.5  # router hits are high-precision when the rule fires

    def __init__(self, router, fused: FusedRetriever):
        self.router = router
        self.fused = fused

    def search(self, query: str, k: int = 10, *, variants: list[str] | None = None) -> SearchResult:
        base = self.fused.search(query, k=max(2 * k, 20), variants=variants)
        routed = self.router.route(query)
        if routed is None:
            base.hits = base.hits[:k]
            return base

        fused_score: dict[str, float] = {}
        by_ref: dict[str, SearchHit] = {}
        for rank, h in enumerate(base.hits):
            fused_score[h.page.ref] = fused_score.get(h.page.ref, 0.0) + 1.0 / (RRF_K0 + rank)
            by_ref.setdefault(h.page.ref, h)
        for rank, h in enumerate(routed.hits):
            fused_score[h.page.ref] = (
                fused_score.get(h.page.ref, 0.0) + self.ROUTER_WEIGHT / (RRF_K0 + rank)
            )
            by_ref.setdefault(h.page.ref, h)
        # true exact hits (id/alias) stay pinned ahead of the blend
        pinned = [h.page.ref for h in base.hits if h.matched in ("exact_id", "exact_alias")]
        order = pinned + [r for r in sorted(fused_score, key=lambda r: -fused_score[r]) if r not in pinned]

        base.hits = [
            SearchHit(page=by_ref[r].page, score=round(fused_score.get(r, 0.0), 6),
                      matched=by_ref[r].matched, snippet=by_ref[r].snippet)
            for r in order[:k]
        ]
        return base


def build_retriever(openwiki_dir, *, arm: str = "fused", encoder=None):
    """arm: 'fused' (default) | 'enriched' | 'baseline' | 'routed' — see eval/ratchet.json
    history. 'routed' = intent router first, fused fallback with the graph-gated second
    pass enabled (candidate default pending eval)."""
    if arm == "fused":
        return FusedRetriever(
            load_corpus(openwiki_dir, enrich=False),
            load_corpus(openwiki_dir, enrich=True),
            encoder=encoder,
        )
    if arm == "routed":
        from .router import Router

        raw = load_corpus(openwiki_dir, enrich=False)
        enriched = load_corpus(openwiki_dir, enrich=True)
        graph = WikiGraph(enriched)
        fused = FusedRetriever(raw, enriched, encoder=encoder, graph=graph)
        return RoutedRetriever(Router(enriched, graph), fused)
    return WikiRetriever(load_corpus(openwiki_dir, enrich=arm == "enriched"), encoder=encoder)
