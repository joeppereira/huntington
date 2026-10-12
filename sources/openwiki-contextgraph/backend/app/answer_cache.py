"""Demo answer cache: recorded graph answers for the scripted Wire Tracking Center questions.

The cache is one Markdown file (demo-cache/answer-cache.md) that lives outside both OpenWiki
corpora, so it is never indexed into either graph. Each entry is a ```yaml block holding a
question intent, example wordings, and the answer + sources + full tool trace captured from a
live run of the graph agent (tools/record_demo_cache.py writes it).

At question time one short model call decides whether the question means the same as a cached
entry (wording may differ freely). On a match the recorded answer and its real trace are served,
flagged as recorded; on no match, a matcher error or a timeout, the live graph agent answers.
"""

import asyncio
import logging
import re
import time
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, Field

from .agent import AgentAnswer, AgentResult, SourceCitation, Turn
from .tracing import TraceStep

logger = logging.getLogger("openwiki_poc")

MATCH_TIMEOUT_SEC = 15.0
MAX_QUESTION_CHARS = 3000
_BLOCK = re.compile(r"^```yaml\n(.*?)\n^```$", re.M | re.S)
_TAG = re.compile(r"^(semantic|memory):")
SEMANTIC_TOOLS = {"semantic_search", "semantic_read", "graph_query", "graph_neighbors"}
MEMORY_TOOLS = {"memory_search", "memory_read"}


class CachedStep(BaseModel):
    step: int
    tool: str
    input: str
    result: str
    ms: int
    refs: list[str] = Field(default_factory=list)


