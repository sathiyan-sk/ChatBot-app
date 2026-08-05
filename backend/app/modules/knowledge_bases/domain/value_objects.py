from __future__ import annotations

from dataclasses import dataclass

from app.core.exceptions import ApplicationError


@dataclass(frozen=True, slots=True)
class KnowledgeBaseStatus:
    value: str

    _ALLOWED_VALUES = {"active", "inactive"}

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()
        if normalized not in self._ALLOWED_VALUES:
            raise ApplicationError(
                message="Invalid knowledge base status.",
                code="invalid_knowledge_base_status",
                status_code=400,
            )
        object.__setattr__(self, "value", normalized)


@dataclass(frozen=True, slots=True)
class KnowledgeBaseName:
    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()
        if not normalized:
            raise ApplicationError(
                message="Knowledge base name is required.",
                code="knowledge_base_name_required",
                status_code=400,
            )
        if len(normalized) > 255:
            raise ApplicationError(
                message="Knowledge base name exceeds maximum length.",
                code="knowledge_base_name_too_long",
                status_code=400,
            )
        object.__setattr__(self, "value", normalized)