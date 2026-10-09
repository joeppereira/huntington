import re

import pytest
from fastapi.testclient import TestClient

from app.agent import AgentAnswer, AgentResult, SourceCitation, Turn, history_messages
from app.config import Settings
from app.main import create_app
from app.tracing import TraceStep


class FakeAgent:
    model_id = "fake-model"

    def __init__(self, fail: Exception | None = None):
        self.calls: list[tuple[str, tuple[Turn, ...]]] = []
        self._fail = fail

    async def ask(self, question: str, history: tuple[Turn, ...]) -> AgentResult:
        self.calls.append((question, history))
        if self._fail:
            raise self._fail
        return AgentResult(
            answer=AgentAnswer(
                answer=f"answer to {question}",
                sources=[SourceCitation(ref="openwiki/m.md#a", why="because")],
                reasoning_summary="looked it up",
                confidence="high",
                follow_up_questions=["next?"],
            ),
            steps=(TraceStep(1, "semantic_search", '"q"', "1 hit: openwiki/m.md#a", 12),),
            tools_used=("semantic_search",),
            semantic_pages_read=("openwiki/m.md#a",),
            context_pages_read=(),
            input_tokens=100,
            output_tokens=20,
            latency_ms=345,
        )


@pytest.fixture
def fake_agent() -> FakeAgent:
    return FakeAgent()


@pytest.fixture
def client(settings: Settings, fake_agent: FakeAgent):
    with TestClient(create_app(settings, agent_factory=lambda _s, _tools: fake_agent)) as c:
        yield c


def _new_session(client: TestClient) -> str:
    return client.post("/api/sessions", json={}).json()["session_id"]


def test_session_id_format(client: TestClient):
    assert re.fullmatch(r"\d{8}-\d{6}-[0-9a-f]{4}", _new_session(client))


def test_chat_returns_answer_and_observed_trace(client: TestClient):
    sid = _new_session(client)
    body = client.post("/api/chat", json={"session_id": sid, "message": "What is CET1?"}).json()
    assert body["session_id"] == sid
    assert body["turn"] == 1
    assert body["answer"] == "answer to What is CET1?"
    assert body["sources"] == [{"ref": "openwiki/m.md#a", "why": "because"}]
    assert body["confidence"] == "high"
    assert body["follow_up_questions"] == ["next?"]
    assert body["reasoning_summary"] == "looked it up"
    assert body["trace"]["latency_ms"] == 345
    assert body["trace"]["steps"] == [
        {"step": 1, "tool": "semantic_search", "input": '"q"', "result": "1 hit: openwiki/m.md#a", "ms": 12, "refs": []}
    ]


def test_turns_increment_and_history_is_passed(client: TestClient, fake_agent: FakeAgent):
    sid = _new_session(client)
    client.post("/api/chat", json={"session_id": sid, "message": "first"})
    second = client.post("/api/chat", json={"session_id": sid, "message": "second"}).json()
    assert second["turn"] == 2
    question, history = fake_agent.calls[1]
    assert question == "second"
    assert history == (Turn(question="first", answer="answer to first"),)


def test_unknown_session_is_404(client: TestClient):
    assert client.post("/api/chat", json={"session_id": "nope", "message": "hi"}).status_code == 404


@pytest.mark.parametrize("message", ["", "   ", "x" * 4001])
def test_message_is_validated(client: TestClient, message: str):
    sid = _new_session(client)
    assert client.post("/api/chat", json={"session_id": sid, "message": message}).status_code == 422


def test_agent_failure_is_502_without_recording_a_turn(settings: Settings):
    agent = FakeAgent(fail=RuntimeError("anthropic overloaded"))
    with TestClient(create_app(settings, agent_factory=lambda _s, _t: agent)) as c:
        sid = _new_session(c)
        resp = c.post("/api/chat", json={"session_id": sid, "message": "hi"})
        assert resp.status_code == 502
        assert "anthropic overloaded" in resp.json()["detail"]
        agent._fail = None
        assert c.post("/api/chat", json={"session_id": sid, "message": "again"}).json()["turn"] == 1


def test_chat_refuses_when_semantic_wiki_missing(settings: Settings, tmp_path, fake_agent: FakeAgent):
    s = settings.model_copy(update={"semantic_corpus_dir": tmp_path / "none"})
    with TestClient(create_app(s, agent_factory=lambda _s, _t: fake_agent)) as c:
        resp = c.post("/api/chat", json={"session_id": _new_session(c), "message": "hi"})
        assert resp.status_code == 409
        assert "build-semantic" in resp.json()["detail"]


def test_health_reports_mcp_running(client: TestClient):
    assert client.get("/api/health").json()["children"]["mcp"] == "running"


def test_history_messages_keeps_last_six_turns():
    turns = tuple(Turn(question=f"q{i}", answer=f"a{i}") for i in range(8))
    msgs = history_messages(turns)
    assert len(msgs) == 12
    assert msgs[0] == {"role": "user", "content": "q2"}
    assert msgs[-1] == {"role": "assistant", "content": "a7"}


def _git_log(corpus) -> list[str]:
    import subprocess

    return subprocess.run(["git", "log", "--format=%s"], cwd=corpus, capture_output=True, text=True, check=True).stdout.splitlines()


def test_chat_writes_and_commits_a_turn_trace(client: TestClient, settings: Settings):
    sid = _new_session(client)
    body = client.post("/api/chat", json={"session_id": sid, "message": "What is CET1?"}).json()
    assert body["trace_file"] == f"sessions/{sid}/turn-0001.md"
    trace = (settings.context_corpus_path / body["trace_file"]).read_text(encoding="utf-8")
    assert "type: TurnTrace" in trace and "## Decision trace" in trace
    assert (settings.context_corpus_path / "sessions" / sid / "session.md").exists()
    assert _git_log(settings.context_corpus_path)[0] == f"turn {sid}/1"


def test_get_session_returns_turns_from_files(client: TestClient):
    sid = _new_session(client)
    assert client.get(f"/api/sessions/{sid}").json() == {"session_id": sid, "turns": []}
    client.post("/api/chat", json={"session_id": sid, "message": "first"})
    client.post("/api/chat", json={"session_id": sid, "message": "second"})
    turns = client.get(f"/api/sessions/{sid}").json()["turns"]
    assert [(t["turn"], t["question"], t["answer"]) for t in turns] == [
        (1, "first", "answer to first"),
        (2, "second", "answer to second"),
    ]
    assert turns[0]["confidence"] == "high"


@pytest.mark.parametrize("sid", ["nope", "..%2F..%2Fsecrets"])
def test_get_unknown_or_invalid_session_is_404(client: TestClient, sid: str):
    assert client.get(f"/api/sessions/{sid}").status_code == 404


def test_trace_write_failure_still_returns_the_answer(client: TestClient):
    from app.context_store import ContextStore

    sid = _new_session(client)
    original = ContextStore.write_turn
    ContextStore.write_turn = lambda self, record, session_started_at: (_ for _ in ()).throw(OSError("disk full"))
    try:
        body = client.post("/api/chat", json={"session_id": sid, "message": "hi"}).json()
    finally:
        ContextStore.write_turn = original
    assert body["answer"] == "answer to hi"
    assert body["trace_file"] is None


class GraphAgent(FakeAgent):
    """Steps that reference real semantic-wiki pages, so the retrieval path resolves titles and links."""

    async def ask(self, question, history):
        result = await super().ask(question, history)
        steps = (
            TraceStep(1, "semantic_search", '"CET1"', "2 hits", 30, (
                "openwiki/metrics/cet1-ratio.md#requirement-stack-and-management-target",
                "openwiki/concepts/stress-capital-buffer.md#definition",
            )),
        )
        answer = result.answer.model_copy(update={"sources": [
            SourceCitation(ref="openwiki/metrics/cet1-ratio.md#requirement-stack-and-management-target", why="ratio"),
        ]})
        return AgentResult(**{**result.__dict__, "steps": steps, "answer": answer})


def test_chat_returns_the_semantic_retrieval_path(settings: Settings):
    with TestClient(create_app(settings, agent_factory=lambda _s, _t: GraphAgent())) as c:
        sid = _new_session(c)
        body = c.post("/api/chat", json={"session_id": sid, "message": "CET1?"}).json()
    path = body["retrieval"]
    assert path["graph_available"] is True
    assert [(n["id"], n["title"], n["type"], n["cited"]) for n in path["nodes"]] == [
        ("metrics/cet1-ratio", "CET1 Ratio", "FinancialMetric", True),
        ("concepts/stress-capital-buffer", "Stress Capital Buffer", "RiskConcept", False),
    ]
    assert {"source": "metrics/cet1-ratio", "target": "concepts/stress-capital-buffer"} in path["links"]
    assert body["trace"]["steps"][0]["refs"][0].startswith("openwiki/metrics/cet1-ratio.md")
