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
        theme: str,
        launcher_label: str | None,
        welcome_message: str | None,
        placeholder_text: str | None,
        is_enabled: bool,
    ) -> Widget:
        raise NotImplementedError

    @abstractmethod
    def get_by_application_id(self, application_id: str) -> Widget | None:
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        *,
        application_id: str,
        display_name: str,
        theme: str,
        launcher_label: str | None,
        welcome_message: str | None,
        placeholder_text: str | None,
        is_enabled: bool,
    ) -> Widget:
        raise NotImplementedError