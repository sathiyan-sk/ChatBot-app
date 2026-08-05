from __future__ import annotations

import secrets

from app.config.settings import SecuritySettings
from app.core.exceptions import AuthenticationError


class AdminAuthenticator:
    def __init__(self, settings: SecuritySettings) -> None:
        self._settings = settings

    def authenticate(self, username: str, password: str) -> None:
        username_matches = secrets.compare_digest(username, self._settings.admin_username)
        password_matches = secrets.compare_digest(password, self._settings.admin_password)

        if not username_matches or not password_matches:
            raise AuthenticationError("Invalid admin credentials.")