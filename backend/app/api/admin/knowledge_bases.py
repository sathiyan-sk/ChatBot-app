from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import get_knowledge_base_application_service
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
from app.modules.knowledge_bases.application.services import KnowledgeBaseApplicationService

router = APIRouter(prefix="/admin/knowledge-bases", tags=["Admin Knowledge Bases"])


@router.post("", response_model=KnowledgeBaseResponse, status_code=status.HTTP_201_CREATED)
def create_knowledge_base(
    request: CreateKnowledgeBaseRequest,
    service: KnowledgeBaseApplicationService = Depends(get_knowledge_base_application_service),
) -> KnowledgeBaseResponse:
    result = service.create(
        CreateKnowledgeBaseCommand(
            application_id=request.application_id,
            name=request.name,
            description=request.description,
            status=request.status,
        )
    )
    return KnowledgeBaseResponse.model_validate(result.__dict__)


@router.get("", response_model=list[KnowledgeBaseResponse])
def list_knowledge_bases(
    status_value: str | None = Query(default=None, alias="status"),
    service: KnowledgeBaseApplicationService = Depends(get_knowledge_base_application_service),
) -> list[KnowledgeBaseResponse]:
    results = service.list(ListKnowledgeBasesQuery(status=status_value))
    return [KnowledgeBaseResponse.model_validate(item.__dict__) for item in results]


@router.get("/{knowledge_base_id}", response_model=KnowledgeBaseResponse)
def get_knowledge_base_by_id(
    knowledge_base_id: str,
    service: KnowledgeBaseApplicationService = Depends(get_knowledge_base_application_service),
) -> KnowledgeBaseResponse:
    result = service.get_by_id(GetKnowledgeBaseByIdQuery(knowledge_base_id=knowledge_base_id))
    return KnowledgeBaseResponse.model_validate(result.__dict__)


@router.get("/by-application/{application_id}", response_model=KnowledgeBaseResponse)
def get_knowledge_base_by_application_id(
    application_id: str,
    service: KnowledgeBaseApplicationService = Depends(get_knowledge_base_application_service),
) -> KnowledgeBaseResponse:
    result = service.get_by_application_id(
        GetKnowledgeBaseByApplicationIdQuery(application_id=application_id)
    )
    return KnowledgeBaseResponse.model_validate(result.__dict__)


@router.put("/{knowledge_base_id}", response_model=KnowledgeBaseResponse)
def update_knowledge_base(
    knowledge_base_id: str,
    request: UpdateKnowledgeBaseRequest,
    service: KnowledgeBaseApplicationService = Depends(get_knowledge_base_application_service),
) -> KnowledgeBaseResponse:
    result = service.update(
        UpdateKnowledgeBaseCommand(
            knowledge_base_id=knowledge_base_id,
            name=request.name,
            description=request.description,
            status=request.status,
        )
    )
    return KnowledgeBaseResponse.model_validate(result.__dict__)


@router.post("/{knowledge_base_id}/activate", response_model=KnowledgeBaseResponse)
def activate_knowledge_base(
    knowledge_base_id: str,
    service: KnowledgeBaseApplicationService = Depends(get_knowledge_base_application_service),
) -> KnowledgeBaseResponse:
    result = service.activate(ActivateKnowledgeBaseCommand(knowledge_base_id=knowledge_base_id))
    return KnowledgeBaseResponse.model_validate(result.__dict__)


@router.post("/{knowledge_base_id}/deactivate", response_model=KnowledgeBaseResponse)
def deactivate_knowledge_base(
    knowledge_base_id: str,
    service: KnowledgeBaseApplicationService = Depends(get_knowledge_base_application_service),
) -> KnowledgeBaseResponse:
    result = service.deactivate(DeactivateKnowledgeBaseCommand(knowledge_base_id=knowledge_base_id))
    return KnowledgeBaseResponse.model_validate(result.__dict__)