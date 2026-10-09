"""FastAPI app: the single process the user starts. It supervises the OpenWiki child processes."""

import asyncio
import logging
from collections.abc import AsyncIterator, Callable, Sequence
from contextlib import asynccontextmanager
from dataclasses import asdict, dataclass
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.tools import BaseTool

from .agent import AgentResult, Answerer, QAAgent, Turn
from .config import Settings
from .context_store import ContextStore, TurnRecord, reset_context_corpus
from .mcp_tools import OpenWikiMCP, OpenWikiTools
from .memory_sync import MemoryStatus, MemorySync, Runner
from .retrieval_path import RetrievalPath, SemanticGraphCache, build_retrieval_path
from .openwiki_cli import build_openwiki_env, openwiki_version, resolve_cli_js
from .schemas import (
    ChatRequest,
    ChatResponse,
    ChildrenStatus,
    ChildStatus,
    ConfigResponse,
    DemoResetResponse,
    HealthResponse,
    SessionDetailResponse,
    SessionResponse,
    SourceOut,
    TraceOut,
    TraceStepOut,
)
from .sessions import SessionStore
from .visualizers import Visualizer

logger = logging.getLogger("openwiki_poc")


def _configure_logging() -> None:
    # uvicorn only configures its own loggers; without this our INFO lines are dropped.
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

AgentFactory = Callable[[Settings, Sequence[BaseTool]], Answerer]


def default_agent_factory(settings: Settings, tools: Sequence[BaseTool]) -> Answerer:
    if settings.google_application_credentials:
        # Claude on Vertex AI Model Garden via the service-account key (the Anthropic
        # API key path stays as fallback when no Google credentials are configured).
        import os

        from langchain_google_vertexai.model_garden import ChatAnthropicVertex

        os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", settings.google_application_credentials)
        model = ChatAnthropicVertex(
            model_name=settings.agent_model_id,
            project=settings.google_cloud_project,
            location=settings.google_cloud_location,
            max_tokens=4096,
        )
        return QAAgent(settings.agent_model_id, "vertex", tools, model=model)
    return QAAgent(settings.agent_model_id, settings.anthropic_api_key, tools)


@dataclass(frozen=True)
class Runtime:
    settings: Settings
    openwiki_version: str
    semantic_vis: Visualizer | None  # None until the semantic wiki has been built
    context_vis: Visualizer
    mcp: OpenWikiMCP
    agent: Answerer
    sessions: SessionStore
    context_store: ContextStore
    memory_sync: MemorySync
    semantic_graph: SemanticGraphCache


def _start_visualizers(settings: Settings) -> tuple[str, Visualizer | None, Visualizer]:
    cli_js = resolve_cli_js(settings)
    env = build_openwiki_env(settings)
    logs = settings.logs_path

    if settings.reset_context_on_start or not settings.context_corpus_path.exists():
        reset_context_corpus(settings)

    semantic_vis = None
    if settings.semantic_ready:
        semantic_vis = Visualizer(
            "semantic", cli_js, settings.semantic_corpus_path / "openwiki",
            settings.semantic_vis_port, env, logs / "vis-semantic.log",
        )
        logger.info("semantic visualizer: %s", semantic_vis.start())
    else:
        logger.warning("semantic wiki not built; run scripts/build-semantic.ps1")

    context_vis = Visualizer(
        "context", cli_js, settings.context_corpus_path / "openwiki",
        settings.context_vis_port, env, logs / "vis-context.log",
    )
    try:
        logger.info("context visualizer: %s", context_vis.start())
    except Exception:
        if semantic_vis:
            semantic_vis.stop()
        raise
    return openwiki_version(cli_js), semantic_vis, context_vis


