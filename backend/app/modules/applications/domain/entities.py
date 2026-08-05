from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class Application:
    id: str
    name: str
    slug: str
    description: str | None
    client_type: str
    allowed_origins: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime