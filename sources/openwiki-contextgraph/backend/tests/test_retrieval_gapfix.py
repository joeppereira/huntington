"""Unit tests for the gap-fix retrieval round (docs/schema-relations.md): alias exact tier,
title-containment promotion, Document demotion, typed graph edges, the intent router, and
the gated second pass. Synthetic Pages are built inline — nothing here depends on the new
frontmatter fields existing in the on-disk corpus yet."""

import pytest

from app.retrieval import FusedRetriever, Router, WikiGraph, WikiRetriever, load_corpus
from app.retrieval.corpus import Chunk, Page


def mk(ref, type_, title, *, ids=(), aliases=(), tags=(), status=None, status_norm=None,
       body="", description="", **relations) -> Page:
    p = Page(
        ref=ref, type=type_, title=title, entity_ids=list(ids), status=status,
        tags=list(tags), description=description, body=body,
        aliases=list(aliases), status_norm=status_norm, **relations,
    )
    text = f"{type_} / {title}. " + (f"aka: {', '.join(p.aliases)}. " if p.aliases else "") + body
    p.chunks = [Chunk(text=text, body=body or description, heading="")]
    return p


# -- corpus: optional frontmatter fields --------------------------------------

def test_corpus_parses_new_fields_and_defaults(tmp_path):
    wiki = tmp_path / "openwiki"
    (wiki / "interfaces").mkdir(parents=True)
    (wiki / "interfaces" / "new.md").write_text(
        "---\n"
        "type: Interface\n"
        "entity_id: EP-NEW-01\n"
        "title: New Status API\n"
        "description: a new api\n"
        "status: Proposed\n"
        "aliases: [tracking number, where is my money]\n"
        "owned_by: openwiki/teams/payments-core.md\n"
        "supersedes: [openwiki/interfaces/old.md]\n"
        "---\n\n## Overview\n\nBody text about wire status lookups and freshness.\n",
        encoding="utf-8",
    )
    (wiki / "interfaces" / "old.md").write_text(
        "---\ntype: Interface\nentity_id: EP-OLD-01\ntitle: Old API\n"
        "status: deprecated (sunset 2027)\n---\n\nLegacy body long enough to chunk here.\n",
        encoding="utf-8",
    )
    pages = {p.ref: p for p in load_corpus(wiki)}
    new = pages["openwiki/interfaces/new.md"]
    assert new.aliases == ["tracking number", "where is my money"]
    assert new.status_norm == "proposed" and new.status == "Proposed"
    assert new.owned_by == ["openwiki/teams/payments-core.md"]
    assert new.supersedes == ["openwiki/interfaces/old.md"]
    # alias enrichment reaches the indexed chunk text
    assert any("aka: tracking number" in c.text for c in new.chunks)
    old = pages["openwiki/interfaces/old.md"]
    # legacy free-text status does not normalize; all new fields default empty
    assert old.status_norm is None and old.aliases == [] and old.owned_by == []
    # whole-page baseline text carries aliases too
    raw = {p.ref: p for p in load_corpus(wiki, enrich=False)}
    assert "aka: tracking number" in raw["openwiki/interfaces/new.md"].chunks[0].text


# -- alias exact tier + title-containment promotion ---------------------------

@pytest.fixture
def alias_pages():
    return [
        mk("openwiki/concepts/uetr.md", "Concept", "UETR", ids=["UETR"],
           aliases=["tracking number", "parcel tracking"],
           body="Unique end to end transaction reference identifies a wire."),
        mk("openwiki/systems/noise.md", "System", "Noise System",
           body="tracking number tracking number tracking number appears often in this body "
                "about a number for tracking things."),
        mk("openwiki/interfaces/wsl.md", "Interface", "Wire Status Lite", ids=["EP-WSL-01"],
           body="A pilot status interface for wires."),
    ]


def test_alias_phrase_in_query_hits_exact_tier(alias_pages):
    r = WikiRetriever(alias_pages)
    res = r.search("what is the tracking number for my wire payment")
    assert res.hits[0].page.ref == "openwiki/concepts/uetr.md"
    assert res.hits[0].matched == "exact_alias"
    assert res.confidence.exact_hit


