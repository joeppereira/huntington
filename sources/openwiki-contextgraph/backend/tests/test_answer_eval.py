"""Deterministic tests for the answer verifier + gap-fill (backend/app/answer_verify.py).

These run in CI with NO LLM call: synthetic answers + a stub graph exercise present / data_used /
contradicts_graph and the gap-fill append + re-verify. The live-agent eval (eval/answer_eval.py)
is covered by a separate test guarded by the `live` marker and RUN_LIVE.
"""

import os
import sys
from pathlib import Path

import pytest

from app.answer_verify import (
    CORRECTIONS_HEADING,
    RequiredFact,
    check_fact,
    fill_gaps,
    score_checks,
    verify_run,
)

# eval/ holds answer_keys.py (the real detectors) — add it so we can test the gpi contradiction logic.
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "eval"))
import answer_keys  # noqa: E402

GPI_REF = "openwiki/systems/swift-gpi-connector.md"


class StubGraph:
    """Minimal WikiGraph stand-in: the gpi connector is owned by GTSI (the ground truth)."""

    def neighbors(self, ref, *, relation=None, direction="out", type=None):
        if ref == GPI_REF and relation == "owned_by":
            return [{"title": "Global Transaction Services Integration (GTSI)"}]
        return []


# --- synthetic facts -----------------------------------------------------------------------------

def _plain_fact() -> RequiredFact:
    return RequiredFact(
        id="F-PLAIN",
        desc="systems depend on PPH",
        present_detect=lambda t: "pph" in t,
        authority_refs=("openwiki/systems/prism-payments-hub.md",),
        source_ref="openwiki/systems/prism-payments-hub.md",
        fill="PPH is a dependency.",
        graph_tools=("graph_dependencies",),
    )


def _gpi_fact() -> RequiredFact:
    return answer_keys._gpi_owner_fact("F-GPI")


GRAPH = StubGraph()


# --- present / data_used / contradicts -----------------------------------------------------------

def test_present_and_data_used_via_citation():
    f = _plain_fact()
    c = check_fact(f, "the hub is PPH", pages_read=[], tools_used=[],
                   citation_refs=["openwiki/systems/prism-payments-hub.md#Overview"], graph=GRAPH)
    assert c.present and c.data_used and not c.contradicts_graph and c.verified_good


def test_data_used_via_graph_tool_when_no_page_cited():
    f = _plain_fact()
    c = check_fact(f, "depends on PPH", pages_read=[], citation_refs=[],
                   tools_used=["graph_dependencies"], graph=GRAPH)
    assert c.data_used and c.verified_good


def test_present_but_not_data_used_is_not_verified_good():
    f = _plain_fact()
    c = check_fact(f, "depends on PPH", pages_read=[], citation_refs=[], tools_used=["semantic_search"],
                   graph=GRAPH)
    assert c.present and not c.data_used and not c.verified_good


def test_absent_fact():
    f = _plain_fact()
    c = check_fact(f, "an unrelated answer", pages_read=[], citation_refs=[], tools_used=[], graph=GRAPH)
    assert not c.present and not c.verified_good


def test_contradiction_is_distinct_from_absence():
    """A stale 'gpi owned by Raj Malhotra' claim must flag contradicts_graph, not just absence."""
    f = _gpi_fact()
    stale = "gpi data comes from Payment Networks Engineering (Raj Malhotra)."
    c = check_fact(f, stale, pages_read=[GPI_REF], citation_refs=[], tools_used=["graph_neighbors"],
                   graph=GRAPH)
    assert c.contradicts_graph is True
    assert c.present is False  # GTSI not named
    assert c.verified_good is False


def test_correct_gpi_answer_not_flagged():
    f = _gpi_fact()
    good = "The gpi connector moved from PNE (Raj Malhotra) to GTSI on 2026-10-01; GTSI owns it now."
    c = check_fact(f, good, pages_read=[GPI_REF], citation_refs=[], tools_used=["graph_neighbors"],
                   graph=GRAPH)
    assert c.present and not c.contradicts_graph and c.verified_good


def test_graph_value_is_derived_from_graph():
    assert answer_keys.gpi_owner_value(GRAPH) == {"Global Transaction Services Integration (GTSI)"}


# --- gap-fill append + re-verify -----------------------------------------------------------------

