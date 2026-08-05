from __future__ import annotations

from app.core.exceptions import ApplicationError


def normalize_document_description(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    if not normalized:
        return None
    if len(normalized) > 2000:
        raise ApplicationError(
            message="Document description exceeds maximum length.",
            code="document_description_too_long",
            status_code=400,
        )
    return normalized


def normalize_source_uri(value: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ApplicationError(
            message="Document source URI is required.",
            code="document_source_uri_required",
            status_code=400,
        )
    if len(normalized) > 2048:
        raise ApplicationError(
            message="Document source URI exceeds maximum length.",
            code="document_source_uri_too_long",
            status_code=400,
        )
    return normalized


def ensure_document_belongs_to_knowledge_base(
    *,
    expected_knowledge_base_id: str,
    actual_knowledge_base_id: str,
) -> None:
    if expected_knowledge_base_id != actual_knowledge_base_id:
        raise ApplicationError(
            message="Document does not belong to the specified knowledge base.",
            code="document_knowledge_base_mismatch",
            status_code=409,
        )