def test_alias_hits_rank_after_id_hits(alias_pages):
    r = WikiRetriever(alias_pages)
    res = r.search("does EP-WSL-01 expose the tracking number")
    assert [h.page.ref for h in res.hits[:2]] == [
        "openwiki/interfaces/wsl.md", "openwiki/concepts/uetr.md",
    ]
    assert res.hits[0].matched == "exact_id" and res.hits[1].matched == "exact_alias"


def test_title_containment_promotion(alias_pages):
    r = WikiRetriever(alias_pages)
    res = r.search("history of the wire status lite pilot rollout")
    assert res.hits[0].page.ref == "openwiki/interfaces/wsl.md"
    assert res.hits[0].matched == "exact_title"
    # title-containment is exact-adjacent, not a true exact hit
    assert not res.confidence.exact_hit


def test_single_word_title_not_promoted():
    pages = [
        mk("openwiki/concepts/wire.md", "Concept", "Wire", body="about wires generally here"),
        mk("openwiki/systems/other.md", "System", "Other Thing", body="unrelated body text here"),
    ]
    res = WikiRetriever(pages).search("how does a wire transfer settle")
    assert all(h.matched != "exact_title" for h in res.hits)


# -- document demotion via described_by ---------------------------------------

def test_document_demoted_below_described_entity():
    doc = mk("openwiki/documents/pph-catalog.md", "Document", "PPH API Catalog",
             body="payments hub api catalog payments hub api catalog payments hub api")
    sys_ = mk("openwiki/systems/pph.md", "System", "PRISM Payments Hub",
              described_by=["openwiki/documents/pph-catalog.md"],
              body="the payments hub processes wires")
    res = WikiRetriever([doc, sys_]).search("payments hub api catalog details")
    refs = [h.page.ref for h in res.hits]
    assert refs.index("openwiki/systems/pph.md") < refs.index("openwiki/documents/pph-catalog.md")


def test_document_demotion_never_outranks_exact_hit():
    doc = mk("openwiki/documents/d.md", "Document", "Spec Doc", ids=["DOC-01"],
             body="spec doc body text long enough")
    sys_ = mk("openwiki/systems/s.md", "System", "Some System",
              described_by=["openwiki/documents/d.md"], body="spec doc consumer body")
    res = WikiRetriever([doc, sys_]).search("what is DOC-01")
    assert res.hits[0].page.ref == "openwiki/documents/d.md"
    assert res.hits[0].matched == "exact_id"


# -- typed graph edges ---------------------------------------------------------

@pytest.fixture
def graph_pages():
    team = mk("openwiki/teams/payments-core.md", "Team", "Payments Core",
              body="the team that owns payment systems")
    v1 = mk("openwiki/interfaces/v1.md", "Interface", "Wire API v1", ids=["EP-V1-01"],
            status="deprecated", status_norm="deprecated",
            superseded_by=["openwiki/interfaces/v2.md"],
            owned_by=["openwiki/teams/payments-core.md"],
            body="legacy deprecated wire interface")
    v2 = mk("openwiki/interfaces/v2.md", "Interface", "Wire API v2", ids=["EP-V2-01"],
            status="proposed", status_norm="proposed",
            supersedes=["openwiki/interfaces/v1.md"],
            owned_by=["openwiki/teams/payments-core.md"],
            body="proposed replacement wire interface")
    # v1 also body-links v2: the edge must carry both relations
    v1.links = ["openwiki/interfaces/v2.md"]
    return [team, v1, v2]


def test_typed_edges_and_relation_filter(graph_pages):
    g = WikiGraph(graph_pages)
    owners = g.neighbors("openwiki/interfaces/v1.md", relation="owned_by")
    assert [o["ref"] for o in owners] == ["openwiki/teams/payments-core.md"]
    succ = g.neighbors("openwiki/interfaces/v1.md", relation="superseded_by", direction="out")
    assert [s["ref"] for s in succ] == ["openwiki/interfaces/v2.md"]
    # one edge, several relations (body link + typed field)
    rels = g.g.edges["openwiki/interfaces/v1.md", "openwiki/interfaces/v2.md"]["relations"]
    assert {"links_to", "superseded_by"} <= rels
    # relation filter excludes edges without that relation
    assert g.neighbors("openwiki/interfaces/v1.md", relation="governed_by") == []


