from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class CreateSettingsCommand:
    application_id: str
    conversation_inactivity_minutes: int
    conversation_retention_days: int
    retrieval_top_k: int
    reranker_enabled: bool
    citations_enabled: bool


@dataclass(slots=True, frozen=True)
class UpdateSettingsCommand:
    application_id: str
    conversation_inactivity_minutes: int
    conversation_retention_days: int
    retrieval_top_k: int
    reranker_enabled: bool
    citations_enabled: bool