from __future__ import annotations

from dataclasses import dataclass

from app.core.exceptions import ApplicationError
from app.modules.documents.application.commands import (
    ArchiveDocumentCommand,
    CreateDocumentCommand,
    MarkDocumentFailedCommand,
    MarkDocumentProcessingCommand,
    MarkDocumentReadyCommand,
    UpdateDocumentCommand,
)
from app.modules.documents.application.dto import DocumentDto
from app.modules.documents.application.queries import (
    GetDocumentByIdQuery,
    ListDocumentsByKnowledgeBaseQuery,
    ListDocumentsByStatusQuery,
)
from app.modules.documents.domain.entities import Document
from app.modules.documents.domain.policies import (
    normalize_document_description,
    normalize_source_uri,
)
from app.modules.documents.domain.repository_interfaces import DocumentRepositoryInterface
from app.modules.documents.domain.value_objects import (
    DocumentSourceType,
    DocumentStatus,
    DocumentTitle,
)
from app.modules.knowledge_bases.domain.repository_interfaces import KnowledgeBaseRepositoryInterface


@dataclass(slots=True)
class DocumentApplicationService:
    document_repository: DocumentRepositoryInterface
    knowledge_base_repository: KnowledgeBaseRepositoryInterface

    def create(self, command: CreateDocumentCommand) -> DocumentDto:
        knowledge_base = self.knowledge_base_repository.get_by_id(command.knowledge_base_id)
        if knowledge_base is None:
            raise ApplicationError(
                message="Knowledge base not found.",
                code="knowledge_base_not_found",
                status_code=404,
            )

        created = self.document_repository.create(
            knowledge_base_id=command.knowledge_base_id,
            title=DocumentTitle(command.title).value,
            description=normalize_document_description(command.description),
            source_type=DocumentSourceType(command.source_type).value,
            source_uri=normalize_source_uri(command.source_uri),
            status=DocumentStatus(command.status).value,
        )
        return self._to_dto(created)

    def get_by_id(self, query: GetDocumentByIdQuery) -> DocumentDto:
        document = self.document_repository.get_by_id(query.document_id)
        if document is None:
            raise ApplicationError(
                message="Document not found.",
                code="document_not_found",
                status_code=404,
            )
        return self._to_dto(document)

    def list_by_knowledge_base(
        self,
        query: ListDocumentsByKnowledgeBaseQuery,
    ) -> list[DocumentDto]:
        status = None if query.status is None else DocumentStatus(query.status).value
        return [
            self._to_dto(item)
            for item in self.document_repository.list_by_knowledge_base_id(
                knowledge_base_id=query.knowledge_base_id,
                status=status,
            )
        ]

    def list_by_status(self, query: ListDocumentsByStatusQuery) -> list[DocumentDto]:
        return [
            self._to_dto(item)
            for item in self.document_repository.list_by_status(
                status=DocumentStatus(query.status).value,
            )
        ]

    def update(self, command: UpdateDocumentCommand) -> DocumentDto:
        existing = self.document_repository.get_by_id(command.document_id)
        if existing is None:
            raise ApplicationError(
                message="Document not found.",
                code="document_not_found",
                status_code=404,
            )

        updated = self.document_repository.update(
            document_id=existing.id,
            title=DocumentTitle(command.title).value,
            description=normalize_document_description(command.description),
            status=DocumentStatus(command.status).value,
            failure_reason=existing.failure_reason,
        )
        return self._to_dto(updated)

    def mark_processing(self, command: MarkDocumentProcessingCommand) -> DocumentDto:
        existing = self._require_document(command.document_id)
        updated = self.document_repository.update(
            document_id=existing.id,
            title=existing.title,
            description=existing.description,
            status="processing",
            failure_reason=None,
        )
        return self._to_dto(updated)

    def mark_ready(self, command: MarkDocumentReadyCommand) -> DocumentDto:
        existing = self._require_document(command.document_id)
        updated = self.document_repository.update(
            document_id=existing.id,
            title=existing.title,
            description=existing.description,
            status="ready",
            failure_reason=None,
        )
        return self._to_dto(updated)

    def mark_failed(self, command: MarkDocumentFailedCommand) -> DocumentDto:
        existing = self._require_document(command.document_id)
        updated = self.document_repository.update(
            document_id=existing.id,
            title=existing.title,
            description=existing.description,
            status="failed",
            failure_reason=command.failure_reason.strip() if command.failure_reason else None,
        )
        return self._to_dto(updated)

    def archive(self, command: ArchiveDocumentCommand) -> DocumentDto:
        existing = self._require_document(command.document_id)
        updated = self.document_repository.update(
            document_id=existing.id,
            title=existing.title,
            description=existing.description,
            status="archived",
            failure_reason=existing.failure_reason,
        )
        return self._to_dto(updated)

    def _require_document(self, document_id: str) -> Document:
        document = self.document_repository.get_by_id(document_id)
        if document is None:
            raise ApplicationError(
                message="Document not found.",
                code="document_not_found",
                status_code=404,
            )
        return document

    def _to_dto(self, document: Document) -> DocumentDto:
        return DocumentDto(
            id=document.id,
            knowledge_base_id=document.knowledge_base_id,
            title=document.title,
            description=document.description,
            source_type=document.source_type,
            source_uri=document.source_uri,
            status=document.status,
            failure_reason=document.failure_reason,
            created_at=document.created_at,
            updated_at=document.updated_at,
        )