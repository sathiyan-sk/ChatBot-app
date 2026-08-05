from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class CitationItem:
    document_id: str
    document_title: str
    chunk_id: str
    source_uri: str | None


@dataclass(slots=True, frozen=True)
class ChatResponseModel:
    conversation_id: str
    user_message_id: str
    assistant_message_id: str
    answer_text: str
    citations: list[CitationItem]