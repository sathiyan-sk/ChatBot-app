from __future__ import annotations

from app.core.exceptions import ApplicationError


def normalize_title(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    return normalized or None


def normalize_summary(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    return normalized or None


def normalize_message_content(value: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ApplicationError(
            message="Message content is required.",
            code="message_content_required",
            status_code=400,
        )
    return normalized