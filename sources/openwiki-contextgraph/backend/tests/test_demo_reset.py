import re
import subprocess
import time
import urllib.request

from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app
from tests.test_chat_api import FakeAgent
from tests.test_memory_sync import FakeRunner


def _client(settings: Settings, runner: FakeRunner) -> TestClient:
    return TestClient(create_app(settings, agent_factory=lambda _s, _t: FakeAgent(), sync_runner=runner))


def test_reset_wipes_memory_and_starts_a_new_session(settings: Settings):
    corpus = settings.context_corpus_path
    with _client(settings, FakeRunner(block=True)) as client:
        old = client.post("/api/sessions", json={}).json()["session_id"]
        client.post("/api/chat", json={"session_id": old, "message": "hi"})
        assert (corpus / "sessions" / old / "turn-0001.md").exists()
        assert client.get("/api/memory/status").json()["state"] == "syncing"

        started = time.monotonic()
        body = client.post("/api/demo/reset").json()
        assert time.monotonic() - started < 15

        assert re.fullmatch(r"\d{8}-\d{6}-[0-9a-f]{4}", body["session_id"]) and body["session_id"] != old
        assert body["memory"]["state"] == "idle" and body["memory"]["pending_turns"] == 0
        assert not body["memory"]["initialized"]
        assert not (corpus / "sessions" / old).exists()
        assert (corpus / "openwiki" / "INSTRUCTIONS.md").exists()
        log = subprocess.run(["git", "log", "--format=%s"], cwd=corpus, capture_output=True, text=True, check=True)
        assert log.stdout.splitlines() == ["context corpus"]

        url = client.get("/api/config").json()["context_vis_url"]
        assert body["context_vis_url"] == url
        with urllib.request.urlopen(url + "/api/graph", timeout=5) as resp:
            assert resp.status == 200
        assert client.get("/api/health").json()["ok"] is True

        # the new session works end to end
        turn = client.post("/api/chat", json={"session_id": body["session_id"], "message": "again"}).json()
        assert turn["turn"] == 1 and turn["trace_file"] == f"sessions/{body['session_id']}/turn-0001.md"


def test_old_sessions_are_gone_after_reset(settings: Settings):
    with _client(settings, FakeRunner()) as client:
        old = client.post("/api/sessions", json={}).json()["session_id"]
        client.post("/api/demo/reset")
        assert client.post("/api/chat", json={"session_id": old, "message": "hi"}).status_code == 404
        assert client.get(f"/api/sessions/{old}").status_code == 404
