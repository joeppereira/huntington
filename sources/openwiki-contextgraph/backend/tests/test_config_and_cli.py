from pathlib import Path

import pytest

from app.config import Settings
from app.openwiki_cli import build_openwiki_env, openwiki_version, resolve_cli_js


def test_relative_paths_resolve_against_project_root(project_root: Path):
    s = Settings(_env_file=None, project_root=project_root)
    assert s.semantic_corpus_path == project_root / "semantic-corpus"
    assert s.config_dir_path == project_root / ".openwiki-state"
    assert s.semantic_corpus_path.is_absolute()


def test_absolute_paths_are_kept(settings: Settings, tmp_path: Path):
    assert settings.context_corpus_path == tmp_path / "context-corpus"


def test_env_has_absolute_config_dir_and_keys(settings: Settings):
    env = build_openwiki_env(settings, base_env={"PATH": "x"})
    assert env["PATH"] == "x"
    assert Path(env["OPENWIKI_CONFIG_DIR"]).is_absolute()
    assert env["ANTHROPIC_API_KEY"] == "test-key"
    assert env["OPENWIKI_PROVIDER"] == "anthropic"
    assert env["LANGCHAIN_TRACING_V2"] == "false"
    assert env["OPENWIKI_MODEL_ID"] == settings.openwiki_model_id


def test_env_model_override(settings: Settings):
    env = build_openwiki_env(settings, model_id="claude-haiku-4-5-20251001", base_env={})
    assert env["OPENWIKI_MODEL_ID"] == "claude-haiku-4-5-20251001"


def test_env_does_not_mutate_base(settings: Settings):
    base = {"PATH": "x"}
    build_openwiki_env(settings, base_env=base)
    assert base == {"PATH": "x"}


def test_cli_js_override_must_exist(project_root: Path, tmp_path: Path):
    s = Settings(_env_file=None, project_root=project_root, openwiki_cli_js=str(tmp_path / "nope.js"))
    with pytest.raises(FileNotFoundError):
        resolve_cli_js(s)


def test_cli_js_resolves_installed_openwiki(project_root: Path):
    cli_js = resolve_cli_js(Settings(_env_file=None, project_root=project_root))
    assert cli_js.name == "cli.js" and cli_js.exists()
    assert openwiki_version(cli_js) == "0.7.0"


def test_env_page_concurrency_override(settings: Settings):
    assert build_openwiki_env(settings, base_env={}, page_concurrency=7)["OPENWIKI_PAGE_CONCURRENCY"] == "7"
