from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import get_document_application_service
from app.api.schemas.documents import (
    CreateDocumentRequest,
    DocumentResponse,
    MarkDocumentFailedRequest,
    UpdateDocumentRequest,
)
from app.modules.documents.application.commands import (
    ArchiveDocumentCommand,
    CreateDocumentCommand,
    MarkDocumentFailedCommand,
    MarkDocumentProcessingCommand,
    MarkDocumentReadyCommand,
    UpdateDocumentCommand,
)
from app.modules.documents.application.queries import (
    GetDocumentByIdQuery,
    ListDocumentsByKnowledgeBaseQuery,
    ListDocumentsByStatusQuery,
)
from app.modules.documents.application.services import DocumentApplicationService

router = APIRouter(prefix="/admin/documents", tags=["Admin Documents"])


@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
def create_document(
    request: CreateDocumentRequest,
    service: DocumentApplicationService = Depends(get_document_application_service),
) -> DocumentResponse:
    result = service.create(
        CreateDocumentCommand(
            knowledge_base_id=request.knowledge_base_id,
            title=request.title,
            description=request.description,
            source_type=request.source_type,
            source_uri=request.source_uri,
            status=request.status,
        )
    )
    return DocumentResponse.model_validate(result.__dict__)


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document_by_id(
    document_id: str,
    service: DocumentApplicationService = Depends(get_document_application_service),
) -> DocumentResponse:
    result = service.get_by_id(GetDocumentByIdQuery(document_id=document_id))
    return DocumentResponse.model_validate(result.__dict__)


@router.get("", response_model=list[DocumentResponse])
def list_documents(
    knowledge_base_id: str | None = Query(default=None),
    status_value: str | None = Query(default=None, alias="status"),
    service: DocumentApplicationService = Depends(get_document_application_service),
) -> list[DocumentResponse]:
    if knowledge_base_id is not None:
        results = service.list_by_knowledge_base(
            ListDocumentsByKnowledgeBaseQuery(
                knowledge_base_id=knowledge_base_id,
                status=status_value,
            )
        )
    elif status_value is not None:
        results = service.list_by_status(ListDocumentsByStatusQuery(status=status_value))
    else:
        results = []

    return [DocumentResponse.model_validate(item.__dict__) for item in results]


@router.put("/{document_id}", response_model=DocumentResponse)
def update_document(
    document_id: str,
    request: UpdateDocumentRequest,
    service: DocumentApplicationService = Depends(get_document_application_service),
) -> DocumentResponse:
    result = service.update(
        UpdateDocumentCommand(
            document_id=document_id,
            title=request.title,
            description=request.description,
            status=request.status,
        )
    )
    return DocumentResponse.model_validate(result.__dict__)


@router.post("/{document_id}/processing", response_model=DocumentResponse)
def mark_document_processing(
    document_id: str,
    service: DocumentApplicationService = Depends(get_document_application_service),
) -> DocumentResponse:
    result = service.mark_processing(MarkDocumentProcessingCommand(document_id=document_id))
    return DocumentResponse.model_validate(result.__dict__)


@router.post("/{document_id}/ready", response_model=DocumentResponse)
def mark_document_ready(
    document_id: str,
    service: DocumentApplicationService = Depends(get_document_application_service),
) -> DocumentResponse:
    result = service.mark_ready(MarkDocumentReadyCommand(document_id=document_id))
    return DocumentResponse.model_validate(result.__dict__)


@router.post("/{document_id}/failed", response_model=DocumentResponse)
def mark_document_failed(
    document_id: str,
    request: MarkDocumentFailedRequest,
    service: DocumentApplicationService = Depends(get_document_application_service),
) -> DocumentResponse:
    result = service.mark_failed(
        MarkDocumentFailedCommand(
            document_id=document_id,
            failure_reason=request.failure_reason,
        )
    )
    return DocumentResponse.model_validate(result.__dict__)


@router.post("/{document_id}/archive", response_model=DocumentResponse)
def archive_document(
    document_id: str,
    service: DocumentApplicationService = Depends(get_document_application_service),
) -> DocumentResponse:
    result = service.archive(ArchiveDocumentCommand(document_id=document_id))
    return DocumentResponse.model_validate(result.__dict__)