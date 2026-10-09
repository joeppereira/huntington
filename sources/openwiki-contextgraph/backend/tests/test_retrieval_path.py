from app.retrieval_path import GraphIndex, build_retrieval_path, node_id_from_ref
from app.tracing import TraceStep

GRAPH = GraphIndex(
    nodes={
        "metrics/cet1-ratio": ("CET1 Ratio", "FinancialMetric"),
        "concepts/stress-capital-buffer": ("Stress Capital Buffer", "RiskConcept"),
        "reports/annual-report-2025": ("2025 Annual Report", "Report"),
        "overview": ("Meridian Harbor overview", "overview"),
    },
    edges={
        ("metrics/cet1-ratio", "concepts/stress-capital-buffer"),
        ("reports/annual-report-2025", "metrics/cet1-ratio"),
        ("overview", "reports/annual-report-2025"),
    },
)

STEPS = (
    TraceStep(1, "memory_search", '"CET1"', "1 hit", 3, ("openwiki/turns/t1.md#a",)),
    TraceStep(2, "semantic_search", '"CET1 requirement"', "3 hits", 40, (
        "openwiki/metrics/cet1-ratio.md#requirement-stack",
        "openwiki/concepts/stress-capital-buffer.md#definition",
        "openwiki/metrics/cet1-ratio.md#reported-values",
    )),
    TraceStep(3, "semantic_read", "openwiki/metrics/cet1-ratio.md [requirement-stack]", "1 section", 20, (
        "openwiki/metrics/cet1-ratio.md#requirement-stack",
    )),
    TraceStep(4, "semantic_search", '"annual report capital"', "1 hit", 30, (
        "openwiki/reports/annual-report-2025.md#capital-pp-13-14",
    )),
)


def test_node_id_from_ref():
    assert node_id_from_ref("openwiki/metrics/cet1-ratio.md#stack") == ("metrics/cet1-ratio", "stack")
    assert node_id_from_ref("openwiki/overview.md") == ("overview", None)
    assert node_id_from_ref("not-a-wiki-ref") is None


def test_nodes_in_order_of_first_discovery_with_roles():
    path = build_retrieval_path(STEPS, ["openwiki/metrics/cet1-ratio.md#requirement-stack"], GRAPH)
    assert [n.id for n in path.nodes] == [
        "metrics/cet1-ratio", "concepts/stress-capital-buffer", "reports/annual-report-2025",
    ]
    cet1, scb, report = path.nodes
    assert (cet1.title, cet1.type, cet1.found_in_step, cet1.best_rank) == ("CET1 Ratio", "FinancialMetric", 2, 1)
    assert cet1.sections == ["requirement-stack", "reported-values"]
    assert (cet1.opened, cet1.cited) == (True, True)
    assert (scb.best_rank, scb.opened, scb.cited) == (2, False, False)
    assert (report.found_in_step, report.best_rank) == (4, 1)


def test_memory_tools_are_left_out():
    path = build_retrieval_path(STEPS, ["openwiki/turns/t1.md#a"], GRAPH)
    assert "turns/t1" not in [n.id for n in path.nodes]
    assert [s.step for s in path.steps] == [2, 3, 4]


def test_steps_name_the_nodes_they_touched():
    path = build_retrieval_path(STEPS, [], GRAPH)
    search, read, _ = path.steps
    assert (search.tool, search.input, search.node_ids) == (
        "semantic_search", '"CET1 requirement"', ["metrics/cet1-ratio", "concepts/stress-capital-buffer"],
    )
    assert (read.tool, read.node_ids) == ("semantic_read", ["metrics/cet1-ratio"])


def test_links_are_graph_edges_between_visited_nodes_only():
    path = build_retrieval_path(STEPS, [], GRAPH)
    assert [(l.source, l.target) for l in path.links] == [
        ("metrics/cet1-ratio", "concepts/stress-capital-buffer"),
        ("reports/annual-report-2025", "metrics/cet1-ratio"),
    ]


def test_citation_of_a_node_no_tool_returned_is_kept_and_marked():
    path = build_retrieval_path(STEPS[:2], ["openwiki/overview.md#intro"], GRAPH)
    overview = path.nodes[-1]
    assert (overview.id, overview.cited, overview.found_in_step, overview.opened) == ("overview", True, None, False)


def test_works_without_the_graph():
    path = build_retrieval_path(STEPS, [], None)
    assert path.nodes[0].title == "metrics/cet1-ratio" and path.nodes[0].type is None
    assert path.links == [] and path.graph_available is False
