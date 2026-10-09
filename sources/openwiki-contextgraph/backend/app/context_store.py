"""Context corpus: lifecycle (BUILD_SPEC 8.1) and turn trace files (8.2).

The context corpus is its own git repository. After each answer the backend writes
`sessions/<session_id>/turn-NNNN.md` plus `session.md` and commits; OpenWiki then documents the
corpus as the agent's memory (the context graph).
"""

import os
import re
import shutil
import stat
import subprocess
import threading
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .agent import AgentResult
from .config import Settings

TITLE_MAX = 120
SESSION_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")
_TOP_HEADING = re.compile(r"^(#{1,2})(?=\s)", re.MULTILINE)


@dataclass(frozen=True)
class TurnRecord:
    session_id: str
    turn: int
    question: str
    timestamp: datetime
    model: str
    result: AgentResult


def _iso(ts: datetime) -> str:
    return ts.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _turn_file(turn: int) -> str:
    return f"turn-{turn:04d}.md"


def _front_matter(data: dict[str, Any]) -> str:
    body = yaml.safe_dump(data, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000)
    return f"---\n{body}---\n"


def _demote_headings(text: str) -> str:
    """Push `#`/`##` headings in free text down to `###` so they cannot fake a trace section."""
    return _TOP_HEADING.sub("###", text.strip())


def _one_line(text: str, limit: int = TITLE_MAX) -> str:
    flat = " ".join(text.split())
    return flat if len(flat) <= limit else flat[: limit - 1].rstrip() + "…"


def _cell(text: str) -> str:
    return " ".join(str(text).split()).replace("|", "\\|")


def _bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items) if items else "- (none)"


def render_turn_markdown(record: TurnRecord) -> str:
    result, answer = record.result, record.result.answer
    front = _front_matter({
        "type": "TurnTrace",
        "session_id": record.session_id,
        "turn": record.turn,
        "timestamp": _iso(record.timestamp),
        "previous_turn": _turn_file(record.turn - 1) if record.turn > 1 else None,
        "model": record.model,
        "latency_ms": result.latency_ms,
        "input_tokens": result.input_tokens,
        "output_tokens": result.output_tokens,
        "confidence": answer.confidence,
        "tools_used": list(result.tools_used),
        "semantic_pages_read": list(result.semantic_pages_read),
        "semantic_refs_seen": list(result.semantic_refs_seen),
        "context_pages_read": list(result.context_pages_read),
        "context_refs_seen": list(result.context_refs_seen),
    })
    rows = [
        "| Step | Tool | Input | Result (refs / summary) | ms |",
        "|---|---|---|---|---|",
        *(f"| {s.step} | {_cell(s.tool)} | {_cell(s.input)} | {_cell(s.result)} | {s.ms} |" for s in result.steps),
    ]
    seen = {*result.semantic_refs_seen, *result.context_refs_seen, *result.context_pages_read}
    sources = [
        f"{s.ref} - why: {_one_line(s.why, 300)}{'' if s.ref in seen else ' [not seen in tool results]'}"
        for s in answer.sources
    ]
    return "\n".join([
        front,
        f"# Turn {record.turn}: {_one_line(record.question)}",
        "",
        "## Question",
        _demote_headings(record.question),
        "",
        "## Answer",
        _demote_headings(answer.answer),
        "",
        "## Decision trace",
        "\n".join(rows) if result.steps else "(no tool calls)",
        "",
        "## Sources cited",
        _bullets(sources),
        "",
        "## Reasoning summary (agent self-report)",
        _demote_headings(answer.reasoning_summary),
        "",
        "## Follow-up questions",
        _bullets([_one_line(q, 300) for q in answer.follow_up_questions]),
        "",
    ])


def render_session_markdown(session_id: str, started_at: datetime, turns: list[tuple[int, str]]) -> str:
    front = _front_matter({
        "type": "SessionLog",
        "session_id": session_id,
        "started_at": _iso(started_at),
        "turn_count": len(turns),
    })
    lines = [f"{n}. [Turn {n}]({_turn_file(n)}): {_one_line(q)}" for n, q in turns]
    return "\n".join([front, f"# Session {session_id}", "", "## Turns", *lines, ""])


