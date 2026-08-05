from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class ApplicationDto:
    id: str
    name: str
    slug: str
    description: str | None
    client_type: str
    allowed_origins: list[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime


@dataclass(slots=True, frozen=True)
class CreatedApplicationDto:
    application: ApplicationDto
    api_key: str
    api_key_prefix: str