def test_depends_on_system_to_system_edges():
    """depends_on (Q1/Q5 gap-fix): a System page carries system->system edges the typed
    graph exposes as a `depends_on`-filtered neighborhood — the dependency set lexical
    search could not assemble."""
    cbo = mk("openwiki/systems/cbo.md", "System", "Wire Center",
             depends_on=["openwiki/systems/pph.md", "openwiki/systems/ces.md"],
             body="the wire center bff consumes PPH and CES")
    pph = mk("openwiki/systems/pph.md", "System", "Payments Hub",
             depends_on=["openwiki/systems/ffc.md"], body="routes to the fedwire connector")
    ces = mk("openwiki/systems/ces.md", "System", "Entitlements", body="entitlement checks")
    ffc = mk("openwiki/systems/ffc.md", "System", "Fedwire Connector", body="fedwire egress")
    g = WikiGraph([cbo, pph, ces, ffc])
    deps = g.neighbors("openwiki/systems/cbo.md", relation="depends_on", direction="out")
    assert sorted(d["ref"] for d in deps) == ["openwiki/systems/ces.md", "openwiki/systems/pph.md"]
    # in-direction answers "what depends on PPH"
    dependents = g.neighbors("openwiki/systems/pph.md", relation="depends_on", direction="in")
    assert [d["ref"] for d in dependents] == ["openwiki/systems/cbo.md"]
    assert g.neighbors("openwiki/systems/pph.md", relation="depends_on", direction="out")[0]["ref"] \
        == "openwiki/systems/ffc.md"


def test_corpus_depends_on_cbo_wire_center_includes_pph():
    """On the real corpus the derived depends_on for the Wire Center must include the PPH
    system (Integration-inventory derivation; EP-PPH-01/02/03 -> SYS-PPH)."""
    from pathlib import Path

    from app.retrieval import load_corpus

    corpus = Path(__file__).resolve().parents[2] / "semantic-corpus-cnb" / "openwiki"
    if not corpus.exists():
        pytest.skip("CNB corpus not present")
    g = WikiGraph(load_corpus(corpus))
    deps = {d["ref"] for d in g.neighbors(
        "openwiki/systems/cbo-wire-center.md", relation="depends_on", direction="out")}
    assert "openwiki/systems/prism-payments-hub.md" in deps
    assert "openwiki/systems/commercial-entitlements-service.md" in deps
    assert "openwiki/systems/enterprise-notification-service.md" in deps
    # and PPH's own derived dependencies include the payment-network connectors
    pph_deps = {d["ref"] for d in g.neighbors(
        "openwiki/systems/prism-payments-hub.md", relation="depends_on", direction="out")}
    assert "openwiki/systems/fedwire-funds-connector.md" in pph_deps


def test_graph_find_status_filter(graph_pages):
    g = WikiGraph(graph_pages)
    proposed = g.find(type="Interface", status="proposed")
    assert [n["ref"] for n in proposed] == ["openwiki/interfaces/v2.md"]
    assert len(g.find(type="Interface")) == 2


# -- router ---------------------------------------------------------------------

@pytest.fixture
def router(graph_pages):
    return Router(graph_pages, WikiGraph(graph_pages))


def test_router_who_owns_by_title_and_id(router):
    res = router.route("who owns the Wire API v2?")
    assert res is not None and res.rule == "ownership"
    assert [h.page.ref for h in res.hits[:2]] == [
        "openwiki/interfaces/v2.md", "openwiki/teams/payments-core.md",
    ]
    assert all(h.matched == "graph" for h in res.hits)
    by_id = router.route("owner of EP-V1-01")
    assert by_id is not None and by_id.hits[1].page.ref == "openwiki/teams/payments-core.md"


def test_router_typed_listing_with_status(router):
    res = router.route("list all proposed interfaces")
    assert res is not None and res.rule == "listing"
    assert [h.page.ref for h in res.hits] == ["openwiki/interfaces/v2.md"]
    all_if = router.route("enumerate the interfaces")
    assert all_if is not None and len(all_if.hits) == 2
    # hits ordered by ref
    assert [h.page.ref for h in all_if.hits] == sorted(h.page.ref for h in all_if.hits)


