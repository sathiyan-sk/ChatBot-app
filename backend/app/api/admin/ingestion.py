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
from sqlalchemy.exc import SQLAlchemyError

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
from app.modules.documents.application.queries import (
    GetDocumentByIdQuery,
)
from app.modules.documents.application.services import (
    DocumentApplicationService,
)

logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/admin/ingestion",
    tags=["Admin Ingestion"],
)
def _safe_rollback(session: Session) -> None:
    try:
        session.rollback()
    except SQLAlchemyError:
        logger.exception(
            "Database rollback failed; closing broken session.",
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

    if isinstance(
        stored_source_type,
        str,
    ):
        normalized_type = (
            stored_source_type.strip().lower()
        )

        if normalized_type in {
            "pdf",
            "website",
            "csv",
            "image",
            "doc",
            "docx",
            "txt",
            "text",
            "md",
            "markdown",
            "xls",
            "xlsx",
            "ppt",
            "pptx",
        }:
            return normalized_type

    filename = source_path.rsplit(
        "/",
        1,
    )[-1]

    if "." not in filename:
        return "file"

    extension = (
        filename.rsplit(
            ".",
            1,
        )[-1]
        .strip()
        .lower()
    )

    extension_aliases = {
        "markdown": "md",
        "text": "txt",
        "jpeg": "image",
        "jpg": "image",
        "png": "image",
        "tiff": "image",
        "webp": "image",
        "htm": "website",
        "html": "website",
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

    if not isinstance(
        source_path,
        str,
    ):
        raise ValueError(
            "Document storage path is missing."
        )

    normalized_path = source_path.strip()

    if not normalized_path:
        raise ValueError(
            "Document storage path is empty."
        )

    if normalized_path.lower() in {
        "null",
        "none",
        "string",
    }:
        raise ValueError(
            "Document storage path is invalid."
        )

    return normalized_path


def _build_pipeline_request(
    document: object,
    source_path: str,
    source_type: str,
) -> KnowledgeIngestionPipelineRequest:
    return KnowledgeIngestionPipelineRequest(
        document_id=str(getattr(document,"id",)
        ),
        knowledge_base_id=str(getattr(document,"knowledge_base_id",)
        ),
        source_type=source_type,
        source_path=source_path,
        source_identifier=source_path,
    )



def _resolve_source_identifier(
    document: object,
) -> str:
    source_type = getattr(
        document,
        "source_type",
        None,
    )

    normalized_source_type = (
        source_type.strip().lower()
        if isinstance(source_type, str)
        else ""
    )

    if normalized_source_type == "website":
        source_uri = getattr(
            document,
            "source_uri",
            None,
        )

        if not isinstance(
            source_uri,
            str,
        ):
            raise ValueError(
                "Website source URI is missing."
            )

        normalized_uri = source_uri.strip()

        if not normalized_uri:
            raise ValueError(
                "Website source URI is empty."
            )

        if not (
            normalized_uri.startswith(
                "http://"
            )
            or normalized_uri.startswith(
                "https://"
            )
        ):
            raise ValueError(
                "Website source URI must use "
                "http or https."
            )

        return normalized_uri

    return _validate_storage_path(
        document,
    )


def run_document_ingestion_task(
    document_id: str,
) -> None:
    from types import SimpleNamespace

    from app.main import app

    request_context = SimpleNamespace(app=app)
    session_factory = app.state.session_factory
    session: Session = session_factory()

    try:
        document_service = get_document_application_service(
            request=request_context,
            session=session,
        )

        document = document_service.get_by_id(
            GetDocumentByIdQuery(
                document_id=document_id,
            )
        )

        document_service.mark_processing(
            MarkDocumentProcessingCommand(
                document_id=document_id,
            )
        )
        session.commit()

        source_identifier = _resolve_source_identifier(
            document,
        )
        source_type = _resolve_source_type(
            document,
            source_identifier,
        )

        ingestion_pipeline = get_knowledge_ingestion_pipeline(
            source_type=source_type,
            request=request_context,
            session=session,
        )

        pipeline_request = _build_pipeline_request(
            document=document,
            source_path=source_identifier,
            source_type=source_type,
        )

        logger.info(
            "Starting background document ingestion",
            extra={
                "document_id": document_id,
                "source_type": source_type,
                "source_path": source_identifier,
            },
        )

        ingestion_pipeline.run(pipeline_request)

        document_service.mark_ready(
            MarkDocumentReadyCommand(
                document_id=document_id,
            )
        )
        session.commit()

        logger.info(
            "Background document ingestion completed",
            extra={
                "document_id": document_id,
                "source_type": source_type,
            },
        )

    except Exception as exc:
        logger.exception(
            "Background document ingestion failed",
            extra={
                "document_id": document_id,
            },
        )

        _safe_rollback(session)
        session.close()

        failed_session: Session | None = None

        try:
            failed_session = session_factory()

            failed_request_context = SimpleNamespace(
                app=app,
            )

            failed_document_service = (
                get_document_application_service(
                    request=failed_request_context,
                    session=failed_session,
                )
            )

            failed_document_service.mark_failed(
                MarkDocumentFailedCommand(
                    document_id=document_id,
                    failure_reason=str(exc),
                )
            )

            failed_session.commit()

        except Exception:
            if failed_session is not None:
                _safe_rollback(failed_session)

            logger.exception(
                "Could not mark document as failed",
                extra={
                    "document_id": document_id,
                },
            )

        finally:
            if failed_session is not None:
                failed_session.close()

        return

    finally:
        try:
            session.close()
        except Exception:
            logger.exception(
                "Could not close ingestion database session.",
                extra={
                    "document_id": document_id,
                },
            )


@router.post(
    "/start",
    response_model=IngestionResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def start_ingestion(
    payload: StartIngestionRequest,
    request: Request,
    document_service: DocumentApplicationService = Depends(get_document_application_service,
),
    session: Session = Depends(get_session),
) -> IngestionResponse:
    processing_document = None
    failure_reason: str | None = None

    try:
        processing_document = document_service.mark_processing(
            MarkDocumentProcessingCommand(
                document_id=payload.document_id,
            )
        )

        source_path = _resolve_source_identifier(
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
            pipeline_factory = get_knowledge_ingestion_pipeline

        ingestion_pipeline = pipeline_factory(
            source_type=source_type,
            request=request,
            session=session,
        )

        pipeline_request = _build_pipeline_request(
            document=processing_document,
            source_path=source_path,
            source_type=source_type,
        )

        ingestion_pipeline.run(
            pipeline_request,
        )

        document_service.mark_ready(
            MarkDocumentReadyCommand(
                document_id=payload.document_id,
            )
        )

        return IngestionResponse(
            document_id=payload.document_id,
            status="ready",
        )

    except Exception as exc:
        failure_reason = str(exc)
        logger.exception(
            "Manual document ingestion failed",
            extra={
                "document_id": payload.document_id,
            },
        )

        try:
            session.rollback()
        except Exception:
            logger.exception(
                "Manual ingestion rollback failed.",
                extra={
                    "document_id": payload.document_id,
                },
            )

        session.close()

        failed_session: Session | None = None

        try:
            failed_session = request.app.state.session_factory()

            failed_document_service = get_document_application_service(
                request=request,
                session=failed_session,
            )

            failed_document_service.mark_failed(
                MarkDocumentFailedCommand(
                    document_id=payload.document_id,
                    failure_reason=failure_reason,
                )
            )

            failed_session.commit()

        except Exception:
            if failed_session is not None:
                try:
                    failed_session.rollback()
                except Exception:
                    logger.exception(
                        "Failed-session rollback also failed.",
                        extra={
                            "document_id": payload.document_id,
                        },
                    )

            logger.exception(
                "Could not mark document as failed",
                extra={
                    "document_id": payload.document_id,
                },
            )

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "code": "document_ingestion_failed",
                "message": "Document ingestion failed.",
            },
        ) from exc