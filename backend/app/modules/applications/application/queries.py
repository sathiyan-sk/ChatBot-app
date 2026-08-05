from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class GetApplicationByIdQuery:
    application_id: str