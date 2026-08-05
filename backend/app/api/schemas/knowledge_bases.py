from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class CreateKnowledgeBaseRequest(BaseModel):
    application_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    status: str = Field(default="active")


class UpdateKnowledgeBaseRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    status: str = Field(..., min_length=1)


class KnowledgeBaseResponse(BaseModel):
    id: str
    application_id: str
    name: str
    description: str | None
    status: str
    created_at: datetime
    updated_at: datetime