def test_router_supersession_current_first(router):
    res = router.route("what replaced EP-V1-01 in the estate?")
    assert res is not None and res.rule == "supersession"
    assert [h.page.ref for h in res.hits[:2]] == [
        "openwiki/interfaces/v2.md", "openwiki/interfaces/v1.md",
    ]
    # resolving via the current side orders the same way
    res2 = router.route("does EP-V2-01 supersede anything?")
    assert [h.page.ref for h in res2.hits[:2]] == [
        "openwiki/interfaces/v2.md", "openwiki/interfaces/v1.md",
    ]


def test_router_returns_none_without_a_rule(router):
    assert router.route("tell me about wire cutoff times") is None
    # unresolvable ownership target falls through
    assert router.route("who owns the quantum marzipan service?") is None
    # bare "which" with no status facet is left to the fused retriever
    assert router.route("which systems publish lifecycle events?") is None


def test_router_result_is_searchresult_compatible(router):
    res = router.route("list all proposed interfaces")
    assert res.schema_version == "2" and res.confidence.exact_hit
    assert res.model_dump()["hits"][0]["matched"] == "graph"


# -- gated second pass -----------------------------------------------------------

def _second_pass_corpus():
    team = mk("openwiki/teams/omega.md", "Team", "Omega Guild",
              body="completely unrelated guild charter prose")
    anchor = mk("openwiki/systems/alpha.md", "System", "Alpha Service",
                owned_by=["openwiki/teams/omega.md"],
                body="freshness of parcel route data and freshness of route tracking "
                     "and parcel freshness again")
    fillers = [
        mk(f"openwiki/concepts/f{i}.md", "Concept", f"Filler {i}",
           body=f"parcel notes volume {i} with miscellaneous prose")
        for i in range(24)
    ]
    return [anchor, *fillers, team]  # team last: lowest zero-score rank in both arms


def test_second_pass_fires_and_injects_graph_neighbor():
    pages = _second_pass_corpus()
    r = FusedRetriever(pages, pages, graph=WikiGraph(pages), second_pass_margin=1e9)
    res = r.search("how fresh is the parcel route data", k=15)
    assert res.confidence.second_pass
    refs = [h.page.ref for h in res.hits]
    assert res.hits[0].page.ref == "openwiki/systems/alpha.md"
    assert "openwiki/teams/omega.md" in refs[:10]  # pulled up by the graph pass


def test_second_pass_does_not_fire_without_trigger():
    pages = _second_pass_corpus()
    # margin gate closed (threshold 0) and arms identical (top-5 overlap = 5)
    r = FusedRetriever(pages, pages, graph=WikiGraph(pages), second_pass_margin=0.0)
    res = r.search("how fresh is the parcel route data", k=15)
    assert not res.confidence.second_pass
    assert "openwiki/teams/omega.md" not in [h.page.ref for h in res.hits]


def test_second_pass_suppressed_by_exact_hit():
    pages = [
        mk("openwiki/interfaces/x.md", "Interface", "X API", ids=["EP-X-01"],
           owned_by=["openwiki/teams/omega.md"], body="an api body"),
        mk("openwiki/teams/omega.md", "Team", "Omega Guild", body="guild charter prose"),
    ]
    r = FusedRetriever(pages, pages, graph=WikiGraph(pages), second_pass_margin=1e9)
    res = r.search("what is EP-X-01")
    assert res.hits[0].matched == "exact_id"
    assert not res.confidence.second_pass


def test_second_pass_off_without_graph():
    pages = _second_pass_corpus()
    r = FusedRetriever(pages, pages, second_pass_margin=1e9)  # no graph injected
    res = r.search("how fresh is the parcel route data", k=15)
    assert not res.confidence.second_pass


# -- fuzzy ID tier -------------------------------------------------------------

