from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class CreateDocumentRequest(BaseModel):
    knowledge_base_id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    source_type: str = Field(..., min_length=1)
    source_uri: str = Field(..., min_length=1, max_length=2048)
    status: str = Field(default="pending")


class UpdateDocumentRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    status: str = Field(..., min_length=1)


class MarkDocumentFailedRequest(BaseModel):
    failure_reason: str | None = Field(default=None, max_length=2000)


class DocumentResponse(BaseModel):
    id: str
    knowledge_base_id: str
    title: str
    description: str | None
    source_type: str
    source_uri: str
    status: str
    failure_reason: str | None
    created_at: datetime
    updated_at: datetime