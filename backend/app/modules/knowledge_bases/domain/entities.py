from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True, frozen=True)
class KnowledgeBase:
    id: UUID
    application_id: UUID
    name: str
    slug: str
    status: str
    is_active: bool
    created_at: datetime
    updated_at: datetime