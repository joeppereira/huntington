import asyncio
import threading
from pathlib import Path

import pytest

from app.config import Settings
from app.memory_sync import INIT_MARKER, MemorySync


class FakeRunner:
    """Records OpenWiki invocations; can block until released or fail with an exit code."""

    def __init__(self, exit_codes: list[int] | None = None, block: bool = False, error: Exception | None = None):
        self.calls: list[dict] = []
        self._exit_codes = list(exit_codes or [])
        self._error = error
        self.release = threading.Event()
        if not block:
            self.release.set()
        self.started = threading.Event()

    def __call__(self, args: list[str], cwd: Path, env: dict[str, str], log_path: Path, timeout: float) -> int:
        self.calls.append({"args": args, "cwd": cwd, "model": env.get("OPENWIKI_MODEL_ID"), "timeout": timeout})
        self.started.set()
        self.release.wait(10)
        log_path.write_text("line 1\nline 2\nboom: provider error\n", encoding="utf-8")
        if self._error:
            raise self._error
        return self._exit_codes.pop(0) if self._exit_codes else 0


def _sync(settings: Settings, runner: FakeRunner, **overrides) -> MemorySync:
    s = settings.model_copy(update={"context_openwiki_model_id": "claude-haiku-test", **overrides})
    s.context_corpus_path.mkdir(parents=True, exist_ok=True)
    s.logs_path.mkdir(parents=True, exist_ok=True)
    return MemorySync(s, cli_js=Path("cli.js"), runner=runner)


async def _settle(sync: MemorySync) -> None:
    for _ in range(200):
        if sync.status().state in ("idle", "error") and not sync.busy:
            return
        await asyncio.sleep(0.02)
    raise AssertionError(f"sync did not settle: {sync.status()}")


async def test_first_sync_inits_then_updates(settings: Settings):
    runner = FakeRunner()
    sync = _sync(settings, runner)
    sync.notify_turn()
    await _settle(sync)
    sync.notify_turn()
    await _settle(sync)
    assert [c["args"][1:] for c in runner.calls] == [["--init", "--print"], ["--update", "--print"]]
    assert runner.calls[0]["args"][0] == "cli.js"
    assert runner.calls[0]["cwd"] == settings.context_corpus_path
    assert runner.calls[0]["model"] == "claude-haiku-test"
    assert (settings.context_corpus_path / INIT_MARKER).exists()
    status = sync.status()
    assert status.state == "idle" and status.pending_turns == 0
    assert status.last_success_at is not None and status.last_duration_s is not None


async def test_turns_during_a_sync_are_coalesced_into_one_more_run(settings: Settings):
    runner = FakeRunner(block=True)
    sync = _sync(settings, runner)
    sync.notify_turn()
    await asyncio.to_thread(runner.started.wait, 5)
    for _ in range(3):
        sync.notify_turn()
    status = sync.status()
    assert status.state == "syncing" and status.pending_turns == 4
    runner.release.set()
    await _settle(sync)
    assert len(runner.calls) == 2
    assert sync.status().pending_turns == 0


async def test_failure_sets_error_with_log_tail_and_keeps_pending(settings: Settings):
    runner = FakeRunner(exit_codes=[1, 0])
    sync = _sync(settings, runner)
    sync.notify_turn()
    await _settle(sync)
    status = sync.status()
    assert status.state == "error"
    assert "boom: provider error" in status.last_error
    assert status.pending_turns == 1
    assert not (settings.context_corpus_path / INIT_MARKER).exists()

    sync.notify_turn()  # retries, still --init because init never succeeded
    await _settle(sync)
    assert runner.calls[1]["args"][1] == "--init"
    assert sync.status().state == "idle" and sync.status().pending_turns == 0


async def test_runner_exception_is_an_error_state(settings: Settings):
    sync = _sync(settings, FakeRunner(error=TimeoutError("openwiki timed out after 1200 s")))
    sync.notify_turn()
    await _settle(sync)
    assert sync.status().state == "error"
    assert "timed out" in sync.status().last_error


async def test_manual_mode_only_counts_until_requested(settings: Settings):
    runner = FakeRunner()
    sync = _sync(settings, runner, memory_sync_mode="manual")
    sync.notify_turn()
    sync.notify_turn()
    await asyncio.sleep(0.1)
    assert runner.calls == [] and sync.status().pending_turns == 2 and sync.status().state == "idle"
    sync.request_sync()
    await _settle(sync)
    assert len(runner.calls) == 1 and sync.status().pending_turns == 0


async def test_falls_back_to_main_model_and_passes_timeout(settings: Settings):
    runner = FakeRunner()
    sync = _sync(settings, runner, context_openwiki_model_id="", memory_sync_timeout_sec=77)
    sync.request_sync()
    await _settle(sync)
    assert runner.calls[0]["model"] == settings.openwiki_model_id
    assert runner.calls[0]["timeout"] == 77


