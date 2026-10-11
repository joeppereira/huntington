#!/usr/bin/env python3
"""Assign ground-truth canonical ids to pages and create registry pages for id families
that have no page of their own. Follow-up to augment_frontmatter.py (gap-fix round,
id_coverage diagnosis): TEAM-*/P-* ids were absent from team/person pages, HRC-* codes
were table rows without ids, backlog Jira keys and DOES-NOT-EXIST interfaces had no page
carrying their id at all. Deterministic, idempotent, stdlib+pyyaml.
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WIKI = ROOT / "semantic-corpus-cnb" / "openwiki"
DEFAULT_GT = (
    ROOT.parent / "demo-docs" / "Wire_Tracking_Demo_Kit" / "estate_ground_truth.json"
)

sys.path.insert(0, str(Path(__file__).parent))
from augment_frontmatter import Page, name_matches, dump_kv  # noqa: E402

SKIP_NAMES = {"index.md", "overview.md", "quickstart.md", "timeline.md", "INSTRUCTIONS.md"}


def set_entity_ids(page: Page, ids: list[str]) -> bool:
    """Rewrite the page's entity_id line to `ids` (existing first removed). Returns True
    if the file changed."""
    if page.entity_ids == ids:
        return False
    text = page.path.read_text(encoding="utf-8")
    new_line = dump_kv("entity_id", ids if len(ids) > 1 else ids[0])
    out, replaced = [], False
    for ln in text.split("\n"):
        if not replaced and re.match(r"entity_id\s*:", ln):
            out.append(new_line.rstrip("\n"))
            replaced = True
        else:
            out.append(ln)
    page.path.write_text("\n".join(out), encoding="utf-8")
    return True


def registry_page(path: Path, *, type_: str, ids: list[str], title: str, description: str,
                  tags: list[str], status: str | None, rows: list[str]) -> bool:
    if path.exists():
        return False
    fm = [
        "---",
        f"type: {type_}",
        dump_kv("entity_id", ids).rstrip("\n"),
        f'title: "{title}"',
        f"description: {description}",
        dump_kv("tags", tags).rstrip("\n"),
    ]
    if status:
        fm.append(f"status: {status}")
    fm.append("---")
    body = ["", f"# {title}", "", description, ""] + rows + [""]
    path.write_text("\n".join(fm + body), encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--wiki", default=str(DEFAULT_WIKI))
    ap.add_argument("--ground-truth", default=str(DEFAULT_GT))
    args = ap.parse_args()
    wiki = Path(args.wiki)
    gt = json.loads(Path(args.ground_truth).read_text(encoding="utf-8"))

    pages = [Page(md, wiki) for md in sorted(wiki.rglob("*.md"))
             if ".claims" not in md.parts and md.name not in SKIP_NAMES and md.parent != wiki]
    claimed = {eid for p in pages for eid in p.entity_ids}
    changed = created = 0

    # 1. Teams: prepend TEAM-* ground-truth id (keep the slug id as a secondary).
    for t in gt.get("teams", []):
        for p in pages:
            if p.type == "Team" and any(name_matches(e, t["name"]) for e in p.entity_ids):
                if t["id"] not in p.entity_ids:
                    changed += set_entity_ids(p, [t["id"], *p.entity_ids])
                break

    # 2. People: prepend P-* id, matching GT name against the page title.
    for person in gt.get("people", []):
        for p in pages:
            if p.type == "Person" and name_matches(p.entity_ids[0] if p.entity_ids else "",
                                                   person["name"]):
                if person["id"] not in p.entity_ids:
                    changed += set_entity_ids(p, [person["id"], *p.entity_ids])
                break

    # 3. Hold reason codes: the taxonomy page IS the registry of HRC-* ids.
    hrc = [r["code"] for r in gt.get("hold_reason_codes", [])]
    for p in pages:
        if "hold-reason-taxonomy" in p.rel:
            missing = [c for c in hrc if c not in p.entity_ids]
            if missing:
                changed += set_entity_ids(p, [*p.entity_ids, *missing])
            break

    # 3b. Documents: claim their ground-truth doc_id (e.g. ENS-INT-3.2, PPH-API-CAT-2026.3)
    #     so document codes cited in sources resolve to the document page.
    for doc in gt.get("documents", []):
        stem = Path(doc["file"]).stem.lower()
        for p in pages:
            if p.type == "Document" and Path(p.rel).stem.lower() in stem:
                if doc["doc_id"] in claimed and doc["doc_id"] not in p.entity_ids:
                    break  # id already owned by its entity page (policy/incident)
                if doc["doc_id"] not in p.entity_ids:
                    changed += set_entity_ids(p, [doc["doc_id"], *p.entity_ids])
                break

    # 3c. Model-registry ids: MRM-registered model ids live on the owning system page
    #     (source: MRM-POL-02 register table).
    MODEL_IDS = {
        "sentinel-fraud-scoring": ["FCT-0021", "FCT-0034"],       # MRM register (MRM-POL-02)
        "pol-fcc-014": "CTRL_SCAN",                               # all CTRL-PAY-* controls it defines
        "treasury-data-insights-platform": ["TRS-0142", "EUA-TRS-0007"],  # MRM register: cash-forecast model + ops corridor dashboard EUA
        "ens-notification-api-trs-catalog": "TPL_SCAN",  # all TPL-* template ids from the ENS/CBO sources
    }
    def scan_ids(pattern: str) -> list[str]:
        return sorted({m.group(0) for f in (wiki.parent / "sources").rglob("*.md")
                       for m in re.finditer(pattern, f.read_text(errors="ignore"))})
    tpl_ids = scan_ids(r"\bTPL-[A-Z0-9-]+\b")
    ctrl_ids = scan_ids(r"\b(?:CTRL-PAY-[0-9]+|COPY-[A-Z]+-[A-Z0-9-]+)\b")
    for p in pages:
        if p.type == "Document":
            continue  # source-doc pages never own control/model/template ids
        extra = MODEL_IDS.get(Path(p.rel).stem)
        if extra == "TPL_SCAN":
            extra = tpl_ids
        elif extra == "CTRL_SCAN":
            extra = ctrl_ids
        if extra:
            missing = [e for e in extra if e not in p.entity_ids]
            if missing:
                changed += set_entity_ids(p, [*p.entity_ids, *missing])

    # 4. Jira backlog registry: keys with no page anywhere get one registry page.
    backlog = [j for j in gt.get("jira", []) if j["key"] not in claimed]
    if backlog:
        rows = [f"- **{j['key']}** ({j['type']}, {j['status']}): {j['summary']} — owner {j['owner']}"
                for j in backlog]
        created += registry_page(
            wiki / "projects" / "jira-backlog-registry.md", type_="Project",
            ids=[j["key"] for j in backlog],
            title="Wire Center Jira Backlog Registry",
            description=("Registry of Wire Tracking discovery backlog tickets that have no "
                         "dedicated project page; facts from JIRA-EXP-2026-10-05."),
            tags=["jira", "backlog", "registry", "wire-center"], status=None, rows=rows)

    # 5. Proposed-but-nonexistent interfaces registry (GT status DOES NOT EXIST).
    absent = [i for i in gt.get("interfaces", [])
              if "DOES NOT EXIST" in str(i.get("status", "")).upper() and i["id"] not in claimed]
    if absent:
        rows = [f"- **{i['id']}** ({i['system']}): {i['interface']} — {i['purpose']}. "
                f"Status: {i['status']}" for i in absent]
        created += registry_page(
            wiki / "interfaces" / "proposed-interfaces-registry.md", type_="Interface",
            ids=[i["id"] for i in absent],
            title="Proposed Interfaces Registry (do not exist yet)",
            description=("Registry of payment-estate interfaces that are proposed or referenced "
                         "but DO NOT EXIST yet, per the estate ground truth; each lists the "
                         "covering system and purpose."),
            tags=["registry", "proposed", "interfaces", "gap"], status="absent", rows=rows)

    print(f"canonical ids: {changed} page(s) updated, {created} registry page(s) created")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
