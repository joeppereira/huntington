"""
Deterministic, idempotent front-matter augmenter for the CNB wiki (stdlib + pyyaml).

Adds the typed-relation fields defined in docs/schema-relations.md to page front
matter, derived only from estate_ground_truth.json, the pages themselves, and the
curated maps below (which implement the schema doc's curated alias/governed_by
tables). It never removes or rewrites fields it does not manage, and re-running it
produces no further changes (managed keys are merged: existing values are kept,
missing computed values are appended).

Usage:
    python tools/augment_frontmatter.py [--wiki semantic-corpus-cnb/openwiki]
                                        [--ground-truth <estate_ground_truth.json>]

Exit is nonzero when a ground-truth reference the script is responsible for cannot
be resolved to exactly one page (each is listed). Jira keys that have no page are
the known jira-backlog coverage gaps and are reported as skips, not failures.
"""
import argparse
import re
import json
import sys
import unicodedata
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
DEFAULT_WIKI = REPO / "semantic-corpus-cnb/openwiki"
DEFAULT_GT = REPO.parent / "demo-docs/Wire_Tracking_Demo_Kit/estate_ground_truth.json"

# Managed relation keys, in the order they are appended to front matter.
MANAGED_KEYS = [
    "owned_by", "owner", "part_of", "status", "status_note",
    "supersedes", "superseded_by", "governed_by", "relates_to",
    "described_by", "depends_on", "aliases",
]
LIST_KEYS = {"supersedes", "superseded_by", "governed_by", "relates_to",
             "described_by", "depends_on", "aliases", "owned_by"}

HONORIFICS = {"dr", "mr", "mrs", "ms", "prof"}
ID_TOKEN_RE = re.compile(
    r"\b((?:SYS|ADR|EP|EV|BT|INC|PIR|CMP|CBO|GTSI|FCT|PPH|PNG|ENS|TDA|CNB)"
    r"-[A-Z0-9][A-Za-z0-9.-]*[A-Za-z0-9])\b")

# ---- curated maps (from docs/schema-relations.md) -------------------------------

# GT team ids with no name-matchable GT `teams` entry (BIZ-DEP is a business data-
# ownership line, not an engineering team; the wiki's Deposits Data Ownership page
# is its counterpart per the org directory).
EXTRA_TEAM_REFS = {"BIZ-DEP": "openwiki/teams/deposits-data-ownership.md"}

# a supersedes b (b gets superseded_by a). Each pair is verified against page prose
# before writing: one side's body must mention the other's entity id or slug.
SUPERSEDES = [
    # v2 endpoints supersede v1 (GT EP-PPH-01..03 notes: sunset 2027-03-31; the v1
    # page's own prose names v2 as the replacement).
    ("openwiki/interfaces/pph-v2-payments-api.md",
     "openwiki/interfaces/pph-v1-wire-status-api.md"),
    # Event-driven SPS read model supersedes v1 status polling (ADR-PAY-019).
    ("openwiki/interfaces/sps-read-model-api.md",
     "openwiki/interfaces/pph-v1-wire-status-api.md"),
    # GT PNG-1544 links: "superseded by GTSI-0107".
    ("openwiki/projects/gtsi-0107-gpi-real-time-service.md",
     "openwiki/decisions/png-1544.md"),
]

# Curated governed_by map (schema-relations.md): predictions/stats pages ->
# MRM-POL-02 + DUS-07; client-disclosure pages -> POL-FCC-014. A policy edge is
# only written when the page's own body or sources mention that policy.
GOVERNED_BY = {
    "openwiki/datasets/beneficiary-behavior-profile.md":
        ["openwiki/policies/mrm-pol-02.md", "openwiki/policies/dus-07.md"],
    "openwiki/datasets/client-wire-history-features.md":
        ["openwiki/policies/mrm-pol-02.md", "openwiki/policies/dus-07.md"],
    "openwiki/datasets/wire-corridor-stats-daily.md":
        ["openwiki/policies/mrm-pol-02.md", "openwiki/policies/dus-07.md"],
    "openwiki/interfaces/tdip-insights-api.md":
        ["openwiki/policies/mrm-pol-02.md", "openwiki/policies/dus-07.md"],
    "openwiki/concepts/hold-reason-taxonomy-disclosure-tiers.md":
        ["openwiki/policies/pol-fcc-014.md"],
    "openwiki/concepts/settlement-release-completed-semantics.md":
        ["openwiki/policies/pol-fcc-014.md"],
    "openwiki/interfaces/hms-hold-api.md":
        ["openwiki/policies/pol-fcc-014.md"],
}

