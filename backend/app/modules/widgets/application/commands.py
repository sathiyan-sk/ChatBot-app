from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class CreateWidgetCommand:
    application_id: str
    display_name: str
    welcome_message: str
    placeholder_text: str
    theme_mode: str
    primary_color: str
    position: str
    is_enabled: bool
    allowed_origins: list[str]


@dataclass(slots=True, frozen=True)
class UpdateWidgetCommand:
    application_id: str
    display_name: str
    welcome_message: str
    placeholder_text: str
    theme_mode: str
    primary_color: str
    position: str
    is_enabled: bool
    allowed_origins: list[str]