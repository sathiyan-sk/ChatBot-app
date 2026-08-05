from __future__ import annotations

from app.core.exceptions import ApplicationError


def ensure_single_knowledge_base_per_application(
    *,
    application_id: str,
    existing_knowledge_base_id: str | None,
) -> None:
    if existing_knowledge_base_id is not None:
        raise ApplicationError(
            message=f"Application '{application_id}' already has a knowledge base.",
            code="knowledge_base_already_exists",
            status_code=409,
        )


def normalize_knowledge_base_description(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    if not normalized:
        return None
    if len(normalized) > 2000:
        raise ApplicationError(
            message="Knowledge base description exceeds maximum length.",
            code="knowledge_base_description_too_long",
            status_code=400,
        )
    return normalized