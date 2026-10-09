import time

from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app
from tests.test_chat_api import FakeAgent
from tests.test_memory_sync import FakeRunner


def _client(settings: Settings, runner: FakeRunner, **overrides) -> TestClient:
    s = settings.model_copy(update=overrides)
    return TestClient(create_app(s, agent_factory=lambda _s, _t: FakeAgent(), sync_runner=runner))


def _wait_idle(client: TestClient) -> dict:
    for _ in range(100):
        status = client.get("/api/memory/status").json()
        if status["state"] in ("idle", "error"):
            return status
        time.sleep(0.05)
    raise AssertionError(status)


def test_status_starts_idle(settings: Settings):
    with _client(settings, FakeRunner()) as client:
        status = client.get("/api/memory/status").json()
        assert status["state"] == "idle" and status["pending_turns"] == 0 and status["mode"] == "per_turn"


def test_each_saved_turn_triggers_a_sync(settings: Settings):
    runner = FakeRunner()
    with _client(settings, runner) as client:
        sid = client.post("/api/sessions", json={}).json()["session_id"]
        client.post("/api/chat", json={"session_id": sid, "message": "hi"})
        status = _wait_idle(client)
        assert status["state"] == "idle" and status["last_success_at"] is not None
        assert runner.calls[0]["args"][1:] == ["--init", "--print"]
        assert runner.calls[0]["cwd"] == settings.context_corpus_path


def test_manual_mode_waits_for_the_sync_endpoint(settings: Settings):
    runner = FakeRunner()
    with _client(settings, runner, memory_sync_mode="manual") as client:
        sid = client.post("/api/sessions", json={}).json()["session_id"]
        client.post("/api/chat", json={"session_id": sid, "message": "hi"})
        assert client.get("/api/memory/status").json()["pending_turns"] == 1
        assert runner.calls == []
        resp = client.post("/api/memory/sync")
        assert resp.status_code == 202
        assert _wait_idle(client)["pending_turns"] == 0
        assert len(runner.calls) == 1


def test_failed_trace_write_does_not_trigger_a_sync(settings: Settings):
    from app.context_store import ContextStore

    runner = FakeRunner()
    with _client(settings, runner) as client:
        sid = client.post("/api/sessions", json={}).json()["session_id"]
        original = ContextStore.write_turn
        ContextStore.write_turn = lambda self, record, session_started_at: (_ for _ in ()).throw(OSError("x"))
        try:
            client.post("/api/chat", json={"session_id": sid, "message": "hi"})
        finally:
            ContextStore.write_turn = original
        assert client.get("/api/memory/status").json()["pending_turns"] == 0
        assert runner.calls == []


def test_app_shutdown_kills_a_running_sync(settings: Settings, tmp_path):
    import psutil

    from app.memory_sync import OpenWikiRunner

    sleeper = tmp_path / "sleep.js"
    sleeper.write_text("setTimeout(() => {}, 60000)\n", encoding="utf-8")

    class SleeperRunner(OpenWikiRunner):
        def __call__(self, args, cwd, env, log_path, timeout):
            return super().__call__([str(sleeper)], cwd, env, log_path, timeout)

    runner = SleeperRunner()
    started = time.monotonic()
    with TestClient(create_app(settings, agent_factory=lambda _s, _t: FakeAgent(), sync_runner=runner)) as client:
        sid = client.post("/api/sessions", json={}).json()["session_id"]
        client.post("/api/chat", json={"session_id": sid, "message": "hi"})
        for _ in range(100):
            if runner._proc is not None:
                break
            time.sleep(0.05)
        pid = runner._proc.pid
        assert client.get("/api/memory/status").json()["state"] == "syncing"
        exit_started = time.monotonic()
    assert time.monotonic() - exit_started < 10, "shutdown waited for the sync process"
    assert not psutil.pid_exists(pid)


def test_successful_sync_restarts_the_context_visualizer_on_the_same_url(settings: Settings):
    import urllib.request

    runner = FakeRunner()
    with _client(settings, runner) as client:
        url_before = client.get("/api/config").json()["context_vis_url"]
        pid_before = client.app.state.runtime.context_vis._proc.pid
        sid = client.post("/api/sessions", json={}).json()["session_id"]
        client.post("/api/chat", json={"session_id": sid, "message": "hi"})
        _wait_idle(client)
        for _ in range(100):
            if client.app.state.runtime.context_vis._proc.pid != pid_before:
                break
            time.sleep(0.05)
        assert client.app.state.runtime.context_vis._proc.pid != pid_before
        assert client.get("/api/config").json()["context_vis_url"] == url_before
        with urllib.request.urlopen(url_before + "/api/graph", timeout=5) as resp:
            assert resp.status == 200
