"""
Normalize the CNB wiki's front matter to the brief's typed-graph contract, without any
model calls: canonical `type` from the page's folder, and `entity_id` from the stable id
the page itself states (title first, then body), else the file slug.

Usage:  python tools/normalize_frontmatter.py [--wiki semantic-corpus-cnb/openwiki]
"""
import argparse
import re
from pathlib import Path

FOLDER_TYPE = {
    "concepts": "Concept", "datasets": "Dataset", "decisions": "Decision",
    "documents": "Document", "incidents": "Incident", "interfaces": "Interface",
    "organizations": "Organization", "people": "Person", "policies": "Policy",
    "projects": "Project", "systems": "System", "teams": "Team",
}

ID_RE = re.compile(
    r"\b((?:SYS|TEAM|BIZ|POL|ADR|EP|INC|PIR|DUS|MRM|ARB|CNB|CBO|PPH|PNG|PRSP|ENS|TDIP)"
    r"-[A-Z0-9][A-Za-z0-9.-]*[A-Za-z0-9])\b")


# Body fallback is restricted to id prefixes that can belong to the page's own kind, so a
# Person page never inherits a SYS- id its body merely mentions.
FOLDER_ID_PREFIXES = {
    "systems": ("SYS-",), "teams": ("TEAM-", "BIZ-"), "interfaces": ("EP-",),
    "policies": ("POL-", "DUS-", "MRM-"), "decisions": ("ADR-",),
    "incidents": ("INC-", "PIR-"), "documents": (), "datasets": (), "projects": ("CBO-",),
    "organizations": (), "people": (), "concepts": (),
}


def pick_entity_id(title: str, body: str, slug: str, folder: str) -> str:
    m = ID_RE.search(title)
    if m:
        return m.group(1)
    prefixes = FOLDER_ID_PREFIXES.get(folder, ())
    for m in ID_RE.finditer(body):
        if m.group(1).startswith(prefixes) if prefixes else False:
            return m.group(1)
    return slug


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wiki", default="semantic-corpus-cnb/openwiki")
    args = ap.parse_args()
    wiki = Path(args.wiki)

    changed = 0
    for md in sorted(wiki.rglob("*.md")):
        if ".claims" in md.parts or md.name in ("INSTRUCTIONS.md", "index.md", "log.md"):
            continue
        folder = md.parent.name
        ctype = FOLDER_TYPE.get(folder)
        if not ctype:
            continue
        text = md.read_text(encoding="utf-8")
        if not text.startswith("---"):
            continue
        end = text.find("\n---", 3)
        if end < 0:
            continue
        fm, body = text[:end], text[end:]

        fm_new = re.sub(r"(?m)^type:\s*.*$", f"type: {ctype}", fm, count=1)
        if re.search(r"(?m)^entity_id:", fm_new) is None:
            title_m = re.search(r'(?m)^title:\s*"?(.+?)"?\s*$', fm_new)
            title = title_m.group(1) if title_m else ""
            eid = pick_entity_id(title, body, md.stem, folder)
            fm_new = re.sub(r"(?m)^(type:.*)$", rf"\1\nentity_id: {eid}", fm_new, count=1)
        if fm_new != fm:
            md.write_text(fm_new + body, encoding="utf-8")
            changed += 1
    print(f"normalized {changed} pages")


if __name__ == "__main__":
    main()
