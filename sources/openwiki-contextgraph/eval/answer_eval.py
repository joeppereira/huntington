#!/usr/bin/env python3
"""Deterministic answer-verification + gap-fill eval for the CNB Q&A agent.

Runs the five scripted demo questions (Q1=G-020 .. Q5=G-022) against the real Vertex agent,
holding the uploaded feature concept as turn-0 context, then for every REQUIRED FACT checks
deterministically (no LLM) whether it is correctly stated, whether the authoritative source was
actually used, and whether the answer CONTRADICTS the graph's ground-truth value. Missing or
contradicting facts are then gap-filled from the graph/page and the answer is re-verified.

Usage:
  .venv/bin/python eval/answer_eval.py [--runs 3] [--questions Q1,Q2,...]
                                       [--out eval/results/answer_eval.json]

The verifier logic lives in backend/app/answer_verify.py (model-free, unit-tested in CI).
"""

import argparse
import asyncio
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.agent import Turn  # noqa: E402
from app.answer_verify import fill_gaps, score_checks, verify_run  # noqa: E402
from app.config import Settings  # noqa: E402
from app.main import default_agent_factory  # noqa: E402
from app.semantic_tools import SemanticToolkit  # noqa: E402

import answer_keys  # noqa: E402  (eval/answer_keys.py, same dir)

CONCEPT_PATH = ROOT / "eval" / "demo_concept.txt"


def _checks_to_json(checks) -> list[dict]:
    return [asdict(c) for c in checks]


async def run_question(agent, graph, qid: str, question: str, facts, concept: str, runs: int) -> dict:
    history = (Turn(question=concept, answer="Acknowledged."),)
    run_records: list[dict] = []
    pre_scores, post_scores = [], []

    for i in range(runs):
        rec: dict = {"run": i + 1}
        try:
            result = await agent.ask(question, history)
        except Exception as err:  # a transient agent failure is a run failure, not a fact failure
            rec.update({"ok": False, "error": f"{type(err).__name__}: {err}"})
            run_records.append(rec)
            continue

        answer = result.answer.answer
        pages_read = [*result.semantic_pages_read, *result.context_pages_read]
        citation_refs = [s.ref for s in result.answer.sources]
        tools_used = list(result.tools_used)

        pre = verify_run(facts, answer, pages_read, citation_refs, tools_used, graph)
        corrected, corrections = fill_gaps(facts, pre, answer, graph)
        filled_ids = frozenset(c.fact_id for c in corrections)
        post = verify_run(facts, corrected, pages_read, citation_refs, tools_used, graph,
                          filled_ids=filled_ids)

        s_pre = score_checks(pre, pre)
        s_post = score_checks(pre, post)
        pre_scores.append(s_pre)
        post_scores.append(s_post)

        rec.update({
            "ok": True,
            "confidence": result.answer.confidence,
            "tools_used": tools_used,
            "pages_read": pages_read,
            "citation_refs": citation_refs,
            "latency_ms": result.latency_ms,
            "answer": answer,
            "corrected_answer": corrected,
            "facts_pre": _checks_to_json(pre),
            "facts_post": _checks_to_json(post),
            "corrections": [asdict(c) for c in corrections],
            "coverage_pre": round(s_pre.coverage_pre, 4),
            "coverage_post": round(s_post.coverage_post, 4),
            "data_used_pct": round(s_pre.data_used_pct, 4),
            "contradictions": s_pre.contradictions,
        })
        run_records.append(rec)

    ok_runs = [r for r in run_records if r.get("ok")]
    n_ok = len(ok_runs) or 1
    summary = {
        "question_id": qid,
        "golden_id": answer_keys.QUESTIONS[qid]["golden_id"],
        "question": question,
        "runs": runs,
        "run_success_pct": round(len(ok_runs) / runs, 4),
        "n_facts": len(facts),
        "coverage_pre_mean": round(sum(r["coverage_pre"] for r in ok_runs) / n_ok, 4) if ok_runs else 0.0,
        "coverage_post_mean": round(sum(r["coverage_post"] for r in ok_runs) / n_ok, 4) if ok_runs else 0.0,
        "data_used_mean": round(sum(r["data_used_pct"] for r in ok_runs) / n_ok, 4) if ok_runs else 0.0,
        "contradictions_total": sum(r["contradictions"] for r in ok_runs),
        # Per-fact pass matrix across runs: how many ok-runs had each fact VERIFIED_GOOD pre/post.
        "fact_pass_matrix": _fact_matrix(facts, ok_runs),
        "runs_detail": run_records,
    }
    return summary


