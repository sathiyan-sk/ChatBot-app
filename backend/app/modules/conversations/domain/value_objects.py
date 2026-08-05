from __future__ import annotations

from dataclasses import dataclass

from app.core.exceptions import ApplicationError


@dataclass(frozen=True, slots=True)
class ConversationIdentity:
    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()
        if not normalized:
            raise ApplicationError(
                message="Conversation identity is required.",
                code="conversation_identity_required",
                status_code=400,
            )
        object.__setattr__(self, "value", normalized)


@dataclass(frozen=True, slots=True)
class MessageRole:
    value: str

    _ALLOWED_VALUES = {"user", "assistant", "system"}

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()
        if normalized not in self._ALLOWED_VALUES:
            raise ApplicationError(
                message="Invalid message role.",
                code="invalid_message_role",
                status_code=400,
            )
        object.__setattr__(self, "value", normalized)