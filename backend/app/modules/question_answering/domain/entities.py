from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class RetrievedChunk:
    document_id: str
    document_title: str
    content: str
    score: float
    source_uri: str | None


@dataclass(slots=True, frozen=True)
class GeneratedAnswer:
    answer_text: str
    citations: list[dict[str, str]]