from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CreateKnowledgeBaseRequest(BaseModel):
    application_id: UUID
    name: str = Field(
        ...,
        min_length=1,
        max_length=150,
    )
    status: str = "ready"


class UpdateKnowledgeBaseRequest(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=150,
    )
    status: str = "ready"


class KnowledgeBaseResponse(BaseModel):
    id: UUID
    application_id: UUID
    name: str
    slug: str
    status: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )