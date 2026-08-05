from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ApplicationError(Exception):
    message: str
    code: str = "application_error"
    status_code: int = 500
    details: dict[str, Any] | None = None

    def __str__(self) -> str:
        return self.message


class ConfigurationError(ApplicationError):
    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(
            message=message,
            code="configuration_error",
            status_code=500,
            details=details,
        )


class InfrastructureError(ApplicationError):
    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(
            message=message,
            code="infrastructure_error",
            status_code=503,
            details=details,
        )


class AuthenticationError(ApplicationError):
    def __init__(self, message: str = "Authentication failed.") -> None:
        super().__init__(
            message=message,
            code="authentication_error",
            status_code=401,
        )


class AuthorizationError(ApplicationError):
    def __init__(self, message: str = "Access denied.") -> None:
        super().__init__(
            message=message,
            code="authorization_error",
            status_code=403,
        )