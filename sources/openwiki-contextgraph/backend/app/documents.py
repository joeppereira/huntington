"""PDFs a PM attaches to a chat session (e.g. their feature concept).

Text is extracted once on upload and pinned to every agent call in that session, so it never
falls out of the chat-history window. Uploads stay in session memory only: they are never
written to either OpenWiki corpus.
"""

from collections.abc import Sequence
from dataclasses import dataclass

import pymupdf

MAX_PDF_BYTES = 10 * 1024 * 1024
MAX_DOCUMENT_CHARS = 40_000  # keeps one upload well inside the model's context budget
MAX_SESSION_DOCUMENTS = 5


@dataclass(frozen=True)
class SessionDocument:
    filename: str
    pages: int
    text: str
    truncated: bool = False


def extract_pdf(filename: str, data: bytes) -> SessionDocument:
    """Plain text of a PDF. Raises ValueError for anything that is not a readable, text-bearing PDF."""
    if not data:
        raise ValueError("The file is empty.")
    if len(data) > MAX_PDF_BYTES:
        raise ValueError(f"The PDF is larger than {MAX_PDF_BYTES // (1024 * 1024)} MB.")
    if not data.startswith(b"%PDF"):
        raise ValueError("Only PDF files can be attached.")
    try:
        with pymupdf.open(stream=data, filetype="pdf") as doc:
            pages = doc.page_count
            text = "\n\n".join(page.get_text().strip() for page in doc).strip()
    except Exception as err:  # pymupdf raises its own error types for damaged files
        raise ValueError(f"Could not read the PDF: {err}") from err
    if not text:
        raise ValueError("The PDF has no extractable text (scanned images are not supported).")
    truncated = len(text) > MAX_DOCUMENT_CHARS
    return SessionDocument(filename, pages, text[:MAX_DOCUMENT_CHARS], truncated)


def document_messages(documents: Sequence[SessionDocument]) -> list[dict[str, str]]:
    """A user/assistant exchange that puts the attached documents in front of the conversation."""
    if not documents:
        return []
    blocks = "\n\n".join(
        f'<document name="{d.filename}" pages="{d.pages}">\n{d.text}\n</document>' for d in documents
    )
    names = ", ".join(d.filename for d in documents)
    return [
        {
            "role": "user",
            "content": "I attached these documents to this chat. They are my own input (for example my "
            "feature concept and assumptions), not estate facts - check them against the wiki.\n\n" + blocks,
        },
        {
            "role": "assistant",
            "content": f"Noted - I'll treat {names} as your input and check it against the estate wiki.",
        },
    ]
