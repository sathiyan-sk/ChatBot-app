from __future__ import annotations

from abc import ABC, abstractmethod

from app.modules.widgets.domain.entities import Widget


class WidgetRepositoryInterface(ABC):
    @abstractmethod
    def create(
        self,
        *,
        application_id: str,
        display_name: str,
        welcome_message: str,
        placeholder_text: str,
        theme_mode: str,
        primary_color: str,
        position: str,
        is_enabled: bool,
        allowed_origins: list[str],
    ) -> Widget:
        raise NotImplementedError

    @abstractmethod
    def get_by_application_id(self, application_id: str) -> Widget | None:
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        *,
        widget_id: str,
        display_name: str,
        welcome_message: str,
        placeholder_text: str,
        theme_mode: str,
        primary_color: str,
        position: str,
        is_enabled: bool,
        allowed_origins: list[str],
    ) -> Widget:
        raise NotImplementedError