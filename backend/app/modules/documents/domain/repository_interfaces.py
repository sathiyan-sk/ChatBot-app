from __future__ import annotations

from abc import ABC, abstractmethod

from app.modules.documents.domain.entities import Document
from uuid import UUID
from datetime import datetime

class DocumentRepositoryInterface(ABC):
    @abstractmethod
    def create(
        self,
        *,
    id: UUID,
    application_id: UUID,
    knowledge_base_id: UUID,
    title: str,
    description: str | None,
    source_type: str,
    source_uri: str | None,
    storage_path: str | None,
    mime_type: str | None,
    file_size_bytes: int | None,
    checksum_sha256: str | None,
    status: str,
    failure_reason: str | None,
    ) -> Document:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, document_id: str) -> Document | None:
        raise NotImplementedError

    @abstractmethod
    def list_by_knowledge_base_id(
        self,
        *,
        knowledge_base_id: UUID | str,
        status: str | None = None,
    ) -> list[Document]:
        raise NotImplementedError

    @abstractmethod
    def list_by_status(self, *, status: str) -> list[Document]:
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        *,
        document_id: str,
        title: str,
        description: str | None,
        status: str,
        failure_reason: str | None,
    ) -> Document:
        raise NotImplementedError