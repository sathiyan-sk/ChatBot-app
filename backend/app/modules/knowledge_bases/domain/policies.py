from __future__ import annotations


def ensure_single_knowledge_base_per_application(
    *,
    application_id: str,
    existing_knowledge_base_id: str | None,
) -> None:
    if existing_knowledge_base_id is not None:
        raise ValueError(
            f"Application '{application_id}' already has a knowledge base."
        )


def normalize_knowledge_base_description(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None