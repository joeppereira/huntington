"""In-memory chat sessions: the agent's history source. The durable record is the turn files."""

import secrets
import threading
from dataclasses import dataclass, replace
from datetime import datetime, timezone

from .agent import Turn
from .documents import MAX_SESSION_DOCUMENTS, SessionDocument


def new_session_id(now: datetime | None = None) -> str:
    """`YYYYMMDD-HHMMSS-<4 hex>` (BUILD_SPEC 8.1)."""
    return f"{(now or datetime.now()):%Y%m%d-%H%M%S}-{secrets.token_hex(2)}"


@dataclass(frozen=True)
class SessionInfo:
    started_at: datetime
    turns: tuple[Turn, ...] = ()
    documents: tuple[SessionDocument, ...] = ()


class SessionStore:
    def __init__(self) -> None:
        self._sessions: dict[str, SessionInfo] = {}
        self._lock = threading.Lock()

    def create(self) -> str:
        with self._lock:
            session_id = new_session_id()
            while session_id in self._sessions:
                session_id = new_session_id()
            self._sessions[session_id] = SessionInfo(started_at=datetime.now(timezone.utc))
            return session_id

    def clear(self) -> None:
        with self._lock:
            self._sessions = {}

    def get(self, session_id: str) -> SessionInfo | None:
        with self._lock:
            return self._sessions.get(session_id)

    def history(self, session_id: str) -> tuple[Turn, ...] | None:
        info = self.get(session_id)
        return info.turns if info else None

    def append(self, session_id: str, turn: Turn) -> int:
        """Record a completed turn; returns its 1-based turn number."""
        with self._lock:
            info = self._sessions[session_id]
            updated = replace(info, turns=(*info.turns, turn))
            self._sessions[session_id] = updated
            return len(updated.turns)

    def documents(self, session_id: str) -> tuple[SessionDocument, ...]:
        info = self.get(session_id)
        return info.documents if info else ()

    def add_document(self, session_id: str, document: SessionDocument) -> tuple[SessionDocument, ...]:
        """Attach a document to the session (a re-upload of the same file name replaces it)."""
        with self._lock:
            info = self._sessions[session_id]
            kept = tuple(d for d in info.documents if d.filename != document.filename)
            if len(kept) >= MAX_SESSION_DOCUMENTS:
                raise ValueError(f"A session can hold at most {MAX_SESSION_DOCUMENTS} documents.")
            updated = replace(info, documents=(*kept, document))
            self._sessions[session_id] = updated
            return updated.documents
