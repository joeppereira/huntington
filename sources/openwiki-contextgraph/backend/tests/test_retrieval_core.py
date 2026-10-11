"""Unit tests for the model-free retrieval layer (docs/plan-retrieval-ratchets.md R0-R4)."""

from pathlib import Path

import pytest

from app.retrieval import WikiGraph, WikiRetriever, load_corpus
from app.retrieval.tokenize import id_tokens, tokenize

CORPUS = Path(__file__).resolve().parents[2] / "semantic-corpus-cnb" / "openwiki"

pytestmark = pytest.mark.skipif(not CORPUS.exists(), reason="CNB corpus not present")


@pytest.fixture(scope="module")
def pages():
    return load_corpus(CORPUS)


@pytest.fixture(scope="module")
def retriever(pages):
    return WikiRetriever(pages)


# -- tokenizer ---------------------------------------------------------------

def test_identifier_tokenized_whole_and_parts():
    toks = tokenize("Is EP-PPH-01 deprecated?")
    assert "ep-pph-01" in toks and "pph" in toks and "01" in toks


def test_id_tokens_dotted():
    assert id_tokens("topic pay.wire.lifecycle.v2 here") == ["pay.wire.lifecycle.v2"]


# -- corpus loader -----------------------------------------------------------

def test_corpus_loads_typed_pages(pages):
    assert len(pages) > 100
    by_ref = {p.ref: p for p in pages}
    v1 = by_ref["openwiki/interfaces/pph-v1-wire-status-api.md"]
    assert v1.type == "Interface" and "EP-PPH-01" in v1.entity_ids
    assert all(p.ref.startswith("openwiki/") for p in pages)
    # nav pages excluded
    assert "openwiki/index.md" not in by_ref
    assert not any(p.ref.endswith("/index.md") for p in pages)


def test_chunks_carry_enrichment(pages):
    v1 = next(p for p in pages if p.ref.endswith("pph-v1-wire-status-api.md"))
    assert v1.chunks, "page should produce chunks"
    head = v1.chunks[0].text
    assert "Interface /" in head and "EP-PPH-01" in head


def test_links_resolved_to_refs(pages):
    sys_page = next(p for p in pages if p.ref.endswith("systems/cbo-wire-center.md"))
    assert "openwiki/interfaces/pph-v1-wire-status-api.md" in sys_page.links


# -- exact tier (ratchet R2: the EP-PPH-01 failure class) --------------------

def test_exact_id_short_circuits_to_owning_page(retriever):
    res = retriever.search("Is EP-PPH-01 deprecated and what replaces it?")
    assert res.hits[0].page.ref == "openwiki/interfaces/pph-v1-wire-status-api.md"
    assert res.hits[0].matched == "exact_id"
    assert res.confidence.exact_hit


def test_exact_id_never_returns_the_colliding_page(retriever):
    # Regression for the corruption incident: EP-SPS-01 must hit the SPS page,
    # EP-PPH-01 the deprecated v1 page — never each other.
    sps = retriever.search("what is EP-SPS-01")
    assert sps.hits[0].page.ref == "openwiki/interfaces/sps-read-model-api.md"


def test_pir_vs_cmp_disambiguation(retriever):
    res = retriever.search("What is the status of PIR-2024-07?")
    assert res.hits[0].page.ref == "openwiki/incidents/pir-2024-07.md"


# -- search behavior ---------------------------------------------------------

def test_search_returns_typed_results(retriever):
    res = retriever.search("Who owns the Hold Management Service?")
    assert res.schema_version == "2"  # bumped in the gap-fix round (second_pass signal)
    assert res.hits and all(h.page.type for h in res.hits)
    refs = [h.page.ref for h in res.hits[:5]]
    assert any("hold" in r for r in refs)


def test_confidence_signals_populated(retriever):
    res = retriever.search("wire status tracking")
    c = res.confidence
    assert c.bm25_top1 > 0 and 0 <= c.term_coverage <= 1


def test_gibberish_query_scores_low(retriever):
    res = retriever.search("zzqx flurbl quantum marzipan")
    assert res.confidence.term_coverage < 0.5
    assert not res.confidence.exact_hit


# -- graph (ratchet R4) -------------------------------------------------------

def test_graph_find_by_type_and_id(pages):
    g = WikiGraph(pages)
    hit = g.find(entity_id="SYS-CBO")
    assert len(hit) == 1 and hit[0]["ref"] == "openwiki/systems/cbo-wire-center.md"
    interfaces = g.find(type="Interface")
    assert len(interfaces) >= 10


def test_graph_neighbors_typed(pages):
    g = WikiGraph(pages)
    deps = g.neighbors("openwiki/systems/cbo-wire-center.md", type="Interface")
    assert any(d["ref"].endswith("pph-v1-wire-status-api.md") for d in deps)


def test_graph_expand_votes(pages):
    g = WikiGraph(pages)
    out = g.expand(["openwiki/systems/cbo-wire-center.md"], limit=5)
    assert 0 < len(out) <= 5 and "openwiki/systems/cbo-wire-center.md" not in out


# -- fused default (the shipped arm) ------------------------------------------

def test_fused_retriever_contract_and_exact_tier():
    from app.retrieval.retriever import build_retriever

    r = build_retriever(CORPUS)  # default arm == fused
    res = r.search("Is EP-PPH-01 deprecated and what replaces it?")
    assert res.hits[0].page.ref == "openwiki/interfaces/pph-v1-wire-status-api.md"
    assert res.hits[0].matched == "exact_id" and res.confidence.exact_hit
    assert res.schema_version == "2" and len(res.hits) <= 10
