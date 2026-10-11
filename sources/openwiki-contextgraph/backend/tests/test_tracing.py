import json
from uuid import uuid4

from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, LLMResult

from app.tracing import TraceRecorder


def _run_tool(rec: TraceRecorder, name: str, inputs: dict, output: str) -> None:
    run_id = uuid4()
    rec.on_tool_start({"name": name}, json.dumps(inputs), run_id=run_id, inputs=inputs)
    rec.on_tool_end(output, run_id=run_id)


def _llm_end(rec: TraceRecorder, input_tokens: int, output_tokens: int) -> None:
    msg = AIMessage(
        content="",
        usage_metadata={"input_tokens": input_tokens, "output_tokens": output_tokens, "total_tokens": input_tokens + output_tokens},
    )
    rec.on_llm_end(LLMResult(generations=[[ChatGeneration(message=msg)]]), run_id=uuid4())


def test_records_tool_steps_in_order_with_summaries():
    rec = TraceRecorder()
    search_out = json.dumps({"results": [{"ref": ["openwiki/m.md#a"]}, {"ref": ["openwiki/r.md#b"]}]})
    read_out = json.dumps({"page": "openwiki/m.md", "sections": [{"section": "a", "content": "x" * 120}]})
    _run_tool(rec, "semantic_search", {"query": "CECL", "limit": 8}, search_out)
    _run_tool(rec, "semantic_read", {"page": "openwiki/m.md", "sections": ["a"]}, read_out)

    steps = rec.steps()
    assert [s.step for s in steps] == [1, 2]
    assert steps[0].tool == "semantic_search"
    assert steps[0].input == '"CECL"'
    assert steps[0].result == "2 hits: openwiki/m.md#a, openwiki/r.md#b"
    assert steps[1].input == "openwiki/m.md [a]"
    assert steps[1].result == "1 section, 120 chars"
    assert all(s.ms >= 0 for s in steps)


def test_pages_read_split_by_wiki():
    rec = TraceRecorder()
    _run_tool(rec, "semantic_read", {"page": "openwiki/m.md", "sections": ["a", "b"]}, "{}")
    _run_tool(rec, "memory_read", {"page": "openwiki/t.md", "sections": ["c"]}, "{}")
    _run_tool(rec, "semantic_read", {"page": "openwiki/m.md", "sections": ["a"]}, "{}")
    assert rec.semantic_pages_read() == ["openwiki/m.md#a", "openwiki/m.md#b"]
    assert rec.context_pages_read() == ["openwiki/t.md#c"]
    assert rec.tools_used() == ["semantic_read", "memory_read"]


def test_errors_and_notes_are_summarised():
    rec = TraceRecorder()
    _run_tool(rec, "semantic_read", {"page": "p", "sections": ["s"]}, "Error: invalid_input: Unknown section: s")
    _run_tool(rec, "memory_search", {"query": "q"}, json.dumps({"results": [], "note": "memory not built yet"}))
    err_id = uuid4()
    rec.on_tool_start({"name": "semantic_search"}, "{}", run_id=err_id, inputs={"query": "z"})
    rec.on_tool_error(RuntimeError("boom"), run_id=err_id)
    results = [s.result for s in rec.steps()]
    assert results == ["Error: invalid_input: Unknown section: s", "0 hits (memory not built yet)", "Error: boom"]


def test_ignores_non_wiki_tools_and_sums_tokens():
    rec = TraceRecorder()
    _run_tool(rec, "AgentAnswer", {"answer": "x"}, "ok")
    _llm_end(rec, 100, 20)
    _llm_end(rec, 300, 50)
    assert rec.steps() == []
    assert rec.token_usage() == (400, 70)


def test_refs_seen_include_every_search_hit_and_read():
    rec = TraceRecorder()
    hits = {"results": [{"ref": [f"openwiki/p{i}.md#s"]} for i in range(6)]}
    _run_tool(rec, "semantic_search", {"query": "q"}, json.dumps(hits))
    _run_tool(rec, "semantic_read", {"page": "openwiki/x.md", "sections": ["a"]}, "{}")
    _run_tool(rec, "memory_search", {"query": "q"}, json.dumps({"results": [{"ref": ["openwiki/turns/t1.md#a"]}]}))
    assert rec.semantic_refs_seen() == [*(f"openwiki/p{i}.md#s" for i in range(6)), "openwiki/x.md#a"]


def test_context_refs_seen_include_memory_search_hits_and_reads():
    rec = TraceRecorder()
    _run_tool(rec, "memory_search", {"query": "q"}, json.dumps({"results": [{"ref": ["openwiki/turns/t1.md#a"]}]}))
    _run_tool(rec, "memory_read", {"page": "openwiki/decisions/d.md", "sections": ["why"]}, "{}")
    _run_tool(rec, "semantic_search", {"query": "q"}, json.dumps({"results": [{"ref": ["openwiki/s.md#x"]}]}))
    assert rec.context_refs_seen() == ["openwiki/turns/t1.md#a", "openwiki/decisions/d.md#why"]
    assert rec.semantic_refs_seen() == ["openwiki/s.md#x"]


