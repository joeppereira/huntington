import asyncio
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.agent import Turn
from app.answer_cache import (
    AnswerCache,
    CacheEntry,
    load_cache,
    matcher_prompt,
    parse_match,
    render_cache_markdown,
    result_from_entry,
)
from app.config import Settings
from app.main import create_app

from .test_chat_api import FakeAgent


def make_entry(entry_id: str = "WTC-Q02", answer: str = "**No.** 'Completed' shows at release.\n\n| a | b |\n|---|---|") -> CacheEntry:
    return CacheEntry.model_validate({
        "id": entry_id,
        "title": "Settled vs Completed",
        "intent": "Whether today's 'Completed' label can serve as the 'Settled' milestone.",
        "example_questions": ["Can we just use Completed as Settled?"],
        "recorded_at": "2026-10-12T10:00:00+00:00",
        "recorded_model": "claude-sonnet-5",
        "recorded_latency_ms": 41000,
        "confidence": "high",
        "answer": answer,
        "sources": [{"ref": "openwiki/concepts/settlement.md#Rules", "why": "status rule"}],
        "follow_up_questions": ["What does v2 add?"],
        "reasoning_summary": "Read the status rules.",
        "trace": {"input_tokens": 50000, "output_tokens": 4000, "steps": [
            {"step": 1, "tool": "semantic_search", "input": '"Completed"', "result": "2 hits", "ms": 400,
             "refs": ["semantic:openwiki/concepts/settlement.md#Rules", "semantic:openwiki/interfaces/pph-v1.md"]},
            {"step": 2, "tool": "semantic_read", "input": "openwiki/concepts/settlement.md [Rules]",
             "result": "1 section", "ms": 30, "refs": ["semantic:openwiki/concepts/settlement.md#Rules"]},
        ]},
    })


class FakeModel:
    def __init__(self, reply: str = "WTC-Q02", fail: Exception | None = None, delay: float = 0):
        self.reply, self.fail, self.delay, self.prompts = reply, fail, delay, []

    async def ainvoke(self, prompt: str):
        self.prompts.append(prompt)
        if self.delay:
            await asyncio.sleep(self.delay)
        if self.fail:
            raise self.fail
        return type("Msg", (), {"content": self.reply})()


def test_markdown_round_trip_keeps_answers_readable(tmp_path: Path):
    path = tmp_path / "answer-cache.md"
    path.write_text(render_cache_markdown([make_entry("WTC-Q01"), make_entry("WTC-Q02")]), encoding="utf-8")
    text = path.read_text(encoding="utf-8")
    assert "Not part of any graph" in text and "## WTC-Q02 - Settled vs Completed" in text
    assert "answer: |" in text  # multi-line answers are block scalars, not escaped strings
    loaded = load_cache(path)
    assert [e.id for e in loaded] == ["WTC-Q01", "WTC-Q02"]
    assert loaded[1].answer == make_entry().answer
    assert loaded[1].trace.steps[0].refs[0] == "semantic:openwiki/concepts/settlement.md#Rules"


def test_invalid_blocks_are_skipped(tmp_path: Path):
    path = tmp_path / "c.md"
    path.write_text(render_cache_markdown([make_entry()]) + "\n```yaml\nid: broken\n```\n", encoding="utf-8")
    assert [e.id for e in load_cache(path)] == ["WTC-Q02"]
    assert load_cache(tmp_path / "missing.md") == []


def test_parse_match_requires_a_known_id():
    ids = ["WTC-Q01", "WTC-Q10"]
    assert parse_match("WTC-Q10", ids) == "WTC-Q10"
    assert parse_match(" wtc-q01\n", ids) == "WTC-Q01"
    assert parse_match("NONE", ids) is None
    assert parse_match("WTC-Q99", ids) is None


def test_prompt_lists_intents_examples_and_context():
    prompt = matcher_prompt([make_entry()], "can completed mean settled?", "Which systems do we depend on?")
    assert "WTC-Q02: Whether today's 'Completed'" in prompt
    assert '"Can we just use Completed as Settled?"' in prompt
    assert 'Previous question in this chat (context only): "Which systems do we depend on?"' in prompt


