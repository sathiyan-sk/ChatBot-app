from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class SettingsDto:
    id: str
    application_id: str
    llm_temperature: str
    max_context_messages: int
    inactivity_timeout_minutes: int
    retention_days: int
    prompt_system_template: str | None
    created_at: datetime
    updated_at: datetime