"""Deterministic answer verification + gap-fill for the CNB Q&A agent (eval layer).

The GRAPH is the source of truth, not the LLM. For each REQUIRED FACT this module checks,
deterministically and with NO model call:

  * present           — is the fact correctly stated in the answer? (present_detect)
  * data_used         — was the authoritative source actually consulted? (a cited/read page,
                        or a graph tool for dependency/ownership facts)
  * contradicts_graph — does the answer assert a value that CONFLICTS with the graph's
                        ground-truth value? (graph_value set + wrong_detect) — this is the
                        stale/wrong-assertion catch, distinct from merely present=False.

A fact is VERIFIED_GOOD iff  present AND data_used AND NOT contradicts_graph.

Gap-fill (the "checks and balances"): for any fact that is MISSING or CONTRADICTS the graph,
derive the authoritative statement deterministically from the graph/page (RequiredFact.fill),
append a "Corrections & gaps filled from wiki records" section to the answer, and re-verify.
The deterministic fill IS the authoritative source being used, so a filled fact counts as
data_used on re-verification.

Kept model-free and dependency-light so it runs in CI (see backend/tests/test_answer_eval.py).
"""

from collections.abc import Callable, Sequence
from dataclasses import dataclass, field, replace

from .retrieval.graph import WikiGraph

# A graph_value callable derives the ground-truth value (a set of acceptable tokens/titles)
# straight from the graph — e.g. the gpi connector's owner. Used both to document the truth
# and (with wrong_detect) to flag a contradicting assertion.
GraphValue = Callable[[WikiGraph], "set[str]"]
Detector = Callable[[str], bool]


@dataclass(frozen=True)
class RequiredFact:
    """One deterministically-checkable fact a correct answer to a demo question must contain."""

    id: str
    desc: str
    present_detect: Detector  # (answer_text_lower) -> bool: "fact correctly stated"
    authority_refs: tuple[str, ...]  # page refs that authoritatively support the fact
    source_ref: str  # primary ref quoted in a gap-fill correction
    fill: "Callable[[WikiGraph], str] | str"  # authoritative statement for gap-fill (graph/page lookup)
    graph_value: GraphValue | None = None  # deterministic ground-truth value, when it exists
    wrong_detect: Detector | None = None  # detects a stale/wrong assertion of this fact
    graph_tools: tuple[str, ...] = ()  # graph tools whose use counts as consulting the authority


@dataclass(frozen=True)
class FactCheck:
    fact_id: str
    desc: str
    present: bool
    data_used: bool
    contradicts_graph: bool
    verified_good: bool
    filled: bool = False


@dataclass(frozen=True)
class Correction:
    fact_id: str
    desc: str
    statement: str
    source: str
    reason: str  # "missing" | "contradicts_graph"


CORRECTIONS_HEADING = "## Corrections & gaps filled from wiki records"


def _base(ref: str) -> str:
    """Strip a '#heading' suffix so a section citation matches its page's authority ref."""
    return ref.split("#", 1)[0].strip()


def authoritative_statement(fact: RequiredFact, graph: WikiGraph) -> str:
    """The deterministic ground-truth statement for a fact (graph lookup or stored page line)."""
    return fact.fill(graph) if callable(fact.fill) else fact.fill


def check_fact(
    fact: RequiredFact,
    answer_text: str,
    pages_read: Sequence[str],
    citation_refs: Sequence[str],
    tools_used: Sequence[str],
    graph: WikiGraph,
) -> FactCheck:
    """Deterministically verify one fact against an answer and the run's tool/citation trace."""
    t = answer_text.lower()
    present = bool(fact.present_detect(t))

    consulted = {_base(r) for r in pages_read} | {_base(r) for r in citation_refs}
    data_used = any(_base(a) in consulted for a in fact.authority_refs)
    if not data_used and fact.graph_tools:
        used = set(tools_used)
        data_used = any(tool in used for tool in fact.graph_tools)

    contradicts = False
    if fact.graph_value is not None and fact.wrong_detect is not None:
        contradicts = bool(fact.wrong_detect(t))

    verified = present and data_used and not contradicts
    return FactCheck(fact.id, fact.desc, present, data_used, contradicts, verified)


def verify_run(
    facts: Sequence[RequiredFact],
    answer_text: str,
    pages_read: Sequence[str],
    citation_refs: Sequence[str],
    tools_used: Sequence[str],
    graph: WikiGraph,
    *,
    filled_ids: "frozenset[str]" = frozenset(),
) -> list[FactCheck]:
    """Verify every fact. Facts in `filled_ids` were gap-filled from the graph/page, so the
    authoritative data WAS used — count them as data_used on this (re-)verification pass."""
    checks: list[FactCheck] = []
    for f in facts:
        c = check_fact(f, answer_text, pages_read, citation_refs, tools_used, graph)
        if f.id in filled_ids:
            du = True
            c = replace(c, data_used=du, filled=True,
                        verified_good=c.present and du and not c.contradicts_graph)
        checks.append(c)
    return checks


def fill_gaps(
    facts: Sequence[RequiredFact],
    checks: Sequence[FactCheck],
    answer_text: str,
    graph: WikiGraph,
) -> "tuple[str, list[Correction]]":
    """For each MISSING or CONTRADICTING fact, append its authoritative statement (derived from
    the graph/page, no LLM) under a corrections section. Returns (corrected_answer, corrections)."""
    corrections: list[Correction] = []
    for fact, chk in zip(facts, checks):
        if chk.present and not chk.contradicts_graph:
            continue
        corrections.append(Correction(
            fact_id=fact.id,
            desc=fact.desc,
            statement=authoritative_statement(fact, graph),
            source=fact.source_ref,
            reason="contradicts_graph" if chk.contradicts_graph else "missing",
        ))
    if not corrections:
        return answer_text, corrections
    lines = ["", CORRECTIONS_HEADING, ""]
    for c in corrections:
        tag = " [CONTRADICTED GRAPH]" if c.reason == "contradicts_graph" else ""
        lines.append(f"- {c.desc}:{tag} {c.statement} (source: {c.source})")
    corrected = answer_text.rstrip() + "\n" + "\n".join(lines) + "\n"
    return corrected, corrections


@dataclass(frozen=True)
class QuestionScore:
    coverage_pre: float  # fraction of facts present before gap-fill
    data_used_pct: float
    contradictions: int
    coverage_post: float  # fraction present after gap-fill
    verified_good_pre: int
    verified_good_post: int
    n_facts: int


def score_checks(pre: Sequence[FactCheck], post: Sequence[FactCheck]) -> QuestionScore:
    n = len(pre) or 1
    return QuestionScore(
        coverage_pre=sum(c.present for c in pre) / n,
        data_used_pct=sum(c.data_used for c in pre) / n,
        contradictions=sum(c.contradicts_graph for c in pre),
        coverage_post=sum(c.present for c in post) / n,
        verified_good_pre=sum(c.verified_good for c in pre),
        verified_good_post=sum(c.verified_good for c in post),
        n_facts=len(pre),
    )
