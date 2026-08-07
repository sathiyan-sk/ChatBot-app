from __future__ import annotations


def normalize_title(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None


def normalize_summary(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None


def normalize_message_content(value: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError("Message content cannot be empty.")
    return cleaned