from __future__ import annotations

from pydantic import BaseModel, Field


class StartIngestionRequest(BaseModel):
    document_id: str = Field(..., min_length=1)
    source_type: str = Field(..., min_length=1)
    source_identifier: str = Field(..., min_length=1, max_length=2048)


class IngestionResponse(BaseModel):
    document_id: str
    status: str