"""Real OpenWiki MCP server against the built semantic wiki. No model calls (search/read are local)."""

import json

import pytest

from app.config import Settings
from app.mcp_tools import OpenWikiMCP, OpenWikiTools


@pytest.fixture
async def tools(settings: Settings):
    if not settings.semantic_ready:
        pytest.skip("semantic wiki not built")
    mcp = OpenWikiMCP(settings)
    await mcp.start()
    try:
        yield OpenWikiTools(mcp, settings.semantic_corpus_path, settings.context_corpus_path)
    finally:
        await mcp.stop()


def _tool(tools, name):
    return next(t for t in tools.as_langchain_tools() if t.name == name)


async def test_search_then_read_round_trip(tools):
    found = json.loads(await _tool(tools, "semantic_search").ainvoke({"query": "CECL model upstream APIs", "limit": 3}))
    assert found["results"], "expected search hits"
    page, section = found["results"][0]["ref"][0].split("#")
    read = json.loads(await _tool(tools, "semantic_read").ainvoke({"page": page, "sections": [section]}))
    assert read["sections"][0]["content"].strip()


async def test_unknown_section_is_an_error_string(tools):
    out = await _tool(tools, "semantic_read").ainvoke(
        {"page": "openwiki/models/cecl-allowance-model.md", "sections": ["no-such-section"]}
    )
    assert out.startswith("Error:")


async def test_memory_search_before_sync(tools):
    out = json.loads(await _tool(tools, "memory_search").ainvoke({"query": "CECL"}))
    assert out["note"] == "memory not built yet"