async def test_stop_cancels_a_running_sync(settings: Settings):
    runner = FakeRunner(block=True)
    sync = _sync(settings, runner)
    sync.notify_turn()
    await asyncio.to_thread(runner.started.wait, 5)
    await sync.stop()
    runner.release.set()
    assert not sync.busy


def test_status_before_any_sync(settings: Settings):
    status = _sync(settings, FakeRunner()).status()
    assert status.model_dump() == {
        "state": "idle", "mode": "per_turn", "pending_turns": 0, "last_success_at": None,
        "last_duration_s": None, "last_error": None, "initialized": False,
    }


def test_marker_from_an_earlier_run_counts_as_initialized(settings: Settings):
    sync = _sync(settings, FakeRunner())
    (settings.context_corpus_path / INIT_MARKER).write_text("x", encoding="utf-8")
    assert sync.status().initialized is True


@pytest.mark.parametrize("bad", [0, -5])
def test_rejects_non_positive_timeout(settings: Settings, bad: int):
    with pytest.raises(ValueError):
        _sync(settings, FakeRunner(), memory_sync_timeout_sec=bad)


async def test_context_sync_uses_its_own_page_concurrency(settings: Settings):
    runner = FakeRunner()
    sync = _sync(settings, runner, openwiki_page_concurrency=3, context_openwiki_page_concurrency=6)
    sync.request_sync()
    await _settle(sync)
    assert sync._env["OPENWIKI_PAGE_CONCURRENCY"] == "6"


async def test_stop_kills_a_real_running_openwiki_process(settings: Settings, tmp_path: Path):
    import psutil

    from app.memory_sync import OpenWikiRunner

    sleeper = tmp_path / "sleep.js"
    sleeper.write_text("setTimeout(() => {}, 60000)\n", encoding="utf-8")
    s = settings.model_copy(update={"context_openwiki_model_id": "x"})
    s.context_corpus_path.mkdir(parents=True, exist_ok=True)
    s.logs_path.mkdir(parents=True, exist_ok=True)
    runner = OpenWikiRunner()
    sync = MemorySync(s, cli_js=sleeper, runner=runner)
    sync.notify_turn()
    for _ in range(100):
        if runner._proc is not None:
            break
        await asyncio.sleep(0.05)
    pid = runner._proc.pid
    assert psutil.pid_exists(pid)

    started = asyncio.get_running_loop().time()
    await asyncio.wait_for(sync.stop(), 10)
    assert asyncio.get_running_loop().time() - started < 5
    await asyncio.sleep(0.5)
    assert not psutil.pid_exists(pid) or psutil.Process(pid).status() == psutil.STATUS_ZOMBIE


async def test_on_success_runs_after_each_successful_sync_only(settings: Settings):
    calls = []

    async def on_success():
        calls.append("synced")

    runner = FakeRunner(exit_codes=[1, 0])
    s = settings.model_copy(update={"context_openwiki_model_id": "x"})
    s.context_corpus_path.mkdir(parents=True, exist_ok=True)
    s.logs_path.mkdir(parents=True, exist_ok=True)
    sync = MemorySync(s, cli_js=Path("cli.js"), runner=runner, on_success=on_success)
    sync.request_sync()
    await _settle(sync)
    assert calls == []  # failed run
    sync.request_sync()
    await _settle(sync)
    assert calls == ["synced"]


async def test_on_success_failure_does_not_break_the_sync(settings: Settings):
    async def broken():
        raise RuntimeError("visualizer restart failed")

    s = settings.model_copy(update={"context_openwiki_model_id": "x"})
    s.context_corpus_path.mkdir(parents=True, exist_ok=True)
    s.logs_path.mkdir(parents=True, exist_ok=True)
    sync = MemorySync(s, cli_js=Path("cli.js"), runner=FakeRunner(), on_success=broken)
    sync.request_sync()
    await _settle(sync)
    assert sync.status().state == "idle" and sync.status().initialized


async def test_reset_stops_a_running_sync_and_clears_state(settings: Settings):
    runner = FakeRunner(exit_codes=[1])
    sync = _sync(settings, runner)
    sync.notify_turn()
    await _settle(sync)
    assert sync.status().state == "error" and sync.status().pending_turns == 1

    blocking = FakeRunner(block=True)
    sync._runner = blocking
    sync.notify_turn()
    await asyncio.to_thread(blocking.started.wait, 5)
    await sync.reset()
    blocking.release.set()
    status = sync.status()
    assert not sync.busy
    assert (status.state, status.pending_turns, status.last_error, status.last_success_at) == ("idle", 0, None, None)
