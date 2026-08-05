from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class Document:
    id: str
    knowledge_base_id: str
    title: str
    description: str | None
    source_type: str
    source_uri: str
    status: str
    failure_reason: str | None
    created_at: datetime
    updated_at: datetime