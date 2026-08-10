from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class Widget:
    id: str
    application_id: str
    display_name: str
    welcome_message: str | None
    placeholder_text: str | None
    theme: str
    is_enabled: bool
    created_at: datetime
    updated_at: datetime