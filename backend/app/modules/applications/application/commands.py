from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class CreateApplicationCommand:
    name: str
    description: str | None
    client_type: str
    allowed_origins: list[str] | None


@dataclass(slots=True, frozen=True)
class UpdateApplicationCommand:
    application_id: str
    name: str
    description: str | None
    client_type: str
    allowed_origins: list[str] | None
    is_active: bool