# Curated system->system dependency statements the source docs state plainly for the
# payment-network systems (schema-relations.md `depends_on`). Each edge is written only
# when the depending page's own prose corroborates it (the target system's core name
# tokens, slug, acronym or entity id appear on the page) — same discipline as SUPERSEDES.
#   PPH overview (PPH-SYS-OVW-9.2 s1): "coordinates screening and holds with ... Hold
#     Management Service (HMS), performs funds control against the Core Deposit Platform
#     (CDP), and routes accepted payments to ... Fedwire Funds Connector or Swift
#     Alliance/gpi Connector".
#   TDIP catalog (TDIP-CAT-2026.2): pay_wire_txn_hist source = PPH (CDC); gpi_tracker_events
#     source = GPI_TRACKER_SNAPSHOT (GPI-C). (fed_ack_events is NOT INGESTED -> no FFC edge.)
DEPENDS_ON_PROSE = {
    "openwiki/systems/prism-payments-hub.md": [
        "openwiki/systems/core-deposit-platform.md",
        "openwiki/systems/fedwire-funds-connector.md",
        "openwiki/systems/swift-gpi-connector.md",
        "openwiki/systems/hold-management-service.md",
    ],
    "openwiki/systems/treasury-data-insights-platform.md": [
        "openwiki/systems/prism-payments-hub.md",
        "openwiki/systems/swift-gpi-connector.md",
    ],
}

# Interface id grammar as it appears inside "Integration inventory" table cells, e.g.
# "GET /pph/v1/wires/{ref}/status (EP-PPH-01)". Consumed endpoints/events/batch feeds.
INVENTORY_ID_RE = re.compile(r"\b((?:EP|EV|BT)-[A-Z0-9]+-[A-Z0-9]+)\b")
GENERIC_NAME_TOKENS = {"the", "a", "of", "and", "service", "platform", "system", "api"}

# Curated vocab-gap alias table (schema-relations.md).
GPI_ALIASES = ["banks passed through", "route", "intermediary banks",
               "freshness", "how fresh", "up to date", "latest data"]
STATUS_API_ALIASES = ["where is my money", "payment location"]
CURATED_ALIASES = {
    "openwiki/concepts/uetr.md": ["tracking number", "parcel tracking"],
    "openwiki/interfaces/gpi-tracker-batch-feed.md": GPI_ALIASES,
    "openwiki/datasets/gpi-tracker-snapshot.md": GPI_ALIASES,
    "openwiki/interfaces/pph-v1-wire-status-api.md": STATUS_API_ALIASES,
    "openwiki/interfaces/pph-v2-payments-api.md": STATUS_API_ALIASES,
    "openwiki/interfaces/sps-read-model-api.md": STATUS_API_ALIASES,
    # refresh page: the Wire Center BFF carries the user-initiated refresh endpoint.
    "openwiki/interfaces/cbo-wire-bff-api.md": ["up to date", "latest data"],
}

SKIP_NAMES = {"INSTRUCTIONS.md", "index.md", "log.md"}

# ---- small helpers --------------------------------------------------------------


def _tokens(text: str) -> list[str]:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return [w for w in re.split(r"[^a-z0-9]+", text.lower()) if w and w not in HONORIFICS]


def name_matches(eid: str, name: str) -> bool:
    """Does a slug-style entity_id plausibly denote this ground-truth name?"""
    nt, et = _tokens(name), _tokens(eid)
    if not et:
        return False
    if "".join(et) == "".join(nt):
        return True
    if set(et) <= set(nt):
        return True
    return len(et) == 1 and et[0] == "".join(w[0] for w in nt)


