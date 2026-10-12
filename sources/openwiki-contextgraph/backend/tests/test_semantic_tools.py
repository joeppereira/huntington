"""Ratchet R7: in-process semantic tools (app/semantic_tools.py).

Unit tests run on a tiny on-disk corpus; the golden smoke tests run on the real CNB
corpus (skipped when it is not present) and assert the expected page lands in the
tool layer's top-5 for three golden regression questions — no LLM anywhere.
"""

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app
from app.semantic_tools import SemanticToolkit

CNB_CORPUS = Path(__file__).resolve().parents[2] / "semantic-corpus-cnb" / "openwiki"
GOLDEN = Path(__file__).resolve().parents[2] / "eval" / "golden_cnb.json"


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


@pytest.fixture(scope="module")
def toolkit(tmp_path_factory) -> SemanticToolkit:
    wiki = tmp_path_factory.mktemp("corpus") / "openwiki"
    _write(wiki / "interfaces" / "old-api.md", (
        "---\n"
        "type: Interface\n"
        "entity_id: EP-OLD-01\n"
        "title: Old Status API (deprecated)\n"
        "description: The legacy wire status lookup API, sunset 2027.\n"
        "status: deprecated\n"
        "tags: [wire-status, rest-api]\n"
        "owned_by: [openwiki/teams/core.md]\n"
        "part_of: openwiki/systems/hub.md\n"
        "superseded_by: [openwiki/interfaces/new-api.md]\n"
        "---\n\n"
        "## Overview\n\nLegacy synchronous wire status lookups, rate limited and deprecated.\n\n"
        "## Endpoint inventory\n\nGET /v1/wires/status is the only endpoint, sunset 2027-03-31.\n"
    ))
    _write(wiki / "interfaces" / "new-api.md", (
        "---\n"
        "type: Interface\n"
        "entity_id: EP-NEW-01\n"
        "title: New Payments API\n"
        "description: The replacement payments API.\n"
        "status: live\n"
        "owned_by: [openwiki/teams/core.md]\n"
        "part_of: openwiki/systems/hub.md\n"
        "supersedes: [openwiki/interfaces/old-api.md]\n"
        "---\n\n## Overview\n\nEvent-driven payments API with a wire status read model.\n"
    ))
    _write(wiki / "systems" / "hub.md", (
        "---\ntype: System\nentity_id: SYS-HUB\ntitle: Payments Hub\n"
        "description: The payments hub system of record.\nstatus: live\n"
        "depends_on: [openwiki/systems/connector.md]\n---\n\n"
        "## Overview\n\nThe hub processes wires, exposes the status APIs, and routes to the connector.\n"
    ))
    _write(wiki / "systems" / "connector.md", (
        "---\ntype: System\nentity_id: SYS-CONN\ntitle: Network Connector\n"
        "description: The network egress connector.\nstatus: live\n---\n\n"
        "## Overview\n\nSends wires to the network and publishes acknowledgments.\n"
    ))
    _write(wiki / "teams" / "core.md", (
        "---\ntype: Team\nentity_id: TEAM-CORE\ntitle: Core Payments Engineering\n"
        "description: Owns the payments hub and its APIs.\n---\n\n"
        "## Charter\n\nBuilds and runs the hub and both status APIs.\n"
    ))
    return SemanticToolkit(wiki)


# -- semantic_search ----------------------------------------------------------

async def test_search_json_contract(toolkit: SemanticToolkit):
    out = json.loads(await toolkit.search("Is EP-OLD-01 deprecated and what replaces it?"))
    assert set(out) == {"query", "hits", "confidence"}
    assert out["hits"], "expected hits"
    top = out["hits"][0]
    assert set(top) == {"ref", "type", "title", "entity_ids", "status", "score", "matched", "snippet"}
    assert top["ref"] == "openwiki/interfaces/old-api.md"  # exact-id pin, ref keeps the openwiki/ shape
    assert top["matched"] == "exact_id"
    assert top["type"] == "Interface" and top["status"] == "deprecated" and top["entity_ids"] == ["EP-OLD-01"]
    conf = out["confidence"]
    assert {"bm25_top1", "bm25_margin", "term_coverage", "exact_hit", "second_pass"} <= set(conf)
    assert conf["exact_hit"] is True


async def test_search_respects_limit_and_every_ref_is_wiki_shaped(toolkit: SemanticToolkit):
    out = json.loads(await toolkit.search("wire status api", limit=2))
    assert len(out["hits"]) <= 2
    assert all(h["ref"].startswith("openwiki/") and h["ref"].endswith(".md") for h in out["hits"])


async def test_repeated_search_is_stateless_and_identical(toolkit: SemanticToolkit):
    """Regression for the MCP repeated-search decay bug: identical query, identical results."""
    first = await toolkit.search("wire status lookups")
    for _ in range(4):
        assert await toolkit.search("wire status lookups") == first


# -- semantic_read ------------------------------------------------------------

async def test_read_whole_page_with_frontmatter_summary(toolkit: SemanticToolkit):
    out = json.loads(await toolkit.read("openwiki/interfaces/old-api.md"))
    assert out["ref"] == "openwiki/interfaces/old-api.md"
    assert out["type"] == "Interface" and out["status"] == "deprecated"
    assert out["entity_ids"] == ["EP-OLD-01"] and out["tags"] == ["wire-status", "rest-api"]
    assert out["description"].startswith("The legacy")
    assert [s["heading"] for s in out["sections"]] == ["Overview", "Endpoint inventory"]
    assert "sunset 2027-03-31" in out["sections"][1]["content"]


async def test_read_one_section_by_heading_text_or_slug(toolkit: SemanticToolkit):
    by_text = json.loads(await toolkit.read("openwiki/interfaces/old-api.md", heading="Endpoint inventory"))
    assert [s["heading"] for s in by_text["sections"]] == ["Endpoint inventory"]
    by_slug = json.loads(await toolkit.read("openwiki/interfaces/old-api.md", heading="endpoint-inventory"))
    assert by_slug["sections"] == by_text["sections"]


async def test_read_errors_name_the_problem(toolkit: SemanticToolkit):
    assert (await toolkit.read("openwiki/interfaces/nope.md")).startswith("Error: unknown page ref")
    out = await toolkit.read("openwiki/interfaces/old-api.md", heading="Nope")
    assert out.startswith("Error: unknown heading") and "Overview" in out


# -- graph_query / graph_neighbors ---------------------------------------------

async def test_graph_query_by_type_status_id_title(toolkit: SemanticToolkit):
    by_type = json.loads(await toolkit.graph_query(type="Interface"))
    assert by_type["count"] == 2
    assert {h["ref"] for h in by_type["hits"]} == {
        "openwiki/interfaces/old-api.md", "openwiki/interfaces/new-api.md"}
    assert all(set(h) == {"ref", "type", "title", "entity_ids", "status", "tags"} for h in by_type["hits"])

    deprecated = json.loads(await toolkit.graph_query(type="Interface", status="deprecated"))
    assert [h["ref"] for h in deprecated["hits"]] == ["openwiki/interfaces/old-api.md"]

    by_id = json.loads(await toolkit.graph_query(entity_id="EP-NEW-01"))
    assert [h["ref"] for h in by_id["hits"]] == ["openwiki/interfaces/new-api.md"]

    by_title = json.loads(await toolkit.graph_query(title_contains="hub"))
    assert [h["ref"] for h in by_title["hits"]] == ["openwiki/systems/hub.md"]


async def test_graph_neighbors_relation_type_direction(toolkit: SemanticToolkit):
    superseded = json.loads(await toolkit.graph_neighbors(
        "openwiki/interfaces/old-api.md", relation="superseded_by", direction="out"))
    assert [h["ref"] for h in superseded["hits"]] == ["openwiki/interfaces/new-api.md"]

    owners = json.loads(await toolkit.graph_neighbors("openwiki/interfaces/old-api.md", relation="owned_by"))
    assert [h["ref"] for h in owners["hits"]] == ["openwiki/teams/core.md"]

    parts = json.loads(await toolkit.graph_neighbors(
        "openwiki/systems/hub.md", relation="part_of", direction="in", type="Interface"))
    assert {h["ref"] for h in parts["hits"]} == {
        "openwiki/interfaces/old-api.md", "openwiki/interfaces/new-api.md"}

    assert (await toolkit.graph_neighbors("openwiki/nope.md")).startswith("Error: unknown page ref")


async def test_graph_neighbors_depends_on_returns_typed_hits(toolkit: SemanticToolkit):
    """depends_on dependency routing (Q1/Q5): graph_neighbors(relation="depends_on")
    returns the dependency set as typed System hits, both directions."""
    out = json.loads(await toolkit.graph_neighbors(
        "openwiki/systems/hub.md", relation="depends_on", direction="out"))
    assert [h["ref"] for h in out["hits"]] == ["openwiki/systems/connector.md"]
    h = out["hits"][0]
    assert h["type"] == "System" and h["entity_ids"] == ["SYS-CONN"]
    assert set(h) == {"ref", "type", "title", "entity_ids", "status", "tags"}
    # in-direction answers "what depends on the connector"
    rev = json.loads(await toolkit.graph_neighbors(
        "openwiki/systems/connector.md", relation="depends_on", direction="in"))
    assert [h["ref"] for h in rev["hits"]] == ["openwiki/systems/hub.md"]
    # depends_on is advertised on the graph_neighbors tool's relation list
    tools = {t.name: t for t in toolkit.as_langchain_tools()}
    assert "depends_on" in tools["graph_neighbors"].description


