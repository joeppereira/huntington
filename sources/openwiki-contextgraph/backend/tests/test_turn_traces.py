import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pytest
import yaml

from app.agent import AgentAnswer, AgentResult, SourceCitation
from app.config import Settings
from app.context_store import ContextStore, TurnRecord, render_session_markdown, render_turn_markdown, reset_context_corpus
from app.tracing import TraceStep

T0 = datetime(2026, 10, 4, 9, 41, 55, tzinfo=timezone.utc)


def _result(answer: str = "CET1 was **15.1%**.", confidence: str = "medium") -> AgentResult:
    return AgentResult(
        answer=AgentAnswer(
            answer=answer,
            sources=[SourceCitation(ref="openwiki/metrics/cet1-ratio.md#stack", why="lists the stack")],
            reasoning_summary="Searched for CET1, then read the metric page.",
            confidence=confidence,
            follow_up_questions=["What drives the SCB?"],
        ),
        steps=(
            TraceStep(1, "memory_search", '"CET1"', "0 hits (memory not built yet)", 3),
            TraceStep(2, "semantic_search", '"CET1 | requirement"', "8 hits: openwiki/metrics/cet1-ratio.md#stack", 41),
            TraceStep(3, "semantic_read", "openwiki/metrics/cet1-ratio.md [stack]", "1 section, 1011 chars", 22),
        ),
        tools_used=("memory_search", "semantic_search", "semantic_read"),
        semantic_pages_read=("openwiki/metrics/cet1-ratio.md#stack",),
        context_pages_read=(),
        input_tokens=5120,
        output_tokens=712,
        latency_ms=8423,
        semantic_refs_seen=("openwiki/metrics/cet1-ratio.md#stack", "openwiki/reports/ar.md#capital"),
    )


def _record(turn: int = 1, question: str = "What was the CET1 ratio?", **kwargs) -> TurnRecord:
    return TurnRecord(
        session_id="20261004-093012-a1b2",
        turn=turn,
        question=question,
        timestamp=T0,
        model="claude-sonnet-5-5",
        result=_result(**kwargs),
    )


def _front_matter(markdown: str) -> dict:
    _, fm, _ = markdown.split("---\n", 2)
    return yaml.safe_load(fm)


def _section(markdown: str, title: str) -> str:
    body = markdown.split(f"\n## {title}\n", 1)[1]
    return body.split("\n## ", 1)[0].strip()


def test_turn_front_matter_matches_spec():
    fm = _front_matter(render_turn_markdown(_record(turn=3)))
    assert fm == {
        "type": "TurnTrace",
        "session_id": "20261004-093012-a1b2",
        "turn": 3,
        "timestamp": "2026-10-04T09:41:55Z",
        "previous_turn": "turn-0002.md",
        "model": "claude-sonnet-5-5",
        "latency_ms": 8423,
        "input_tokens": 5120,
        "output_tokens": 712,
        "confidence": "medium",
        "tools_used": ["memory_search", "semantic_search", "semantic_read"],
        "semantic_pages_read": ["openwiki/metrics/cet1-ratio.md#stack"],
        "semantic_refs_seen": ["openwiki/metrics/cet1-ratio.md#stack", "openwiki/reports/ar.md#capital"],
        "context_pages_read": [],
        "context_refs_seen": [],
    }


def test_first_turn_has_no_previous():
    assert _front_matter(render_turn_markdown(_record(turn=1)))["previous_turn"] is None


def test_turn_sections_in_spec_order():
    md = render_turn_markdown(_record(turn=3))
    headings = [line for line in md.splitlines() if line.startswith("#")]
    assert headings == [
        "# Turn 3: What was the CET1 ratio?",
        "## Question",
        "## Answer",
        "## Decision trace",
        "## Sources cited",
        "## Reasoning summary (agent self-report)",
        "## Follow-up questions",
    ]
    assert _section(md, "Question") == "What was the CET1 ratio?"
    assert _section(md, "Answer") == "CET1 was **15.1%**."
    assert _section(md, "Sources cited") == "- openwiki/metrics/cet1-ratio.md#stack - why: lists the stack"
    assert _section(md, "Reasoning summary (agent self-report)") == "Searched for CET1, then read the metric page."
    assert _section(md, "Follow-up questions") == "- What drives the SCB?"


def test_decision_trace_table_escapes_pipes():
    table = _section(render_turn_markdown(_record()), "Decision trace").splitlines()
    assert table[0] == "| Step | Tool | Input | Result (refs / summary) | ms |"
    assert table[1] == "|---|---|---|---|---|"
    assert table[3] == '| 2 | semantic_search | "CET1 \\| requirement" | 8 hits: openwiki/metrics/cet1-ratio.md#stack | 41 |'
    assert len(table) == 5


def test_long_multiline_question_gets_a_one_line_title():
    md = render_turn_markdown(_record(question="Line one\nline two " + "x" * 200))
    title = md.split("\n# ", 1)[1].splitlines()[0]
    assert "\n" not in title and len(title) <= 130 and title.endswith("…")
    assert _section(md, "Question").startswith("Line one\nline two")


