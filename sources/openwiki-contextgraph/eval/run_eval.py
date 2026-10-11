#!/usr/bin/env python3
"""Run the golden set against the retrieval layer and report ratchet metrics.

Usage:
  python eval/run_eval.py [--corpus semantic-corpus-cnb/openwiki] [--arm enriched|baseline]
                          [--expand] [--k 10] [--out eval/results/<arm>.json]

Metrics (positive items, i.e. expected_refs non-empty):
  ref_hit@1/@5/@10 — any expected_refs page in top-k
  id_coverage@10   — fraction of expected_entity_ids present on top-10 pages
Negative items are excluded from recall; their confidence signals are logged for R6.
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.retrieval import WikiGraph, load_corpus  # noqa: E402
from app.retrieval.retriever import build_retriever  # noqa: E402


def evaluate(corpus_dir: Path, golden: list[dict], *, arm: str, k: int, expand: bool) -> dict:
    retriever = build_retriever(corpus_dir, arm=arm)
    graph = WikiGraph(load_corpus(corpus_dir)) if expand else None

    per_item, per_class = [], {}
    agg = {"ref_hit@1": 0, "ref_hit@5": 0, "ref_hit@10": 0, "id_coverage@10": 0.0, "n": 0}
    negatives = []

    for item in golden:
        result = retriever.search(item["question"], k=k)
        refs = [h.page.ref for h in result.hits]
        if expand and graph is not None:
            # Expansion competes inside the top-k window: keep top half of the retrieval
            # list, then graph neighbors of those seeds, then the rest of the list.
            seeds = refs[: k // 2]
            expanded = [r for r in graph.expand(seeds) if r not in seeds]
            refs = seeds + expanded + [r for r in refs[k // 2 :] if r not in expanded]
        record = {
            "id": item["id"],
            "class": item["class"],
            "confidence": result.confidence.model_dump(),
            "top_refs": refs[:k],
        }
        if not item.get("expected_refs"):
            negatives.append(record)
            continue

        expected = set(item["expected_refs"])
        hit_at = next((i + 1 for i, r in enumerate(refs[:k]) if r in expected), None)
        ids_expected = item.get("expected_entity_ids") or []
        top_ids = {eid for h in result.hits[:10] for eid in h.page.entity_ids}
        id_cov = (sum(1 for e in ids_expected if e in top_ids) / len(ids_expected)) if ids_expected else None

        record.update({"hit_rank": hit_at, "id_coverage": id_cov})
        per_item.append(record)
        agg["n"] += 1
        cls = per_class.setdefault(item["class"], {"n": 0, "hit@10": 0})
        cls["n"] += 1
        if hit_at:
            if hit_at <= 1:
                agg["ref_hit@1"] += 1
            if hit_at <= 5:
                agg["ref_hit@5"] += 1
            if hit_at <= 10:
                agg["ref_hit@10"] += 1
                cls["hit@10"] += 1
        if id_cov is not None:
            agg["id_coverage@10"] += id_cov

    n = agg["n"] or 1
    n_id = sum(1 for r in per_item if r["id_coverage"] is not None) or 1
    metrics = {
        "ref_hit@1": round(agg["ref_hit@1"] / n, 4),
        "ref_hit@5": round(agg["ref_hit@5"] / n, 4),
        "ref_hit@10": round(agg["ref_hit@10"] / n, 4),
        "id_coverage@10": round(agg["id_coverage@10"] / n_id, 4),
    }
    return {
        "metrics": metrics,
        "n_positive": agg["n"],
        "per_class": {
            c: {"n": v["n"], "hit@10": round(v["hit@10"] / v["n"], 4)} for c, v in sorted(per_class.items())
        },
        "negatives": negatives,
        "items": per_item,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=str(ROOT / "semantic-corpus-cnb" / "openwiki"))
    ap.add_argument("--golden", default=str(ROOT / "eval" / "golden_cnb.json"))
    ap.add_argument("--arm", choices=["routed", "fused", "enriched", "baseline"], default="fused")
    ap.add_argument("--expand", action="store_true", help="add 1-hop graph link-expansion")
    ap.add_argument("--k", type=int, default=10)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    golden = json.loads(Path(args.golden).read_text())
    if isinstance(golden, dict):
        golden = golden.get("items", golden.get("questions", []))
    report = evaluate(Path(args.corpus), golden, arm=args.arm, k=args.k, expand=args.expand)
    report["arm"] = args.arm + ("+expand" if args.expand else "")

    out = Path(args.out) if args.out else ROOT / "eval" / "results" / f"{report['arm']}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2))

    print(f"arm={report['arm']} n={report['n_positive']}")
    for k_, v in report["metrics"].items():
        print(f"  {k_:<16} {v:.4f}")
    for c, v in report["per_class"].items():
        print(f"  class {c:<28} hit@10 {v['hit@10']:.2f} (n={v['n']})")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
