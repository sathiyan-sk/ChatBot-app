from __future__ import annotations

from app.config.settings import SecuritySettings


def validate_security_settings(settings: SecuritySettings) -> None:
    if not settings.admin_username.strip():
        raise ValueError("ADMIN_USERNAME must not be empty.")

    if not settings.admin_password.strip():
        raise ValueError("ADMIN_PASSWORD must not be empty.")

    if len(settings.admin_password) < 8:
        raise ValueError("ADMIN_PASSWORD must be at least 8 characters long.")

    if not settings.api_key_header_name.strip():
        raise ValueError("API_KEY_HEADER_NAME must not be empty.")

    if not settings.request_id_header_name.strip():
        raise ValueError("REQUEST_ID_HEADER_NAME must not be empty.")
    