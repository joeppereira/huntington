"""Per-demo-question REQUIRED FACTS for the deterministic answer verifier.

Facts and their authoritative values were read from semantic-corpus-cnb/openwiki and the golden
set (eval/golden_cnb.json). The GRAPH is the source of truth: `graph_value` facts derive their
ground-truth value from the WikiGraph at verify time, and `wrong_detect` catches an answer that
asserts a stale/conflicting value (the gpi-ownership = PNE/Raj-Malhotra trap).

Covered demo questions (demo_pack items in golden_cnb.json):
  Q1 = G-020  which systems does the Wire Tracking Center depend on, who owns each
  Q2 = G-037  'Settled' vs today's 'Completed' label
  Q3 = G-021  live SWIFT gpi route refreshed every minute, feasible for Q1 2027?
  Q4 = G-042  held-wire design review (exact reason + Confirm/Reject on every hold)
  Q5 = G-022  anything in backlog/prod that conflicts with policy or this feature
"""

import re

from app.answer_verify import RequiredFact

# --- demo questions (verbatim from golden_cnb.json) --------------------------------------------

QUESTIONS: dict[str, dict[str, str]] = {
    "Q1": {
        "golden_id": "G-020",
        "question": (
            "I've uploaded my market research and concept. Before I write the BRD: which existing "
            "systems does the Wire Tracking Center depend on, and who owns each today?"
        ),
    },
    "Q2": {
        "golden_id": "G-037",
        "question": (
            "My timeline ends in 'Settled'. Wire Center already shows 'Completed' - can we just use that?"
        ),
    },
    "Q3": {
        "golden_id": "G-021",
        "question": (
            "For international wires I want the live SWIFT gpi route, refreshed every minute, with "
            "'Expected delivery: Today'. Feasible for Q1 2027?"
        ),
    },
    "Q4": {
        "golden_id": "G-042",
        "question": (
            "Review my held-wire design: clients see the exact hold reason and get Confirm/Reject "
            "buttons on every held wire. Any issues?"
        ),
    },
    "Q5": {
        "golden_id": "G-022",
        "question": (
            "Before I go further - is anything already in the Wire Center backlog or in production "
            "that conflicts with policy or with this feature?"
        ),
    },
}


# --- shared detectors ---------------------------------------------------------------------------

_GRAPH_TOOLS = ("graph_dependencies", "graph_neighbors")

SWIFT_GPI_REF = "openwiki/systems/swift-gpi-connector.md"
MEMO_REF = "openwiki/documents/cnb-memo-2026-09.md"


def _tokens_any(*tokens: str):
    """present_detect: true if any token appears in the (lowercased) answer."""
    toks = tuple(t.lower() for t in tokens)
    return lambda t: any(tok in t for tok in toks)


def gpi_owner_value(graph) -> set[str]:
    """Deterministic ground truth: the Swift gpi Connector's current owner, from the graph."""
    return {n["title"] for n in graph.neighbors(SWIFT_GPI_REF, relation="owned_by", direction="out")}


def gpi_owner_present(t: str) -> bool:
    """Correctly names GTSI as the current gpi-connector owner."""
    return "gtsi" in t or "global transaction services integration" in t


_GPI_PNE_NEAR = re.compile(r"gpi[^.\n]{0,100}(pne|payment networks engineering)")
_PNE_NEAR_GPI = re.compile(r"(pne|payment networks engineering)[^.\n]{0,60}gpi")


def gpi_owner_wrong(t: str) -> bool:
    """Stale/wrong assertion: gpi owned by PNE / Raj Malhotra as CURRENT, without naming GTSI.

    The guard (GTSI not named) means a correct answer that keeps PNE only as the *prior* owner
    while naming GTSI as current does NOT trip the contradiction — only a genuinely stale claim
    (the demo concept's "gpi data: Payment Networks Engineering (Raj Malhotra)") does."""
    if gpi_owner_present(t):
        return False
    return bool("raj malhotra" in t or _GPI_PNE_NEAR.search(t) or _PNE_NEAR_GPI.search(t))


def _gpi_owner_fill(graph) -> str:
    owners = ", ".join(sorted(gpi_owner_value(graph))) or "Global Transaction Services Integration (GTSI)"
    return (f"The Swift gpi Connector (SYS-PNG-GPI) is owned by {owners}, effective 2026-10-01 "
            f"(transferred from Payment Networks Engineering per CNB-MEMO-2026-09) - NOT Raj Malhotra / PNE.")


def _gpi_owner_fact(fact_id: str) -> RequiredFact:
    """The gpi-ownership fact shared by Q1 and Q5 — the graph-backed contradiction catch."""
    return RequiredFact(
        id=fact_id,
        desc="gpi connector current owner is GTSI (not PNE/Raj Malhotra)",
        present_detect=gpi_owner_present,
        authority_refs=(SWIFT_GPI_REF, MEMO_REF),
        source_ref=SWIFT_GPI_REF,
        fill=_gpi_owner_fill,
        graph_value=gpi_owner_value,
        wrong_detect=gpi_owner_wrong,
        graph_tools=_GRAPH_TOOLS,
    )


# --- Q1 (G-020): dependency systems (from graph.dependency_closure) + gpi owner -----------------

# The 7 systems in dependency_closure(cbo-wire-center) — the graph is the source of truth for the
# set. Each tuple: (id, friendly name, detect tokens, page ref, owner-from-graph).
_Q1_SYSTEMS = [
    ("PPH", "PRISM Payments Hub (PPH)", ("prism", "pph", "payments hub"),
     "openwiki/systems/prism-payments-hub.md", "Payments Hub Engineering"),
    ("FFC", "Fedwire Funds Connector (FFC)", ("fedwire funds connector", "ffc", "fedwire"),
     "openwiki/systems/fedwire-funds-connector.md", "Payment Networks Engineering (PNE)"),
    ("GPI", "Swift gpi Connector", ("swift gpi", "gpi connector", "gpi"),
     SWIFT_GPI_REF, "Global Transaction Services Integration (GTSI)"),
    ("HMS", "Hold Management Service (HMS)", ("hold management", "hms"),
     "openwiki/systems/hold-management-service.md", "Financial Crimes Technology (FCT)"),
    ("ENS", "Enterprise Notification Service (ENS)", ("enterprise notification", "ens"),
     "openwiki/systems/enterprise-notification-service.md", "Enterprise Notification Platform"),
    ("CES", "Commercial Entitlements Service (CES)", ("commercial entitlements", "ces", "entitlements"),
     "openwiki/systems/commercial-entitlements-service.md", "CBO Platform & Entitlements"),
    ("CDP", "Core Deposit Platform (CDP)", ("core deposit", "cdp"),
     "openwiki/systems/core-deposit-platform.md", "Deposits Data Ownership"),
]


def _system_fact(sid, name, tokens, ref, owner) -> RequiredFact:
    return RequiredFact(
        id=f"Q1-SYS-{sid}",
        desc=f"dependency: {name}",
        present_detect=_tokens_any(*tokens),
        authority_refs=(ref,),
        source_ref=ref,
        fill=f"{name} is a dependency of the Wire Tracking Center (depends_on closure of "
             f"cbo-wire-center), owned by {owner}.",
        graph_tools=_GRAPH_TOOLS,
    )


def q1_facts() -> list[RequiredFact]:
    facts = [_system_fact(*s) for s in _Q1_SYSTEMS]
    facts.append(_gpi_owner_fact("Q1-GPI-OWNER"))
    return facts


# --- Q2 (G-037): today's 'Completed' label is not a settlement milestone ------------------------

SETTLEMENT_REF = "openwiki/concepts/settlement-release-completed-semantics.md"
CMP_REF = "openwiki/incidents/cmp-2026-1189.md"


