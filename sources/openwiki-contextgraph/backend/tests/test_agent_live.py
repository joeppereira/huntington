"""BUILD_SPEC Section 9, Stage 2 questions 1-4 against the real agent (Anthropic API, costs money).

Run with:  RUN_LIVE=1 pytest -m live -s
"""

import os
import re

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app

pytestmark = [
    pytest.mark.live,
    pytest.mark.skipif(os.environ.get("RUN_LIVE") != "1", reason="set RUN_LIVE=1 to call the Anthropic API"),
]


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("−", "-").replace("–", "-")).lower()


ESTIMATE = re.compile(
    r"(roughly|approximately|around|about|~|≈)\s*\$?\d[\d,.]*\s*(%|bn|billion|mm|million)"
    r"|back[- ]of[- ](the[- ])?envelope|hand[- ]estimate|rough estimate"
)


def _invents_estimate(text: str) -> bool:
    return bool(ESTIMATE.search(text))


def _live_settings(tmp_path) -> Settings:
    # manual memory sync: a live test must never start a real (~20 min) OpenWiki run
    return Settings(context_corpus_dir=tmp_path / "context-corpus", logs_dir=tmp_path / "logs",
                    semantic_vis_port=4391, context_vis_port=4392, memory_sync_mode="manual")


def _ask(client: TestClient, sid: str, question: str) -> dict:
    resp = client.post("/api/chat", json={"session_id": sid, "message": question})
    assert resp.status_code == 200, resp.text
    body = resp.json()
    print(f"\nQ: {question}\nA: {body['answer']}\nconfidence={body['confidence']} "
          f"latency={body['trace']['latency_ms']}ms steps={[s['tool'] for s in body['trace']['steps']]}")
    return body


def test_spec_questions_1_to_4_in_one_session(tmp_path):
    settings = _live_settings(tmp_path)
    with TestClient(create_app(settings)) as client:
        sid = client.post("/api/sessions", json={}).json()["session_id"]

        q1 = _ask(client, sid, "What was Meridian Harbor's CET1 ratio at year-end 2025, and what is its requirement?")
        a1 = _norm(q1["answer"])
        assert "15.1" in a1 or "15.08" in a1
        assert "10.2" in a1
        assert "semantic_search" in {s["tool"] for s in q1["trace"]["steps"]}
        assert q1["sources"]

        q2 = _ask(client, sid, "Which APIs feed the CECL model, and who owns that model?")
        a2 = _norm(q2["answer"])
        for api in ("api-10", "api-11", "api-14"):
            assert api in a2
        assert "allowance methodology" in a2

        q3 = _ask(client, sid, "How does that model turn scenarios into an allowance?")
        a3 = _norm(q3["answer"])
        assert "cecl" in a3 or "mdl-cr-007" in a3  # resolved "that model" from history
        assert "lgd" in a3 and "ead" in a3
        # qualitative overlay $681mm: stated outright, or as modeled 15,238.9 + overlay = 15,920
        assert "681" in a3 or ("15,238.9" in a3 and "15,920" in a3 and "overlay" in a3)
        assert re.search(r"20\s*%.*50\s*%.*30\s*%|20\s*/\s*50\s*/\s*30", a3)

        q4 = _ask(client, sid, "What happens to NII if rates drop 200 bp?")
        a4 = _norm(q4["answer"])
        assert re.search(r"6\.0\d?\s*%", a4)  # spec: about -6.0%
        assert re.search(r"3,01\d|3\.0\s*(bn|billion)", a4)  # spec: about -$3.0bn
        assert re.search(r"\b7(\.0)?\s*%", a4)  # spec: within the 7% limit


def test_spec_question_5_declines_to_compute_a_new_scenario(tmp_path):
    settings = _live_settings(tmp_path)
    with TestClient(create_app(settings)) as client:
        sid = client.post("/api/sessions", json={}).json()["session_id"]
        q5 = _ask(client, sid, "What would the CET1 ratio be if buybacks doubled?")
        a5 = _norm(q5["answer"])
        assert re.search(r"can(no|')t (run|re-?run|recalculate|compute)|not able to (run|compute)", a5)
        assert "capital planning" in a5 or "mdl-cap-003" in a5
        assert "assumptions" in a5  # points to the sheet holding the buyback input
        assert not _invents_estimate(a5), "the agent must not hand-compute a new scenario"
