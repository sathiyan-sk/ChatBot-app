from __future__ import annotations

from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_knowledge_base_application_service,
    get_session,
)
from app.api.schemas.knowledge_bases import (
    CreateKnowledgeBaseRequest,
    KnowledgeBaseResponse,
    UpdateKnowledgeBaseRequest,
)
from app.modules.knowledge_bases.application.commands import (
    ActivateKnowledgeBaseCommand,
    CreateKnowledgeBaseCommand,
    DeactivateKnowledgeBaseCommand,
    UpdateKnowledgeBaseCommand,
)
from app.modules.knowledge_bases.application.queries import (
    GetKnowledgeBaseByApplicationIdQuery,
    GetKnowledgeBaseByIdQuery,
    ListKnowledgeBasesQuery,
)
from app.modules.knowledge_bases.application.services import (
    KnowledgeBaseApplicationService,
)
from app.modules.knowledge_bases.infrastructure.repositories import (
    SqlAlchemyKnowledgeBaseRepository,
)


router = APIRouter(
    prefix="/admin/knowledge-bases",
    tags=["Admin Knowledge Bases"],
)


def _build_service(
    session: Session,
) -> KnowledgeBaseApplicationService:
    return KnowledgeBaseApplicationService(
        knowledge_base_repository=(
            SqlAlchemyKnowledgeBaseRepository(
                session=session,
            )
        ),
    )


@router.post(
    "",
    response_model=KnowledgeBaseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_knowledge_base(
    request: CreateKnowledgeBaseRequest,
    session: Session = Depends(get_session),
) -> KnowledgeBaseResponse:
    service = _build_service(session)

    result = service.create(
        CreateKnowledgeBaseCommand(
            application_id=request.application_id,
            name=request.name,
            status=request.status,
        ),
    )

    return KnowledgeBaseResponse.model_validate(
        result,
        from_attributes=True,
    )


@router.get(
    "/by-application/{application_id}",
    response_model=KnowledgeBaseResponse,
)
def get_knowledge_base_by_application_id(
    application_id: UUID,
    service: KnowledgeBaseApplicationService = Depends(
        get_knowledge_base_application_service,
    ),
) -> KnowledgeBaseResponse:
    result = service.get_by_application_id(
        GetKnowledgeBaseByApplicationIdQuery(
            application_id=application_id,
        ),
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge base not found.",
        )

    return KnowledgeBaseResponse.model_validate(
        result,
        from_attributes=True,
    )


@router.get(
    "",
    response_model=list[KnowledgeBaseResponse],
)
def list_knowledge_bases(
    status_value: str | None = Query(
        default=None,
        alias="status",
    ),
    service: KnowledgeBaseApplicationService = Depends(
        get_knowledge_base_application_service,
    ),
) -> list[KnowledgeBaseResponse]:
    results = service.list(
        ListKnowledgeBasesQuery(
            status=status_value,
        ),
    )

    return [
        KnowledgeBaseResponse.model_validate(
            item,
            from_attributes=True,
        )
        for item in results
    ]


@router.get(
    "/{knowledge_base_id}",
    response_model=KnowledgeBaseResponse,
)
def get_knowledge_base_by_id(
    knowledge_base_id: UUID,
    service: KnowledgeBaseApplicationService = Depends(
        get_knowledge_base_application_service,
    ),
) -> KnowledgeBaseResponse:
    result = service.get_by_id(
        GetKnowledgeBaseByIdQuery(
            knowledge_base_id=knowledge_base_id,
        ),
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge base not found.",
        )

    return KnowledgeBaseResponse.model_validate(
        result,
        from_attributes=True,
    )


@router.put(
    "/{knowledge_base_id}",
    response_model=KnowledgeBaseResponse,
)
def update_knowledge_base(
    knowledge_base_id: str,
    request: UpdateKnowledgeBaseRequest,
    session: Session = Depends(get_session),
) -> KnowledgeBaseResponse:
    service = _build_service(session)

    result = service.update(
        UpdateKnowledgeBaseCommand(
            knowledge_base_id=knowledge_base_id,
            name=request.name,
            status=request.status,
        ),
    )

    return KnowledgeBaseResponse.model_validate(
        result,
        from_attributes=True,
    )


@router.post(
    "/{knowledge_base_id}/activate",
    response_model=KnowledgeBaseResponse,
)
def activate_knowledge_base(
    knowledge_base_id: str,
    session: Session = Depends(get_session),
) -> KnowledgeBaseResponse:
    service = _build_service(session)

    result = service.activate(
        ActivateKnowledgeBaseCommand(
            knowledge_base_id=knowledge_base_id,
        ),
    )

    return KnowledgeBaseResponse.model_validate(
        result,
        from_attributes=True,
    )


@router.post(
    "/{knowledge_base_id}/deactivate",
    response_model=KnowledgeBaseResponse,
)
def deactivate_knowledge_base(
    knowledge_base_id: str,
    session: Session = Depends(get_session),
) -> KnowledgeBaseResponse:
    service = _build_service(session)

    result = service.deactivate(
        DeactivateKnowledgeBaseCommand(
            knowledge_base_id=knowledge_base_id,
        ),
    )

    return KnowledgeBaseResponse.model_validate(
        result,
        from_attributes=True,
    )