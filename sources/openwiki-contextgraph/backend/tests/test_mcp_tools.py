import json
from pathlib import Path

import pytest

from app.mcp_tools import OpenWikiTools, ToolCallError


class FakeOpenWiki:
    """Stands in for the MCP session: records calls, returns canned JSON or raises."""

    def __init__(self, responses: dict[str, object] | None = None, error: str | None = None):
        self.calls: list[tuple[str, dict]] = []
        self._responses = responses or {}
        self._error = error

    async def call(self, name: str, arguments: dict) -> str:
        self.calls.append((name, arguments))
        if self._error:
            raise ToolCallError(self._error)
        return json.dumps(self._responses.get(name, {"results": []}))


def _roots(tmp_path: Path, context_built: bool) -> tuple[Path, Path]:
    semantic, context = tmp_path / "semantic", tmp_path / "context"
    (semantic / "openwiki").mkdir(parents=True)
    (semantic / "openwiki" / "index.md").write_text("x", encoding="utf-8")
    (context / "openwiki").mkdir(parents=True)
    if context_built:
        (context / "openwiki" / "index.md").write_text("x", encoding="utf-8")
    return semantic, context


def _tool(tools, name):
    return next(t for t in tools.as_langchain_tools() if t.name == name)


async def test_semantic_search_binds_semantic_root(tmp_path: Path):
    semantic, context = _roots(tmp_path, context_built=True)
    fake = FakeOpenWiki({"openwiki_search": {"results": [{"ref": ["openwiki/a.md#x"], "content": "c"}]}})
    tools = OpenWikiTools(fake, semantic, context)
    out = json.loads(await _tool(tools, "semantic_search").ainvoke({"query": "CECL"}))
    assert out["results"][0]["ref"] == ["openwiki/a.md#x"]
    assert fake.calls == [("openwiki_search", {"root": str(semantic), "query": "CECL", "limit": 8})]


async def test_semantic_read_passes_page_and_sections(tmp_path: Path):
    semantic, context = _roots(tmp_path, context_built=True)
    fake = FakeOpenWiki()
    tools = OpenWikiTools(fake, semantic, context)
    await _tool(tools, "semantic_read").ainvoke({"page": "openwiki/a.md", "sections": ["x", "y"]})
    assert fake.calls == [("openwiki_read", {"root": str(semantic), "page": "openwiki/a.md", "sections": ["x", "y"]})]


async def test_memory_tools_use_context_root(tmp_path: Path):
    semantic, context = _roots(tmp_path, context_built=True)
    fake = FakeOpenWiki()
    tools = OpenWikiTools(fake, semantic, context)
    await _tool(tools, "memory_search").ainvoke({"query": "earlier"})
    await _tool(tools, "memory_read").ainvoke({"page": "openwiki/t.md", "sections": ["s"]})
    assert fake.calls[0] == ("openwiki_search", {"root": str(context), "query": "earlier", "limit": 5})
    assert fake.calls[1][1]["root"] == str(context)


async def test_memory_search_before_first_sync_returns_note_without_calling_mcp(tmp_path: Path):
    semantic, context = _roots(tmp_path, context_built=False)
    fake = FakeOpenWiki()
    tools = OpenWikiTools(fake, semantic, context)
    out = json.loads(await _tool(tools, "memory_search").ainvoke({"query": "x"}))
    assert out == {"results": [], "note": "memory not built yet"}
    assert fake.calls == []


async def test_tool_errors_are_returned_to_the_model_as_text(tmp_path: Path):
    semantic, context = _roots(tmp_path, context_built=True)
    tools = OpenWikiTools(FakeOpenWiki(error="invalid_input: Unknown section: nope"), semantic, context)
    out = await _tool(tools, "semantic_read").ainvoke({"page": "openwiki/a.md", "sections": ["nope"]})
    assert out.startswith("Error:") and "Unknown section" in out


@pytest.mark.parametrize("bad", [{"query": ""}, {"query": "x", "limit": 0}, {"query": "x", "limit": 21}])
async def test_search_validates_arguments(tmp_path: Path, bad: dict):
    semantic, context = _roots(tmp_path, context_built=True)
    with pytest.raises(Exception):
        await _tool(OpenWikiTools(FakeOpenWiki(), semantic, context), "semantic_search").ainvoke(bad)


def test_exposes_exactly_four_tools(tmp_path: Path):
    semantic, context = _roots(tmp_path, context_built=True)
    names = sorted(t.name for t in OpenWikiTools(FakeOpenWiki(), semantic, context).as_langchain_tools())
    assert names == ["memory_read", "memory_search", "semantic_read", "semantic_search"]
