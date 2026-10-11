"""Identifier-aware tokenization, identical at index and query time.

Hyphenated/dotted identifiers ("EP-PPH-01", "pay.wire.lifecycle.v2") are emitted as one
whole token AND as their parts, so "what is EP-PPH-01" matches the whole-ID token exactly
while natural-language queries still match the parts. BM25's exact-identifier advantage
is conditional on exactly this (research report §5) — dense retrievers smear rare ID tokens.
"""

import re

_ID = re.compile(r"[A-Za-z0-9]+(?:[-.][A-Za-z0-9]+)+")
_WORD = re.compile(r"[a-z0-9]+")


def id_tokens(text: str) -> list[str]:
    """Whole compound identifiers found in text, lowercased (e.g. 'ep-pph-01')."""
    return [m.group(0).lower() for m in _ID.finditer(text)]


def tokenize(text: str) -> list[str]:
    """Plain word tokens plus one whole-token per compound identifier."""
    out = _WORD.findall(text.lower())
    out.extend(id_tokens(text))
    return out
