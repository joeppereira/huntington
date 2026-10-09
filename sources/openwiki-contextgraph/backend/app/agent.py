"""The MHFC Q&A agent: LangChain create_agent + ChatAnthropic over the OpenWiki tools (BUILD_SPEC 8.4)."""

import time
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Literal, Protocol

from langchain.agents import create_agent
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AIMessage, BaseMessage, ToolMessage
from langchain_core.tools import BaseTool, StructuredTool
from langgraph.errors import GraphRecursionError
from pydantic import BaseModel, Field

from .tracing import TraceRecorder, TraceStep

HISTORY_TURNS = 6

SYSTEM_PROMPT = """\
You answer questions about Meridian Harbor Financial Corp., a fictional bank, using its knowledge wiki.
Always ground answers in the wiki: call `semantic_search`, then `semantic_read` on the most relevant refs
before answering numeric or factual questions. Quote numbers exactly with units and as-of dates, and cite
the refs you used. If the user refers to earlier conversation ("as you said", "that model"), check
`memory_search` and the chat history first. For questions about the conversation itself (what was asked,
earlier answers, decisions, sources used, where you were unsure), always call `memory_search` first and
cite the memory refs you used; then use the chat history only for recent turns that memory does not have
yet (memory lags behind the chat). If the wiki does not contain the answer, say so; do not use
outside knowledge about real banks. Keep answers concise.

You can explain how the Excel models work, but you cannot run them with new inputs. If asked for a new
scenario or changed assumption (e.g. "what if buybacks doubled?"), do not calculate, estimate or
approximate the result yourself, not even roughly or "for illustration". Instead: say you cannot run the
model with new inputs; name the model and the sheet and cell that hold the input (e.g. the Assumptions
sheet) and the outputs that would change; give the current reported figures from the wiki for context;
and set confidence to "low" for the requested number.

When you have enough information, call `submit_answer` once with your final answer; do not reply with
plain text. In `sources`, list each wiki ref you relied on (page#section exactly as returned by the tools)
with a short reason. In `reasoning_summary`, write 2-5 sentences on what you looked up, why, and what you
chose.
"""

SUBMIT_TOOL_NAME = "submit_answer"
# Caps a runaway tool loop (each tool round is two graph steps).
RECURSION_LIMIT = 40

EXTRACTION_PROMPT = """\
Turn this answer from the MHFC Q&A agent into the structured format. Keep the answer text as written.
Only cite refs that appear in the list of refs the agent read; if none apply, return an empty list.

Question: {question}

Answer: {answer}

Refs the agent read: {refs}
"""


class SourceCitation(BaseModel):
    ref: str = Field(description='Wiki ref, e.g. "openwiki/models/cecl-allowance-model.md#upstream-apis"')
    why: str


MAX_FOLLOW_UPS = 3


class AgentAnswer(BaseModel):
    answer: str
    sources: list[SourceCitation]
    reasoning_summary: str = Field(description="2-5 sentences: what was looked up and why, what was chosen")
    confidence: Literal["high", "medium", "low"]
    follow_up_questions: list[str] = Field(max_length=MAX_FOLLOW_UPS, description="0-3 useful follow-up questions")


class SubmitAnswerArgs(AgentAnswer):
    """Lenient input for submit_answer: extra follow-ups are trimmed instead of failing the submission."""

    follow_up_questions: list[str] = Field(default_factory=list, description="0-3 useful follow-up questions")


@dataclass(frozen=True)
class Turn:
    question: str
    answer: str


@dataclass(frozen=True)
class AgentResult:
    answer: AgentAnswer
    steps: tuple[TraceStep, ...]
    tools_used: tuple[str, ...]
    semantic_pages_read: tuple[str, ...]
    context_pages_read: tuple[str, ...]
    input_tokens: int
    output_tokens: int
    latency_ms: int
    semantic_refs_seen: tuple[str, ...] = ()
    context_refs_seen: tuple[str, ...] = ()


class Answerer(Protocol):
    model_id: str

    async def ask(self, question: str, history: tuple[Turn, ...]) -> AgentResult: ...


def history_messages(turns: Sequence[Turn], limit: int = HISTORY_TURNS) -> list[dict[str, str]]:
    """The last `limit` turns as chat messages: memory_search cannot see turns that are not synced yet."""
    messages: list[dict[str, str]] = []
    for turn in turns[-limit:]:
        messages.append({"role": "user", "content": turn.question})
        messages.append({"role": "assistant", "content": turn.answer})
    return messages