async def _start_runtime(settings: Settings, agent_factory: AgentFactory, sync_runner: Runner | None) -> Runtime:
    version, semantic_vis, context_vis = _start_visualizers(settings)
    mcp = OpenWikiMCP(settings)
    try:
        await mcp.start()
        tools = OpenWikiTools(mcp, settings.semantic_corpus_path, settings.context_corpus_path)
        agent = agent_factory(settings, tools.as_langchain_tools())
    except BaseException:
        await mcp.stop()
        for vis in (semantic_vis, context_vis):
            if vis is not None:
                vis.stop()
        raise
    context_store = ContextStore(settings.context_corpus_path)
    async def refresh_context_graph() -> None:
        # OpenWiki --init deletes and recreates openwiki/, which silently kills the visualizer's
        # recursive fs.watch; a restart re-scans the folder (same port, it was just freed).
        url = await asyncio.to_thread(context_vis.restart)
        logger.info("context visualizer restarted after memory sync: %s", url)

    memory_sync = MemorySync(settings, resolve_cli_js(settings), runner=sync_runner, on_success=refresh_context_graph)
    semantic_graph = SemanticGraphCache(lambda: semantic_vis.url if semantic_vis else None)
    return Runtime(
        settings, version, semantic_vis, context_vis, mcp, agent, SessionStore(), context_store, memory_sync,
        semantic_graph,
    )


async def _stop_runtime(runtime: Runtime) -> None:
    await runtime.memory_sync.stop()
    await runtime.mcp.stop()
    for vis in (runtime.semantic_vis, runtime.context_vis):
        if vis is not None:
            vis.stop()


def _vis_status(vis: Visualizer | None) -> ChildStatus:
    if vis is None:
        return "not_built"
    return "running" if vis.is_running else "stopped"


def _chat_response(
    session_id: str,
    turn: int,
    model: str,
    result: AgentResult,
    trace_file: str | None,
    retrieval: RetrievalPath,
) -> ChatResponse:
    answer = result.answer
    return ChatResponse(
        session_id=session_id,
        turn=turn,
        answer=answer.answer,
        sources=[SourceOut(ref=s.ref, why=s.why) for s in answer.sources],
        confidence=answer.confidence,
        follow_up_questions=answer.follow_up_questions,
        reasoning_summary=answer.reasoning_summary,
        trace=TraceOut(
            steps=[TraceStepOut(**asdict(step)) for step in result.steps],
            latency_ms=result.latency_ms,
            input_tokens=result.input_tokens,
            output_tokens=result.output_tokens,
            model=model,
        ),
        trace_file=trace_file,
        retrieval=retrieval,
    )


async def _save_trace(rt: Runtime, session_id: str, turn: int, question: str, result: AgentResult) -> str | None:
    """Write and commit the turn trace. A failure is logged but never loses the answer."""
    info = rt.sessions.get(session_id)
    started_at = info.started_at if info else datetime.now(timezone.utc)
    record = TurnRecord(session_id, turn, question, datetime.now(timezone.utc), rt.agent.model_id, result)
    try:
        path = await asyncio.to_thread(rt.context_store.write_turn, record, started_at)
    except Exception:
        logger.exception("could not write the trace for %s turn %d", session_id, turn)
        return None
    return path.relative_to(rt.settings.context_corpus_path).as_posix()


