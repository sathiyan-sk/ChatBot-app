from __future__ import annotations

from abc import ABC, abstractmethod

from app.modules.security.domain.entities import ClientApplicationContext


class ClientSecurityRepository(ABC):
    @abstractmethod
    def resolve_application_context_by_api_key(self, raw_api_key: str) -> ClientApplicationContext | None:
        raise NotImplementedError