def submit_answer_tool() -> BaseTool:
    """Final-answer tool that ends the run (return_direct).

    Used instead of create_agent's response_format: with claude-sonnet-5-5 + langchain 1.4, every
    response_format strategy either loops on tool calls until the recursion limit (auto/provider) or is
    rejected (ToolStrategy forces tool_choice, which this model does not support). See
    docs/openwiki-findings.md.
    """

    async def submit_answer(**fields: Any) -> str:
        follow_ups = list(fields.get("follow_up_questions") or [])[:MAX_FOLLOW_UPS]
        return AgentAnswer(**{**fields, "follow_up_questions": follow_ups}).model_dump_json()

    return StructuredTool.from_function(
        coroutine=submit_answer,
        name=SUBMIT_TOOL_NAME,
        description="Submit your final answer. Call this exactly once, when you are done researching.",
        args_schema=SubmitAnswerArgs,
        return_direct=True,
    )


def answer_from_messages(messages: Sequence[BaseMessage]) -> AgentAnswer | None:
    last = messages[-1] if messages else None
    if isinstance(last, ToolMessage) and last.name == SUBMIT_TOOL_NAME and last.status != "error":
        return AgentAnswer.model_validate_json(last.text)
    return None


def attempted_answer_text(messages: Sequence[BaseMessage]) -> str:
    """The `answer` argument of the latest submit_answer call, even if that call failed validation."""
    for message in reversed(messages):
        if isinstance(message, AIMessage):
            for call in reversed(message.tool_calls):
                if call["name"] == SUBMIT_TOOL_NAME:
                    return str(call["args"].get("answer", "")).strip()
    return ""


def final_text(messages: Sequence[BaseMessage]) -> str:
    last = messages[-1] if messages else None
    if not isinstance(last, AIMessage):
        return ""
    if isinstance(last.content, str):
        return last.content.strip()
    texts = [block.get("text", "") for block in last.content if isinstance(block, dict) and block.get("type") == "text"]
    return "\n".join(t.strip() for t in texts if t.strip())


class QAAgent:
    def __init__(self, model_id: str, api_key: str, tools: Sequence[BaseTool], model=None) -> None:
        if model is None and not api_key:
            raise ValueError("ANTHROPIC_API_KEY is not configured")
        self.model_id = model_id
        if model is None:
            model = ChatAnthropic(model=model_id, api_key=api_key, max_tokens=4096, timeout=120, max_retries=2)
            # Fallback when the model answers in plain text: native JSON-schema output (no forced tool_choice).
            self._extractor = model.with_structured_output(AgentAnswer, method="json_schema")
        else:
            # Injected model (e.g. ChatAnthropicVertex): json_schema mode is Anthropic-API-only,
            # so use the default tool-calling structured output.
            self._extractor = model.with_structured_output(AgentAnswer)
        self._graph = create_agent(model, [*tools, submit_answer_tool()], system_prompt=SYSTEM_PROMPT)

    async def _extract(self, question: str, text: str, refs: Sequence[str], recorder: TraceRecorder) -> AgentAnswer:
        if not text:
            raise RuntimeError("agent finished without an answer")
        prompt = EXTRACTION_PROMPT.format(question=question, answer=text, refs=", ".join(refs) or "(none)")
        answer = await self._extractor.ainvoke(prompt, config={"callbacks": [recorder]})
        if not isinstance(answer, AgentAnswer):
            raise RuntimeError("could not structure the agent's answer")
        return answer

    async def ask(self, question: str, history: tuple[Turn, ...]) -> AgentResult:
        recorder = TraceRecorder()
        started = time.perf_counter()
        messages = [*history_messages(history), {"role": "user", "content": question}]
        config = {"callbacks": [recorder], "recursion_limit": RECURSION_LIMIT}
        try:
            state = await self._graph.ainvoke({"messages": messages}, config=config)
        except GraphRecursionError as err:
            raise RuntimeError(f"agent did not finish within {RECURSION_LIMIT} steps") from err
        answer = answer_from_messages(state["messages"])
        if answer is None:
            refs = [*recorder.semantic_pages_read(), *recorder.context_pages_read()]
            text = final_text(state["messages"]) or attempted_answer_text(state["messages"])
            answer = await self._extract(question, text, refs, recorder)
        input_tokens, output_tokens = recorder.token_usage()
        return AgentResult(
            answer=answer,
            steps=tuple(recorder.steps()),
            tools_used=tuple(recorder.tools_used()),
            semantic_pages_read=tuple(recorder.semantic_pages_read()),
            context_pages_read=tuple(recorder.context_pages_read()),
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=int((time.perf_counter() - started) * 1000),
            semantic_refs_seen=tuple(recorder.semantic_refs_seen()),
            context_refs_seen=tuple(recorder.context_refs_seen()),
        )
