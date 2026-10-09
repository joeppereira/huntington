import sys
from pathlib import Path

import pytest

BACKEND_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BACKEND_DIR.parent
sys.path.insert(0, str(BACKEND_DIR))

from app.config import Settings  # noqa: E402


@pytest.fixture
def project_root() -> Path:
    return PROJECT_ROOT


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    """Settings isolated from .env: temp context corpus and high ports so tests never clash with dev."""
    return Settings(
        _env_file=None,
        project_root=PROJECT_ROOT,
        anthropic_api_key="test-key",
        context_corpus_dir=tmp_path / "context-corpus",
        logs_dir=tmp_path / "logs",
        semantic_vis_port=4391,
        context_vis_port=4392,
    )
