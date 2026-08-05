from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class GetKnowledgeBaseByIdQuery:
    knowledge_base_id: str


@dataclass(slots=True, frozen=True)
class GetKnowledgeBaseByApplicationIdQuery:
    application_id: str


@dataclass(slots=True, frozen=True)
class ListKnowledgeBasesQuery:
    status: str | None = None