def test_answer_headings_cannot_break_the_trace_structure():
    md = render_turn_markdown(_record(answer="Intro\n## Decision trace\nfake"))
    assert md.count("\n## Decision trace\n") == 1
    assert "### Decision trace" in _section(md, "Answer")


def test_session_markdown_lists_turns():
    md = render_session_markdown("20261004-093012-a1b2", T0, [(1, "First?"), (2, "Second\nquestion?")])
    fm = _front_matter(md)
    assert fm == {"type": "SessionLog", "session_id": "20261004-093012-a1b2",
                  "started_at": "2026-10-04T09:41:55Z", "turn_count": 2}
    assert "1. [Turn 1](turn-0001.md): First?" in md
    assert "2. [Turn 2](turn-0002.md): Second question?" in md


def _git(corpus: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=corpus, capture_output=True, text=True, check=True).stdout


@pytest.fixture
def store(settings: Settings) -> ContextStore:
    reset_context_corpus(settings)
    return ContextStore(settings.context_corpus_path)


def test_write_turns_commits_files_and_session_log(store: ContextStore, settings: Settings):
    corpus = settings.context_corpus_path
    path1 = store.write_turn(_record(turn=1), session_started_at=T0)
    path2 = store.write_turn(_record(turn=2, question="Follow-up?"), session_started_at=T0)

    session_dir = corpus / "sessions" / "20261004-093012-a1b2"
    assert path1 == session_dir / "turn-0001.md" and path2 == session_dir / "turn-0002.md"
    assert _front_matter(path2.read_text(encoding="utf-8"))["previous_turn"] == "turn-0001.md"
    session = (session_dir / "session.md").read_text(encoding="utf-8")
    assert _front_matter(session)["turn_count"] == 2
    assert "[Turn 2](turn-0002.md): Follow-up?" in session

    log = _git(corpus, "log", "--format=%s").splitlines()
    assert log[:2] == ["turn 20261004-093012-a1b2/2", "turn 20261004-093012-a1b2/1"]
    assert _git(corpus, "status", "--porcelain") == ""


def test_load_session_reads_turns_back_from_files(store: ContextStore):
    store.write_turn(_record(turn=1), session_started_at=T0)
    store.write_turn(_record(turn=2, question="Follow-up?", confidence="low"), session_started_at=T0)
    turns = store.load_session("20261004-093012-a1b2")
    assert [(t["turn"], t["question"], t["confidence"]) for t in turns] == [
        (1, "What was the CET1 ratio?", "medium"),
        (2, "Follow-up?", "low"),
    ]
    assert turns[0]["answer"] == "CET1 was **15.1%**."
    assert turns[0]["timestamp"] == "2026-10-04T09:41:55Z"
    assert turns[0]["tools_used"] == ["memory_search", "semantic_search", "semantic_read"]


def test_load_unknown_session_is_empty(store: ContextStore):
    assert store.load_session("nope") == []


@pytest.mark.parametrize("bad", ["..", "../x", "a/b", "a\\b", ""])
def test_session_ids_cannot_escape_the_corpus(store: ContextStore, bad: str):
    with pytest.raises(ValueError):
        store.load_session(bad)


def test_front_matter_lists_refs_seen_and_flags_unseen_citations():
    base = _result()
    answer = base.answer.model_copy(update={"sources": [
        SourceCitation(ref="openwiki/metrics/cet1-ratio.md#stack", why="seen"),
        SourceCitation(ref="openwiki/made-up.md#x", why="not seen"),
    ]})
    result = AgentResult(**{**base.__dict__, "answer": answer,
                            "semantic_refs_seen": ("openwiki/metrics/cet1-ratio.md#stack", "openwiki/o.md#y")})
    md = render_turn_markdown(TurnRecord("20261004-093012-a1b2", 1, "q", T0, "m", result))
    assert _front_matter(md)["semantic_refs_seen"] == ["openwiki/metrics/cet1-ratio.md#stack", "openwiki/o.md#y"]
    assert _section(md, "Sources cited").splitlines() == [
        "- openwiki/metrics/cet1-ratio.md#stack - why: seen",
        "- openwiki/made-up.md#x - why: not seen [not seen in tool results]",
    ]


def test_front_matter_is_block_style():
    md = render_session_markdown("s1", T0, [(1, "q")])
    assert md.startswith("---\ntype: SessionLog\nsession_id: s1\n")


def test_memory_citations_seen_in_memory_search_are_not_flagged():
    base = _result()
    answer = base.answer.model_copy(update={"sources": [SourceCitation(ref="openwiki/turns/t1.md#a", why="memory")]})
    result = AgentResult(**{**base.__dict__, "answer": answer, "context_refs_seen": ("openwiki/turns/t1.md#a",)})
    md = render_turn_markdown(TurnRecord("20261004-093012-a1b2", 2, "q", T0, "m", result))
    assert _front_matter(md)["context_refs_seen"] == ["openwiki/turns/t1.md#a"]
    assert _section(md, "Sources cited") == "- openwiki/turns/t1.md#a - why: memory"
