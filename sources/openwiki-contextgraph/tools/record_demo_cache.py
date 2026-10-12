"""
Record the demo answer cache (demo-cache/answer-cache.md) from live runs of the graph agent.

Runs the ten Wire Tracking Center demo questions through the running backend in ONE chat session
(concept PDF attached first, cache bypassed), then writes each answer, its sources and its full
tool trace into the cache file with the question's intent and example wordings for the matcher.

Usage (from the project root, with the app running):
    .venv/bin/python tools/record_demo_cache.py
    .venv/bin/python tools/record_demo_cache.py --only WTC-Q04 WTC-Q07   # re-record some entries
    .venv/bin/python tools/record_demo_cache.py --base-url http://127.0.0.1:8010

--only re-asks just those questions (in a fresh session with the concept attached) and keeps the
other entries of the existing file. Turn on serving with DEMO_CACHE_ENABLED=true in .env.
"""
import argparse
import base64
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
sys.path.insert(0, str(ROOT / "eval"))

from app.agent import split_leaked_markup  # noqa: E402
from app.answer_cache import CacheEntry, load_cache, render_cache_markdown  # noqa: E402
from app.answer_verify import fill_gaps, verify_run  # noqa: E402
from app.config import Settings  # noqa: E402
from app.retrieval import WikiGraph, load_corpus  # noqa: E402

import answer_keys  # noqa: E402  (eval/answer_keys.py)


def verify_and_fill(entry_id: str, response: dict, graph: WikiGraph) -> tuple[str, str]:
    """Run the deterministic verifier over a recorded answer and gap-fill from the graph, so the
    CACHED answer is provably correct (e.g. the gpi owner is GTSI, not the concept's stale PNE).
    Returns (answer_to_cache, one-line verification summary)."""
    qkey = f"Q{int(entry_id.rsplit('Q', 1)[-1])}"  # "WTC-Q01" -> "Q1"
    facts = answer_keys.all_answer_keys().get(qkey)
    answer = split_leaked_markup(response["answer"])[0]
    if not facts:
        return answer, "no fact key"
    steps = response["trace"]["steps"]
    tools_used = [s["tool"] for s in steps]
    pages_read = [r for s in steps if s["tool"] == "semantic_read" for r in s.get("refs", [])]
    citations = [s["ref"] for s in response["sources"]]
    pre = verify_run(facts, answer, pages_read, citations, tools_used, graph)
    corrected, corrections = fill_gaps(facts, pre, answer, graph)
    good = sum(c.verified_good for c in pre)
    contra = sum(c.contradicts_graph for c in pre)
    summary = (f"{good}/{len(facts)} facts good"
               + (f", {contra} CONTRADICTED graph" if contra else "")
               + (f", {len(corrections)} gap-filled" if corrections else " (clean)"))
    return corrected, summary

DEFAULT_CONCEPT = (ROOT.parent / "demo-docs" / "Wire_Tracking_Demo_Kit" / "Demo_Script"
                   / "01_Wire_Tracking_Center_Concept.pdf")
DEFAULT_OUT = ROOT / "demo-cache" / "answer-cache.md"

