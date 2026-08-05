from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ChatRequestModel:
    application_id: str
    conversation_identity: str
    message_text: str
    conversation_title: str | None