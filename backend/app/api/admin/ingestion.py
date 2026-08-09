from __future__ import annotations

import logging

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    status,
)
from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_document_application_service,
    get_knowledge_ingestion_pipeline,
    get_session,
)
from app.api.schemas.ingestion import (
    IngestionResponse,
    StartIngestionRequest,
)
from app.knowledge_engine.shared.models import (
    KnowledgeIngestionPipelineRequest,
)
from app.modules.documents.application.commands import (
    MarkDocumentFailedCommand,
    MarkDocumentProcessingCommand,
    MarkDocumentReadyCommand,
)
from app.modules.documents.application.services import (
    DocumentApplicationService,
)


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/admin/ingestion",
    tags=["Admin Ingestion"],
)


def _resolve_source_type(
    document: object,
    source_path: str,
) -> str:
    stored_source_type = getattr(
        document,
        "source_type",
        None,
    )

    if isinstance(stored_source_type, str):
        stored_source_type = stored_source_type.strip().lower()

    if stored_source_type in {
        "pdf",
        "docx",
        "xlsx",
        "pptx",
        "md",
        "markdown",
        "txt",
        "text",
        "csv",
        "image",
        "png",
        "jpg",
        "jpeg",
        "tiff",
        "website",
    }:
        return stored_source_type

    filename = source_path.rsplit(
        "/",
        1,
    )[-1]

    if "." not in filename:
        return "file"

    extension = filename.rsplit(
        ".",
        1,
    )[-1].strip().lower()

    extension_aliases = {
        "markdown": "md",
        "text": "txt",
        "jpeg": "image",
        "jpg": "image",
        "png": "image",
        "tiff": "image",
        "webp": "image",
    }

    return extension_aliases.get(
        extension,
        extension or "file",
    )


def _validate_storage_path(
    document: object,
) -> str:
    source_path = getattr(
        document,
        "storage_path",
        None,
    )

    if source_path is None:
        raise HTTPException(
            status_code=(
                status.HTTP_422_UNPROCESSABLE_ENTITY
            ),
            detail={
                "code": (
                    "document_storage_path_missing"
                ),
                "message": (
                    "The document has no stored "
                    "Supabase Storage path."
                ),
            },
        )

    if not isinstance(source_path, str):
        raise HTTPException(
            status_code=(
                status.HTTP_422_UNPROCESSABLE_ENTITY
            ),
            detail={
                "code": (
                    "document_storage_path_invalid"
                ),
                "message": (
                    "The document storage path "
                    "must be a string."
                ),
            },
        )

    normalized_path = source_path.strip()

    if not normalized_path:
        raise HTTPException(
            status_code=(
                status.HTTP_422_UNPROCESSABLE_ENTITY
            ),
            detail={
                "code": (
                    "document_storage_path_empty"
                ),
                "message": (
                    "The document storage path "
                    "is empty."
                ),
            },
        )

    if normalized_path.lower() in {
        "null",
        "none",
        "string",
    }:
        raise HTTPException(
            status_code=(
                status.HTTP_422_UNPROCESSABLE_ENTITY
            ),
            detail={
                "code": (
                    "document_storage_path_invalid"
                ),
                "message": (
                    "The document has an invalid "
                    "Supabase Storage path."
                ),
            },
        )

    return normalized_path


@router.post(
    "/start",
    response_model=IngestionResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def start_ingestion(
    payload: StartIngestionRequest,
    request: Request,
    document_service: DocumentApplicationService = Depends(
        get_document_application_service,
    ),
    session: Session = Depends(get_session),
) -> IngestionResponse:
    processing_document = None

    try:
        processing_document = (
            document_service.mark_processing(
                MarkDocumentProcessingCommand(
                    document_id=payload.document_id,
                )
            )
        )

        source_path = _validate_storage_path(
            processing_document,
        )

        source_type = _resolve_source_type(
            processing_document,
            source_path,
        )

        pipeline_factory = getattr(
            request.app.state,
            "knowledge_ingestion_pipeline_factory",
            None,
        )

        if pipeline_factory is None:
            pipeline_factory = (
                get_knowledge_ingestion_pipeline
            )

        ingestion_pipeline = pipeline_factory(
            source_type=source_type,
            request=request,
            session=session,
        )

        pipeline_request = (
            KnowledgeIngestionPipelineRequest(
                document_id=str(
                    payload.document_id,
                ),
                knowledge_base_id=str(
                    processing_document.knowledge_base_id,
                ),
                source_type=source_type,
                source_path=source_path,
                source_identifier=source_path,
            )
        )

        logger.info(
            "Starting knowledge ingestion",
            extra={
                "document_id": str(
                    payload.document_id,
                ),
                "knowledge_base_id": str(
                    processing_document.knowledge_base_id,
                ),
                "source_type": source_type,
                "source_path": source_path,
            },
        )

        ingestion_pipeline.run(
            pipeline_request,
        )

        document_service.mark_ready(
            MarkDocumentReadyCommand(
                document_id=payload.document_id,
            )
        )

        logger.info(
            "Knowledge ingestion completed",
            extra={
                "document_id": str(
                    payload.document_id,
                ),
                "source_type": source_type,
                "source_path": source_path,
            },
        )

        return IngestionResponse(
            document_id=payload.document_id,
            status="ready",
        )

    except HTTPException as exc:
        logger.exception(
            "Knowledge ingestion rejected for "
            "document_id=%s",
            payload.document_id,
        )

        session.rollback()

        if processing_document is not None:
            document_service.mark_failed(
                MarkDocumentFailedCommand(
                    document_id=payload.document_id,
                    failure_reason=str(
                        exc.detail,
                    ),
                )
            )

        raise

    except Exception as exc:

        logger.exception(
        "Knowledge ingestion failed for "
        "document_id=%s",
        payload.document_id,
        )

        session.rollback()

        try:
            document_service.mark_failed(
                MarkDocumentFailedCommand(
                    document_id=payload.document_id,
                    failure_reason=str(exc),
                )
            )
        except Exception:
            logger.exception(
                "Could not mark document as failed: %s",
                payload.document_id,
            )

            raise