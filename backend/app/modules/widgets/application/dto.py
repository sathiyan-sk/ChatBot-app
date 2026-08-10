from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class WidgetDto:
    id: str
    application_id: str
    display_name: str
    theme: str
    launcher_label: str | None
    welcome_message: str | None
    placeholder_text: str | None
    is_enabled: bool
    created_at: datetime
    updated_at: datetime