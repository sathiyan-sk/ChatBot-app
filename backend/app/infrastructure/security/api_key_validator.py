from __future__ import annotations

from app.core.exceptions import AuthenticationError


class ApiKeyValidator:
    def validate_presence(self, api_key: str | None) -> str:
        if api_key is None or not api_key.strip():
            raise AuthenticationError("Missing application API key.")
        return api_key.strip()