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