from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class GetDocumentByIdQuery:
    document_id: str


@dataclass(slots=True, frozen=True)
class ListDocumentsByKnowledgeBaseQuery:
    knowledge_base_id: str
    status: str | None = None


@dataclass(slots=True, frozen=True)
class ListDocumentsByStatusQuery:
    status: str