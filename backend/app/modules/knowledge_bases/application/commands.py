from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class CreateKnowledgeBaseCommand:
    application_id: str
    name: str
    description: str | None = None
    status: str = "active"


@dataclass(slots=True, frozen=True)
class UpdateKnowledgeBaseCommand:
    knowledge_base_id: str
    name: str
    description: str | None
    status: str


@dataclass(slots=True, frozen=True)
class ActivateKnowledgeBaseCommand:
    knowledge_base_id: str


@dataclass(slots=True, frozen=True)
class DeactivateKnowledgeBaseCommand:
    knowledge_base_id: str