from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from uuid import UUID, uuid4

from app.core.exceptions import ApplicationError
from app.infrastructure.providers.providers import (
    StorageContract,
)
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
from app.modules.documents.domain.repository_interfaces import (
    DocumentRepositoryInterface,
)
from app.modules.documents.domain.value_objects import (
    DocumentSourceType,
    DocumentStatus,
    DocumentTitle,
)
from app.modules.knowledge_bases.domain.repository_interfaces import (
    KnowledgeBaseRepositoryInterface,
)


@dataclass(slots=True)
class DocumentApplicationService:
    document_repository: DocumentRepositoryInterface
    knowledge_base_repository: (
        KnowledgeBaseRepositoryInterface
    )
    storage_provider: StorageContract

    def upload(
        self,
        *,
        knowledge_base_id: UUID,
        title: str,
        description: str | None,
        filename: str,
        content_type: str | None,
        content: bytes,
    ) -> DocumentDto:
        knowledge_base = (
            self.knowledge_base_repository.get_by_id(
                knowledge_base_id,
            )
        )

        if knowledge_base is None:
            raise ApplicationError(
                message="Knowledge base not found.",
                code="knowledge_base_not_found",
                status_code=404,
            )

        if not content:
            raise ApplicationError(
                message="Uploaded file is empty.",
                code="uploaded_file_empty",
                status_code=422,
            )

        document_id = uuid4()

        safe_filename = Path(filename).name.strip()

        if not safe_filename:
            safe_filename = "uploaded-file"

        checksum_sha256 = sha256(content).hexdigest()

        storage_path = (
            f"applications/"
            f"{knowledge_base.application_id}/"
            f"knowledge-bases/"
            f"{knowledge_base.id}/"
            f"documents/"
            f"{document_id}/"
            f"{safe_filename}"
        )

        # Important:
        # upload() must return the normalized path that was
        # actually used in Supabase Storage.
        stored_path = self.storage_provider.upload(
            path=storage_path,
            content=content,
            content_type=content_type,
        )

        if not stored_path:
            raise ApplicationError(
                message=(
                    "Storage provider did not return "
                    "the uploaded file path."
                ),
                code="storage_path_not_returned",
                status_code=502,
            )

        created = self.document_repository.create(
            id=document_id,
            application_id=knowledge_base.application_id,
            knowledge_base_id=knowledge_base.id,
            title=DocumentTitle(title).value,
            description=normalize_document_description(
                description,
            ),
            source_type=DocumentSourceType(
                "file",
            ).value,
            source_uri=None,
            storage_path=stored_path,
            mime_type=content_type,
            file_size_bytes=len(content),
            checksum_sha256=checksum_sha256,
            status=DocumentStatus(
                "pending",
            ).value,
            failure_reason=None,
        )

        return self._to_dto(created)

    def create(
        self,
        command: CreateDocumentCommand,
    ) -> DocumentDto:
        knowledge_base = (
            self.knowledge_base_repository.get_by_id(
                command.knowledge_base_id,
            )
        )

        if knowledge_base is None:
            raise ApplicationError(
                message=(
                    "Knowledge base with ID "
                    f"{command.knowledge_base_id} "
                    "was not found."
                ),
                code="knowledge_base_not_found",
                status_code=404,
            )

        created = self.document_repository.create(
            application_id=knowledge_base.application_id,
            knowledge_base_id=knowledge_base.id,
            title=DocumentTitle(
                command.title,
            ).value,
            description=normalize_document_description(
                command.description,
            ),
            source_type=DocumentSourceType(
                command.source_type,
            ).value,
            source_uri=normalize_source_uri(
                command.source_uri,
            ),
            status=DocumentStatus(
                command.status,
            ).value,
        )

        return self._to_dto(created)

    def get_by_id(
        self,
        query: GetDocumentByIdQuery,
    ) -> DocumentDto:
        document = self.document_repository.get_by_id(
            query.document_id,
        )

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
        document_status = (
            None
            if query.status is None
            else DocumentStatus(
                query.status,
            ).value
        )

        documents = (
            self.document_repository.list_by_knowledge_base_id(
                knowledge_base_id=query.knowledge_base_id,
                status=document_status,
            )
        )

        return [
            self._to_dto(document)
            for document in documents
        ]

    def list_by_status(
        self,
        query: ListDocumentsByStatusQuery,
    ) -> list[DocumentDto]:
        document_status = DocumentStatus(
            query.status,
        ).value

        documents = (
            self.document_repository.list_by_status(
                status=document_status,
            )
        )

        return [
            self._to_dto(document)
            for document in documents
        ]

    def list_all(self) -> list[DocumentDto]:
        documents = (
            self.document_repository.list_all()
        )

        return [
            self._to_dto(document)
            for document in documents
        ]

    def update(
        self,
        command: UpdateDocumentCommand,
    ) -> DocumentDto:
        existing = self.document_repository.get_by_id(
            command.document_id,
        )

        if existing is None:
            raise ApplicationError(
                message="Document not found.",
                code="document_not_found",
                status_code=404,
            )

        updated = self.document_repository.update(
            document_id=existing.id,
            title=DocumentTitle(
                command.title,
            ).value,
            description=normalize_document_description(
                command.description,
            ),
            status=DocumentStatus(
                command.status,
            ).value,
            failure_reason=existing.failure_reason,
        )

        return self._to_dto(updated)

    def mark_processing(
        self,
        command: MarkDocumentProcessingCommand,
    ) -> DocumentDto:
        existing = self._require_document(
            command.document_id,
        )

        updated = self.document_repository.update(
            document_id=existing.id,
            title=existing.title,
            description=existing.description,
            status="processing",
            failure_reason=None,
        )

        return self._to_dto(updated)

    def mark_ready(
        self,
        command: MarkDocumentReadyCommand,
    ) -> DocumentDto:
        existing = self._require_document(
            command.document_id,
        )

        updated = self.document_repository.update(
            document_id=existing.id,
            title=existing.title,
            description=existing.description,
            status="ready",
            failure_reason=None,
        )

        return self._to_dto(updated)

    def mark_failed(
        self,
        command: MarkDocumentFailedCommand,
    ) -> DocumentDto:
        existing = self._require_document(
            command.document_id,
        )

        failure_reason = (
            command.failure_reason.strip()
            if command.failure_reason
            else None
        )

        updated = self.document_repository.update(
            document_id=existing.id,
            title=existing.title,
            description=existing.description,
            status="failed",
            failure_reason=failure_reason,
        )

        return self._to_dto(updated)

    def archive(
        self,
        command: ArchiveDocumentCommand,
    ) -> DocumentDto:
        existing = self._require_document(
            command.document_id,
        )

        updated = self.document_repository.update(
            document_id=existing.id,
            title=existing.title,
            description=existing.description,
            status="archived",
            failure_reason=existing.failure_reason,
        )

        return self._to_dto(updated)

    def _require_document(
        self,
        document_id: str | UUID,
    ) -> Document:
        document = self.document_repository.get_by_id(
            document_id,
        )

        if document is None:
            raise ApplicationError(
                message="Document not found.",
                code="document_not_found",
                status_code=404,
            )

        return document

    def _to_dto(
        self,
        document: Document,
    ) -> DocumentDto:
        return DocumentDto(
            id=document.id,
            application_id=document.application_id,
            knowledge_base_id=document.knowledge_base_id,
            title=document.title,
            description=document.description,
            source_type=document.source_type,
            source_uri=document.source_uri,
            storage_path=document.storage_path,
            mime_type=document.mime_type,
            file_size_bytes=document.file_size_bytes,
            checksum_sha256=document.checksum_sha256,
            status=document.status,
            failure_reason=document.failure_reason,
            created_at=document.created_at,
            updated_at=document.updated_at,
        )