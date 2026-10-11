"""Callback handler that records the agent's observed tool calls (BUILD_SPEC 8.4 "Trace capture").

The decision trace is built only from calls that actually happened; nothing is inferred.
"""

import json
import time
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult

WIKI_TOOLS = {"semantic_search", "semantic_read", "graph_query", "graph_neighbors",
              "memory_search", "memory_read"}
READ_TOOLS = {"semantic_read": "semantic", "memory_read": "context"}
# Refs from both wikis look alike ("openwiki/..."), so trace steps tag each ref with the
# wiki it came from. Untagged refs (older stored traces) are still accepted downstream.
# graph_query/graph_neighbors are in-process views over the semantic wiki (ratchet R7).
TOOL_WIKI = {"semantic_search": "semantic", "semantic_read": "semantic",
             "graph_query": "semantic", "graph_neighbors": "semantic",
             "memory_search": "memory", "memory_read": "memory"}
MAX_REFS_IN_SUMMARY = 3


def tag_ref(wiki: str, ref: str) -> str:
    """Namespace a wiki ref at capture time: ("semantic", "openwiki/x.md") -> "semantic:openwiki/x.md"."""
    return f"{wiki}:{ref}"


@dataclass(frozen=True)
class TraceStep:
    step: int
    tool: str
    input: str
    result: str
    ms: int
    refs: tuple[str, ...] = ()  # search hits in rank order, or the sections read


@dataclass(frozen=True)
class _Pending:
    tool: str
    inputs: dict[str, Any]
    started: float


def _read_targets(inputs: dict[str, Any]) -> tuple[str, list[str]]:
    """(page, sections) for both read shapes: MCP page+sections and in-process ref+heading."""
    page = inputs.get("page") or inputs.get("ref", "")
    sections = inputs.get("sections")
    if sections is None:
        heading = inputs.get("heading")
        sections = [heading] if heading else []
    return page, list(sections)


def _format_input(tool: str, inputs: dict[str, Any]) -> str:
    if tool.endswith("_search"):
        return json.dumps(inputs.get("query", ""))
    if tool.startswith("graph_"):
        return json.dumps({k: v for k, v in inputs.items() if v is not None}, default=str)
    page, sections = _read_targets(inputs)
    return f"{page} [{', '.join(sections)}]"


def _hit_refs(data: Any) -> list[str]:
    """Ranked refs from either search shape: in-process {"hits":[{"ref": "..."}]} (ref is a
    string) or OpenWiki MCP {"results":[{"ref": [...]}]} (ref is a list)."""
    if not isinstance(data, dict):
        return []
    refs = [h["ref"] for h in data.get("hits", []) if isinstance(h.get("ref"), str)]
    refs += [ref for result in data.get("results", []) for ref in result.get("ref", [])]
    return refs


def _summarise(tool: str, output: str) -> str:
    if output.startswith("Error:"):
        return output[:200]
    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        return f"{len(output)} chars"
    if tool not in READ_TOOLS:
        refs = _hit_refs(data)
        hits = f"{len(refs)} hit{'s' if len(refs) != 1 else ''}"
        if isinstance(data, dict) and data.get("note"):
            return f"{hits} ({data['note']})"
        return f"{hits}: {', '.join(refs[:MAX_REFS_IN_SUMMARY])}" if refs else hits
    sections = data.get("sections", [])
    chars = sum(len(s.get("content", "")) for s in sections)
    return f"{len(sections)} section{'s' if len(sections) != 1 else ''}, {chars} chars"


def _search_refs(output: str) -> list[str]:
    try:
        return _hit_refs(json.loads(output))
    except json.JSONDecodeError:
        return []


def _text(output: Any) -> str:
    # Agents call tools with ToolCalls, so on_tool_end receives a ToolMessage rather than a string.
    content = getattr(output, "content", output)
    return content if isinstance(content, str) else json.dumps(content, default=str)


class TraceRecorder(BaseCallbackHandler):
    run_inline = True  # record in call order even when the agent runs async

    def __init__(self) -> None:
        self._pending: dict[UUID, _Pending] = {}
        self._steps: list[TraceStep] = []
        self._reads: list[tuple[str, str]] = []  # (wiki, "page#section")
        self._semantic_seen: list[str] = []  # every semantic ref returned by search or read
        self._context_seen: list[str] = []  # same for the memory (context) wiki
        self._input_tokens = 0
        self._output_tokens = 0

    def on_tool_start(
        self,
        serialized: dict[str, Any],
        input_str: str,
        *,
        run_id: UUID,
        inputs: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        tool = (serialized or {}).get("name") or kwargs.get("name", "")
        if tool not in WIKI_TOOLS:
            return
        if inputs is None:
            try:
                inputs = json.loads(input_str)
            except json.JSONDecodeError:
                inputs = {}
        self._pending[run_id] = _Pending(tool, dict(inputs), time.perf_counter())

    def on_tool_end(self, output: Any, *, run_id: UUID, **kwargs: Any) -> None:
        pending = self._pending.pop(run_id, None)
        if pending is None:
            return
        text = _text(output)
        failed = text.startswith("Error:")
        if failed:
            step_refs: list[str] = []
        elif pending.tool in READ_TOOLS:
            page, sections = _read_targets(pending.inputs)
            step_refs = [f"{page}#{s}" for s in sections] or ([page] if page else [])
        else:
            step_refs = _search_refs(text)
        wiki = TOOL_WIKI[pending.tool]
        self._finish(pending, _summarise(pending.tool, text), tuple(tag_ref(wiki, r) for r in step_refs))
        if failed:
            return
        if pending.tool in READ_TOOLS:
            refs = step_refs
            self._reads.extend((READ_TOOLS[pending.tool], ref) for ref in refs)
            (self._semantic_seen if pending.tool == "semantic_read" else self._context_seen).extend(refs)
        elif wiki == "semantic":  # semantic_search, graph_query, graph_neighbors
            self._semantic_seen.extend(step_refs)
        elif pending.tool == "memory_search":
            self._context_seen.extend(step_refs)

    def on_tool_error(self, error: BaseException, *, run_id: UUID, **kwargs: Any) -> None:
        pending = self._pending.pop(run_id, None)
        if pending is not None:
            self._finish(pending, f"Error: {error}"[:200])

    def on_llm_end(self, response: LLMResult, *, run_id: UUID, **kwargs: Any) -> None:
        for generations in response.generations:
            for generation in generations:
                usage = getattr(getattr(generation, "message", None), "usage_metadata", None) or {}
                self._input_tokens += usage.get("input_tokens", 0)
                self._output_tokens += usage.get("output_tokens", 0)

    def _finish(self, pending: _Pending, result: str, refs: tuple[str, ...] = ()) -> None:
        ms = int((time.perf_counter() - pending.started) * 1000)
        step = TraceStep(
            len(self._steps) + 1, pending.tool, _format_input(pending.tool, pending.inputs), result, ms, refs
        )
        self._steps.append(step)

    def steps(self) -> list[TraceStep]:
        return list(self._steps)

    def tools_used(self) -> list[str]:
        return list(dict.fromkeys(step.tool for step in self._steps))

    def _pages(self, wiki: str) -> list[str]:
        return list(dict.fromkeys(ref for w, ref in self._reads if w == wiki))

    def semantic_pages_read(self) -> list[str]:
        return self._pages("semantic")

    def context_pages_read(self) -> list[str]:
        return self._pages("context")

    def semantic_refs_seen(self) -> list[str]:
        """Every semantic-wiki ref the tools returned (search hits and reads): what the agent could cite."""
        return list(dict.fromkeys(self._semantic_seen))

    def context_refs_seen(self) -> list[str]:
        """Every memory-wiki ref the tools returned (memory_search hits and memory_read)."""
        return list(dict.fromkeys(self._context_seen))

    def token_usage(self) -> tuple[int, int]:
        return self._input_tokens, self._output_tokens
