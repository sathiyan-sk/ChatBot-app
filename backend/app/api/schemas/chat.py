from __future__ import annotations

from pydantic import BaseModel, Field


class AskChatRequestSchema(BaseModel):
    conversation_identity: str = Field(min_length=1, max_length=255)
    message_text: str = Field(min_length=1)
    conversation_title: str | None = Field(default=None, max_length=255)


class CitationSchema(BaseModel):
    document_id: str
    document_title: str
    chunk_id: str
    source_uri: str | None = None


class AskChatResponseSchema(BaseModel):
    conversation_id: str
    user_message_id: str
    assistant_message_id: str
    answer_text: str
    citations: list[CitationSchema]