class Page:
    def __init__(self, path: Path, wiki: Path):
        self.path = path
        self.rel = str(path.relative_to(wiki))           # e.g. teams/gtsi.md
        self.ref = f"openwiki/{self.rel}"                # schema page-ref form
        self.folder = path.parent.name
        text = path.read_text(encoding="utf-8")
        end = text.find("\n---", 3)
        self.fm_text = text[3:end]
        self.body = text[end + len("\n---"):]
        self.fm = yaml.safe_load(self.fm_text) or {}
        raw = self.fm.get("entity_id")
        self.entity_ids = [str(x) for x in raw] if isinstance(raw, list) else (
            [str(raw)] if raw is not None else [])
        self.type = str(self.fm.get("type", ""))
        self.title = str(self.fm.get("title", ""))
        self.additions: dict[str, object] = {}

    def add(self, key: str, value):
        """Record a computed value for a managed key (merged with existing later)."""
        if key in LIST_KEYS:
            cur = self.additions.setdefault(key, [])
            for v in (value if isinstance(value, list) else [value]):
                if v not in cur:
                    cur.append(v)
        else:
            self.additions.setdefault(key, value)

    def source_files(self) -> list[str]:
        out = []
        for s in self.fm.get("sources", []) or []:
            res = str(s.get("resource", "")) if isinstance(s, dict) else str(s)
            if res:
                out.append(res.rsplit("/", 1)[-1])
        return out


def remove_key_lines(lines: list[str], key: str) -> list[str]:
    """Drop a top-level front-matter key and any indented continuation lines."""
    out, i = [], 0
    while i < len(lines):
        if re.match(rf"^{re.escape(key)}:", lines[i]):
            i += 1
            while i < len(lines) and (lines[i].startswith((" ", "\t")) or lines[i] == ""):
                # stop at a blank line followed by a new top-level key
                if lines[i] == "" and i + 1 < len(lines) and not lines[i + 1].startswith(" "):
                    break
                i += 1
            continue
        out.append(lines[i])
        i += 1
    return out


def dump_kv(key: str, value) -> str:
    # default_flow_style=None would render a scalar-valued mapping itself in flow
    # style ("{key: value}"); force block style there, flow only for list values.
    flow = None if isinstance(value, (list, dict)) else False
    text = yaml.safe_dump({key: value}, default_flow_style=flow, width=4096,
                          allow_unicode=True, sort_keys=False)
    return text.rstrip("\n")


# ---- normalization --------------------------------------------------------------


def norm_interface_status(raw: str) -> tuple[str, str]:
    s = raw.strip()
    low = s.lower()
    if low.startswith("deprecated"):
        enum = "deprecated"
    elif low.startswith("does not exist"):
        enum = "absent"
    elif low.startswith("proposed"):
        enum = "proposed"
    else:
        enum = "live"
    m = re.match(r"(?i)^(deprecated|does not exist|proposed|ga|production|live)\s*(.*)$", s)
    rest = m.group(2) if m else s
    rest = rest.strip().strip("()").strip()
    return enum, rest


def norm_jira_status(raw: str) -> tuple[str, str]:
    s = raw.strip()
    low = s.lower()
    if low.startswith(("closed", "done", "won't do", "wont do")):
        enum = "closed"
    elif low.startswith(("backlog", "planned", "to do")):
        enum = "proposed"
    elif low.startswith(("in progress", "open")):
        enum = "live"
    else:
        raise ValueError(f"unmapped jira status: {raw!r}")
    m = re.match(r"(?i)^(closed|done|won't do|backlog \(no sponsor\)|backlog|planned|to do|in progress|open)\s*(.*)$", s)
    rest = (m.group(2) if m else "").strip().strip("()").strip()
    if low.startswith("backlog (no sponsor)"):
        rest = "no sponsor"
    return enum, rest


