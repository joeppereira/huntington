"""Locate OpenWiki's cli.js and build the environment for OpenWiki child processes.

OpenWiki is always launched as `node <cli.js> ...`: the npm `.cmd` shim on Windows cannot be
exec'd reliably without a shell (BUILD_SPEC Section 5).
"""

import json
import os
import shutil
import subprocess
from collections.abc import Mapping
from functools import lru_cache
from pathlib import Path

from .config import Settings


@lru_cache(maxsize=1)
def _npm_root_global() -> Path:
    npm = shutil.which("npm")
    if npm is None:
        raise FileNotFoundError("npm not found on PATH; install Node.js and run scripts/setup.ps1")
    # npm is a .cmd shim on Windows; passing the resolved path as an argument list is safe.
    out = subprocess.run([npm, "root", "-g"], capture_output=True, text=True, check=True)
    return Path(out.stdout.strip())


def resolve_cli_js(settings: Settings) -> Path:
    if settings.openwiki_cli_js:
        cli_js = Path(settings.openwiki_cli_js)
        if not cli_js.exists():
            raise FileNotFoundError(f"OPENWIKI_CLI_JS points to a missing file: {cli_js}")
        return cli_js
    cli_js = _npm_root_global() / "openwiki" / "dist" / "cli" / "cli.js"
    if not cli_js.exists():
        raise FileNotFoundError(f"OpenWiki not found at {cli_js}; run scripts/setup.ps1")
    return cli_js


def openwiki_version(cli_js: Path) -> str:
    package_json = cli_js.parents[2] / "package.json"
    try:
        return json.loads(package_json.read_text(encoding="utf-8"))["version"]
    except (OSError, KeyError, json.JSONDecodeError):
        return "unknown"


def build_openwiki_env(
    settings: Settings,
    model_id: str | None = None,
    base_env: Mapping[str, str] | None = None,
    page_concurrency: int | None = None,
) -> dict[str, str]:
    """Process env plus the OpenWiki keys from .env, with OPENWIKI_CONFIG_DIR made absolute."""
    base = dict(os.environ if base_env is None else base_env)
    overrides = {
        "ANTHROPIC_API_KEY": settings.anthropic_api_key,
        "OPENWIKI_PROVIDER": settings.openwiki_provider,
        "OPENWIKI_MODEL_ID": model_id or settings.openwiki_model_id,
        "OPENWIKI_PAGE_CONCURRENCY": str(page_concurrency or settings.openwiki_page_concurrency),
        "LANGCHAIN_TRACING_V2": settings.langchain_tracing_v2,
        "OPENWIKI_TELEMETRY_DISABLED": settings.openwiki_telemetry_disabled,
        "OPENWIKI_CONFIG_DIR": str(settings.config_dir_path),
        "OPENWIKI_MAX_OUTPUT_TOKENS": settings.openwiki_max_output_tokens,
    }
    # Vertex (gemini-enterprise) auth for Claude-on-Model-Garden child runs; empty values
    # are skipped so the anthropic provider path is unaffected.
    for key, value in {
        "GOOGLE_APPLICATION_CREDENTIALS": settings.google_application_credentials,
        "GOOGLE_CLOUD_PROJECT": settings.google_cloud_project,
        "GOOGLE_CLOUD_LOCATION": settings.google_cloud_location,
    }.items():
        if value:
            overrides[key] = value
    return {**base, **overrides}
