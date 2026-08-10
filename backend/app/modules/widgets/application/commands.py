from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class CreateWidgetCommand:
    application_id: str
    display_name: str
    theme: str = "light"
    launcher_label: str | None = None
    welcome_message: str | None = None
    placeholder_text: str | None = None
    is_enabled: bool = True


@dataclass(slots=True, frozen=True)
class UpdateWidgetCommand:
    application_id: str
    display_name: str
    theme: str
    launcher_label: str | None = None
    welcome_message: str | None = None
    placeholder_text: str | None = None
    is_enabled: bool = True