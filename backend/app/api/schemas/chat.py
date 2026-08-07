from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class ChatMessageRequest(BaseModel):
    application_id: str = Field(..., min_length=1)
    conversation_identity: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=1, max_length=8000)
    conversation_title: str | None = Field(default=None, max_length=255)


class CitationResponse(BaseModel):
    document_id: str
    title: str
    chunk_id: str
    source_uri: str | None


class ChatMessageResponse(BaseModel):
    conversation_id: str
    answer: str
    citations: list[CitationResponse] = Field(default_factory=list)
    created_at: datetime