# id, title, the Demo Pack question, the intent the matcher compares against, other wordings.
QUESTIONS = [
    ("WTC-Q01", "Dependencies and owners",
     "I've uploaded my market research and concept. Before I write the BRD: which existing systems does the "
     "Wire Tracking Center depend on, and who owns each today?",
     "Which existing systems, platform services and approval functions the Wire Tracking Center depends on, "
     "and who owns each of them today (including any recent ownership change).",
     ["What are the dependencies for this feature and who are the owners?",
      "Map the systems and teams the wire tracker relies on.",
      "Who do I need to work with - which systems does this touch and who owns them now?"]),
    ("WTC-Q02", "'Settled' vs 'Completed' for domestic wires",
     "My timeline ends in 'Settled'. Wire Center already shows 'Completed' - can we just use that?",
     "Whether today's 'Completed' status can be used as the 'Settled' step of the domestic wire timeline, "
     "and what a true settled milestone would need.",
     ["Can 'Completed' be our 'Settled' status?",
      "Is the existing Completed label good enough to show a wire as settled?",
      "What do we need to show 'Settled' on the timeline?"]),
    ("WTC-Q03", "Live international gpi route",
     "For international wires I want the live SWIFT gpi route, refreshed every minute, with 'Expected delivery: "
     "Today'. Feasible for Q1 2027?",
     "Whether a live, minute-by-minute SWIFT gpi route with 'Expected delivery: Today' for international wires "
     "is feasible (for Q1 2027), and what is realistic instead.",
     ["Can we show a live FedEx-style map for international wires?",
      "Is real-time gpi tracking possible for the Q1 2027 launch?",
      "How fresh can the international wire route be?"]),
    ("WTC-Q04", "Held-wire design review",
     "Review FC-03. Clients want to know why a wire is held and to fix it themselves. Any issues?",
     "A review of the held-wire design (FC-03: showing the hold reason, Confirm/Reject self-service, release "
     "time estimate) for policy, control and missing-interface issues.",
     ["Any problems with showing clients why their wire is held?",
      "Can clients confirm or reject held wires themselves?",
      "Check my held wire self-service design."]),
    ("WTC-Q05", "In-flight conflicts",
     "Before I go further - is anything already in the Wire Center backlog or in production that conflicts with "
     "policy or with this feature?",
     "Whether anything already in flight (backlog, upcoming release or production) conflicts with policy or "
     "with the Wire Tracking Center.",
     ["Is there anything in progress that clashes with this?",
      "Any existing Jira work or live features that conflict with policy?",
      "What in the current backlog could block or contradict this feature?"]),
    ("WTC-Q06", "Insights and predictions",
     "FC-04: can we show 'Beneficiary typically moves funds within 4 hours', '92% of similar EUR wires complete "
     "same day', and a predicted delivery time based on the client's similar past wires?",
     "Whether the FC-04 wire insights (beneficiary moves funds within N hours, share of similar wires completing "
     "same day, predicted delivery time) can be shown to clients, and compliant alternatives.",
     ["Are the wire insights in FC-04 allowed?",
      "Can we predict delivery time from past wires?",
      "Can we tell clients how fast the beneficiary usually moves the money?"]),
    ("WTC-Q07", "Missing endpoints and builders",
     "List every endpoint, field or event we need that doesn't exist yet, the owning team, and any existing ticket.",
     "The full list of endpoints, fields, events or data the feature needs that do not exist yet, with the "
     "owning team and any existing ticket.",
     ["What APIs are missing and who builds them?",
      "Give me the gap list of interfaces we need.",
      "Which endpoints don't exist yet for this feature?"]),
    ("WTC-Q08", "Per-wire notifications",
     "Can a client subscribe to a single wire - 'notify me when it settles'?",
     "Whether a client can subscribe to notifications for one specific wire (for example 'notify me when it "
     "settles'), and the workaround and lead times.",
     ["Can we notify a client when one particular wire settles?",
      "Do per-wire alerts work with the notification service?",
      "Is 'notify me when this wire settles' possible?"]),
    ("WTC-Q09", "Prior attempts and reuse",
     "Has anyone attempted wire tracking before? What should we avoid, and what can we reuse?",
     "Whether wire tracking was attempted before, what went wrong, what to avoid and what can be reused.",
     ["Was this tried before?",
      "Any lessons learned from earlier wire status projects?",
      "What existing components can we reuse for the tracker?"]),
    ("WTC-Q10", "Effort, engagement plan and critical path",
     "Draft the dependency, effort and engagement section of the BRD: which teams to talk to, how many hours to "
     "allocate, approvals, lead times and the critical path.",
     "The BRD dependency, effort and engagement plan: teams to engage, hours per team, approvals, lead times, "
     "phasing and the critical path.",
     ["How many hours and which teams will this take?",
      "Give me the effort estimate and critical path.",
      "Write the engagement plan for the BRD."]),
]

# Sharper wording sent while recording, where the Demo Pack wording alone gives a thin answer.
# The Demo Pack wording stays the first example the matcher compares against.
RECORD_AS = {
    "WTC-Q01": "I've uploaded my market research and concept. Before I write the BRD: which existing systems does "
               "the Wire Tracking Center depend on, and who owns each today? Cover the core payment systems "
               "(payments hub, Fedwire and gpi connectors, hold management, notifications, the data and insights "
               "platform), the CBO platform services, and every partner or approval function that holds a gate "
               "(compliance, model risk, privacy, disclosure review, architecture, security, operations, support). "
               "Flag any owner in my concept that is out of date.",
    "WTC-Q02": "My timeline ends in 'Settled'. Wire Center already shows 'Completed' - can we just use that? If not, "
               "what would a true 'Settled' milestone need (APIs, fields, tickets, deadlines, rail differences "
               "between Fedwire and Swift), and what should the domestic milestones be?",
    "WTC-Q05": "Before I go further - is anything already in the Wire Center backlog or in production that conflicts "
               "with policy or with this feature? Check across the whole concept (FC-01 to FC-07): status labels and "
               "templates, holds, gpi, migrations and data loads - and rank them by urgency.",
    "WTC-Q10": "Draft the dependency, effort and engagement section of the BRD. For every engineering team and "
               "approval function: scope, size in story points from the tickets, hours (apply the planning factors "
               "from the engagement directory to those sizes), lead time or gate, and contact. Then give the total "
               "hours, the critical path, a phased plan, and the actions for this week.",
}