def _split_sections(markdown: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    for chunk in markdown.split("\n## ")[1:]:
        title, _, body = chunk.partition("\n")
        sections[title.strip()] = body.strip()
    return sections


def _parse_turn(markdown: str) -> dict[str, Any]:
    _, fm, body = markdown.split("---\n", 2)
    meta = yaml.safe_load(fm) or {}
    sections = _split_sections(body)
    return {
        "turn": meta.get("turn"),
        "timestamp": meta.get("timestamp"),
        "confidence": meta.get("confidence"),
        "model": meta.get("model"),
        "latency_ms": meta.get("latency_ms"),
        "tools_used": meta.get("tools_used") or [],
        "semantic_pages_read": meta.get("semantic_pages_read") or [],
        "question": sections.get("Question", ""),
        "answer": sections.get("Answer", ""),
    }


class ContextStore:
    """Writes turn traces into the context corpus and commits them. Thread-safe (one git at a time)."""

    def __init__(self, corpus: Path) -> None:
        self._corpus = corpus
        self._lock = threading.Lock()

    def _session_dir(self, session_id: str) -> Path:
        if not SESSION_ID_RE.fullmatch(session_id):
            raise ValueError(f"invalid session id: {session_id!r}")
        return self._corpus / "sessions" / session_id

    def write_turn(self, record: TurnRecord, session_started_at: datetime) -> Path:
        session_dir = self._session_dir(record.session_id)
        with self._lock:
            session_dir.mkdir(parents=True, exist_ok=True)
            path = session_dir / _turn_file(record.turn)
            path.write_text(render_turn_markdown(record), encoding="utf-8")
            turns = [(t["turn"], t["question"]) for t in self._read_turns(session_dir)]
            (session_dir / "session.md").write_text(
                render_session_markdown(record.session_id, session_started_at, turns), encoding="utf-8"
            )
            _git(self._corpus, "add", "-A")
            _git(self._corpus, "commit", "--quiet", "-m", f"turn {record.session_id}/{record.turn}")
            return path

    def load_session(self, session_id: str) -> list[dict[str, Any]]:
        session_dir = self._session_dir(session_id)
        with self._lock:
            return self._read_turns(session_dir)

    @staticmethod
    def _read_turns(session_dir: Path) -> list[dict[str, Any]]:
        if not session_dir.is_dir():
            return []
        files = sorted(session_dir.glob("turn-[0-9][0-9][0-9][0-9].md"))
        return [_parse_turn(f.read_text(encoding="utf-8")) for f in files]

README = (
    "# MHFC Q&A agent trace log\n\n"
    "Trace log of the MHFC Q&A agent: one Markdown file per conversation turn under `sessions/`. "
    "See openwiki/INSTRUCTIONS.md.\n"
)
# Marker the memory sync writes after its first successful init; never part of the corpus.
LOCAL_GITIGNORE = ".poc-initialized\n"


def _git(corpus: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=corpus, check=True, capture_output=True, text=True)


def _force_remove(func, path, _exc) -> None:
    # git object files are read-only on Windows; clear the flag and retry.
    os.chmod(path, stat.S_IWRITE)
    func(path)


def _assert_safe_to_wipe(corpus: Path, settings: Settings) -> None:
    root = settings.project_root.resolve()
    if corpus.resolve() in (root, *root.parents) or corpus.resolve() == Path.home().resolve():
        raise ValueError(f"Refusing to wipe {corpus}: it is the project root or one of its parents")


def reset_context_corpus(settings: Settings) -> Path:
    """Delete and recreate the context corpus as a fresh git repo with the context brief.

    When `prebuilt/context-corpus-template/` exists (an empty-memory corpus captured after a
    one-time `openwiki --init`, including the init marker and OpenWiki's checkpoint), restore it
    by file copy instead: the next memory sync is then an incremental `--update` (minutes), not
    a full `--init` (10-20 min). No model calls happen on reset either way.
    """
    corpus = settings.context_corpus_path
    _assert_safe_to_wipe(corpus, settings)
    template = settings.project_root / "prebuilt" / "context-corpus-template"
    if corpus.exists():
        shutil.rmtree(corpus, onexc=_force_remove)
    if template.is_dir():
        shutil.copytree(template, corpus)
        sessions = corpus / "sessions"
        if sessions.exists():
            shutil.rmtree(sessions, onexc=_force_remove)
        sessions.mkdir()
        (sessions / ".gitkeep").write_text("", encoding="utf-8")
        if not (corpus / ".git").exists():
            # Fresh clones ship the template without its nested .git (git cannot commit
            # one); OpenWiki requires the corpus to be its own repository, so recreate it.
            _git(corpus, "init", "--quiet")
            _git(corpus, "config", "core.autocrlf", "false")
            _git(corpus, "config", "user.email", "poc@openwiki.local")
            _git(corpus, "config", "user.name", "OpenWiki POC")
            _git(corpus, "add", "-A")
            _git(corpus, "commit", "--quiet", "-m", "context corpus from template")
        return corpus
    (corpus / "openwiki").mkdir(parents=True)
    (corpus / "sessions").mkdir()
    (corpus / "sessions" / ".gitkeep").write_text("", encoding="utf-8")
    (corpus / "README.md").write_text(README, encoding="utf-8")
    (corpus / ".openwikiignore").write_text("*.log\n", encoding="utf-8")
    (corpus / ".gitignore").write_text(LOCAL_GITIGNORE, encoding="utf-8")
    shutil.copyfile(settings.templates_path / "context-INSTRUCTIONS.md", corpus / "openwiki" / "INSTRUCTIONS.md")

    _git(corpus, "init", "--quiet")
    _git(corpus, "config", "core.autocrlf", "false")
    _git(corpus, "config", "user.email", "poc@openwiki.local")
    _git(corpus, "config", "user.name", "OpenWiki POC")
    _git(corpus, "add", "-A")
    _git(corpus, "commit", "--quiet", "-m", "context corpus")
    return corpus