def test_steps_keep_every_ref_in_rank_order():
    rec = TraceRecorder()
    hits = {"results": [{"ref": [f"openwiki/p{i}.md#s"]} for i in range(5)]}
    _run_tool(rec, "semantic_search", {"query": "q"}, json.dumps(hits))
    _run_tool(rec, "semantic_read", {"page": "openwiki/x.md", "sections": ["a", "b"]}, "{}")
    _run_tool(rec, "semantic_read", {"page": "openwiki/x.md", "sections": ["c"]}, "Error: invalid_input")
    search, read, failed = rec.steps()
    # Step refs are tagged with their wiki at capture time (both wikis share "openwiki/").
    assert search.refs == tuple(f"semantic:openwiki/p{i}.md#s" for i in range(5))
    assert read.refs == ("semantic:openwiki/x.md#a", "semantic:openwiki/x.md#b")
    assert failed.refs == ()


def test_in_process_search_hits_are_parsed_and_tagged_semantic():
    """Ratchet R7: semantic_search now returns {"hits":[{"ref": "<str>", ...}], ...}."""
    rec = TraceRecorder()
    out = json.dumps({
        "query": "q",
        "hits": [
            {"ref": "openwiki/interfaces/a.md", "type": "Interface", "title": "A", "matched": "exact_id"},
            {"ref": "openwiki/systems/b.md", "type": "System", "title": "B", "matched": "bm25"},
        ],
        "confidence": {"exact_hit": True},
    })
    _run_tool(rec, "semantic_search", {"query": "q", "limit": 8}, out)
    (step,) = rec.steps()
    assert step.result == "2 hits: openwiki/interfaces/a.md, openwiki/systems/b.md"
    assert step.refs == ("semantic:openwiki/interfaces/a.md", "semantic:openwiki/systems/b.md")
    assert rec.semantic_refs_seen() == ["openwiki/interfaces/a.md", "openwiki/systems/b.md"]


def test_graph_tools_are_traced_as_semantic():
    rec = TraceRecorder()
    out = json.dumps({"count": 1, "hits": [{"ref": "openwiki/teams/core.md", "type": "Team"}]})
    _run_tool(rec, "graph_query", {"type": "Team", "entity_id": None, "title_contains": None, "status": None}, out)
    _run_tool(rec, "graph_neighbors",
              {"ref": "openwiki/teams/core.md", "relation": "owned_by", "type": None, "direction": "both"},
              json.dumps({"ref": "openwiki/teams/core.md", "count": 1,
                          "hits": [{"ref": "openwiki/systems/hub.md", "type": "System"}]}))
    query, neighbors = rec.steps()
    assert query.input == json.dumps({"type": "Team"})
    assert query.refs == ("semantic:openwiki/teams/core.md",)
    assert neighbors.input == json.dumps({"ref": "openwiki/teams/core.md", "relation": "owned_by",
                                          "direction": "both"})
    # the queried ref is not a hit; only returned neighbors are refs seen
    assert neighbors.refs == ("semantic:openwiki/systems/hub.md",)
    assert rec.semantic_refs_seen() == ["openwiki/teams/core.md", "openwiki/systems/hub.md"]
    assert rec.tools_used() == ["graph_query", "graph_neighbors"]


def test_in_process_read_uses_ref_and_optional_heading():
    rec = TraceRecorder()
    read_out = json.dumps({"ref": "openwiki/interfaces/a.md",
                           "sections": [{"heading": "Overview", "content": "x" * 80}]})
    _run_tool(rec, "semantic_read", {"ref": "openwiki/interfaces/a.md", "heading": "Overview"}, read_out)
    _run_tool(rec, "semantic_read", {"ref": "openwiki/interfaces/a.md", "heading": None},
              json.dumps({"ref": "openwiki/interfaces/a.md",
                          "sections": [{"heading": "Overview", "content": "y" * 40}]}))
    section_read, page_read = rec.steps()
    assert section_read.input == "openwiki/interfaces/a.md [Overview]"
    assert section_read.result == "1 section, 80 chars"
    assert section_read.refs == ("semantic:openwiki/interfaces/a.md#Overview",)
    assert page_read.input == "openwiki/interfaces/a.md []"
    assert page_read.refs == ("semantic:openwiki/interfaces/a.md",)
    assert rec.semantic_pages_read() == ["openwiki/interfaces/a.md#Overview", "openwiki/interfaces/a.md"]


def test_memory_step_refs_are_tagged_memory():
    rec = TraceRecorder()
    _run_tool(rec, "memory_search", {"query": "q"}, json.dumps({"results": [{"ref": ["openwiki/turns/t1.md#a"]}]}))
    _run_tool(rec, "memory_read", {"page": "openwiki/decisions/d.md", "sections": ["why"]}, "{}")
    search, read = rec.steps()
    assert search.refs == ("memory:openwiki/turns/t1.md#a",)
    assert read.refs == ("memory:openwiki/decisions/d.md#why",)
