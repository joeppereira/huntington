#!/usr/bin/env bash
# macOS/Linux equivalent of scripts/dev.ps1: start the backend (which starts both OpenWiki
# visualizers and the MCP server) and the Vite frontend.
# Usage (from the project root):  bash scripts/dev.sh      Stop with Ctrl-C.

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PY="$ROOT/.venv/bin/python"
[ -x "$PY" ] || { echo "No .venv; create it and pip install -r backend/requirements.txt first." >&2; exit 1; }

# Node can come from the nodejs-wheel-binaries package inside .venv (used where nodejs.org downloads
# are blocked); OpenWiki is then installed under that Node's global prefix.
NODE_BIN="$("$PY" -c 'import nodejs_wheel, os; print(os.path.join(os.path.dirname(nodejs_wheel.__file__), "bin"))' 2>/dev/null || true)"
[ -n "$NODE_BIN" ] && export PATH="$NODE_BIN:$PATH"
command -v node >/dev/null || { echo "node not found on PATH." >&2; exit 1; }

grep -qE '^ANTHROPIC_API_KEY=.+' .env || { echo "ANTHROPIC_API_KEY is empty in .env." >&2; exit 1; }
BACKEND_PORT="$(grep -E '^BACKEND_PORT=' .env | cut -d= -f2 | tr -d '[:space:]' || true)"
BACKEND_PORT="${BACKEND_PORT:-8000}"

echo "==> Starting frontend (Vite) on http://127.0.0.1:5173"
(cd frontend && exec ./node_modules/.bin/vite) &
FRONTEND_PID=$!
trap 'kill "$FRONTEND_PID" 2>/dev/null || true; wait "$FRONTEND_PID" 2>/dev/null || true' EXIT

echo "==> Starting backend on http://127.0.0.1:$BACKEND_PORT"
"$PY" -m uvicorn app.main:create_app --factory --app-dir backend \
    --host 127.0.0.1 --port "$BACKEND_PORT" --timeout-graceful-shutdown 5
