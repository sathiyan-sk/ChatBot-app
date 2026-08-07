from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class ResolveConversationRequest(BaseModel):
    application_id: str = Field(..., min_length=1)
    conversation_identity: str = Field(..., min_length=1, max_length=255)
    title: str | None = Field(default=None, max_length=255)


class AppendMessageRequest(BaseModel):
    role: str = Field(..., min_length=1, max_length=50)
    content: str = Field(..., min_length=1, max_length=8000)
    citation_payload: str | None = Field(default=None, max_length=20000)


class UpdateConversationRequest(BaseModel):
    title: str | None = Field(default=None, max_length=255)
    summary: str | None = Field(default=None, max_length=4000)
    is_active: bool = True


class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    role: str
    content: str
    sequence_number: int
    citation_payload: str | None
    created_at: datetime
    updated_at: datetime


class ConversationResponse(BaseModel):
    id: str
    application_id: str
    conversation_identity: str
    title: str | None
    summary: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class ConversationDetailResponse(BaseModel):
    conversation: ConversationResponse
    messages: list[MessageResponse]