from __future__ import annotations

import re


def normalize_application_name(value: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError("Application name cannot be empty.")
    return cleaned


def build_application_slug(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    if not slug:
        raise ValueError("Application slug cannot be empty.")
    return slug


def normalize_optional_text(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None