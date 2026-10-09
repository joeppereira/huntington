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

WIKI_TOOLS = {"semantic_search", "semantic_read", "memory_search", "memory_read"}
READ_TOOLS = {"semantic_read": "semantic", "memory_read": "context"}
MAX_REFS_IN_SUMMARY = 3


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


def _format_input(tool: str, inputs: dict[str, Any]) -> str:
    if tool.endswith("_search"):
        return json.dumps(inputs.get("query", ""))
    return f"{inputs.get('page', '')} [{', '.join(inputs.get('sections', []))}]"


def _summarise(tool: str, output: str) -> str:
    if output.startswith("Error:"):
        return output[:200]
    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        return f"{len(output)} chars"
    if tool.endswith("_search"):
        results = data.get("results", [])
        refs = [ref for result in results for ref in result.get("ref", [])][:MAX_REFS_IN_SUMMARY]
        hits = f"{len(results)} hit{'s' if len(results) != 1 else ''}"
        if data.get("note"):
            return f"{hits} ({data['note']})"
        return f"{hits}: {', '.join(refs)}" if refs else hits
    sections = data.get("sections", [])
    chars = sum(len(s.get("content", "")) for s in sections)
    return f"{len(sections)} section{'s' if len(sections) != 1 else ''}, {chars} chars"


def _search_refs(output: str) -> list[str]:
    try:
        results = json.loads(output).get("results", [])
    except (json.JSONDecodeError, AttributeError):
        return []
    return [ref for result in results for ref in result.get("ref", [])]


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
            page = pending.inputs.get("page", "")
            step_refs = [f"{page}#{s}" for s in pending.inputs.get("sections", [])]
        else:
            step_refs = _search_refs(text)
        self._finish(pending, _summarise(pending.tool, text), tuple(step_refs))
        if failed:
            return
        if pending.tool in READ_TOOLS:
            refs = step_refs
            self._reads.extend((READ_TOOLS[pending.tool], ref) for ref in refs)
            (self._semantic_seen if pending.tool == "semantic_read" else self._context_seen).extend(refs)
        elif pending.tool == "semantic_search":
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
