from __future__ import annotations

import re

from app.core.exceptions import ApplicationError


_HEX_COLOR_PATTERN = re.compile(r"^#[0-9a-fA-F]{6}$")


def normalize_widget_text(value: str, *, field_name: str, max_length: int) -> str:
    normalized = value.strip()
    if not normalized:
        raise ApplicationError(
            message=f"{field_name} is required.",
            code=f"{field_name.lower()}_required",
            status_code=400,
        )
    if len(normalized) > max_length:
        raise ApplicationError(
            message=f"{field_name} exceeds maximum length.",
            code=f"{field_name.lower()}_too_long",
            status_code=400,
        )
    return normalized


def normalize_color_hex(value: str) -> str:
    normalized = value.strip()
    if not _HEX_COLOR_PATTERN.match(normalized):
        raise ApplicationError(
            message="Primary color must be a valid hex color.",
            code="invalid_widget_primary_color",
            status_code=400,
        )
    return normalized.lower()


def normalize_allowed_origins(values: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()

    for item in values:
        normalized = item.strip().rstrip("/")
        if not normalized:
            continue
        if normalized in seen:
            continue
        seen.add(normalized)
        result.append(normalized)

    return result