from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class KnowledgeBaseDto:
    id: str
    application_id: str
    name: str
    description: str | None
    status: str
    created_at: datetime
    updated_at: datetime