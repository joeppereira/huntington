import urllib.request

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app


def test_config_and_health_with_running_visualizers(settings: Settings):
    with TestClient(create_app(settings)) as client:
        config = client.get("/api/config").json()
        assert config["semantic_vis_url"] == "http://127.0.0.1:4391"
        assert config["context_vis_url"] == "http://127.0.0.1:4392"
        assert config["semantic_ready"] is True
        for url in (config["semantic_vis_url"], config["context_vis_url"]):
            with urllib.request.urlopen(url + "/api/graph", timeout=5) as resp:
                assert resp.status == 200

        health = client.get("/api/health").json()
        assert health["ok"] is True
        assert health["openwiki_version"] == "0.7.0"
        assert health["children"]["semantic_vis"] == "running"
        assert health["children"]["context_vis"] == "running"
        assert (settings.context_corpus_path / "openwiki" / "INSTRUCTIONS.md").exists()

    # Leaving the client runs the lifespan shutdown, which must stop both visualizers.
    for url in (config["semantic_vis_url"], config["context_vis_url"]):
        with pytest.raises(OSError):
            urllib.request.urlopen(url + "/api/graph", timeout=2)


def test_cors_allows_frontend_origin(settings: Settings):
    with TestClient(create_app(settings)) as client:
        resp = client.get("/api/config", headers={"Origin": settings.frontend_origin})
        assert resp.headers["access-control-allow-origin"] == settings.frontend_origin


def test_semantic_not_ready_without_index(settings: Settings, tmp_path):
    s = settings.model_copy(update={"semantic_corpus_dir": tmp_path / "no-semantic"})
    with TestClient(create_app(s)) as client:
        config = client.get("/api/config").json()
        assert config["semantic_ready"] is False
        assert config["semantic_vis_url"] is None
        assert client.get("/api/health").json()["children"]["semantic_vis"] == "not_built"
