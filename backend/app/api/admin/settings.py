from __future__ import annotations
from dataclasses import asdict
from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_settings_application_service
from app.api.schemas.settings import (
    CreateSettingsRequest,
    SettingsResponse,
    UpdateSettingsRequest,
)
from app.modules.settings.application.commands import (
    CreateSettingsCommand,
    UpdateSettingsCommand,
)
from app.modules.settings.application.queries import GetSettingsByApplicationQuery
from app.modules.settings.application.services import SettingsApplicationService

router = APIRouter(prefix="/admin/settings", tags=["Admin Settings"])


@router.post("", response_model=SettingsResponse, status_code=status.HTTP_201_CREATED)
def create_settings(
    request: CreateSettingsRequest,
    service: SettingsApplicationService = Depends(get_settings_application_service),
) -> SettingsResponse:
    result = service.create(
        CreateSettingsCommand(
            application_id=request.application_id,
            conversation_inactivity_minutes=request.conversation_inactivity_minutes,
            conversation_retention_days=request.conversation_retention_days,
            retrieval_top_k=request.retrieval_top_k,
            reranker_enabled=request.reranker_enabled,
            citations_enabled=request.citations_enabled,
        )
    )
    return SettingsResponse.model_validate(asdict(result))


@router.get("/by-application/{application_id}", response_model=SettingsResponse)
def get_settings_by_application(
    application_id: str,
    service: SettingsApplicationService = Depends(get_settings_application_service),
) -> SettingsResponse:
    result = service.get_by_application(
        GetSettingsByApplicationQuery(application_id=application_id)
    )
    data = asdict(result)
    data["id"] = str(data["id"])
    data["application_id"] = str(data["application_id"])
    return SettingsResponse.model_validate(data)

@router.put("/by-application/{application_id}", response_model=SettingsResponse)
def update_settings(
    application_id: str,
    request: UpdateSettingsRequest,
    service: SettingsApplicationService = Depends(get_settings_application_service),
) -> SettingsResponse:
    result = service.update(
        UpdateSettingsCommand(
            application_id=application_id,
            conversation_inactivity_minutes=request.conversation_inactivity_minutes,
            conversation_retention_days=request.conversation_retention_days,
            retrieval_top_k=request.retrieval_top_k,
            reranker_enabled=request.reranker_enabled,
            citations_enabled=request.citations_enabled,
        )
    )
    return SettingsResponse.model_validate(asdict(result))