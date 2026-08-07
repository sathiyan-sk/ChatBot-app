from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field
from uuid import UUID
from pydantic import ConfigDict

class CreateDocumentRequest(BaseModel):
    knowledge_base_id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    source_type: str = Field(..., min_length=1, max_length=50)
    source_uri: str = Field(..., min_length=1, max_length=2048)
    status: str = Field(default="pending", min_length=1)


class UpdateDocumentRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    status: str = Field(..., min_length=1)


class MarkDocumentFailedRequest(BaseModel):
    failure_reason: str | None = Field(default=None, max_length=2000)



class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    application_id: UUID
    knowledge_base_id: UUID
    title: str
    description: str | None = None
    source_type: str
    source_uri: str | None = None
    storage_path: str | None = None
    mime_type: str | None = None
    file_size_bytes: int | None = None
    checksum_sha256: str | None = None
    status: str
    failure_reason: str | None = None
    created_at: datetime
    updated_at: datetime

class UploadedDocumentMetadata(BaseModel):
    knowledge_base_id: UUID
    title: str
    description: str | None = None
