"""Settings loaded from the project's .env (BUILD_SPEC Section 6)."""

from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=PROJECT_ROOT / ".env", env_file_encoding="utf-8", extra="ignore")

    project_root: Path = PROJECT_ROOT

    # Anthropic / OpenWiki
    anthropic_api_key: str = ""
    openwiki_provider: str = "anthropic"
    openwiki_model_id: str = "claude-sonnet-5-5"
    context_openwiki_model_id: str = ""
    agent_model_id: str = "claude-sonnet-5-5"
    openwiki_page_concurrency: int = 3
    context_openwiki_page_concurrency: int = 6  # memory syncs: more parallel pages, less lag
    langchain_tracing_v2: str = "false"
    openwiki_telemetry_disabled: str = "1"
    openwiki_config_dir: Path = Path(".openwiki-state")
    openwiki_cli_js: str = ""
    # Vertex AI (gemini-enterprise provider): Claude served from Model Garden via a
    # service-account key instead of an Anthropic API key.
    google_application_credentials: str = ""
    google_cloud_project: str = ""
    google_cloud_location: str = "global"
    # Large submit_plan calls truncate at OpenWiki's 16K default (see CLAUDE.md).
    openwiki_max_output_tokens: str = "60000"

    # Paths and ports
    semantic_corpus_dir: Path = Path("semantic-corpus")
    context_corpus_dir: Path = Path("context-corpus")
    logs_dir: Path = Path("logs")
    semantic_vis_port: int = 4321
    context_vis_port: int = 4322
    backend_port: int = 8000
    frontend_origin: str = "http://127.0.0.1:5173"

    # Behaviour
    reset_context_on_start: bool = True
    memory_sync_mode: Literal["per_turn", "manual"] = "per_turn"
    memory_sync_timeout_sec: int = 1200

    def _resolve(self, path: Path) -> Path:
        return path if path.is_absolute() else (self.project_root / path).resolve()

    @property
    def semantic_corpus_path(self) -> Path:
        return self._resolve(self.semantic_corpus_dir)

    @property
    def context_corpus_path(self) -> Path:
        return self._resolve(self.context_corpus_dir)

    @property
    def config_dir_path(self) -> Path:
        return self._resolve(self.openwiki_config_dir)

    @property
    def logs_path(self) -> Path:
        return self._resolve(self.logs_dir)

    @property
    def templates_path(self) -> Path:
        return self.project_root / "templates"

    @property
    def semantic_ready(self) -> bool:
        return (self.semantic_corpus_path / "openwiki" / "index.md").exists()