def create_app(
    settings: Settings | None = None,
    agent_factory: AgentFactory | None = None,
    sync_runner: Runner | None = None,
) -> FastAPI:
    settings = settings or Settings()
    factory = agent_factory or default_agent_factory
    reset_lock = asyncio.Lock()
    _configure_logging()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        settings.logs_path.mkdir(parents=True, exist_ok=True)
        app.state.runtime = await _start_runtime(settings, factory, sync_runner)
        try:
            yield
        finally:
            await _stop_runtime(app.state.runtime)

    app = FastAPI(title="OpenWiki Graph POC", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.frontend_origin],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/api/health", response_model=HealthResponse)
    def health(request: Request) -> HealthResponse:
        rt: Runtime = request.app.state.runtime
        children = ChildrenStatus(
            semantic_vis=_vis_status(rt.semantic_vis),
            context_vis=_vis_status(rt.context_vis),
            mcp="running" if rt.mcp.is_running else "stopped",
        )
        ok = rt.context_vis.is_running and rt.mcp.is_running and children.semantic_vis != "stopped"
        return HealthResponse(ok=ok, openwiki_version=rt.openwiki_version, children=children)

    @app.get("/api/config", response_model=ConfigResponse)
    def config(request: Request) -> ConfigResponse:
        rt: Runtime = request.app.state.runtime
        return ConfigResponse(
            semantic_vis_url=rt.semantic_vis.url if rt.semantic_vis else None,
            context_vis_url=rt.context_vis.url,
            semantic_ready=rt.settings.semantic_ready,
        )

    @app.post("/api/sessions", response_model=SessionResponse)
    def create_session(request: Request) -> SessionResponse:
        rt: Runtime = request.app.state.runtime
        return SessionResponse(session_id=rt.sessions.create())

    @app.post("/api/chat", response_model=ChatResponse)
    async def chat(body: ChatRequest, request: Request) -> ChatResponse:
        rt: Runtime = request.app.state.runtime
        if not rt.settings.semantic_ready:
            raise HTTPException(409, "The semantic wiki is not built yet. Run scripts/build-semantic.ps1.")
        history = rt.sessions.history(body.session_id)
        if history is None:
            raise HTTPException(404, f"Unknown session {body.session_id}; start one with POST /api/sessions.")
        try:
            result = await rt.agent.ask(body.message, history)
        except Exception as err:
            logger.exception("agent failed for session %s", body.session_id)
            raise HTTPException(502, f"The agent failed: {err}") from err
        turn = rt.sessions.append(body.session_id, Turn(question=body.message, answer=result.answer.answer))
        trace_file = await _save_trace(rt, body.session_id, turn, body.message, result)
        if trace_file is not None:
            rt.memory_sync.notify_turn()
        graph = await asyncio.to_thread(rt.semantic_graph.get)
        retrieval = build_retrieval_path(result.steps, [s.ref for s in result.answer.sources], graph)
        return _chat_response(body.session_id, turn, rt.agent.model_id, result, trace_file, retrieval)

    @app.get("/api/memory/status", response_model=MemoryStatus)
    def memory_status(request: Request) -> MemoryStatus:
        return request.app.state.runtime.memory_sync.status()

    @app.post("/api/memory/sync", response_model=MemoryStatus, status_code=202)
    async def memory_sync_now(request: Request) -> MemoryStatus:  # async: the sync task needs the event loop
        rt: Runtime = request.app.state.runtime
        rt.memory_sync.request_sync()
        return rt.memory_sync.status()

    @app.post("/api/demo/reset", response_model=DemoResetResponse)
    async def demo_reset(request: Request) -> DemoResetResponse:
        """Wipe agent memory: stop syncing, recreate the context corpus, restart its visualizer."""
        rt: Runtime = request.app.state.runtime
        async with reset_lock:
            await rt.memory_sync.reset()
            # Windows will not delete a folder another process is watching, so stop the visualizer first.
            await asyncio.to_thread(rt.context_vis.stop)
            try:
                await asyncio.to_thread(reset_context_corpus, rt.settings)
            except Exception as err:
                logger.exception("demo reset failed")
                raise HTTPException(500, f"Could not wipe the memory folder: {err}") from err
            finally:
                await asyncio.to_thread(rt.context_vis.start)
            rt.sessions.clear()
            session_id = rt.sessions.create()
        logger.info("demo reset: memory wiped, new session %s", session_id)
        return DemoResetResponse(
            session_id=session_id,
            context_vis_url=rt.context_vis.url,
            memory=rt.memory_sync.status(),
        )

    @app.get("/api/sessions/{session_id}", response_model=SessionDetailResponse)
    async def get_session(session_id: str, request: Request) -> SessionDetailResponse:
        rt: Runtime = request.app.state.runtime
        try:
            turns = await asyncio.to_thread(rt.context_store.load_session, session_id)
        except ValueError as err:
            raise HTTPException(404, f"Unknown session {session_id}") from err
        if not turns and rt.sessions.get(session_id) is None:
            raise HTTPException(404, f"Unknown session {session_id}")
        return SessionDetailResponse(session_id=session_id, turns=turns)

    return app
