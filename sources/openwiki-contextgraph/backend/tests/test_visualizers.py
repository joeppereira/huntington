import json
import urllib.request
from pathlib import Path

import pytest

from app.config import Settings
from app.openwiki_cli import build_openwiki_env, resolve_cli_js
from app.visualizers import Visualizer, parse_visualizer_url


def test_parse_url_strips_ansi():
    line = "  open:  \x1b[36mhttp://127.0.0.1:4321\x1b[0m"
    assert parse_visualizer_url(line) == "http://127.0.0.1:4321"


def test_parse_url_ignores_other_lines():
    assert parse_visualizer_url("  wiki:  C:\\x\\openwiki") is None


def _make_wiki(tmp_path: Path) -> Path:
    wiki = tmp_path / "wiki" / "openwiki"
    wiki.mkdir(parents=True)
    (wiki / "INSTRUCTIONS.md").write_text("# brief\n", encoding="utf-8")
    return wiki


def _visualizer(settings: Settings, wiki: Path, port: int) -> Visualizer:
    return Visualizer(
        name="test",
        cli_js=resolve_cli_js(settings),
        wiki_dir=wiki,
        port=port,
        env=build_openwiki_env(settings),
        log_path=settings.logs_path / "vis-test.log",
    )


def _get(url: str) -> int:
    with urllib.request.urlopen(url, timeout=5) as resp:
        return resp.status


def test_start_serves_graph_and_stop_frees_port(settings: Settings, tmp_path: Path):
    vis = _visualizer(settings, _make_wiki(tmp_path), 4393)
    url = vis.start()
    try:
        assert url == "http://127.0.0.1:4393"
        assert vis.is_running
        assert _get(url + "/api/graph") == 200
    finally:
        vis.stop()
    assert not vis.is_running
    with pytest.raises(OSError):
        _get(url + "/api/graph")


def _wiki_with_page(tmp_path: Path, name: str) -> Path:
    wiki = tmp_path / name / "openwiki"
    wiki.mkdir(parents=True)
    (wiki / "INSTRUCTIONS.md").write_text("# brief\n", encoding="utf-8")
    (wiki / f"page-{name}.md").write_text(f"---\ntitle: {name}\n---\n# {name}\n", encoding="utf-8")
    return wiki


def _graph_ids(url: str) -> list[str]:
    with urllib.request.urlopen(url + "/api/graph", timeout=5) as resp:
        return [node["id"] for node in json.load(resp)["nodes"]]


@pytest.mark.parametrize("attempt", range(5))
def test_reports_actual_port_when_taken(settings: Settings, tmp_path: Path, attempt: int):
    # OpenWiki 0.7.0 prints a stale banner with the taken port before the real one when it
    # auto-increments, so the URL must come from the process's actual listening socket.
    first = _visualizer(settings, _wiki_with_page(tmp_path, "a"), 4394)
    second = _visualizer(settings, _wiki_with_page(tmp_path, "b"), 4394)
    try:
        assert first.start() == "http://127.0.0.1:4394"
        url = second.start()
        assert url != "http://127.0.0.1:4394"
        assert _graph_ids(url) == ["page-b"]
    finally:
        second.stop()
        first.stop()


def test_start_fails_cleanly_for_missing_wiki(settings: Settings, tmp_path: Path):
    vis = _visualizer(settings, tmp_path / "missing", 4395)
    with pytest.raises(RuntimeError):
        vis.start(timeout=15)
    assert not vis.is_running