def default_base_url() -> str:
    port = os.environ.get("BACKEND_PORT")
    if not port and (ROOT / ".env").is_file():
        match = re.search(r"^BACKEND_PORT=(\d+)", (ROOT / ".env").read_text(), re.M)
        port = match.group(1) if match else None
    return f"http://127.0.0.1:{port or 8000}"


class RequestFailed(Exception):
    pass


def post(base: str, path: str, body: dict, timeout: float = 600) -> dict:
    request = urllib.request.Request(
        base + path, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as err:
        raise RequestFailed(f"POST {path} failed: HTTP {err.code} {err.read().decode()[:300]}") from err


def entry_from_response(spec: tuple, response: dict, model: str, asked: str, answer: str) -> CacheEntry:
    entry_id, title, question, intent, examples = spec
    trace = response["trace"]
    return CacheEntry(
        id=entry_id, title=title, intent=intent, example_questions=[question, *examples],
        recorded_question=asked if asked != question else "",
        recorded_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        recorded_model=model, recorded_latency_ms=trace["latency_ms"],
        confidence=response["confidence"], answer=answer, sources=response["sources"],
        follow_up_questions=response["follow_up_questions"], reasoning_summary=response["reasoning_summary"],
        trace={"input_tokens": trace["input_tokens"], "output_tokens": trace["output_tokens"],
               "steps": trace["steps"]},
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base-url", default=default_base_url())
    parser.add_argument("--concept", type=Path, default=DEFAULT_CONCEPT, help="PDF attached before the questions")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--only", nargs="+", metavar="ID", help="re-record only these entries")
    args = parser.parse_args()

    ids = [q[0] for q in QUESTIONS]
    wanted = args.only or ids
    unknown = sorted(set(wanted) - set(ids))
    if unknown:
        raise SystemExit(f"Unknown id(s): {', '.join(unknown)}. Known: {', '.join(ids)}")

    graph = WikiGraph(load_corpus(Settings().semantic_corpus_path))
    base = args.base_url.rstrip("/")
    session = post(base, "/api/sessions", {})["session_id"]
    pdf = args.concept.read_bytes()
    docs = post(base, f"/api/sessions/{session}/documents",
                {"filename": args.concept.name, "content_base64": base64.b64encode(pdf).decode()})["documents"]
    print(f"session {session}; attached {docs[0]['filename']} ({docs[0]['pages']} pages)", flush=True)

    recorded: dict[str, CacheEntry] = {}
    for spec in QUESTIONS:
        if spec[0] not in wanted:
            continue
        started = time.time()
        asked = RECORD_AS.get(spec[0], spec[2])
        try:
            response = post(base, "/api/chat", {"session_id": session, "message": asked, "use_cache": False})
        except RequestFailed as err:
            print(f"{spec[0]}: FAILED after {time.time() - started:.1f}s - {err} (kept the previous entry)", flush=True)
            continue
        model = response["trace"]["model"]
        answer, verdict = verify_and_fill(spec[0], response, graph)
        recorded[spec[0]] = entry_from_response(spec, response, model, asked, answer)
        print(f"{spec[0]}: {time.time() - started:5.1f}s, {len(response['trace']['steps'])} tool calls, "
              f"{len(answer)} chars, confidence {response['confidence']} | verify: {verdict}", flush=True)

    existing = {e.id: e for e in load_cache(args.out)}
    merged = [recorded.get(i) or existing.get(i) for i in ids]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render_cache_markdown([e for e in merged if e is not None]), encoding="utf-8")
    print(f"wrote {sum(e is not None for e in merged)} entries to {args.out}")


if __name__ == "__main__":
    main()