class CachedTrace(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0
    steps: list[CachedStep]


class CachedSource(BaseModel):
    ref: str
    why: str


class CacheEntry(BaseModel):
    id: str
    title: str
    intent: str
    example_questions: list[str]
    recorded_question: str = ""  # exact wording asked during the recorded run, if it differs from the examples
    recorded_at: str
    recorded_model: str
    recorded_latency_ms: int
    confidence: Literal["high", "medium", "low"]
    answer: str
    sources: list[CachedSource]
    follow_up_questions: list[str] = Field(default_factory=list)
    reasoning_summary: str = ""
    trace: CachedTrace


@dataclass(frozen=True)
class CacheHit:
    entry: CacheEntry
    result: AgentResult
    match_ms: int


HEADER = """\
# Demo answer cache - Wire Tracking Center

> **Not part of any graph.** This file sits outside `semantic-corpus-cnb/` and `context-corpus/`,
> so OpenWiki never indexes it. The backend reads it only when `DEMO_CACHE_ENABLED=true`.
>
> Each entry was recorded from a live run of the graph agent by `tools/record_demo_cache.py`:
> the answer, its sources and the full tool trace (every search / read the agent made over the
> semantic graph). When a question means the same as an entry's intent - any wording - the app
> serves the entry in seconds and labels it *Recorded*; anything else goes to the live graph agent.
>
> To change an answer, edit its `answer:` block or re-record it:
> `.venv/bin/python tools/record_demo_cache.py --only WTC-Q04`
"""


def load_cache(path: Path) -> list[CacheEntry]:
    """Every entry in the cache file; an invalid block is logged and skipped, never fatal."""
    if not path.is_file():
        return []
    entries: list[CacheEntry] = []
    for block in _BLOCK.findall(path.read_text(encoding="utf-8")):
        try:
            entries.append(CacheEntry.model_validate(yaml.safe_load(block)))
        except Exception:
            logger.exception("skipping an invalid entry in %s", path)
    return entries


class _LiteralDumper(yaml.SafeDumper):
    """Multi-line strings (answers, reasoning) as readable `|` blocks."""


def _str_representer(dumper: yaml.SafeDumper, data: str) -> Any:
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


_LiteralDumper.add_representer(str, _str_representer)


def _clean(text: str) -> str:
    # YAML cannot emit a `|` block with trailing spaces; they carry no meaning in Markdown answers.
    return "\n".join(line.rstrip() for line in text.strip().splitlines())


def render_cache_markdown(entries: Sequence[CacheEntry]) -> str:
    parts = [HEADER]
    for entry in entries:
        data = entry.model_dump()
        data["answer"] = _clean(entry.answer)
        data["reasoning_summary"] = _clean(entry.reasoning_summary)
        body = yaml.dump(data, Dumper=_LiteralDumper, sort_keys=False, allow_unicode=True, width=110)
        parts.append(f"## {entry.id} - {entry.title}\n\n```yaml\n{body.rstrip()}\n```\n")
    return "\n".join(parts)


def matcher_prompt(entries: Sequence[CacheEntry], question: str, previous_question: str | None) -> str:
    catalog = "\n".join(
        f"- {e.id}: {e.intent} Example wordings: " + " | ".join(f'"{q}"' for q in e.example_questions)
        for e in entries
    )
    previous = f'"{previous_question[:500]}"' if previous_question else "(none)"
    return f"""\
You route a product manager's question to a cache of pre-recorded answers. All cached answers are
about ONE feature: the Wire Tracking Center (FedEx-style tracking of domestic and international wires
in the CBO Wire Center portal at Crestline National Bank; concept PM-WTC-MR-0.3, items FC-01 to FC-07).

Cached answers:
{catalog}

Previous question in this chat (context only): {previous}
New question: "{question[:MAX_QUESTION_CHARS]}"

Reply with the one cache id whose answer fully answers the new question, or NONE.
Match on meaning, not wording: paraphrases, shorter or longer phrasings, different word order and typos
are the same question. Reply NONE if the question is about a different feature or product, asks for
something the cached answer does not cover (a narrower detail, a single fact, a different item, a
follow-up on part of an earlier answer), combines several cached questions, or is unclear.
Reply with only the id or NONE."""


def parse_match(reply: str, ids: Sequence[str]) -> str | None:
    text = reply.strip().upper()
    for entry_id in ids:
        if re.search(rf"\b{re.escape(entry_id.upper())}\b", text):
            return entry_id
    return None


def _untag(ref: str) -> str:
    return _TAG.sub("", ref)


def result_from_entry(entry: CacheEntry, latency_ms: int) -> AgentResult:
    """The recorded run as an AgentResult, so the normal trace / memory / retrieval path applies."""
    steps = tuple(TraceStep(s.step, s.tool, s.input, s.result, s.ms, tuple(s.refs)) for s in entry.trace.steps)

    def refs(tools: set[str]) -> tuple[str, ...]:
        return tuple(dict.fromkeys(_untag(r) for s in entry.trace.steps if s.tool in tools for r in s.refs))

    return AgentResult(
        answer=AgentAnswer(
            answer=entry.answer,
            sources=[SourceCitation(ref=s.ref, why=s.why) for s in entry.sources],
            reasoning_summary=entry.reasoning_summary,
            confidence=entry.confidence,
            follow_up_questions=entry.follow_up_questions[:3],
        ),
        steps=steps,
        tools_used=tuple(dict.fromkeys(s.tool for s in steps)),
        semantic_pages_read=refs({"semantic_read"}),
        context_pages_read=refs({"memory_read"}),
        input_tokens=entry.trace.input_tokens,
        output_tokens=entry.trace.output_tokens,
        latency_ms=latency_ms,
        semantic_refs_seen=refs(SEMANTIC_TOOLS),
        context_refs_seen=refs(MEMORY_TOOLS),
    )


class AnswerCache:
    """Recorded entries plus the model that decides whether a question matches one of them."""

    def __init__(self, entries: Sequence[CacheEntry], model: Any, timeout: float = MATCH_TIMEOUT_SEC) -> None:
        self.entries = list(entries)
        self._by_id = {e.id: e for e in self.entries}
        self._model = model
        self._timeout = timeout

    async def lookup(self, question: str, history: tuple[Turn, ...]) -> CacheHit | None:
        if not self.entries:
            return None
        started = time.perf_counter()
        previous = history[-1].question if history else None
        prompt = matcher_prompt(self.entries, question, previous)
        try:
            reply = await asyncio.wait_for(self._model.ainvoke(prompt), self._timeout)
        except Exception:
            logger.warning("answer cache matcher failed; falling back to the live agent", exc_info=True)
            return None
        content = reply.content if hasattr(reply, "content") else reply
        text = content if isinstance(content, str) else " ".join(
            b.get("text", "") for b in content if isinstance(b, dict))
        entry_id = parse_match(text, list(self._by_id))
        match_ms = int((time.perf_counter() - started) * 1000)
        logger.info("answer cache: %s in %d ms for %r", entry_id or "no match", match_ms, question[:80])
        if entry_id is None:
            return None
        entry = self._by_id[entry_id]
        return CacheHit(entry, result_from_entry(entry, match_ms), match_ms)
