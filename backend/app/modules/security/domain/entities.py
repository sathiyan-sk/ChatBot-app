from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ClientApplicationContext:
    application_id: str
    application_slug: str
    client_type: str
    api_key_prefix: str