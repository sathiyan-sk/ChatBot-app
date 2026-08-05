from __future__ import annotations

from abc import ABC, abstractmethod

from app.modules.settings.domain.entities import PlatformSettings


class SettingsRepositoryInterface(ABC):
    @abstractmethod
    def create(
        self,
        *,
        application_id: str,
        conversation_inactivity_minutes: int,
        conversation_retention_days: int,
        retrieval_top_k: int,
        reranker_enabled: bool,
        citations_enabled: bool,
    ) -> PlatformSettings:
        raise NotImplementedError

    @abstractmethod
    def get_by_application_id(self, application_id: str) -> PlatformSettings | None:
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        *,
        settings_id: str,
        conversation_inactivity_minutes: int,
        conversation_retention_days: int,
        retrieval_top_k: int,
        reranker_enabled: bool,
        citations_enabled: bool,
    ) -> PlatformSettings:
        raise NotImplementedError