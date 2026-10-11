"""
Normalize the CNB wiki's front matter to the brief's typed-graph contract, without any
model calls: canonical `type` from the page's folder, and `entity_id` from the stable id
the page itself states in its title/H1, else the file slug.

The id is taken ONLY from the front-matter title or the first H1 heading. A body-wide
fallback used to exist and corrupted the corpus by assigning other entities' ids (a page
that merely *mentions* EP-PPH-01 is not EP-PPH-01), so it was removed deliberately.

Pages in unknown folders, without front matter, or whose declared `type` disagrees with
their folder are never silently skipped or overwritten: they are reported and the script
exits nonzero.

Usage:  python tools/normalize_frontmatter.py [--wiki semantic-corpus-cnb/openwiki]
"""
import argparse
import re
import sys
from pathlib import Path

FOLDER_TYPE = {
    "concepts": "Concept", "datasets": "Dataset", "decisions": "Decision",
    "documents": "Document", "incidents": "Incident", "interfaces": "Interface",
    "organizations": "Organization", "people": "Person", "policies": "Policy",
    "projects": "Project", "systems": "System", "teams": "Team",
}

# Non-entity pages that legitimately carry no typed front matter.
SKIP_NAMES = {"INSTRUCTIONS.md", "index.md", "log.md"}

ID_RE = re.compile(
    r"\b((?:SYS|TEAM|BIZ|POL|ADR|EP|EV|BT|INC|PIR|CMP|DUS|MRM|ARB|CNB|CBO|GTSI|FCT|PPH|PNG|PRSP|ENS|TDIP|DOC)"
    r"-[A-Z0-9][A-Za-z0-9.-]*[A-Za-z0-9])\b")


def pick_entity_id(title: str, body: str, slug: str) -> str:
    """Stable id from the title or the first H1 only; otherwise the file slug.

    Never scan the whole body: pages constantly mention *other* entities' ids, and a
    body fallback historically assigned those foreign ids to the page itself.
    """
    m = ID_RE.search(title)
    if m:
        return m.group(1)
    h1 = re.search(r"(?m)^#\s+(.+)$", body)
    if h1:
        m = ID_RE.search(h1.group(1))
        if m:
            return m.group(1)
    return slug


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--wiki", default="semantic-corpus-cnb/openwiki")
    args = ap.parse_args()
    wiki = Path(args.wiki)

    changed = 0
    errors: list[str] = []
    for md in sorted(wiki.rglob("*.md")):
        if ".claims" in md.parts or md.name in SKIP_NAMES:
            continue
        rel = md.relative_to(wiki)
        if md.parent == wiki:
            # Wiki-root pages (overview.md, quickstart.md) are navigation, not entities.
            continue
        folder = md.parent.name
        ctype = FOLDER_TYPE.get(folder)
        if not ctype:
            errors.append(f"{rel}: unknown folder '{folder}' (no type mapping)")
            continue
        text = md.read_text(encoding="utf-8")
        if not text.startswith("---"):
            errors.append(f"{rel}: no front matter")
            continue
        end = text.find("\n---", 3)
        if end < 0:
            errors.append(f"{rel}: unterminated front matter")
            continue
        fm, body = text[:end], text[end:]

        fm_new = fm
        declared = re.search(r"(?m)^type:\s*(\S.*?)\s*$", fm)
        if declared is None:
            fm_new = fm.rstrip("\n") + f"\ntype: {ctype}"
        elif declared.group(1).strip('"\'') != ctype:
            errors.append(
                f"{rel}: declared type '{declared.group(1)}' disagrees with folder "
                f"'{folder}' (expected '{ctype}') — not overwriting; fix the page or move it")
            continue
        if re.search(r"(?m)^entity_id:", fm_new) is None:
            title_m = re.search(r'(?m)^title:\s*"?(.+?)"?\s*$', fm_new)
            title = title_m.group(1) if title_m else ""
            eid = pick_entity_id(title, body, md.stem)
            fm_new = re.sub(r"(?m)^(type:.*)$", rf"\1\nentity_id: {eid}", fm_new, count=1)
        if fm_new != fm:
            md.write_text(fm_new + body, encoding="utf-8")
            changed += 1
    print(f"normalized {changed} pages")
    if errors:
        print(f"\n{len(errors)} page(s) need attention:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
