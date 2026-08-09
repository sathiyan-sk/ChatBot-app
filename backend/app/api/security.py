from __future__ import annotations

from fastapi import (
    Depends,
    Header,
    HTTPException,
    status,
)

from app.infrastructure.security.admin_authenticator import (
    AdminAuthenticator,
)
from app.infrastructure.security.origin_validator import (
    OriginValidator,
)
from app.api.dependencies import get_session
from app.infrastructure.security.api_key_validator import (
    ApiKeyValidator,
)
from sqlalchemy.orm import Session


def require_admin(
    authorization: str | None = Header(
        default=None,
        alias="Authorization",
    ),
    authenticator: AdminAuthenticator = Depends(),
) -> None:
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin authorization is required.",
        )

    if not authenticator.is_valid(authorization):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin authorization.",
        )


def require_application_key(
    x_api_key: str | None = Header(
        default=None,
        alias="X-API-Key",
    ),
    session: Session = Depends(get_session),
) -> str:
    if not x_api_key or not x_api_key.strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Application API key is required.",
        )

    validator = ApiKeyValidator(
        session=session,
    )

    normalized_key = x_api_key.strip()

    if not validator.is_valid(x_api_key.strip()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid application API key.",
        )

    return normalized_key


def validate_origin(
    origin: str | None = Header(
        default=None,
        alias="Origin",
    ),
    validator: OriginValidator = Depends(),
) -> None:
    if origin and not validator.is_allowed(origin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Origin is not allowed.",
        )