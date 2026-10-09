import json

import pytest
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from app.agent import AgentAnswer, SUBMIT_TOOL_NAME, answer_from_messages, final_text, submit_answer_tool

ANSWER = {
    "answer": "CET1 was 15.1%.",
    "sources": [{"ref": "openwiki/metrics/cet1-ratio.md#x", "why": "states the ratio"}],
    "reasoning_summary": "Searched for CET1.",
    "confidence": "high",
    "follow_up_questions": [],
}


def test_answer_from_submit_tool_message():
    msgs = [HumanMessage("q"), ToolMessage(json.dumps(ANSWER), tool_call_id="1", name=SUBMIT_TOOL_NAME)]
    answer = answer_from_messages(msgs)
    assert answer == AgentAnswer.model_validate(ANSWER)


def test_no_answer_when_model_replied_in_plain_text():
    msgs = [HumanMessage("q"), AIMessage("CET1 was 15.1%.")]
    assert answer_from_messages(msgs) is None
    assert final_text(msgs) == "CET1 was 15.1%."


def test_final_text_joins_text_blocks():
    msg = AIMessage(content=[{"type": "text", "text": "Part 1."}, {"type": "tool_use", "id": "x", "name": "t", "input": {}},
                             {"type": "text", "text": "Part 2."}])
    assert final_text([msg]) == "Part 1.\nPart 2."


async def test_submit_tool_validates_and_ends_the_run():
    tool = submit_answer_tool()
    assert tool.return_direct is True
    out = await tool.ainvoke(ANSWER)
    assert AgentAnswer.model_validate_json(out).answer == "CET1 was 15.1%."
    with pytest.raises(Exception):
        await tool.ainvoke({**ANSWER, "confidence": "certain"})


class _StubGraph:
    def __init__(self, messages=None, error=None):
        self._messages, self._error = messages, error

    async def ainvoke(self, _input, config):
        if self._error:
            raise self._error
        return {"messages": self._messages}


class _StubExtractor:
    def __init__(self):
        self.prompts = []

    async def ainvoke(self, prompt, config):
        self.prompts.append(prompt)
        return AgentAnswer.model_validate(ANSWER)


def _agent(graph, extractor=None):
    from app.agent import QAAgent

    agent = QAAgent("claude-test", "key", [])
    agent._graph = graph
    agent._extractor = extractor or _StubExtractor()
    return agent


async def test_ask_uses_submitted_answer_without_extraction():
    extractor = _StubExtractor()
    msgs = [HumanMessage("q"), ToolMessage(json.dumps(ANSWER), tool_call_id="1", name=SUBMIT_TOOL_NAME)]
    result = await _agent(_StubGraph(msgs), extractor).ask("q", ())
    assert result.answer.answer == "CET1 was 15.1%."
    assert extractor.prompts == []
    assert result.latency_ms >= 0


async def test_ask_structures_a_plain_text_reply():
    extractor = _StubExtractor()
    result = await _agent(_StubGraph([HumanMessage("q"), AIMessage("CET1 was 15.1%.")]), extractor).ask("q", ())
    assert result.answer.confidence == "high"
    assert "CET1 was 15.1%." in extractor.prompts[0] and "Question: q" in extractor.prompts[0]


async def test_ask_fails_cleanly_on_runaway_loop_or_empty_reply():
    from langgraph.errors import GraphRecursionError

    with pytest.raises(RuntimeError, match="did not finish"):
        await _agent(_StubGraph(error=GraphRecursionError("limit"))).ask("q", ())
    with pytest.raises(RuntimeError, match="without an answer"):
        await _agent(_StubGraph([HumanMessage("q"), AIMessage("")])).ask("q", ())


def test_agent_requires_api_key():
    from app.agent import QAAgent

    with pytest.raises(ValueError):
        QAAgent("claude-test", "", [])


async def test_submit_tool_keeps_only_three_follow_ups():
    out = await submit_answer_tool().ainvoke({**ANSWER, "follow_up_questions": ["a", "b", "c", "d"]})
    assert AgentAnswer.model_validate_json(out).follow_up_questions == ["a", "b", "c"]


def test_failed_submission_is_not_an_answer():
    msgs = [HumanMessage("q"), ToolMessage("Error invoking tool 'submit_answer'", tool_call_id="1",
                                            name=SUBMIT_TOOL_NAME, status="error")]
    assert answer_from_messages(msgs) is None


async def test_ask_recovers_the_answer_text_from_a_failed_submission():
    bad_args = {**ANSWER, "answer": "Recovered answer text.", "confidence": "certain"}
    msgs = [
        HumanMessage("q"),
        AIMessage("", tool_calls=[{"name": SUBMIT_TOOL_NAME, "args": bad_args, "id": "c1", "type": "tool_call"}]),
        ToolMessage("Error invoking tool 'submit_answer'", tool_call_id="c1", name=SUBMIT_TOOL_NAME, status="error"),
    ]
    extractor = _StubExtractor()
    result = await _agent(_StubGraph(msgs), extractor).ask("q", ())
    assert result.answer.answer == "CET1 was 15.1%."  # from the stub extractor
    assert "Recovered answer text." in extractor.prompts[0]
