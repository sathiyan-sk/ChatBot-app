from __future__ import annotations

import re

from app.core.exceptions import ApplicationError


_SLUG_PATTERN = re.compile(r"[^a-z0-9]+")


def normalize_application_name(name: str) -> str:
    normalized = " ".join(name.strip().split())
    if not normalized:
        raise ApplicationError(
            message="Application name is required.",
            code="application_name_required",
            status_code=400,
        )
    return normalized


def build_application_slug(name: str) -> str:
    normalized = normalize_application_name(name).lower()
    slug = _SLUG_PATTERN.sub("-", normalized).strip("-")
    if not slug:
        raise ApplicationError(
            message="Unable to generate a valid application slug.",
            code="invalid_application_slug",
            status_code=400,
        )
    return slug


def normalize_optional_text(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    return normalized if normalized else None