def test_result_from_entry_replays_the_recorded_trace():
    result = result_from_entry(make_entry(), latency_ms=2100)
    assert result.answer.confidence == "high" and result.latency_ms == 2100
    assert [s.tool for s in result.steps] == ["semantic_search", "semantic_read"]
    assert result.steps[0].refs[0] == "semantic:openwiki/concepts/settlement.md#Rules"
    assert result.semantic_pages_read == ("openwiki/concepts/settlement.md#Rules",)
    assert "openwiki/interfaces/pph-v1.md" in result.semantic_refs_seen
    assert result.output_tokens == 4000


@pytest.mark.parametrize("model, expected", [
    (FakeModel("WTC-Q02"), "WTC-Q02"),
    (FakeModel("NONE"), None),
    (FakeModel(fail=RuntimeError("vertex down")), None),
    (FakeModel(delay=1), None),
])
def test_lookup_hits_misses_and_falls_back(model: FakeModel, expected: str | None):
    cache = AnswerCache([make_entry()], model, timeout=0.2)
    hit = asyncio.run(cache.lookup("Is Completed the same as Settled?", (Turn("q1", "a1"),)))
    assert (hit.entry.id if hit else None) == expected
    if hit:
        assert hit.result.answer.answer == make_entry().answer


@pytest.fixture
def cached_settings(settings: Settings, tmp_path: Path) -> Settings:
    path = tmp_path / "answer-cache.md"
    path.write_text(render_cache_markdown([make_entry()]), encoding="utf-8")
    return settings.model_copy(update={"demo_cache_enabled": True, "demo_cache_file": path})


def _client(settings: Settings, agent: FakeAgent, model: FakeModel) -> TestClient:
    return TestClient(create_app(settings, agent_factory=lambda _s, _t: agent, cache_model_factory=lambda _s: model))


def test_chat_serves_a_cache_hit_without_running_the_agent(cached_settings: Settings):
    agent = FakeAgent()
    with _client(cached_settings, agent, FakeModel("WTC-Q02")) as client:
        sid = client.post("/api/sessions", json={}).json()["session_id"]
        body = client.post("/api/chat", json={"session_id": sid, "message": "completed == settled?"}).json()
    assert agent.calls == []
    assert body["answer"] == make_entry().answer
    assert body["cache"]["entry_id"] == "WTC-Q02" and body["cache"]["recorded_latency_ms"] == 41000
    assert body["trace"]["model"].startswith("answer cache WTC-Q02")
    assert [s["tool"] for s in body["trace"]["steps"]] == ["semantic_search", "semantic_read"]
    assert body["trace_file"]  # cache hits are still written to agent memory


def test_chat_goes_live_on_no_match_or_when_cache_is_bypassed(cached_settings: Settings):
    agent = FakeAgent()
    with _client(cached_settings, agent, FakeModel("NONE")) as client:
        sid = client.post("/api/sessions", json={}).json()["session_id"]
        miss = client.post("/api/chat", json={"session_id": sid, "message": "unrelated"}).json()
    assert miss["cache"] is None and miss["answer"] == "answer to unrelated"

    model = FakeModel("WTC-Q02")
    with _client(cached_settings, agent, model) as client:
        sid = client.post("/api/sessions", json={}).json()["session_id"]
        live = client.post("/api/chat", json={"session_id": sid, "message": "x", "use_cache": False}).json()
    assert live["cache"] is None and model.prompts == []


def test_cache_is_off_unless_enabled(settings: Settings, tmp_path: Path):
    path = tmp_path / "answer-cache.md"
    path.write_text(render_cache_markdown([make_entry()]), encoding="utf-8")
    model = FakeModel("WTC-Q02")
    with _client(settings.model_copy(update={"demo_cache_file": path}), FakeAgent(), model) as client:
        sid = client.post("/api/sessions", json={}).json()["session_id"]
        body = client.post("/api/chat", json={"session_id": sid, "message": "x"}).json()
    assert body["cache"] is None and model.prompts == []
