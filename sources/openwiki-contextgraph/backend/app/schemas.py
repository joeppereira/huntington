"""Pydantic models for the HTTP API (BUILD_SPEC Section 8.5)."""

from typing import Literal

from pydantic import BaseModel, Field, field_validator

from .memory_sync import MemoryStatus
from .retrieval_path import RetrievalPath

ChildStatus = Literal["running", "stopped", "not_built", "not_started"]


class ChildrenStatus(BaseModel):
    semantic_vis: ChildStatus
    context_vis: ChildStatus
    mcp: ChildStatus


class HealthResponse(BaseModel):
    ok: bool
    openwiki_version: str
    children: ChildrenStatus


class ConfigResponse(BaseModel):
    semantic_vis_url: str | None
    context_vis_url: str | None
    semantic_ready: bool


class SessionResponse(BaseModel):
    session_id: str


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=64)
    message: str = Field(min_length=1, max_length=4000)

    @field_validator("message")
    @classmethod
    def not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("message must not be blank")
        return value.strip()


class SourceOut(BaseModel):
    ref: str
    why: str


class TraceStepOut(BaseModel):
    step: int
    tool: str
    input: str
    result: str
    ms: int
    refs: list[str] = []


class TraceOut(BaseModel):
    steps: list[TraceStepOut]
    latency_ms: int
    input_tokens: int
    output_tokens: int
    model: str


class ChatResponse(BaseModel):
    session_id: str
    turn: int
    answer: str
    sources: list[SourceOut]
    confidence: Literal["high", "medium", "low"]
    follow_up_questions: list[str]
    reasoning_summary: str
    trace: TraceOut
    trace_file: str | None  # corpus-relative turn file; None if writing the trace failed
    retrieval: RetrievalPath  # semantic-graph nodes found, opened and cited


class DemoResetResponse(BaseModel):
    session_id: str
    context_vis_url: str | None
    memory: MemoryStatus


class SessionTurnOut(BaseModel):
    turn: int
    timestamp: str
    question: str
    answer: str
    confidence: str
    model: str | None = None
    latency_ms: int | None = None
    tools_used: list[str]
    semantic_pages_read: list[str]


class SessionDetailResponse(BaseModel):
    session_id: str
    turns: list[SessionTurnOut]
