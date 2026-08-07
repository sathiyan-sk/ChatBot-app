from __future__ import annotations

from abc import ABC, abstractmethod

from app.modules.settings.domain.entities import PlatformSettings


class SettingsRepositoryInterface(ABC):
    @abstractmethod
    def create(
        self,
        *,
        application_id: str,
        llm_temperature: str,
        max_context_messages: int,
        inactivity_timeout_minutes: int,
        retention_days: int,
        prompt_system_template: str | None,
    ) -> PlatformSettings:
        raise NotImplementedError

    @abstractmethod
    def get_by_application_id(self, application_id: str) -> PlatformSettings | None:
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        *,
        application_id: str,
        llm_temperature: str,
        max_context_messages: int,
        inactivity_timeout_minutes: int,
        retention_days: int,
        prompt_system_template: str | None,
    ) -> PlatformSettings:
        raise NotImplementedError