def test_gap_fill_appends_section_and_fixes_coverage_for_missing_fact():
    facts = [_plain_fact()]
    answer = "an answer that forgot the hub"
    pre = verify_run(facts, answer, pages_read=[], citation_refs=[], tools_used=["graph_dependencies"],
                     graph=GRAPH)
    assert not pre[0].present
    corrected, corrections = fill_gaps(facts, pre, answer, GRAPH)
    assert CORRECTIONS_HEADING in corrected
    assert "PPH is a dependency." in corrected
    assert corrections[0].reason == "missing" and corrections[0].source.endswith("prism-payments-hub.md")
    filled = frozenset(c.fact_id for c in corrections)
    post = verify_run(facts, corrected, pages_read=[], citation_refs=[], tools_used=["graph_dependencies"],
                      graph=GRAPH, filled_ids=filled)
    assert post[0].present and post[0].data_used and post[0].verified_good and post[0].filled


def test_gap_fill_resolves_a_contradiction():
    facts = [_gpi_fact()]
    stale = "gpi is owned by Payment Networks Engineering (Raj Malhotra)."
    pre = verify_run(facts, stale, pages_read=[GPI_REF], citation_refs=[], tools_used=[], graph=GRAPH)
    assert pre[0].contradicts_graph and not pre[0].verified_good
    corrected, corrections = fill_gaps(facts, pre, stale, GRAPH)
    assert corrections[0].reason == "contradicts_graph"
    assert "GTSI" in corrected and "[CONTRADICTED GRAPH]" in corrected
    filled = frozenset(c.fact_id for c in corrections)
    post = verify_run(facts, corrected, pages_read=[GPI_REF], citation_refs=[], tools_used=[],
                      graph=GRAPH, filled_ids=filled)
    assert post[0].present and not post[0].contradicts_graph and post[0].verified_good


def test_gap_fill_noop_when_all_good():
    facts = [_plain_fact()]
    answer = "depends on PPH"
    pre = verify_run(facts, answer, pages_read=[], citation_refs=[], tools_used=["graph_dependencies"],
                     graph=GRAPH)
    corrected, corrections = fill_gaps(facts, pre, answer, GRAPH)
    assert corrections == [] and corrected == answer


def test_score_checks_coverage_math():
    facts = [_plain_fact(), _gpi_fact()]
    # one present+good, one missing
    answer = "only mentions pph"
    pre = verify_run(facts, answer, pages_read=["openwiki/systems/prism-payments-hub.md", GPI_REF],
                     citation_refs=[], tools_used=[], graph=GRAPH)
    corrected, corrections = fill_gaps(facts, pre, answer, GRAPH)
    filled = frozenset(c.fact_id for c in corrections)
    post = verify_run(facts, corrected, pages_read=["openwiki/systems/prism-payments-hub.md", GPI_REF],
                      citation_refs=[], tools_used=[], graph=GRAPH, filled_ids=filled)
    s_pre = score_checks(pre, pre)
    s_post = score_checks(pre, post)
    assert s_pre.coverage_pre == 0.5
    assert s_post.coverage_post == 1.0  # gap-fill brings graph-backed coverage to 100%


# --- live agent eval (skipped in CI) -------------------------------------------------------------

@pytest.mark.live
@pytest.mark.skipif(os.environ.get("RUN_LIVE") != "1", reason="set RUN_LIVE=1 to call the live agent")
def test_live_answer_eval_single_question():
    import asyncio

    import answer_eval  # eval/answer_eval.py
    from app.config import Settings
    from app.main import default_agent_factory
    from app.semantic_tools import SemanticToolkit

    settings = Settings()
    toolkit = SemanticToolkit(settings.semantic_corpus_path / "openwiki")
    agent = default_agent_factory(settings, toolkit.as_langchain_tools())
    concept = (ROOT / "eval" / "demo_concept.txt").read_text()
    facts = answer_keys.q1_facts()
    summary = asyncio.run(answer_eval.run_question(
        agent, toolkit.graph, "Q1", answer_keys.QUESTIONS["Q1"]["question"], facts, concept, runs=1))
    assert summary["run_success_pct"] == 1.0
    assert summary["coverage_post_mean"] >= summary["coverage_pre_mean"]
