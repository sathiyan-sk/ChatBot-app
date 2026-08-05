from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class WidgetDto:
    id: str
    application_id: str
    display_name: str
    welcome_message: str
    placeholder_text: str
    theme_mode: str
    primary_color: str
    position: str
    is_enabled: bool
    allowed_origins: list[str]
    created_at: datetime
    updated_at: datetime