def q2_facts() -> list[RequiredFact]:
    return [
        RequiredFact(
            id="Q2-COMPLETED-PROCESSED",
            desc="'Completed' maps PPH v1 PROCESSED (set at release, before Fed acceptance) - not settled",
            present_detect=lambda t: "processed" in t and "completed" in t,
            authority_refs=(SETTLEMENT_REF, "openwiki/concepts/wire-lifecycle-state-model.md"),
            source_ref=SETTLEMENT_REF,
            fill="Today's 'Completed' maps PPH v1 PROCESSED, which is set at wire release before Fed "
                 "acceptance - it is not a settlement milestone (the ENS 'Wire completed' template "
                 "TPL-WIRE-REL-02 has the same defect).",
        ),
        RequiredFact(
            id="Q2-CMP-1189",
            desc="release-time 'Completed' is the defect behind complaint CMP-2026-1189",
            present_detect=_tokens_any("cmp-2026-1189", "cmp 2026-1189", "halvorsen"),
            authority_refs=(CMP_REF,),
            source_ref=CMP_REF,
            fill="This defect caused complaint CMP-2026-1189: a EUR 412,600 wire for Halvorsen "
                 "Industrial Supply was shown 'Completed' at release, then rejected by the beneficiary "
                 "bank the next day (RJCT AC04).",
        ),
    ]


# --- Q3 (G-021): live per-minute gpi route is not feasible for Q1 2027 --------------------------

GPI_BATCH_REF = "openwiki/interfaces/gpi-tracker-batch-feed.md"
PNG_1544_REF = "openwiki/decisions/png-1544.md"
GTSI_0107_REF = "openwiki/projects/gtsi-0107-gpi-real-time-service.md"

_FOUR_HOUR = re.compile(r"(4[\s-]?hour|every 4 hours|four[\s-]?hour|4h\b)")


def q3_facts() -> list[RequiredFact]:
    return [
        RequiredFact(
            id="Q3-BATCH-4H",
            desc="gpi status is a 4-hourly batch (BT-PNG-01), no streaming/per-payment API",
            present_detect=lambda t: bool(_FOUR_HOUR.search(t)) and ("batch" in t or "bt-png-01" in t),
            authority_refs=(GPI_BATCH_REF,),
            source_ref=GPI_BATCH_REF,
            fill="gpi status is pulled only by a 4-hourly batch (BT-PNG-01, runs 00/04/08/12/16/20 ET) "
                 "into GPI_TRACKER_SNAPSHOT; there is no streaming/webhook and no per-payment on-demand "
                 "API, so a per-minute live route is not available.",
        ),
        RequiredFact(
            id="Q3-QUOTA-PNG1544",
            desc="per-payment Tracker calls blocked by the 250k/month quota; 4h->2h declined (PNG-1544)",
            present_detect=lambda t: "png-1544" in t or ("quota" in t and "250" in t),
            authority_refs=(PNG_1544_REF, GPI_BATCH_REF),
            source_ref=PNG_1544_REF,
            fill="Per-payment Tracker calls are blocked by the contracted 250,000 Swift Tracker calls/"
                 "month quota (client demand ~1.9M/month, ~7x over); the 4h->2h frequency increase was "
                 "declined as PNG-1544 (Won't Do, 2026-03-03).",
        ),
        RequiredFact(
            id="Q3-GTSI0107-UNFUNDED",
            desc="the real-time gpi service GTSI-0107 (GTRS) is unfunded for 2026",
            present_detect=lambda t: "gtsi-0107" in t or "gtrs" in t,
            authority_refs=(GTSI_0107_REF,),
            source_ref=GTSI_0107_REF,
            fill="The real-time gpi service GTSI-0107 (GTRS) is not funded for 2026 - discovery 2027-Q2, "
                 "build 2027-Q3/Q4 - so a real-time route cannot land for Q1 2027.",
        ),
    ]


# --- Q4 (G-042): held-wire design — tiered disclosure + confirm/reject only HRC-01 --------------

HRC_TAXONOMY_REF = "openwiki/concepts/hold-reason-taxonomy-disclosure-tiers.md"
ADR_PAY_021_REF = "openwiki/decisions/adr-pay-021.md"


