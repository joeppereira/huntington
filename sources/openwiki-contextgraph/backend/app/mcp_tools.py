"""OpenWiki MCP client: one stdio session plus root-bound LangChain tools.

Each tool wraps OpenWiki's `openwiki_search` or `openwiki_read` with the absolute wiki root filled
in (BUILD_SPEC 8.4), so the model never handles Windows paths.

Ratchet R7 (serve-path switchover): the agent's SEMANTIC query path no longer goes through MCP —
`semantic_search`/`semantic_read` here are deprecated and kept for build-time/debugging only; the
in-process replacements live in app/semantic_tools.py. The MCP session remains in use for the
MEMORY (context) wiki tools and build-time operations.
"""

import asyncio
import json
from contextlib import AsyncExitStack
from pathlib import Path
from typing import Protocol

from langchain_core.tools import BaseTool, StructuredTool
from langchain_mcp_adapters.client import MultiServerMCPClient
from mcp import ClientSession
from pydantic import BaseModel, Field

from .config import Settings
from .openwiki_cli import build_openwiki_env, resolve_cli_js

REQUIRED_MCP_TOOLS = {"openwiki_search", "openwiki_read"}
MEMORY_NOT_BUILT = {"results": [], "note": "memory not built yet"}


class ToolCallError(Exception):
    """OpenWiki reported an error (e.g. unknown section); surfaced to the model as text."""


class OpenWikiCaller(Protocol):
    async def call(self, name: str, arguments: dict) -> str: ...


class OpenWikiMCP:
    """Owns the `openwiki mcp` stdio process for the app's lifetime.

    The session's anyio cancel scopes must be entered and exited in the same task, so a dedicated
    owner task opens it, waits for stop(), and closes it; start()/stop() can be called from any task.
    """

    def __init__(self, settings: Settings) -> None:
        self._connections = {
            "openwiki": {
                "transport": "stdio",
                "command": "node",
                "args": [str(resolve_cli_js(settings)), "mcp", "--host", "poc-agent"],
                "env": build_openwiki_env(settings),
            }
        }
        self._session: ClientSession | None = None
        self._owner: asyncio.Task[None] | None = None
        self._stop = asyncio.Event()

    @property
    def is_running(self) -> bool:
        return self._session is not None and self._owner is not None and not self._owner.done()

    async def start(self, timeout: float = 60.0) -> None:
        ready: asyncio.Future[ClientSession] = asyncio.get_running_loop().create_future()
        self._stop = asyncio.Event()
        self._owner = asyncio.create_task(self._own_session(ready), name="openwiki-mcp")
        try:
            self._session = await asyncio.wait_for(asyncio.shield(ready), timeout)
        except BaseException:
            await self.stop()
            raise

    async def _own_session(self, ready: "asyncio.Future[ClientSession]") -> None:
        try:
            async with AsyncExitStack() as stack:
                client = MultiServerMCPClient(self._connections)
                session = await stack.enter_async_context(client.session("openwiki"))
                available = {tool.name for tool in (await session.list_tools()).tools}
                missing = REQUIRED_MCP_TOOLS - available
                if missing:
                    raise RuntimeError(f"OpenWiki MCP server is missing tools: {sorted(missing)}")
                ready.set_result(session)
                await self._stop.wait()
        except BaseException as err:
            if not ready.done():
                ready.set_exception(err)
            if not isinstance(err, (Exception, asyncio.CancelledError)):
                raise

    async def stop(self) -> None:
        owner, self._owner, self._session = self._owner, None, None
        if owner is None:
            return
        self._stop.set()
        try:
            await asyncio.wait_for(owner, 10)
        except (asyncio.TimeoutError, asyncio.CancelledError, Exception):
            owner.cancel()

    async def call(self, name: str, arguments: dict) -> str:
        if self._session is None:
            raise ToolCallError("OpenWiki MCP server is not running")
        result = await self._session.call_tool(name, arguments)
        text = "\n".join(block.text for block in result.content if getattr(block, "type", "") == "text")
        if result.isError:
            raise ToolCallError(text or f"{name} failed")
        return text