def gt_name_alias_parts(name: str) -> list[str]:
    """Split a GT display name into candidate alias phrases."""
    parts = []
    for paren in re.findall(r"\(([^)]+)\)", name):
        parts.append(paren)
    bare = re.sub(r"\([^)]*\)", "", name)
    for seg in re.split(r"\s+-\s+|\s+/\s+", bare):
        seg = seg.strip(" ,")
        if seg:
            parts.append(seg)
    out = []
    for p in parts:
        p = p.lower().strip()
        if p and not re.match(r"^\d", p) and p not in out:
            out.append(p)
    return out


# ---- main -----------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--wiki", default=str(DEFAULT_WIKI))
    ap.add_argument("--ground-truth", default=str(DEFAULT_GT))
    args = ap.parse_args()

    wiki = Path(args.wiki)
    gt = json.loads(Path(args.ground_truth).read_text(encoding="utf-8"))

    errors: list[str] = []
    skips: list[str] = []

    pages: list[Page] = []
    for md in sorted(wiki.rglob("*.md")):
        if ".claims" in md.parts or md.name in SKIP_NAMES or md.parent == wiki:
            continue
        pages.append(Page(md, wiki))
    by_ref = {p.ref: p for p in pages}
    by_id: dict[str, list[Page]] = {}
    for p in pages:
        for eid in p.entity_ids:
            by_id.setdefault(eid, []).append(p)

    def resolve_id(eid: str) -> Page | None:
        ps = by_id.get(eid, [])
        return ps[0] if len(ps) == 1 else None

    # --- GT id -> page ref maps ---
    team_ref: dict[str, str] = dict(EXTRA_TEAM_REFS)
    team_pages = [p for p in pages if p.type == "Team"]
    for t in gt.get("teams", []):
        hits = [p for p in team_pages
                if any(name_matches(e, t["name"]) for e in p.entity_ids)
                or name_matches(p.path.stem, t["name"])]
        if len(hits) != 1:
            errors.append(f"team {t['id']} ({t['name']!r}): {len(hits)} page matches "
                          f"({', '.join(p.rel for p in hits)})")
            continue
        team_ref[t["id"]] = hits[0].ref
    for gid, ref in EXTRA_TEAM_REFS.items():
        if ref not in by_ref:
            errors.append(f"curated team ref for {gid} does not exist: {ref}")

    person_ref: dict[str, str] = {}
    person_pages = [p for p in pages if p.type == "Person"]
    for pe in gt.get("people", []):
        hits = [p for p in person_pages
                if any(name_matches(e, pe["name"]) for e in p.entity_ids)
                or name_matches(p.path.stem, pe["name"])]
        if len(hits) == 1:
            person_ref[pe["id"]] = hits[0].ref
        elif len(hits) > 1:
            errors.append(f"person {pe['id']} ({pe['name']!r}): multiple page matches")
        # P-SWHIT has no page by design; absence only matters if referenced below.

    gt_systems = {s["id"]: s for s in gt.get("systems", [])}

    # --- owned_by on systems; aliases from GT system names ---
    for sid, s in gt_systems.items():
        p = resolve_id(sid)
        if p is None:
            errors.append(f"system {sid}: no unique page claims this id")
            continue
        owner = s.get("owner_team_current")
        if owner not in team_ref:
            errors.append(f"system {sid}: owner team {owner} has no team page mapping")
        else:
            p.add("owned_by", team_ref[owner])
        title_toks = set(_tokens(p.title))
        for part in gt_name_alias_parts(s["name"]):
            if not set(_tokens(part)) <= title_toks:
                p.add("aliases", part)

    # --- interfaces: part_of, owned_by, status(+note) ---
    iface_pages: dict[str, list[dict]] = {}
    for itf in gt.get("interfaces", []):
        if "does not exist" in itf["status"].lower():
            # no page is created for these by design; if a page *does* claim the id,
            # it still gets status: absent below via iface_pages handling
            p = resolve_id(itf["id"])
            if p is None:
                continue
        else:
            p = resolve_id(itf["id"])
            if p is None:
                errors.append(f"interface {itf['id']}: no unique page claims this id")
                continue
        iface_pages.setdefault(p.ref, []).append(itf)

    for ref, itfs in iface_pages.items():
        p = by_ref[ref]
        systems = {i["system"] for i in itfs}
        if len(systems) != 1:
            # A cross-system page whose interfaces all "do not exist" is a proposed-
            # interfaces registry, not a real interface of one system: skip part_of/
            # owned_by (its own front matter already carries status: absent).
            if all("does not exist" in i["status"].lower() for i in itfs):
                skips.append(f"{p.rel}: cross-system proposed-interfaces registry; part_of skipped")
                continue
            errors.append(f"{p.rel}: entity_ids span multiple GT systems: {sorted(systems)}")
            continue
        sysid = systems.pop()
        sys_page = resolve_id(sysid)
        if sys_page is None:
            errors.append(f"{p.rel}: GT system {sysid} has no page")
            continue
        p.add("part_of", sys_page.ref)
        owner = gt_systems[sysid].get("owner_team_current")
        if owner in team_ref:
            p.add("owned_by", team_ref[owner])
        else:
            errors.append(f"{p.rel}: owner team {owner} unresolved")
        enums, notes = [], []
        for i in itfs:
            e, n = norm_interface_status(i["status"])
            enums.append(e)
            if n and n not in notes:
                notes.append(n)
        if len(set(enums)) != 1:
            errors.append(f"{p.rel}: conflicting normalized statuses {sorted(set(enums))}")
            continue
        p.add("status", enums[0])
        if notes:
            p.add("status_note", "; ".join(notes))

    # --- jira-keyed pages: status(+note), owner (projects), relates_to ---
    for j in gt.get("jira", []):
        p = resolve_id(j["key"])
        if p is None:
            skips.append(f"jira {j['key']}: no page (known backlog coverage gap)")
            continue
        try:
            enum, note = norm_jira_status(j["status"])
        except ValueError as e:
            errors.append(f"{p.rel}: {e}")
            continue
        p.add("status", enum)
        if note:
            p.add("status_note", note)
        if p.type == "Project":  # schema: `owner` is Project -> Person only
            oref = person_ref.get(j.get("owner", ""))
            if oref is None:
                errors.append(f"{p.rel}: jira owner {j.get('owner')} has no person page")
            else:
                p.add("owner", oref)
        links = j.get("links", "") or ""
        linked_ids = [x for x in ID_TOKEN_RE.findall(links) if x != j["key"]]
        for lid in linked_ids:
            tp = resolve_id(lid)
            if tp is None:
                skips.append(f"jira {j['key']} links -> {lid}: no page (known coverage gap)")
                continue
            if p.type not in ("Project", "Incident", "Document", "Person"):
                continue  # schema restricts relates_to sources
            if any(tp.ref in (p.additions.get(k) or []) for k in ("supersedes", "superseded_by")):
                continue
            p.add("relates_to", tp.ref)

    # --- supersedes / superseded_by (verified against prose) ---
    for a_ref, b_ref in SUPERSEDES:
        a, b = by_ref.get(a_ref), by_ref.get(b_ref)
        if a is None or b is None:
            errors.append(f"supersedes pair missing page: {a_ref} / {b_ref}")
            continue
        mention = (
            any(eid in b.body or eid in b.fm_text for eid in a.entity_ids)
            or any(eid in a.body or eid in a.fm_text for eid in b.entity_ids)
            or a.path.stem in b.body or b.path.stem in a.body
        )
        if not mention:
            errors.append(f"supersedes {a_ref} -> {b_ref}: no corroborating mention in prose")
            continue
        a.add("supersedes", b.ref)
        b.add("superseded_by", a.ref)

    # --- governed_by (curated, corroborated by page sources/body) ---
    for ref, pol_refs in GOVERNED_BY.items():
        p = by_ref.get(ref)
        if p is None:
            errors.append(f"governed_by source page missing: {ref}")
            continue
        for pol in pol_refs:
            polp = by_ref.get(pol)
            if polp is None:
                errors.append(f"governed_by target missing: {pol}")
                continue
            pid = polp.entity_ids[0]
            hay = p.body + p.fm_text
            if pid in hay or polp.path.stem in hay.lower():
                p.add("governed_by", pol)
            else:
                skips.append(f"{p.rel}: governed_by {pid} skipped (no mention on page)")

    # --- described_by: page sources -> documents/ pages (System/Interface/Policy) ---
    doc_pages = [p for p in pages if p.folder == "documents"]
    for p in pages:
        if p.type not in ("System", "Interface", "Policy"):
            continue
        for fname in p.source_files():
            hits = [d for d in doc_pages
                    if fname == d.path.stem + ".md" or fname.startswith(d.path.stem + "-")]
            if len(hits) == 1:
                p.add("described_by", hits[0].ref)
            elif len(hits) > 1:
                skips.append(f"{p.rel}: source {fname} matches {len(hits)} document pages; skipped")
            else:
                errors.append(f"{p.rel}: source {fname} matches no documents/ page")

    # --- depends_on: system->system edges (docs/schema-relations.md) ---
    # (a) interface id -> owning system ref (ground truth interfaces[].system).
    iface_sys_ref: dict[str, str] = {}
    for itf in gt.get("interfaces", []):
        sp = resolve_id(itf["system"])
        if sp is not None:
            iface_sys_ref[itf["id"]] = sp.ref

    # (b) a consumer-component string -> its system page ref. A component (e.g.
    # "cbo-wire-bff") resolves via the interface page whose slug is that component,
    # taking its part_of; falling back to a system page that name-matches. Only an
    # unambiguous single system counts.
    iface_pages_all = [p for p in pages if p.type == "Interface"]
    system_pages = [p for p in pages if p.type == "System"]

    def part_of_ref(p: Page) -> str | None:
        v = p.additions.get("part_of") or p.fm.get("part_of")
        return v if isinstance(v, str) else None

    def resolve_consumer(component: str) -> str | None:
        slug = "-".join(_tokens(component))
        if not slug:
            return None
        sysrefs = set()
        for ip in iface_pages_all:
            stem = ip.path.stem
            if stem == slug or stem == f"{slug}-api" or stem.startswith(f"{slug}-"):
                r = part_of_ref(ip)
                if r:
                    sysrefs.add(r)
        if not sysrefs:
            for sp in system_pages:
                if name_matches(sp.path.stem, component) or any(
                    name_matches(e, component) for e in sp.entity_ids
                ):
                    sysrefs.add(sp.ref)
        return next(iter(sysrefs)) if len(sysrefs) == 1 else None

    derived: dict[str, set] = {}  # consumer system ref -> set of depended system refs

    def add_dep(consumer_ref: str, target_ref: str) -> None:
        if consumer_ref and target_ref and consumer_ref != target_ref \
                and consumer_ref in by_ref and target_ref in by_ref:
            derived.setdefault(consumer_ref, set()).add(target_ref)

    # (c) parse source "Integration inventory"-style tables: a consumer component in
    # column 0 and the interface id(s) it consumes (EP-/EV-/BT- in parentheses).
    sources_dir = wiki.parent / "sources"
    for src in sorted(sources_dir.rglob("*.md")) if sources_dir.is_dir() else []:
        for line in src.read_text(encoding="utf-8", errors="ignore").splitlines():
            if not line.lstrip().startswith("|") or set(line.strip()) <= set("|-: "):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if not cells:
                continue
            consumer = re.sub(r"[*`<][^>]*>?|[*`]", "", cells[0]).strip()
            ids = INVENTORY_ID_RE.findall(line)
            if not consumer or not ids:
                continue
            consumer_ref = resolve_consumer(consumer)
            if consumer_ref is None:
                continue
            for iid in ids:
                tgt = iface_sys_ref.get(iid)
                if tgt:
                    add_dep(consumer_ref, tgt)

    # (d) curated, prose-corroborated payment-network dependency statements.
    for consumer_ref, targets in DEPENDS_ON_PROSE.items():
        cp = by_ref.get(consumer_ref)
        if cp is None:
            errors.append(f"depends_on source page missing: {consumer_ref}")
            continue
        hay = set(_tokens(cp.body + cp.fm_text))
        for tgt in targets:
            tp = by_ref.get(tgt)
            if tp is None:
                errors.append(f"depends_on target missing: {tgt}")
                continue
            core = re.sub(r"\([^)]*\)", "", tp.title)
            name_toks = set(_tokens(core)) - GENERIC_NAME_TOKENS
            corroborated = (
                (name_toks and name_toks <= hay)
                or tp.path.stem in cp.body
                or any(e.lower() in cp.body.lower() for e in tp.entity_ids)
            )
            if corroborated:
                add_dep(consumer_ref, tgt)
            else:
                skips.append(f"{cp.rel}: depends_on {tp.rel} skipped (no corroborating prose)")

    for consumer_ref, targets in sorted(derived.items()):
        by_ref[consumer_ref].add("depends_on", sorted(targets))
        names = ", ".join(Path(t).stem for t in sorted(targets))
        print(f"  depends_on {Path(consumer_ref).stem}: {names}", file=sys.stderr)

    # --- aliases: GT team/people names that differ from page titles ---
    for t in gt.get("teams", []):
        ref = team_ref.get(t["id"])
        if not ref:
            continue
        p = by_ref[ref]
        title_toks = set(_tokens(p.title))
        for part in gt_name_alias_parts(t["name"]):
            if not set(_tokens(part)) <= title_toks:
                p.add("aliases", part)
    for pe in gt.get("people", []):
        ref = person_ref.get(pe["id"])
        if not ref:
            continue
        p = by_ref[ref]
        title_toks = set(_tokens(p.title))
        for part in gt_name_alias_parts(pe["name"]):
            if not set(_tokens(part)) <= title_toks:
                p.add("aliases", part)

    # --- aliases: curated vocab-gap table ---
    for ref, aliases in CURATED_ALIASES.items():
        p = by_ref.get(ref)
        if p is None:
            errors.append(f"curated alias page missing: {ref}")
            continue
        p.add("aliases", aliases)

    if errors:
        print("UNRESOLVED ground-truth references:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    # --- write: merge additions into front matter ---
    added: dict[str, dict[str, int]] = {}   # folder -> field -> count of values added
    changed_files = 0
    for p in pages:
        if not p.additions:
            continue
        new_fm = dict(p.fm)
        changed_keys = []
        for key in MANAGED_KEYS:
            if key not in p.additions:
                continue
            want = p.additions[key]
            if key in LIST_KEYS:
                existing = new_fm.get(key)
                existing = ([existing] if isinstance(existing, str) else list(existing or []))
                missing = [v for v in want if v not in existing]
                if not missing:
                    continue
                new_fm[key] = existing + missing
                changed_keys.append(key)
                added.setdefault(p.folder, {}).setdefault(key, 0)
                added[p.folder][key] += len(missing)
            else:
                if key in new_fm:
                    continue  # never overwrite an existing scalar
                new_fm[key] = want
                changed_keys.append(key)
                added.setdefault(p.folder, {}).setdefault(key, 0)
                added[p.folder][key] += 1
        if not changed_keys:
            continue
        lines = p.fm_text.split("\n")
        for key in changed_keys:
            lines = remove_key_lines(lines, key)
        while lines and lines[-1] == "":
            lines.pop()
        for key in changed_keys:
            lines.append(dump_kv(key, new_fm[key]))
        p.path.write_text("---" + "\n".join(lines) + "\n---" + p.body, encoding="utf-8")
        changed_files += 1

    print(f"augmented {changed_files} page(s)")
    for folder in sorted(added):
        fields = ", ".join(f"{k}+{v}" for k, v in sorted(added[folder].items()))
        print(f"  {folder}: {fields}")
    if skips:
        print(f"\n{len(skips)} skip(s) (known coverage gaps / uncorroborated):")
        for s in skips:
            print(f"  - {s}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