def q4_facts() -> list[RequiredFact]:
    return [
        RequiredFact(
            id="Q4-RG-IDENTICAL",
            desc="R/G tiers must show identical generic copy - the exact reason may not be shown",
            present_detect=lambda t: ("identical" in t or "same" in t or "generic" in t)
            and ("tier" in t or "restricted" in t or "r/g" in t or "r and g" in t),
            authority_refs=(HRC_TAXONOMY_REF, "openwiki/policies/pol-fcc-014.md"),
            source_ref=HRC_TAXONOMY_REF,
            fill="POL-FCC-014 §5.1(2): tier R and tier G holds must be presented identically (same "
                 "generic copy COPY-HOLD-GEN-01, no action, no ETA); the exact hold reason may never "
                 "be shown - showing it to every held wire leaks Restricted categories.",
        ),
        RequiredFact(
            id="Q4-CONFIRM-HRC01-ONLY",
            desc="Confirm/attestation permitted for HRC-01 only (CTRL-PAY-031), not every hold",
            present_detect=lambda t: "hrc-01" in t and ("confirm" in t or "attestation" in t or "ctrl-pay-031" in t),
            authority_refs=(HRC_TAXONOMY_REF,),
            source_ref=HRC_TAXONOMY_REF,
            fill="Digital confirm/attestation is permitted for HRC-01 (DUP_SUSPECT) only, with step-up "
                 "auth under CTRL-PAY-031 up to $5M; it does not extend to any other HRC code (HRC-02 "
                 "gets callback only, CTRL-PAY-018), so Confirm/Reject cannot appear on every held wire.",
        ),
        RequiredFact(
            id="Q4-REASON-RESTRICTED",
            desc="exact hold reason text is Restricted, confined to the FC trust boundary (ADR-PAY-021)",
            present_detect=lambda t: "restricted" in t or "adr-pay-021" in t or "trust boundary" in t,
            authority_refs=(ADR_PAY_021_REF, HRC_TAXONOMY_REF),
            source_ref=ADR_PAY_021_REF,
            fill="Hold reason codes, descriptions, scores and analyst notes are Restricted and must stay "
                 "inside the financial-crimes trust boundary (ADR-PAY-021); PPH v2 exposes only isHeld + "
                 "holdId, so the exact reason cannot be surfaced to clients.",
        ),
    ]


# --- Q5 (G-022): backlog/prod conflicts with policy or this feature -----------------------------

JIRA_REF = "openwiki/documents/jira-export-wt-discovery-2026-10-05.md"
CBO_4471_REF = "openwiki/projects/cbo-4471-pph-v1-to-v2-migration.md"


def q5_facts() -> list[RequiredFact]:
    return [
        RequiredFact(
            id="Q5-CBO4388-LEAK",
            desc="CRITICAL: CBO-4388 ships Restricted HMS holdReasonDesc free text to clients",
            present_detect=lambda t: "cbo-4388" in t
            and ("restricted" in t or "holdreasondesc" in t or "hold reason" in t or "leak" in t),
            authority_refs=(JIRA_REF, ADR_PAY_021_REF, "openwiki/policies/pol-fcc-014.md"),
            source_ref=JIRA_REF,
            fill="CRITICAL: CBO-4388 (In Progress, Sprint 26.20, ships ~2026-10-22) populates a client "
                 "tooltip from PPH v1 holdReasonDesc, which carries Restricted HMS free text (FCT-2004) "
                 "- stop it and notify FCC (Jordan Ellis) and FCT.",
        ),
        RequiredFact(
            id="Q5-CBO4471-SUNSET",
            desc="CBO-4471 v1->v2 migration is unscheduled against the hard 2027-03-31 sunset",
            present_detect=lambda t: "cbo-4471" in t and ("2027-03-31" in t or "sunset" in t),
            authority_refs=(CBO_4471_REF, JIRA_REF),
            source_ref=CBO_4471_REF,
            fill="CBO-4471 (PPH v1->v2 migration, Epic, 34 pts) is in backlog/unscheduled against the "
                 "hard 2027-03-31 v1 sunset (no extensions) - a migration risk.",
        ),
        _gpi_owner_fact("Q5-GPI-OWNER"),
    ]


def all_answer_keys() -> dict[str, list[RequiredFact]]:
    return {
        "Q1": q1_facts(),
        "Q2": q2_facts(),
        "Q3": q3_facts(),
        "Q4": q4_facts(),
        "Q5": q5_facts(),
    }
