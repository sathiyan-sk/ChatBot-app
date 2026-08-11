from __future__ import annotations

from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    status,
    Response,
)

from app.api.dependencies import (
    get_widget_application_service,
    require_admin,
)
from app.api.schemas.widgets import (
    CreateWidgetRequest,
    UpdateWidgetRequest,
    WidgetResponse,
)
from app.modules.widgets.application.commands import (
    CreateWidgetCommand,
    UpdateWidgetCommand,
)
from app.modules.widgets.application.services import (
    WidgetApplicationService,
)


router = APIRouter(
    prefix="/admin/widgets",
    tags=["Admin Widgets"],
    dependencies=[
        Depends(require_admin),
    ],
)


@router.post(
    "",
    response_model=WidgetResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_widget(
    request: CreateWidgetRequest,
    service: WidgetApplicationService = Depends(
        get_widget_application_service,
    ),
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

    return WidgetResponse.model_validate(
        result,
        from_attributes=True,
    )


@router.get(
    "/application/{application_id}",
    response_model=WidgetResponse,
)
def get_widget_by_application(
    application_id: UUID,
    service: WidgetApplicationService = Depends(
        get_widget_application_service,
    ),
) -> WidgetResponse:
    result = service.get_by_application_id(
        application_id,
    )

    return WidgetResponse.model_validate(
        result,
        from_attributes=True,
    )


@router.get(
    "/{widget_id}",
    response_model=WidgetResponse,
)
def get_widget(
    widget_id: UUID,
    service: WidgetApplicationService = Depends(
        get_widget_application_service,
    ),
) -> WidgetResponse:
    result = service.get_by_id(widget_id)

    return WidgetResponse.model_validate(
        result,
        from_attributes=True,
    )


@router.put(
    "/{widget_id}",
    response_model=WidgetResponse,
)
def update_widget(
    widget_id: UUID,
    request: UpdateWidgetRequest,
    service: WidgetApplicationService = Depends(
        get_widget_application_service,
    ),
) -> WidgetResponse:
    result = service.update(
        UpdateWidgetCommand(
            widget_id=widget_id,
            display_name=request.display_name,
            theme=request.theme,
            launcher_label=request.launcher_label,
            welcome_message=request.welcome_message,
            placeholder_text=request.placeholder_text,
            is_enabled=request.is_enabled,
        )
    )

    return WidgetResponse.model_validate(
        result,
        from_attributes=True,
    )




@router.delete(
    "/{widget_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
def delete_widget(
    widget_id: UUID,
    service: WidgetApplicationService = Depends(
        get_widget_application_service,
    ),
) -> Response:
    service.delete(widget_id)

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )