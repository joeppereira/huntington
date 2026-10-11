"""Corpus loader: frontmatter walker + deterministic chunk enrichment.

Walks <corpus>/openwiki/**/*.md, parses YAML frontmatter, and produces Pages with
enriched chunks. Enrichment (ratchet R3) is the deterministic adaptation of the
measured-best gtm_cloud HierarchicalChunker-F: each chunk is prefixed with
  type / title > heading-breadcrumb . [type · status · entity ids] . entities: <co-entities>
where co-entities are the titles of pages this page cross-links (author-curated graph),
restricted to links appearing in that chunk's section. No LLM anywhere (experiment #4:
how much of contextual retrieval's gain the corpus structure yields for free).

Folder index.md listing pages and wiki-root nav pages are excluded from the search index
(they match broadly and ground nothing), but index pages still contribute no links either.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

NAV_STEMS = {"index", "overview", "quickstart", "timeline", "INSTRUCTIONS"}

# Typed-relation frontmatter fields (docs/schema-relations.md). All optional: the corpus
# build adds them incrementally, so every field defaults to [] and nothing here may
# assume their presence. Values are page refs ("openwiki/<folder>/<slug>.md").
RELATION_FIELDS = (
    "owned_by", "owner", "part_of", "governed_by",
    "relates_to", "described_by", "supersedes", "superseded_by",
)
STATUS_ENUM = {"live", "deprecated", "proposed", "closed", "absent"}
_FRONT = re.compile(r"\A---\n(.*?)\n---\n?", re.S)
_MD_LINK = re.compile(r"\]\(((?:\.\./|\./)?[\w./-]+\.md)(?:#[^)]*)?\)")
_HEADING = re.compile(r"^(#{1,3})\s+(.*)")


@dataclass
class Chunk:
    text: str  # enriched text (what gets indexed)
    body: str  # raw section body (for snippets)
    heading: str


@dataclass
class Page:
    ref: str  # "openwiki/<folder>/<slug>.md"
    type: str
    title: str
    entity_ids: list[str]
    status: str | None
    tags: list[str]
    description: str
    body: str
    links: list[str] = field(default_factory=list)  # refs of cross-linked pages
    chunks: list[Chunk] = field(default_factory=list)
    # Gap-fix round (docs/schema-relations.md) — all optional, default-empty:
    aliases: list[str] = field(default_factory=list)
    status_norm: str | None = None  # `status` normalized to STATUS_ENUM, else None
    owned_by: list[str] = field(default_factory=list)
    owner: list[str] = field(default_factory=list)
    part_of: list[str] = field(default_factory=list)
    governed_by: list[str] = field(default_factory=list)
    relates_to: list[str] = field(default_factory=list)
    described_by: list[str] = field(default_factory=list)
    supersedes: list[str] = field(default_factory=list)
    superseded_by: list[str] = field(default_factory=list)


def _as_list(v) -> list[str]:
    if v is None:
        return []
    if isinstance(v, str):
        return [v]
    return [str(x) for x in v]


def _parse_page(path: Path, root: Path) -> Page | None:
    text = path.read_text(encoding="utf-8")
    m = _FRONT.match(text)
    if not m:
        return None
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return None
    body = text[m.end():]
    ref = path.relative_to(root.parent).as_posix()
    links = []
    for raw in _MD_LINK.findall(body):
        target = (path.parent / raw).resolve()
        try:
            links.append(target.relative_to(root.parent.resolve()).as_posix())
        except ValueError:
            continue
    raw_status = fm.get("status")
    norm = str(raw_status).strip().lower() if raw_status is not None else ""
    return Page(
        ref=ref,
        type=str(fm.get("type", path.parent.name)),
        title=str(fm.get("title", path.stem)),
        entity_ids=_as_list(fm.get("entity_id")),
        status=raw_status,
        tags=_as_list(fm.get("tags")),
        description=str(fm.get("description", "")),
        body=body,
        links=links,
        aliases=_as_list(fm.get("aliases")),
        status_norm=norm if norm in STATUS_ENUM else None,
        **{f: _as_list(fm.get(f)) for f in RELATION_FIELDS},
    )


def _chunk_page(page: Page, titles_by_ref: dict[str, str], cap: int = 600, max_co: int = 8) -> list[Chunk]:
    doc_tags = " · ".join(filter(None, [page.type, page.status, *page.entity_ids]))
    aka = f" aka: {', '.join(page.aliases)}." if page.aliases else ""
    chunks: list[Chunk] = []
    stack: dict[int, str] = {}
    buf: list[str] = []
    cur = ""

    def flush(hpath: str):
        body = "\n".join(buf).strip()
        if not body:
            return
        co = []
        for raw in _MD_LINK.findall(body):
            slug = Path(raw).name
            for ref, title in titles_by_ref.items():
                if ref.endswith("/" + slug) and title not in co:
                    co.append(title)
        crumb = f"{page.type} / {page.title}" + (f" > {hpath}" if hpath else "")
        ce = f" entities: {', '.join(co[:max_co])}." if co else ""
        prefix = f"{crumb}. [{doc_tags}].{aka}{ce} "
        for s in range(0, len(body), cap):
            chunks.append(Chunk(text=prefix + body[s : s + cap], body=body[s : s + cap], heading=hpath))

    for ln in page.body.split("\n"):
        m = _HEADING.match(ln)
        if m:
            flush(cur)
            buf = []
            lvl = len(m.group(1))
            stack[lvl] = m.group(2).strip()
            for l in [x for x in stack if x > lvl]:
                stack.pop(l, None)
            cur = " > ".join(stack[l] for l in sorted(stack))
        else:
            buf.append(ln)
    flush(cur)
    # The description is the page's best self-summary — index it as a chunk too.
    if page.description:
        chunks.insert(
            0,
            Chunk(
                text=f"{page.type} / {page.title}. [{doc_tags}].{aka} {page.description}",
                body=page.description,
                heading="",
            ),
        )
    return [c for c in chunks if len(c.text) > 40]


def load_corpus(openwiki_dir: str | Path, *, enrich: bool = True) -> list[Page]:
    """Load all entity pages (nav/index pages excluded) with chunks ready to index.

    enrich=False indexes raw section text only (the R0 baseline arm for the eval)."""
    root = Path(openwiki_dir)
    pages: list[Page] = []
    for path in sorted(root.rglob("*.md")):
        if path.stem in NAV_STEMS or path.parent == root:
            continue
        page = _parse_page(path, root)
        if page is not None:
            pages.append(page)
    titles = {p.ref: p.title for p in pages} if enrich else {}
    for p in pages:
        if enrich:
            p.chunks = _chunk_page(p, titles)
        else:
            aka = f"aka: {', '.join(p.aliases)}.\n" if p.aliases else ""
            p.chunks = [
                Chunk(text=aka + p.description + "\n" + p.body, body=p.body, heading="")
            ]
    return pages
