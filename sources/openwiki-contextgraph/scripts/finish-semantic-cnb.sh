#!/usr/bin/env bash
# macOS/Linux port of the tail end of scripts/build-semantic.ps1, for the CNB corpus:
# re-run pages OpenWiki silently skipped during --init (left as openwiki_generated: true stubs),
# then verify the wiki. Usage (from the project root):  bash scripts/finish-semantic-cnb.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

set -a; source .env; set +a
export OPENWIKI_CONFIG_DIR="$ROOT/.openwiki-state"
CORPUS="$ROOT/${SEMANTIC_CORPUS_DIR:-semantic-corpus-cnb}"
WIKI="$CORPUS/openwiki"
CLI="${OPENWIKI_CLI_JS:-$(npm root -g)/openwiki/dist/cli/cli.js}"
STAMP="$(date +%Y%m%d-%H%M%S)"

stubs=()
while IFS= read -r f; do
    stubs+=("/openwiki/${f#"$WIKI"/}")
done < <(grep -rl '^openwiki_generated: *true' "$WIKI" --include='*.md' 2>/dev/null || true)

if [ "${#stubs[@]}" -gt 0 ]; then
    LOG="$ROOT/logs/semantic-cnb-update-$STAMP.log"
    echo "==> Re-running ${#stubs[@]} skipped page(s) with --update (log: $LOG)"
    msg="Required page edits: these ${#stubs[@]} pages were skipped during init and are still \
placeholder stubs (openwiki_generated: true, no description, type Reference). Plan all of them \
for a full rewrite following openwiki/INSTRUCTIONS.md (correct front-matter type from the brief, \
entity_id, description, content, Relationships section with links): $(IFS=', '; echo "${stubs[*]}"). \
Do not change other pages."
    (cd "$CORPUS" && node "$CLI" --update --print "$msg") >"$LOG" 2>&1 || {
        echo "openwiki --update failed; see $LOG"; exit 1; }
fi

echo "==> Verifying generated wiki"
pages=$(find "$WIKI" -name '*.md' ! -path '*/.claims/*' ! -name INSTRUCTIONS.md ! -name log.md | wc -l | tr -d ' ')
remaining=$(grep -rl '^openwiki_generated: *true' "$WIKI" --include='*.md' 2>/dev/null | wc -l | tr -d ' ')
echo "    pages: $pages"
echo "    still stubs: $remaining"
[ -f "$WIKI/index.md" ] && echo "    index.md: present" || echo "    index.md: MISSING"
[ -d "$WIKI/.claims" ] && echo "    .claims/: present" || echo "    .claims/: missing"
echo "    pages by type:"
grep -rh '^type:' "$WIKI" --include='*.md' 2>/dev/null | sed 's/type: *//' | sort | uniq -c | sort -rn | sed 's/^/      /'
echo
echo "View it:  node \"$CLI\" visualize \"$WIKI\" --no-open"