def test_fuzzy_id_zero_padding_and_edit1():
    from pathlib import Path
    from app.retrieval import WikiRetriever, load_corpus

    corpus = Path(__file__).resolve().parents[2] / "semantic-corpus-cnb" / "openwiki"
    r = WikiRetriever(load_corpus(corpus))
    # zero-padding: EP-PPH-1 -> EP-PPH-01 (deprecated v1 page)
    res = r.search("what is EP-PPH-1")
    assert res.hits[0].page.ref.endswith("pph-v1-wire-status-api.md")
    assert res.hits[0].matched == "fuzzy_id"
    # single-typo: EP-PHH-01 -> EP-PPH-01 (unique edit-1 candidate)
    res2 = r.search("is EP-PHH-01 deprecated?")
    assert res2.hits[0].page.ref.endswith("pph-v1-wire-status-api.md")
    # gibberish ID with no near candidate: no fuzzy pin
    res3 = r.search("what is ZZ-QQQ-99")
    assert not res3.hits or res3.hits[0].matched not in ("exact_id", "fuzzy_id")


def test_fuzzy_id_budget_scales_with_length():
    from app.retrieval.retriever import _edit_budget, _edit_within

    assert _edit_budget("EP-X") == 1 and _edit_budget("EP-PPH-01") == 2
    assert _edit_budget("CNB-MEMO-2026-09") == 3
    # two typos resolve for a long id, not for a short one
    assert _edit_within("cnb-memo-2026-09", "cnb-mem0-2026-9", 3)
    assert not _edit_within("ep-x", "eq-y", 1)


def test_fuzzy_id_two_typos_long_id_resolves():
    from pathlib import Path
    from app.retrieval import WikiRetriever, load_corpus

    corpus = Path(__file__).resolve().parents[2] / "semantic-corpus-cnb" / "openwiki"
    r = WikiRetriever(load_corpus(corpus))
    res = r.search("what changed in CNB-MEM0-2026-9?")  # 0-for-O typo + dropped zero
    assert res.hits and res.hits[0].matched == "fuzzy_id"
    assert "cnb-memo-2026-09" in res.hits[0].page.ref


def test_moving_pattern_id_match_separator_variants():
    from pathlib import Path
    from app.retrieval import WikiRetriever, load_corpus

    corpus = Path(__file__).resolve().parents[2] / "semantic-corpus-cnb" / "openwiki"
    r = WikiRetriever(load_corpus(corpus))
    # spaces instead of hyphens: tokenizer never produces the id token
    res = r.search("tell me about EP PPH 01")
    assert res.hits and res.hits[0].matched == "fuzzy_id"
    assert res.hits[0].page.ref.endswith("pph-v1-wire-status-api.md")
    # missing hyphen entirely
    res2 = r.search("what is EPPPH-01?")
    assert res2.hits and res2.hits[0].page.ref.endswith("pph-v1-wire-status-api.md")
    # plain prose with no id-like content must not fuzzy-pin anything
    res3 = r.search("who approves wire releases")
    assert not res3.hits or res3.hits[0].matched not in ("fuzzy_id",)


def test_moving_pattern_tolerates_head_errors():
    from pathlib import Path
    from app.retrieval import WikiRetriever, load_corpus

    corpus = Path(__file__).resolve().parents[2] / "semantic-corpus-cnb" / "openwiki"
    r = WikiRetriever(load_corpus(corpus))
    # transposed head: PE-PPH-01 -> EP-PPH-01 (no anchor requirement)
    res = r.search("status of PE-PPH-01 please")
    assert res.hits and res.hits[0].page.ref.endswith("pph-v1-wire-status-api.md")


def test_whole_token_fuzzy_tie_means_no_pin():
    from pathlib import Path
    from app.retrieval import WikiRetriever, load_corpus

    corpus = Path(__file__).resolve().parents[2] / "semantic-corpus-cnb" / "openwiki"
    r = WikiRetriever(load_corpus(corpus))
    # GTSI-0117 is edit-distance 1 from GTSI-0107, GTSI-0112 and GTSI-0115 (different
    # pages): ambiguous intent -> the fuzzy tier must NOT pin any of them (golden G-069).
    res = r.search("what is the status of GTSI-0117?")
    assert not res.hits or res.hits[0].matched != "fuzzy_id"
