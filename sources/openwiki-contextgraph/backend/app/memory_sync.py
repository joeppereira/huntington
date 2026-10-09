"""Memory sync engine (BUILD_SPEC 8.3): runs OpenWiki over the context corpus in the background.

Each sync is a full OpenWiki agent run, so memory lags behind the chat. Turns that arrive while a sync
is running are coalesced into exactly one follow-up run.
"""

import asyncio
import logging
import subprocess
import threading
import time
from collections.abc import Awaitable, Callable
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from .config import Settings
from .openwiki_cli import build_openwiki_env
from .visualizers import kill_process_tree

logger = logging.getLogger("openwiki_poc")

INIT_MARKER = ".poc-initialized"  # written after the first successful --init; git-ignored in the corpus
LOG_TAIL_LINES = 15

SyncState = Literal["idle", "queued", "syncing", "error"]
# (args after `node`, cwd, env, log file, timeout seconds) -> exit code
Runner = Callable[[list[str], Path, dict[str, str], Path, float], int]


class MemoryStatus(BaseModel):
    state: SyncState
    mode: Literal["per_turn", "manual"]
    pending_turns: int
    last_success_at: str | None
    last_duration_s: float | None
    last_error: str | None
    initialized: bool


class OpenWikiRunner:
    """Runs `node <args>` with output to a log file; kill() stops the whole process tree."""

    def __init__(self) -> None:
        self._proc: subprocess.Popen[bytes] | None = None
        self._lock = threading.Lock()

    def __call__(self, args: list[str], cwd: Path, env: dict[str, str], log_path: Path, timeout: float) -> int:
        with log_path.open("w", encoding="utf-8") as log:
            proc = subprocess.Popen(
                ["node", *args], cwd=cwd, env=env, stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT
            )
            with self._lock:
                self._proc = proc
            try:
                return proc.wait(timeout)
            except subprocess.TimeoutExpired as err:
                kill_process_tree(proc.pid)
                raise TimeoutError(f"openwiki timed out after {timeout:.0f} s") from err
            finally:
                with self._lock:
                    self._proc = None

    def kill(self) -> None:
        with self._lock:
            proc = self._proc
        if proc is not None:
            kill_process_tree(proc.pid)


def _log_tail(path: Path, lines: int = LOG_TAIL_LINES) -> str:
    try:
        return "\n".join(path.read_text(encoding="utf-8", errors="replace").splitlines()[-lines:])
    except OSError:
        return ""


class MemorySync:
    def __init__(
        self,
        settings: Settings,
        cli_js: Path,
        runner: Runner | None = None,
        on_success: Callable[[], Awaitable[None]] | None = None,
    ) -> None:
        if settings.memory_sync_timeout_sec <= 0:
            raise ValueError("MEMORY_SYNC_TIMEOUT_SEC must be positive")
        self._settings = settings
        self._cli_js = cli_js
        self._runner = runner or OpenWikiRunner()
        self._on_success = on_success
        self._env = build_openwiki_env(
            settings,
            model_id=settings.context_openwiki_model_id or None,
            page_concurrency=settings.context_openwiki_page_concurrency,
        )
        self._corpus = settings.context_corpus_path
        self._state: SyncState = "idle"
        self._pending = 0
        self._dirty = False
        self._task: asyncio.Task[None] | None = None
        self._last_success_at: str | None = None
        self._last_duration_s: float | None = None
        self._last_error: str | None = None

    @property
    def busy(self) -> bool:
        return self._task is not None and not self._task.done()

    @property
    def initialized(self) -> bool:
        return (self._corpus / INIT_MARKER).exists()

    def status(self) -> MemoryStatus:
        return MemoryStatus(
            state=self._state,
            mode=self._settings.memory_sync_mode,
            pending_turns=self._pending,
            last_success_at=self._last_success_at,
            last_duration_s=self._last_duration_s,
            last_error=self._last_error,
            initialized=self.initialized,
        )

    def notify_turn(self) -> None:
        """A turn was committed to the corpus. Syncs now in per_turn mode; only counts in manual mode."""
        self._pending += 1
        if self._settings.memory_sync_mode == "per_turn":
            self._kick()

    def request_sync(self) -> None:
        self._kick()

    def _kick(self) -> None:
        if self.busy:
            self._dirty = True
            return
        self._state = "queued"
        self._task = asyncio.get_running_loop().create_task(self._run_until_clean(), name="memory-sync")

    async def _run_until_clean(self) -> None:
        while True:
            self._dirty = False
            if not await self._run_once() or not self._dirty:
                return

    async def _run_once(self) -> bool:
        synced_turns = self._pending
        self._state = "syncing"
        command = "--update" if self.initialized else "--init"
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        log_path = self._settings.logs_path / f"context-sync-{stamp}.log"
        args = [str(self._cli_js), command, "--print"]
        started = time.monotonic()
        try:
            code = await asyncio.to_thread(
                self._runner, args, self._corpus, self._env, log_path, float(self._settings.memory_sync_timeout_sec)
            )
        except Exception as err:  # timeout, OS error: report, keep pending turns
            return self._fail(f"{err}\n{_log_tail(log_path)}")
        if code != 0:
            return self._fail(f"openwiki {command} exited with code {code}\n{_log_tail(log_path)}")
        (self._corpus / INIT_MARKER).write_text(datetime.now(timezone.utc).isoformat(), encoding="utf-8")
        await self._after_success()
        self._pending = max(0, self._pending - synced_turns)
        self._last_success_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        self._last_duration_s = round(time.monotonic() - started, 1)
        self._last_error = None
        self._state = "idle"
        return True

    async def _after_success(self) -> None:
        # Runs before last_success_at changes, so clients that reload on it see the refreshed view.
        if self._on_success is None:
            return
        try:
            await self._on_success()
        except Exception:
            logger.exception("post-sync hook failed")

    def _fail(self, message: str) -> bool:
        self._last_error = message.strip()
        self._state = "error"
        return False

    async def reset(self) -> None:
        """Stop any running sync and forget all state (used when the context corpus is wiped)."""
        await self.stop()
        self._state = "idle"
        self._pending = 0
        self._dirty = False
        self._last_success_at = None
        self._last_duration_s = None
        self._last_error = None

    async def stop(self) -> None:
        task, self._task = self._task, None
        if isinstance(self._runner, OpenWikiRunner):
            self._runner.kill()
        if task is not None and not task.done():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