class SearchArgs(BaseModel):
    query: str = Field(min_length=1, max_length=2000, description="What to look for, in plain words.")
    limit: int = Field(default=8, ge=1, le=20, description="Maximum number of ranked results.")


class MemorySearchArgs(SearchArgs):
    limit: int = Field(default=5, ge=1, le=20, description="Maximum number of ranked results.")


class ReadArgs(BaseModel):
    page: str = Field(min_length=1, max_length=1000, description='Page from a search ref, e.g. "openwiki/models/x.md".')
    sections: list[str] = Field(
        min_length=1, max_length=20, description='Heading anchors from search refs (the part after "#").'
    )


class OpenWikiTools:
    def __init__(self, caller: OpenWikiCaller, semantic_root: Path, context_root: Path) -> None:
        self._caller = caller
        self._semantic_root = semantic_root
        self._context_root = context_root

    def _memory_built(self) -> bool:
        return (self._context_root / "openwiki" / "index.md").exists()

    async def _call(self, name: str, arguments: dict) -> str:
        try:
            return await self._caller.call(name, arguments)
        except ToolCallError as err:
            return f"Error: {err}"

    async def semantic_search(self, query: str, limit: int = 8) -> str:
        """Deprecated (ratchet R7): the agent's semantic query path is served in-process by
        app.semantic_tools.SemanticToolkit. Kept for build-time/debugging only."""
        return await self._call("openwiki_search", {"root": str(self._semantic_root), "query": query, "limit": limit})

    async def semantic_read(self, page: str, sections: list[str]) -> str:
        """Deprecated (ratchet R7): see semantic_search above."""
        return await self._call("openwiki_read", {"root": str(self._semantic_root), "page": page, "sections": sections})

    async def memory_search(self, query: str, limit: int = 5) -> str:
        if not self._memory_built():
            return json.dumps(MEMORY_NOT_BUILT)
        return await self._call("openwiki_search", {"root": str(self._context_root), "query": query, "limit": limit})

    async def memory_read(self, page: str, sections: list[str]) -> str:
        if not self._memory_built():
            return json.dumps(MEMORY_NOT_BUILT)
        return await self._call("openwiki_read", {"root": str(self._context_root), "page": page, "sections": sections})

    def as_memory_langchain_tools(self) -> list[BaseTool]:
        """The memory-wiki tools only: what the agent still gets from MCP after ratchet R7."""
        return [t for t in self.as_langchain_tools() if t.name.startswith("memory_")]

    def as_langchain_tools(self) -> list[BaseTool]:
        """All four tools. The semantic pair is deprecated for the agent's query path (R7):
        wire as_memory_langchain_tools() plus app.semantic_tools into the agent instead."""
        return [
            StructuredTool.from_function(
                coroutine=self.semantic_search,
                name="semantic_search",
                description="Search the CNB knowledge wiki (systems, interfaces, teams, policies, decisions, incidents, datasets). "
                "Returns ranked sections with refs like openwiki/models/x.md#section.",
                args_schema=SearchArgs,
            ),
            StructuredTool.from_function(
                coroutine=self.semantic_read,
                name="semantic_read",
                description="Read complete sections of a knowledge-wiki page, using page and anchors from search refs.",
                args_schema=ReadArgs,
            ),
            StructuredTool.from_function(
                coroutine=self.memory_search,
                name="memory_search",
                description="Search your memory wiki of earlier conversation turns, decisions and sources. "
                "It lags behind the chat; recent turns are in the chat history instead.",
                args_schema=MemorySearchArgs,
            ),
            StructuredTool.from_function(
                coroutine=self.memory_read,
                name="memory_read",
                description="Read complete sections of a memory-wiki page, using page and anchors from memory_search refs.",
                args_schema=ReadArgs,
            ),
        ]