def _fact_matrix(facts, ok_runs) -> list[dict]:
    rows = []
    for idx, f in enumerate(facts):
        pre_good = sum(1 for r in ok_runs if r["facts_pre"][idx]["verified_good"])
        post_good = sum(1 for r in ok_runs if r["facts_post"][idx]["verified_good"])
        present_pre = sum(1 for r in ok_runs if r["facts_pre"][idx]["present"])
        contra = sum(1 for r in ok_runs if r["facts_pre"][idx]["contradicts_graph"])
        rows.append({
            "fact_id": f.id, "desc": f.desc, "n_ok_runs": len(ok_runs),
            "present_pre": present_pre, "contradicts_graph": contra,
            "verified_good_pre": pre_good, "verified_good_post": post_good,
        })
    return rows


def print_scorecard(report: dict) -> None:
    print("\n" + "=" * 100)
    print("CNB Q&A ANSWER-VERIFICATION SCORECARD  (graph = source of truth; gap-fill is deterministic)")
    print("=" * 100)
    hdr = f"{'Q':<5}{'golden':<8}{'runs':>5}{'run-ok%':>9}{'facts':>6}{'cov-pre':>9}{'contra':>8}{'cov-post':>10}"
    print(hdr)
    print("-" * 100)
    for q in report["questions"]:
        print(f"{q['question_id']:<5}{q['golden_id']:<8}{q['runs']:>5}"
              f"{q['run_success_pct'] * 100:>8.0f}%{q['n_facts']:>6}"
              f"{q['coverage_pre_mean'] * 100:>8.0f}%{q['contradictions_total']:>8}"
              f"{q['coverage_post_mean'] * 100:>9.0f}%")
    print("-" * 100)

    print("\ngpi-ownership contradiction tracker (the graph-backed stale-value catch):")
    for q in report["questions"]:
        for row in q["fact_pass_matrix"]:
            if "GPI-OWNER" in row["fact_id"]:
                print(f"  {q['question_id']} {row['fact_id']}: "
                      f"present_pre {row['present_pre']}/{row['n_ok_runs']}, "
                      f"contradicted_graph {row['contradicts_graph']}/{row['n_ok_runs']}, "
                      f"verified_good pre {row['verified_good_pre']} -> post {row['verified_good_post']}")
    print()


async def main_async(args) -> int:
    settings = Settings()
    corpus = settings.semantic_corpus_path / "openwiki"
    if not corpus.exists():
        print(f"ERROR: semantic corpus not found at {corpus}", file=sys.stderr)
        return 2
    print(f"Loading semantic toolkit from {corpus} ...")
    toolkit = await asyncio.to_thread(SemanticToolkit, corpus)
    graph = toolkit.graph  # the WikiGraph is the deterministic ground-truth source
    agent = default_agent_factory(settings, toolkit.as_langchain_tools())
    print(f"Agent model: {agent.model_id}")

    concept = CONCEPT_PATH.read_text(encoding="utf-8")
    keys = answer_keys.all_answer_keys()
    wanted = args.questions.split(",") if args.questions else list(keys)

    questions = []
    for qid in wanted:
        q = answer_keys.QUESTIONS[qid]["question"]
        print(f"\n### {qid} ({answer_keys.QUESTIONS[qid]['golden_id']}) x{args.runs} runs ...")
        summary = await run_question(agent, graph, qid, q, keys[qid], concept, args.runs)
        questions.append(summary)
        print(f"  run-ok {summary['run_success_pct'] * 100:.0f}%  cov-pre {summary['coverage_pre_mean'] * 100:.0f}%"
              f"  contradictions {summary['contradictions_total']}  cov-post {summary['coverage_post_mean'] * 100:.0f}%")

    report = {
        "model": agent.model_id,
        "runs_per_question": args.runs,
        "corpus": str(corpus),
        "questions": questions,
    }
    out = Path(args.out) if args.out else ROOT / "eval" / "results" / "answer_eval.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2))
    print_scorecard(report)
    print(f"wrote {out}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--questions", default=None, help="comma list, e.g. Q1,Q3 (default: all five)")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    return asyncio.run(main_async(args))


if __name__ == "__main__":
    raise SystemExit(main())
