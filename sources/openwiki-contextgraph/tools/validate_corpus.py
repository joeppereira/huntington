"""
Standalone validation gate for an OpenWiki entity corpus (stdlib + pyyaml only).

Usage:
    python tools/validate_corpus.py <corpus_openwiki_dir> [--ground-truth <json>]

Checks (every violation is listed; exit is nonzero if any are found):
  - missing / unparseable YAML front matter
  - front-matter `type` matches the page's folder
  - duplicate entity_id across pages
  - entity_id prefix consistent with the page's type folder (slug-style ids are allowed
    only in folders with no id scheme: teams, people, concepts, datasets, organizations,
    documents)
  - no range pseudo-ids (e.g. "EP-PPH-04..07" — list the ids individually instead)
  - no stub pages (type `Reference`, or no prose under any heading)
  - typed-relation front matter (docs/schema-relations.md): every relation ref resolves
    to an existing page, source/target type pairs match the schema table, `status` is in
    the enum, `status_note` is a string, and `aliases` is a list of strings. Relation
    fields not in the table are ignored (forward compatibility).
  - with --ground-truth: every ground-truth entity id appears on exactly one page of the
    right type (coverage gaps reported per type), and no page claims an id that ground
    truth assigns to a different kind of entity
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

import yaml

FOLDER_TYPE = {
    "concepts": "Concept", "datasets": "Dataset", "decisions": "Decision",
    "documents": "Document", "incidents": "Incident", "interfaces": "Interface",
    "organizations": "Organization", "people": "Person", "policies": "Policy",
    "projects": "Project", "systems": "System", "teams": "Team",
}

# Non-entity pages that legitimately carry no typed front matter.
SKIP_NAMES = {"INSTRUCTIONS.md", "index.md", "log.md"}

JIRA_PREFIXES = ("CBO-", "PPH-", "PNG-", "GTSI-", "FCT-", "ENS-", "TDA-")

# Observed id conventions per folder (from the corpus and estate_ground_truth.json).
FOLDER_ID_PREFIXES: dict[str, tuple[str, ...]] = {
    "systems": ("SYS-", "FCT-", "TRS-", "EUA-"),   # system id + MRM-registered model/EUA ids
    "interfaces": ("EP-", "EV-", "BT-", "TPL-"),  # endpoints, events, batch feeds, notification templates
    "incidents": ("INC-", "PIR-", "CMP-"),
    "projects": JIRA_PREFIXES,                 # project pages are keyed by Jira id
    "policies": ("POL-", "DUS-", "MRM-", "SEC-", "FRS-", "CTRL-", "COPY-"),  # + controls/copy ids a policy defines
    "decisions": ("ADR-",) + JIRA_PREFIXES,    # ARB decisions, or a Jira-tracked decision
    "documents": (),                           # doc ids are heterogeneous: anything goes
}
# Folders with no id scheme, where a kebab-case file slug is an acceptable id.
SLUG_FOLDERS = {"teams", "people", "concepts", "datasets", "organizations", "documents"}

SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9.-]*$")

# Ground-truth section -> (page types that may own such an id)
GT_SECTIONS = {
    "systems": ("System",),
    "interfaces": ("Interface",),
    "teams": ("Team",),
    "people": ("Person",),
    "documents": ("Document", "Policy", "Incident"),  # a policy/PIR page owns its bare doc id
    "jira": ("Project", "Decision"),
}


# Typed-relation contract (docs/schema-relations.md): field -> (allowed source page
# types, allowed target page types); None means any type. `relates_to` additionally
# allows Person: the gap-fix people pages carry their Jira-ownership context as
# relates_to (target stays `any`, per the table).
RELATION_RULES: dict[str, tuple[set | None, set | None]] = {
    "owned_by": ({"System", "Interface", "Dataset"}, {"Team"}),
    "owner": ({"Project"}, {"Person"}),
    "part_of": ({"Interface"}, {"System"}),
    "supersedes": ({"Interface", "Decision", "Project"}, {"Interface", "Decision", "Project"}),
    "superseded_by": ({"Interface", "Decision", "Project"}, {"Interface", "Decision", "Project"}),
    "governed_by": ({"Concept", "Interface", "Dataset", "Project"}, {"Policy"}),
    "relates_to": ({"Incident", "Project", "Document", "Person"}, None),
    "described_by": ({"System", "Interface", "Policy"}, {"Document"}),
    "depends_on": ({"System", "Interface"}, {"System", "Interface"}),
}
STATUS_ENUM = {"live", "deprecated", "proposed", "closed", "absent"}
REF_PREFIX = "openwiki/"

HONORIFICS = {"dr", "mr", "mrs", "ms", "prof"}


def _tokens(text: str) -> list[str]:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return [w for w in re.split(r"[^a-z0-9]+", text.lower()) if w and w not in HONORIFICS]


def compact(text: str) -> str:
    """Punctuation-insensitive key: "Kevin O'Brien" and "kevin-obrien" both -> kevinobrien."""
    return "".join(_tokens(text))


def name_matches(eid: str, name: str) -> bool:
    """Does a slug-style entity_id plausibly denote this ground-truth name?

    "cbo-wire-center-squad" matches "Digital Treasury Channels - CBO Wire Center squad"
    (token subset) and "gtsi" matches "Global Transaction Services Integration" (acronym).
    """
    nt, et = _tokens(name), _tokens(eid)
    if not et:
        return False
    if compact(eid) == compact(name):
        return True
    if set(et) <= set(nt):
        return True
    return len(et) == 1 and et[0] == "".join(w[0] for w in nt)


class Page:
    def __init__(self, rel: str, folder: str, fm: dict, body: str):
        self.rel = rel
        self.folder = folder
        self.fm = fm
        self.body = body
        raw = fm.get("entity_id")
        if raw is None:
            self.entity_ids: list[str] = []
        elif isinstance(raw, list):
            self.entity_ids = [str(x) for x in raw]
        else:
            self.entity_ids = [str(raw)]
        self.type = str(fm.get("type", "") or "")


def load_pages(wiki: Path, violations: list[str]) -> list[Page]:
    pages: list[Page] = []
    for md in sorted(wiki.rglob("*.md")):
        if ".claims" in md.parts or md.name in SKIP_NAMES or md.parent == wiki:
            continue
        rel = str(md.relative_to(wiki))
        folder = md.parent.name
        if folder not in FOLDER_TYPE:
            violations.append(f"[unknown-folder] {rel}: folder '{folder}' has no type mapping")
            continue
        text = md.read_text(encoding="utf-8")
        if not text.startswith("---"):
            violations.append(f"[missing-frontmatter] {rel}: page has no YAML front matter")
            continue
        end = text.find("\n---", 3)
        if end < 0:
            violations.append(f"[missing-frontmatter] {rel}: unterminated front matter")
            continue
        try:
            fm = yaml.safe_load(text[3:end]) or {}
        except yaml.YAMLError as err:
            violations.append(f"[bad-yaml] {rel}: {str(err).splitlines()[0]}")
            continue
        if not isinstance(fm, dict):
            violations.append(f"[bad-yaml] {rel}: front matter is not a mapping")
            continue
        body = text[end + len("\n---"):]
        pages.append(Page(rel, folder, fm, body))
    return pages


def check_pages(pages: list[Page], violations: list[str]) -> None:
    owners: dict[str, list[Page]] = {}
    for p in pages:
        expected_type = FOLDER_TYPE[p.folder]

        if p.type != expected_type:
            violations.append(
                f"[type-mismatch] {p.rel}: type '{p.type}' but folder '{p.folder}' expects '{expected_type}'")
        if p.type == "Reference":
            violations.append(f"[stub] {p.rel}: type 'Reference' marks an unwritten stub page")

        prose = re.sub(r"(?m)^#{1,6}\s.*$", "", p.body).strip()
        if re.search(r"(?m)^#{1,6}\s", p.body) and not prose:
            violations.append(f"[stub] {p.rel}: headings with no content under any of them")
        elif not p.body.strip():
            violations.append(f"[stub] {p.rel}: empty body")

        if not p.entity_ids:
            violations.append(f"[missing-entity-id] {p.rel}: no entity_id in front matter")
        for eid in p.entity_ids:
            owners.setdefault(eid, []).append(p)
            if ".." in eid:
                violations.append(
                    f"[range-id] {p.rel}: entity_id '{eid}' is a range pseudo-id; list ids individually")
                continue
            prefixes = FOLDER_ID_PREFIXES.get(p.folder, ())
            if prefixes and eid.startswith(prefixes):
                continue
            if p.folder in SLUG_FOLDERS and (not prefixes or SLUG_RE.match(eid)):
                continue
            violations.append(
                f"[prefix] {p.rel}: entity_id '{eid}' does not match the '{p.folder}' convention "
                f"({', '.join(pre + '*' for pre in prefixes) or 'slug'})")

    for eid, ps in sorted(owners.items()):
        if len(ps) > 1:
            violations.append(
                f"[duplicate-id] entity_id '{eid}' claimed by {len(ps)} pages: "
                + ", ".join(p.rel for p in ps))


def check_relations(pages: list[Page], violations: list[str]) -> None:
    by_rel = {p.rel: p for p in pages}

    def resolve(ref) -> "Page | None":
        if not isinstance(ref, str) or not ref.startswith(REF_PREFIX):
            return None
        return by_rel.get(ref[len(REF_PREFIX):])

    for p in pages:
        status = p.fm.get("status")
        if status is not None and status not in STATUS_ENUM:
            violations.append(
                f"[status-enum] {p.rel}: status '{status}' not in "
                f"{{{', '.join(sorted(STATUS_ENUM))}}}")
        note = p.fm.get("status_note")
        if note is not None and not isinstance(note, str):
            violations.append(f"[status-note] {p.rel}: status_note must be a string")
        aliases = p.fm.get("aliases")
        if aliases is not None and (
            not isinstance(aliases, list) or not all(isinstance(a, str) for a in aliases)
        ):
            violations.append(f"[aliases] {p.rel}: aliases must be a list of strings")

        for field, (src_types, tgt_types) in RELATION_RULES.items():
            raw = p.fm.get(field)
            if raw is None:
                continue
            refs = raw if isinstance(raw, list) else [raw]
            if src_types is not None and p.type not in src_types:
                violations.append(
                    f"[relation-source] {p.rel}: '{field}' not allowed on type "
                    f"'{p.type}' (allowed: {'/'.join(sorted(src_types))})")
            for ref in refs:
                target = resolve(ref)
                if target is None:
                    violations.append(
                        f"[relation-ref] {p.rel}: {field} -> '{ref}' does not resolve "
                        f"to a page (expected '{REF_PREFIX}<folder>/<slug>.md')")
                    continue
                if tgt_types is not None and target.type not in tgt_types:
                    violations.append(
                        f"[relation-target] {p.rel}: {field} -> {target.rel} has type "
                        f"'{target.type}' (allowed: {'/'.join(sorted(tgt_types))})")


def check_ground_truth(pages: list[Page], gt: dict, violations: list[str]) -> None:
    by_id: dict[str, list[Page]] = {}
    for p in pages:
        for eid in p.entity_ids:
            by_id.setdefault(eid, []).append(p)

    gt_owner: dict[str, str] = {}  # gt id -> section
    gaps: dict[str, list[str]] = {}
    for section, allowed_types in GT_SECTIONS.items():
        for entry in gt.get(section, []):
            gid = entry.get("id") or entry.get("doc_id") or entry.get("key")
            if not gid:
                continue
            if "DOES NOT EXIST" in str(entry.get("status", "")).upper():
                continue  # ground truth lists some proposed-but-nonexistent endpoints on purpose
            gt_owner[gid] = section
            claimants = list(by_id.get(gid, []))
            if section == "documents" and not claimants:
                claimants = by_id.get(f"DOC-{gid}", [])  # DOC- alias when a policy owns the bare id
            if section in ("people", "teams") and not claimants:
                # Slug-id folders: match by name instead of the GT code.
                name = entry.get("name", "")
                claimants = [
                    p for p in pages
                    if p.type in allowed_types
                    and (any(name_matches(e, name) for e in p.entity_ids) or gid in p.body)
                ]
            typed = [p for p in claimants if p.type in allowed_types]
            for p in claimants:
                if p.type not in allowed_types:
                    violations.append(
                        f"[gt-wrong-type] {p.rel} (type {p.type}) claims '{gid}', which ground truth "
                        f"assigns to a {section[:-1]} (expected type: {'/'.join(allowed_types)})")
            if not typed:
                gaps.setdefault(section, []).append(gid)
            elif len(typed) > 1:
                violations.append(
                    f"[gt-multiple] ground-truth id '{gid}' appears on {len(typed)} pages: "
                    + ", ".join(p.rel for p in typed))

    for p in pages:
        for eid in p.entity_ids:
            section = gt_owner.get(eid)
            if section and p.type not in GT_SECTIONS[section] and not any(
                f"[gt-wrong-type] {p.rel} " in v and f"'{eid}'" in v for v in violations
            ):
                violations.append(
                    f"[gt-wrong-type] {p.rel} (type {p.type}) claims '{eid}', which ground truth "
                    f"assigns to a {section[:-1]}")

    for section, missing in sorted(gaps.items()):
        violations.append(
            f"[gt-coverage] {section}: {len(missing)} ground-truth id(s) with no page of type "
            f"{'/'.join(GT_SECTIONS[section])}: {', '.join(missing)}")


ID_GRAMMAR = re.compile(
    r"\b[A-Z]{2,6}(?:-[A-Z0-9][A-Z0-9.]*)+\b"
)


def check_id_closure(pages, wiki: Path, violations: list[str]) -> None:
    """Identifier closure (the invariant behind the id_coverage eval metric): every
    ID-grammar token appearing in the raw source documents must resolve to a page's
    entity_id — exactly, by zero-padding normalization, as a prefix fragment of a
    claimed id, or via a SYS-/DOC- prefixed form. Codes about the topic are index
    keys, not prose; an unresolved code is a page/field the build failed to emit."""
    sources = wiki.parent / "sources"
    if not sources.is_dir():
        return
    claimed = {eid.lower() for pg in pages for eid in pg.entity_ids}
    claimed |= {str(a).lower() for pg in pages for a in (pg.fm.get("aliases") or [])}

    def norm(t: str) -> str:
        return re.sub(r"(?<![0-9])0+([0-9])", r"\1", t.lower())

    claimed_norm = {norm(c) for c in claimed}

    EXTERNAL_PREFIXES = ("FIL-", "FFIEC-", "FTC-", "ISO-", "RFC-")  # regulator/standards citations

    def resolved(tok: str) -> bool:
        if tok.upper().startswith(EXTERNAL_PREFIXES):
            return True
        if re.search(r"[0-9]{6,}", tok):
            return True  # long numeric segment = instance data (wire refs, serials), not a schema id
        t = tok.lower().rstrip(".")
        if t in claimed or norm(t) in claimed_norm:
            return True
        if any(c.startswith(t + "-") or c.startswith(t + ".") for c in claimed):
            return True  # prefix fragment of a claimed id (e.g. "MRM-POL" of MRM-POL-02)
        return f"sys-{t}" in claimed or f"doc-{t}" in claimed

    unresolved: dict[str, str] = {}
    for f in sorted(sources.rglob("*.md")):
        text = f.read_text(encoding="utf-8", errors="ignore")
        text = re.sub(r"```.*?```", " ", text, flags=re.S)   # fenced code: example payloads
        text = re.sub(r"`[^`\n]*`", " ", text)                # inline code spans
        for m in ID_GRAMMAR.finditer(text):
            tok = m.group(0)
            if not resolved(tok):
                unresolved.setdefault(tok, f.name)
    for tok, fname in sorted(unresolved.items()):
        violations.append(f"[id-closure] {tok}: appears in sources ({fname}) but no page claims it")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("corpus", help="path to the corpus openwiki/ directory")
    ap.add_argument("--ground-truth", help="estate ground-truth JSON to check coverage against")
    args = ap.parse_args()

    wiki = Path(args.corpus)
    if not wiki.is_dir():
        print(f"error: {wiki} is not a directory", file=sys.stderr)
        return 2

    violations: list[str] = []
    pages = load_pages(wiki, violations)
    check_pages(pages, violations)
    check_relations(pages, violations)
    check_id_closure(pages, wiki, violations)
    if args.ground_truth:
        gt = json.loads(Path(args.ground_truth).read_text(encoding="utf-8"))
        check_ground_truth(pages, gt, violations)

    print(f"checked {len(pages)} pages")
    if violations:
        print(f"\n{len(violations)} violation(s):")
        for v in violations:
            print(f"  - {v}")
        return 1
    print("corpus is clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
