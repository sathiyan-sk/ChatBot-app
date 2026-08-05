from __future__ import annotations

from dataclasses import dataclass

from app.core.exceptions import ApplicationError


@dataclass(frozen=True, slots=True)
class DocumentSourceType:
    value: str

    _ALLOWED_VALUES = {"file", "website", "csv", "image"}

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()
        if normalized not in self._ALLOWED_VALUES:
            raise ApplicationError(
                message="Invalid document source type.",
                code="invalid_document_source_type",
                status_code=400,
            )
        object.__setattr__(self, "value", normalized)


@dataclass(frozen=True, slots=True)
class DocumentStatus:
    value: str

    _ALLOWED_VALUES = {
        "pending",
        "processing",
        "ready",
        "failed",
        "archived",
    }

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()
        if normalized not in self._ALLOWED_VALUES:
            raise ApplicationError(
                message="Invalid document status.",
                code="invalid_document_status",
                status_code=400,
            )
        object.__setattr__(self, "value", normalized)


@dataclass(frozen=True, slots=True)
class DocumentTitle:
    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()
        if not normalized:
            raise ApplicationError(
                message="Document title is required.",
                code="document_title_required",
                status_code=400,
            )
        if len(normalized) > 255:
            raise ApplicationError(
                message="Document title exceeds maximum length.",
                code="document_title_too_long",
                status_code=400,
            )
        object.__setattr__(self, "value", normalized)