from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID

class CreateKnowledgeBaseRequest(BaseModel):
    application_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1, max_length=150)
    description: str | None = Field(default=None, max_length=2000)
    status: str = Field(default="ready", min_length=1)


class UpdateKnowledgeBaseRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    description: str | None = Field(default=None, max_length=2000)
    status: str = Field(..., min_length=1)


class KnowledgeBaseResponse(BaseModel):
    id: UUID
    application_id: UUID
    name: str
    description: str | None
    status: str
    created_at: datetime
    updated_at: datetime