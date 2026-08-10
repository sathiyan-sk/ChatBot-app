from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_widget_application_service
from app.api.schemas.widgets import (
    CreateWidgetRequest,
    UpdateWidgetRequest,
    WidgetResponse,
)
from app.modules.widgets.application.commands import (
    CreateWidgetCommand,
    UpdateWidgetCommand,
)
from app.modules.widgets.application.queries import GetWidgetByApplicationQuery
from app.modules.widgets.application.services import WidgetApplicationService

router = APIRouter(prefix="/admin/widgets", tags=["Admin Widgets"])


@router.post("", response_model=WidgetResponse, status_code=status.HTTP_201_CREATED)
def create_widget(
    request: CreateWidgetRequest,
    service: WidgetApplicationService = Depends(get_widget_application_service),
) -> WidgetResponse:
    result = service.create(
        CreateWidgetCommand(
            application_id=request.application_id,
            display_name=request.display_name,
            theme=request.theme,
            launcher_label=request.launcher_label,
            welcome_message=request.welcome_message,
            placeholder_text=request.placeholder_text,
            is_enabled=request.is_enabled,
        )
    )
    return WidgetResponse.model_validate(result,from_attributes=True,)


@router.get("/by-application/{application_id}", response_model=WidgetResponse)
def get_widget_by_application(
    application_id: str,
    service: WidgetApplicationService = Depends(get_widget_application_service),
) -> WidgetResponse:
    result = service.get_by_application(
        GetWidgetByApplicationQuery(application_id=application_id)
    )
    return WidgetResponse.model_validate(result.__dict__)


@router.put("/by-application/{application_id}", response_model=WidgetResponse)
def update_widget(
    application_id: str,
    request: UpdateWidgetRequest,
    service: WidgetApplicationService = Depends(get_widget_application_service),
) -> WidgetResponse:
    result = service.update(
        UpdateWidgetCommand(
            application_id=application_id,
            display_name=request.display_name,
            welcome_message=request.welcome_message,
            placeholder_text=request.placeholder_text,
            theme=request.theme,
            primary_color=request.primary_color,
            is_enabled=request.is_enabled,
        )
    )
    return WidgetResponse.model_validate(result.__dict__)