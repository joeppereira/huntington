import base64

import pymupdf
import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.documents import MAX_DOCUMENT_CHARS, SessionDocument, document_messages, extract_pdf
from app.main import create_app

from .test_chat_api import FakeAgent


def make_pdf(*pages: str) -> bytes:
    doc = pymupdf.open()
    for text in pages:
        doc.new_page().insert_text((72, 72), text)
    return doc.tobytes()


def test_extract_pdf_reads_every_page():
    document = extract_pdf("concept.pdf", make_pdf("FC-01 timeline", "FC-02 gpi route"))
    assert document.filename == "concept.pdf"
    assert document.pages == 2
    assert "FC-01 timeline" in document.text and "FC-02 gpi route" in document.text
    assert not document.truncated


@pytest.mark.parametrize("data, reason", [
    (b"", "empty"),
    (b"hello, not a pdf", "Only PDF"),
    (make_pdf(""), "no extractable text"),
])
def test_extract_pdf_rejects_unusable_files(data: bytes, reason: str):
    with pytest.raises(ValueError, match=reason):
        extract_pdf("x.pdf", data)


def test_extract_pdf_truncates_very_long_text(monkeypatch):
    monkeypatch.setattr("app.documents.MAX_DOCUMENT_CHARS", 10)
    document = extract_pdf("long.pdf", make_pdf("abcdefghijklmnopqrstuvwxyz"))
    assert document.truncated and len(document.text) == 10
    assert MAX_DOCUMENT_CHARS > 10  # the real limit is unchanged


def test_document_messages_lead_the_conversation():
    assert document_messages(()) == []
    doc = SessionDocument("concept.pdf", 1, "FC-03 held wires")
    user, assistant = document_messages((doc,))
    assert user["role"] == "user" and '<document name="concept.pdf" pages="1">' in user["content"]
    assert "FC-03 held wires" in user["content"]
    assert assistant["role"] == "assistant" and "concept.pdf" in assistant["content"]


@pytest.fixture
def fake_agent() -> FakeAgent:
    return FakeAgent()


@pytest.fixture
def client(settings: Settings, fake_agent: FakeAgent):
    with TestClient(create_app(settings, agent_factory=lambda _s, _tools: fake_agent)) as c:
        yield c


def _upload(client: TestClient, sid: str, data: bytes, filename: str = "concept.pdf"):
    payload = {"filename": filename, "content_base64": base64.b64encode(data).decode()}
    return client.post(f"/api/sessions/{sid}/documents", json=payload)


def test_upload_attaches_pdf_and_pins_it_to_every_agent_call(client: TestClient, fake_agent: FakeAgent):
    sid = client.post("/api/sessions", json={}).json()["session_id"]
    response = _upload(client, sid, make_pdf("FC-04 insights"))
    assert response.status_code == 200
    assert response.json()["documents"] == [{"filename": "concept.pdf", "pages": 1, "chars": 14, "truncated": False}]

    for message in ("q1", "q2"):
        client.post("/api/chat", json={"session_id": sid, "message": message})
        assert [d.filename for d in fake_agent.documents] == ["concept.pdf"]
        assert "FC-04 insights" in fake_agent.documents[0].text


def test_reuploading_the_same_file_replaces_it(client: TestClient):
    sid = client.post("/api/sessions", json={}).json()["session_id"]
    _upload(client, sid, make_pdf("v1"))
    docs = _upload(client, sid, make_pdf("version two")).json()["documents"]
    assert [(d["filename"], d["chars"]) for d in docs] == [("concept.pdf", 11)]


def test_upload_errors(client: TestClient):
    sid = client.post("/api/sessions", json={}).json()["session_id"]
    assert _upload(client, "20990101-000000-dead", make_pdf("x")).status_code == 404
    assert _upload(client, sid, b"not a pdf").status_code == 422
    bad = client.post(f"/api/sessions/{sid}/documents", json={"filename": "a.pdf", "content_base64": "%%%"})
    assert bad.status_code == 422
