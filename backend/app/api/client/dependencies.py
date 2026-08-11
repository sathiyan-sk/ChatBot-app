from __future__ import annotations

from fastapi import (
    Depends,
    Header,
    HTTPException,
    status,
)

from app.api.dependencies import get_container
from app.composition import ApplicationContainer
from app.modules.security.application.services import (
    ClientSecurityServices,
)
from app.modules.security.domain.entities import (
    ClientApplicationContext,
)
from app.modules.security.infrastructure.repositories import (
    ClientSecuritySqlAlchemyRepository,
)
from app.modules.widgets.infrastructure.repositories import (
    SqlAlchemyWidgetRepository,
)


def get_client_application_context(
    x_api_key: str = Header(
        default="",
        alias="X-API-Key",
    ),
    container: ApplicationContainer = Depends(
        get_container,
    ),
) -> ClientApplicationContext:
    normalized_api_key = x_api_key.strip()

    if not normalized_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-API-Key header is required.",
        )

    session = container.session_factory()

    try:
        security_service = ClientSecurityServices(
            client_security_repository=(
                ClientSecuritySqlAlchemyRepository(
                    session=session,
                )
            ),
        )

        return (
            security_service.resolve_application_context(
                normalized_api_key,
            )
        )

    finally:
        session.close()

def get_widget_application_id(
    x_widget_key: str = Header(
        default="",
        alias="X-Widget-Key",
    ),
    container: ApplicationContainer = Depends(
        get_container,
    ),
) -> str:
    normalized_key = x_widget_key.strip()

    if not normalized_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Widget key is required.",
        )

    session = container.session_factory()

    try:
        repository = SqlAlchemyWidgetRepository(
            session=session,
        )

        widget = repository.get_by_public_key(
            normalized_key,
        )

        if widget is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid widget key.",
            )

        if not widget.is_enabled:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Widget is disabled.",
            )

        return str(widget.application_id)

    finally:
        session.close()