# -- LangChain tool surface and agent wiring ------------------------------------

async def test_langchain_tools_expose_the_semantic_tools(toolkit: SemanticToolkit):
    tools = {t.name: t for t in toolkit.as_langchain_tools()}
    assert set(tools) == {"semantic_search", "semantic_read", "graph_query", "graph_neighbors", "graph_dependencies"}
    out = json.loads(await tools["semantic_search"].ainvoke({"query": "EP-OLD-01"}))
    assert out["hits"][0]["ref"] == "openwiki/interfaces/old-api.md"
    out = json.loads(await tools["graph_neighbors"].ainvoke(
        {"ref": "openwiki/interfaces/old-api.md", "relation": "superseded_by"}))
    assert out["hits"]


def test_app_wires_in_process_semantic_tools_and_mcp_memory_tools(settings: Settings):
    """The agent gets the in-process semantic tools (ratchet R7) and keeps MCP memory tools."""
    captured: dict[str, list] = {}

    class _NullAgent:
        model_id = "null"

        async def ask(self, question, history, documents=()):  # pragma: no cover - never called
            raise AssertionError

    def spy_factory(_settings, tools):
        captured["tools"] = list(tools)
        return _NullAgent()

    with TestClient(create_app(settings, agent_factory=spy_factory)):
        pass
    by_name = {t.name: t for t in captured["tools"]}
    assert set(by_name) == {
        "semantic_search", "semantic_read", "graph_query", "graph_neighbors", "graph_dependencies",
        "memory_search", "memory_read",
    }
    # The semantic pair must be the in-process toolkit, not the MCP wrappers.
    for name in ("semantic_search", "semantic_read", "graph_query", "graph_neighbors", "graph_dependencies"):
        assert isinstance(by_name[name].coroutine.__self__, SemanticToolkit)
    from app.mcp_tools import OpenWikiTools

    for name in ("memory_search", "memory_read"):
        assert isinstance(by_name[name].coroutine.__self__, OpenWikiTools)


# -- golden smoke (CNB corpus, tool layer only — no LLM) ------------------------

SMOKE_IDS = ("G-009", "G-015", "G-032")


@pytest.fixture(scope="module")
def cnb_toolkit() -> SemanticToolkit:
    if not CNB_CORPUS.exists():
        pytest.skip("CNB corpus not present")
    return SemanticToolkit(CNB_CORPUS)


@pytest.fixture(scope="module")
def golden_items() -> dict[str, dict]:
    if not GOLDEN.exists():
        pytest.skip("golden set not present")
    data = json.loads(GOLDEN.read_text(encoding="utf-8"))
    items = data if isinstance(data, list) else data.get("items", [])
    return {item["id"]: item for item in items if item.get("id") in SMOKE_IDS}


@pytest.mark.parametrize("golden_id", SMOKE_IDS)
async def test_golden_smoke_expected_page_in_top5(cnb_toolkit, golden_items, golden_id):
    item = golden_items[golden_id]
    out = json.loads(await cnb_toolkit.search(item["question"], limit=5))
    top5 = [h["ref"] for h in out["hits"]]
    assert set(top5) & set(item["expected_refs"]), (
        f"{golden_id}: none of {item['expected_refs']} in top-5 {top5}")


CNB_CORPUS = Path(__file__).resolve().parents[2] / "semantic-corpus-cnb" / "openwiki"


@pytest.mark.skipif(not CNB_CORPUS.exists(), reason="CNB corpus absent")
async def test_graph_dependencies_one_call_closure():
    tk = SemanticToolkit(CNB_CORPUS)
    out = json.loads(await tk.graph_dependencies("openwiki/systems/cbo-wire-center.md", depth=2))
    refs = {d["ref"].split("/")[-1] for d in out["dependencies"]}
    # 2-hop closure reaches the systems lexical retrieval could not: PPH's own deps.
    assert {"prism-payments-hub.md", "hold-management-service.md", "swift-gpi-connector.md"} <= refs
    gpi = next(d for d in out["dependencies"] if d["ref"].endswith("swift-gpi-connector.md"))
    assert any("GTSI" in o for o in gpi["owner"])  # ownership correction, pre-joined in one call
