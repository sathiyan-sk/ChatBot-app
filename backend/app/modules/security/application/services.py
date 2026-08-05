from __future__ import annotations

from dataclasses import dataclass

from app.core.exceptions import ApplicationError
from app.modules.security.domain.entities import ClientApplicationContext
from app.modules.security.domain.repository_interfaces import ClientSecurityRepository


@dataclass(slots=True)
class ClientSecurityServices:
    client_security_repository: ClientSecurityRepository

    def resolve_application_context(self, raw_api_key: str) -> ClientApplicationContext:
        normalized_key = raw_api_key.strip()
        if not normalized_key:
            raise ApplicationError(
                message="API key is required.",
                code="api_key_required",
                status_code=401,
            )

        context = self.client_security_repository.resolve_application_context_by_api_key(normalized_key)
        if context is None:
            raise ApplicationError(
                message="Invalid API key.",
                code="invalid_api_key",
                status_code=401,
            )

        return context