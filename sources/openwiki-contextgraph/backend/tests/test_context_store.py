import subprocess
from pathlib import Path

import pytest

from app.config import Settings
from app.context_store import reset_context_corpus


def _git(corpus: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=corpus, capture_output=True, text=True, check=True).stdout


def test_reset_creates_committed_repo(settings: Settings):
    corpus = settings.context_corpus_path
    reset_context_corpus(settings)
    assert (corpus / "README.md").exists()
    assert (corpus / ".openwikiignore").exists()
    assert (corpus / "sessions").is_dir()
    brief = (corpus / "openwiki" / "INSTRUCTIONS.md").read_text(encoding="utf-8")
    assert brief == (settings.templates_path / "context-INSTRUCTIONS.md").read_text(encoding="utf-8")
    assert _git(corpus, "rev-parse", "--show-toplevel").strip() == corpus.as_posix()
    assert len(_git(corpus, "log", "--oneline").splitlines()) == 1
    assert _git(corpus, "status", "--porcelain") == ""


def test_reset_wipes_previous_contents(settings: Settings):
    reset_context_corpus(settings)
    stale = settings.context_corpus_path / "sessions" / "old" / "turn-0001.md"
    stale.parent.mkdir(parents=True)
    stale.write_text("old", encoding="utf-8")
    reset_context_corpus(settings)
    assert not stale.exists()
    assert len(_git(settings.context_corpus_path, "log", "--oneline").splitlines()) == 1


def test_reset_refuses_project_root(project_root: Path):
    s = Settings(_env_file=None, project_root=project_root, context_corpus_dir=project_root)
    with pytest.raises(ValueError):
        reset_context_corpus(s)
