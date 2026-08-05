from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class PlatformSettings:
    id: str
    application_id: str
    conversation_inactivity_minutes: int
    conversation_retention_days: int
    retrieval_top_k: int
    reranker_enabled: bool
    citations_enabled: bool
    created_at: datetime
    updated_at: datetime