from __future__ import annotations

from fastapi import APIRouter, Depends, Request, status

from app.api.dependencies import (
    get_document_application_service,
    get_session,
)
from app.api.schemas.ingestion import IngestionResponse, StartIngestionRequest
from app.modules.documents.application.commands import (
    MarkDocumentFailedCommand,
    MarkDocumentProcessingCommand,
    MarkDocumentReadyCommand,
)
from app.modules.documents.application.services import DocumentApplicationService
from sqlalchemy.orm import Session

router = APIRouter(prefix="/admin/ingestion", tags=["Admin Ingestion"])


@router.post("/start", response_model=IngestionResponse, status_code=status.HTTP_202_ACCEPTED)
def start_ingestion(
    payload: StartIngestionRequest,
    request: Request,
    document_service: DocumentApplicationService = Depends(get_document_application_service),
    session: Session = Depends(get_session),
) -> IngestionResponse:
    processing_document = document_service.mark_processing(
        MarkDocumentProcessingCommand(document_id=payload.document_id)
    )

    try:
        pipeline = request.app.dependency_overrides.get("knowledge_ingestion_pipeline_factory")
        if pipeline is None:
            pipeline = request.app.state.knowledge_ingestion_pipeline_factory

        ingestion_pipeline = pipeline(
            source_type=payload.source_type,
            request=request,
            session=session,
        )

        ingestion_pipeline.run(
            source_identifier=payload.source_identifier,
            document_id=payload.document_id,
            knowledge_base_id=processing_document.knowledge_base_id,
        )

        document_service.mark_ready(
            MarkDocumentReadyCommand(document_id=payload.document_id)
        )

        return IngestionResponse(
            document_id=payload.document_id,
            status="ready",
        )
    except Exception as exc:
        document_service.mark_failed(
            MarkDocumentFailedCommand(
                document_id=payload.document_id,
                failure_reason=str(exc),
            )
        )
        raise