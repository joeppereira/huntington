#!/usr/bin/env bash
# One-time: snapshot the current context-corpus (after its first successful empty-memory
# `openwiki --init`) into prebuilt/context-corpus-template/. From then on, every demo reset /
# backend start restores this template by file copy, so the first memory sync of a session is an
# incremental --update (minutes) instead of a full --init.
# Usage (from the project root): bash scripts/capture-context-template.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/context-corpus"
DST="$ROOT/prebuilt/context-corpus-template"

[ -f "$SRC/.poc-initialized" ] || { echo "context-corpus has no .poc-initialized marker — run one successful memory sync first." >&2; exit 1; }

rm -rf "$DST"
mkdir -p "$(dirname "$DST")"
cp -R "$SRC" "$DST"
# Template must represent EMPTY memory: no session turns.
rm -rf "$DST/sessions"
mkdir "$DST/sessions"
touch "$DST/sessions/.gitkeep"
echo "captured $(du -sh "$DST" | cut -f1) template at $DST"
