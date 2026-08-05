from __future__ import annotations

from urllib.parse import urlparse

from app.config.settings import SecuritySettings
from app.core.exceptions import AuthorizationError


class OriginValidator:
    def __init__(self, settings: SecuritySettings) -> None:
        self._allowed_origins = set(settings.allowed_origins)

    def validate(self, origin: str | None) -> None:
        if not self._allowed_origins:
            return

        if not origin:
            raise AuthorizationError("Request origin is required.")

        parsed = urlparse(origin)
        normalized = f"{parsed.scheme}://{parsed.netloc}"

        if normalized not in self._allowed_origins:
            raise AuthorizationError("Origin is not allowed.")