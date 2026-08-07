from __future__ import annotations


def normalize_document_description(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None


def normalize_source_uri(value: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError("Source URI cannot be empty.")
    return cleaned