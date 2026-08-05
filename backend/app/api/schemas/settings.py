from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class CreateSettingsRequest(BaseModel):
    application_id: str = Field(..., min_length=1)
    conversation_inactivity_minutes: int = Field(..., ge=5, le=10080)
    conversation_retention_days: int = Field(..., ge=1, le=3650)
    retrieval_top_k: int = Field(..., ge=1, le=50)
    reranker_enabled: bool = True
    citations_enabled: bool = True


class UpdateSettingsRequest(BaseModel):
    conversation_inactivity_minutes: int = Field(..., ge=5, le=10080)
    conversation_retention_days: int = Field(..., ge=1, le=3650)
    retrieval_top_k: int = Field(..., ge=1, le=50)
    reranker_enabled: bool
    citations_enabled: bool


class SettingsResponse(BaseModel):
    id: str
    application_id: str
    conversation_inactivity_minutes: int
    conversation_retention_days: int
    retrieval_top_k: int
    reranker_enabled: bool
    citations_enabled: bool
    created_at: datetime
    updated_at: datetime