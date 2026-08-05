from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class KnowledgeChunk:
    chunk_id: str
    document_id: str
    document_title: str
    content: str
    source_uri: str | None
    score: float
    metadata: dict[str, str]


@dataclass(slots=True, frozen=True)
class RetrievalQuery:
    application_id: str
    knowledge_base_id: str
    query_text: str
    top_k: int


@dataclass(slots=True, frozen=True)
class GeneratedResponse:
    answer_text: str
    citations: list[dict[str, str]]