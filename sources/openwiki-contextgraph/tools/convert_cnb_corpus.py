"""
Convert the Crestline National Bank (CNB) payments-estate PDFs into Markdown that
OpenWiki's agent can read.

Same idea as tools/convert_corpus.py (Meridian Harbor corpus): OpenWiki cannot open
binary PDFs, so this writes a text corpus into <out>/sources/estate/ and keeps the
originals in <out>/raw/estate/ (excluded from OpenWiki via .openwikiignore).

Usage:
    python tools/convert_cnb_corpus.py --data <dir with the 15 estate PDFs> --out semantic-corpus-cnb

Requires: pymupdf4llm  (pip install pymupdf4llm)
"""
import argparse
import re
import shutil
from pathlib import Path

import pymupdf4llm

# Running headers/footers and bare page numbers seen across the CNB estate PDFs.
_NOISE = re.compile(
    r"^\s*(\**Crestline National Bank\**|\**CRESTLINE NATIONAL BANK\**"
    r"|Synthetic document.*fictional.*|.*[Ff]ictional institution.*"
    r"|Page \d{1,3}(\s+of\s+\d{1,3})?|\d{1,3})\s*$"
)


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9.]+", "-", s.lower()).strip("-")


def clean_page(text: str) -> str:
    out = [ln for ln in text.splitlines() if not _NOISE.match(ln)]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out))


def convert_pdf(pdf: Path, out_dir: Path) -> Path:
    pages = pymupdf4llm.to_markdown(str(pdf), page_chunks=True)
    parts = [
        f"<!-- source: raw/estate/{pdf.name} | converted by tools/convert_cnb_corpus.py -->",
        f"# {pdf.stem.replace('_', ' ')}",
        "",
    ]
    for i, page in enumerate(pages, 1):
        text = page["text"] if isinstance(page, dict) else str(page)
        parts.append(f"\n<!-- page {i} -->\n")
        parts.append(clean_page(text).strip())
    target = out_dir / f"{slug(pdf.stem)}.md"
    target.write_text("\n".join(parts), encoding="utf-8")
    return target


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="directory containing the estate PDFs")
    ap.add_argument("--out", required=True, help="corpus output directory")
    args = ap.parse_args()

    data, out = Path(args.data), Path(args.out)
    src_dir, raw_dir = out / "sources" / "estate", out / "raw" / "estate"
    src_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)

    pdfs = sorted(data.glob("*.pdf"))
    if not pdfs:
        raise SystemExit(f"no PDFs found in {data}")
    for pdf in pdfs:
        shutil.copy2(pdf, raw_dir / pdf.name)
        target = convert_pdf(pdf, src_dir)
        kb = target.stat().st_size // 1024
        print(f"  {pdf.name} -> {target.relative_to(out)} ({kb} KB)")
    print(f"converted {len(pdfs)} PDFs into {src_dir}")


if __name__ == "__main__":
    main()
