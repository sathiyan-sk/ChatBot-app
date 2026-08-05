from __future__ import annotations

from dataclasses import dataclass

from app.core.exceptions import ApplicationError


@dataclass(frozen=True, slots=True)
class WidgetThemeMode:
    value: str

    _ALLOWED_VALUES = {"light", "dark", "system"}

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()
        if normalized not in self._ALLOWED_VALUES:
            raise ApplicationError(
                message="Invalid widget theme mode.",
                code="invalid_widget_theme_mode",
                status_code=400,
            )
        object.__setattr__(self, "value", normalized)


@dataclass(frozen=True, slots=True)
class WidgetPosition:
    value: str

    _ALLOWED_VALUES = {"bottom-right", "bottom-left"}

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()
        if normalized not in self._ALLOWED_VALUES:
            raise ApplicationError(
                message="Invalid widget position.",
                code="invalid_widget_position",
                status_code=400,
            )
        object.__setattr__(self, "value", normalized)