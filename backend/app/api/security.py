from __future__ import annotations

from fastapi import Depends, Header, HTTPException, status

from app.infrastructure.security.admin_authenticator import AdminAuthenticator
from app.infrastructure.security.api_key_validator import ApiKeyValidator
from app.infrastructure.security.origin_validator import OriginValidator


def require_admin(
    authorization: str | None = Header(default=None, alias="Authorization"),
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
    x_application_api_key: str | None = Header(default=None, alias="X-Application-Api-Key"),
    validator: ApiKeyValidator = Depends(),
) -> str:
    if not x_application_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Application API key is required.",
        )
    if not validator.is_valid(x_application_api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid application API key.",
        )
    return x_application_api_key


def validate_origin(
    origin: str | None = Header(default=None, alias="Origin"),
    validator: OriginValidator = Depends(),
) -> None:
    if origin and not validator.is_allowed(origin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Origin is not allowed.",
        )