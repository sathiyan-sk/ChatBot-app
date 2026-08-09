from __future__ import annotations

from pydantic import BaseModel, Field


class StartIngestionRequest(BaseModel):
    document_id: str = Field(..., min_length=1)


class IngestionResponse(BaseModel):
    document_id: str
    status: str