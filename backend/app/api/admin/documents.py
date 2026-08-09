from __future__ import annotations

from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    Query,
    UploadFile,
    status,
)

from app.api.dependencies import (
    get_document_application_service,
    require_admin,
)
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
from app.modules.documents.application.services import (
    DocumentApplicationService,
)


router = APIRouter(
    prefix="/admin/documents",
    tags=["Admin Documents"],
    dependencies=[
        Depends(require_admin),
    ],
)


@router.post(
    "/upload",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_document(
    knowledge_base_id: UUID = Form(...),
    title: str = Form(...),
    description: str | None = Form(None),
    file: UploadFile = File(...),
    service: DocumentApplicationService = Depends(
        get_document_application_service,
    ),
) -> DocumentResponse:
    content = file.file.read()

    result = service.upload(
        knowledge_base_id=knowledge_base_id,
        title=title,
        description=description,
        filename=file.filename or "uploaded-file",
        content_type=file.content_type,
        content=content,
    )

    return DocumentResponse.model_validate(
        result,
        from_attributes=True,
    )


@router.post(
    "",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_document(
    request: CreateDocumentRequest,
    service: DocumentApplicationService = Depends(
        get_document_application_service,
    ),
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

    return DocumentResponse.model_validate(
        result,
        from_attributes=True,
    )


@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
)
def get_document_by_id(
    document_id: UUID,
    service: DocumentApplicationService = Depends(
        get_document_application_service,
    ),
) -> DocumentResponse:
    result = service.get_by_id(
        GetDocumentByIdQuery(
            document_id=document_id,
        )
    )

    return DocumentResponse.model_validate(
        result,
        from_attributes=True,
    )


@router.get(
    "",
    response_model=list[DocumentResponse],
)
def list_documents(
    knowledge_base_id: UUID | None = Query(
        default=None,
    ),
    status_value: str | None = Query(
        default=None,
        alias="status",
    ),
    service: DocumentApplicationService = Depends(
        get_document_application_service,
    ),
) -> list[DocumentResponse]:
    if knowledge_base_id is not None:
        results = service.list_by_knowledge_base(
            ListDocumentsByKnowledgeBaseQuery(
                knowledge_base_id=knowledge_base_id,
                status=status_value,
            )
        )

    elif status_value is not None:
        results = service.list_by_status(
            ListDocumentsByStatusQuery(
                status=status_value,
            )
        )

    else:
        results = service.list_all()

    return [
        DocumentResponse.model_validate(
            item,
            from_attributes=True,
        )
        for item in results
    ]


@router.put(
    "/{document_id}",
    response_model=DocumentResponse,
)
def update_document(
    document_id: UUID,
    request: UpdateDocumentRequest,
    service: DocumentApplicationService = Depends(
        get_document_application_service,
    ),
) -> DocumentResponse:
    result = service.update(
        UpdateDocumentCommand(
            document_id=document_id,
            title=request.title,
            description=request.description,
            status=request.status,
        )
    )

    return DocumentResponse.model_validate(
        result,
        from_attributes=True,
    )


@router.post(
    "/{document_id}/processing",
    response_model=DocumentResponse,
)
def mark_document_processing(
    document_id: UUID,
    service: DocumentApplicationService = Depends(
        get_document_application_service,
    ),
) -> DocumentResponse:
    result = service.mark_processing(
        MarkDocumentProcessingCommand(
            document_id=document_id,
        )
    )

    return DocumentResponse.model_validate(
        result,
        from_attributes=True,
    )


@router.post(
    "/{document_id}/ready",
    response_model=DocumentResponse,
)
def mark_document_ready(
    document_id: UUID,
    service: DocumentApplicationService = Depends(
        get_document_application_service,
    ),
) -> DocumentResponse:
    result = service.mark_ready(
        MarkDocumentReadyCommand(
            document_id=document_id,
        )
    )

    return DocumentResponse.model_validate(
        result,
        from_attributes=True,
    )


@router.post(
    "/{document_id}/failed",
    response_model=DocumentResponse,
)
def mark_document_failed(
    document_id: UUID,
    request: MarkDocumentFailedRequest,
    service: DocumentApplicationService = Depends(
        get_document_application_service,
    ),
) -> DocumentResponse:
    result = service.mark_failed(
        MarkDocumentFailedCommand(
            document_id=document_id,
            failure_reason=request.failure_reason,
        )
    )

    return DocumentResponse.model_validate(
        result,
        from_attributes=True,
    )


@router.post(
    "/{document_id}/archive",
    response_model=DocumentResponse,
)
def archive_document(
    document_id: UUID,
    service: DocumentApplicationService = Depends(
        get_document_application_service,
    ),
) -> DocumentResponse:
    result = service.archive(
        ArchiveDocumentCommand(
            document_id=document_id,
        )
    )

    return DocumentResponse.model_validate(
        result,
        from_attributes=True,
    )