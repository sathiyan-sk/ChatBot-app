from __future__ import annotations

from dataclasses import dataclass

from app.core.exceptions import ApplicationError
from app.modules.settings.application.commands import CreateSettingsCommand, UpdateSettingsCommand
from app.modules.settings.application.dto import SettingsDto
from app.modules.settings.application.queries import GetSettingsByApplicationQuery
from app.modules.settings.domain.entities import PlatformSettings
from app.modules.settings.domain.policies import (
    validate_conversation_inactivity_minutes,
    validate_conversation_retention_days,
    validate_retrieval_top_k,
)
from app.modules.settings.domain.repository_interfaces import SettingsRepositoryInterface


@dataclass(slots=True)
class SettingsApplicationService:
    settings_repository: SettingsRepositoryInterface

    def create(self, command: CreateSettingsCommand) -> SettingsDto:
        existing = self.settings_repository.get_by_application_id(command.application_id)
        if existing is not None:
            raise ApplicationError(
                message="Settings already exist for application.",
                code="settings_already_exist",
                status_code=409,
            )

        created = self.settings_repository.create(
            application_id=command.application_id,
            conversation_inactivity_minutes=validate_conversation_inactivity_minutes(
                command.conversation_inactivity_minutes
            ),
            conversation_retention_days=validate_conversation_retention_days(
                command.conversation_retention_days
            ),
            retrieval_top_k=validate_retrieval_top_k(command.retrieval_top_k),
            reranker_enabled=command.reranker_enabled,
            citations_enabled=command.citations_enabled,
        )
        return self._to_dto(created)

    def get_by_application(self, query: GetSettingsByApplicationQuery) -> SettingsDto:
        settings = self.settings_repository.get_by_application_id(query.application_id)
        if settings is None:
            raise ApplicationError(
                message="Settings not found.",
                code="settings_not_found",
                status_code=404,
            )
        return self._to_dto(settings)

    def update(self, command: UpdateSettingsCommand) -> SettingsDto:
        existing = self.settings_repository.get_by_application_id(command.application_id)
        if existing is None:
            raise ApplicationError(
                message="Settings not found.",
                code="settings_not_found",
                status_code=404,
            )

        updated = self.settings_repository.update(
            settings_id=existing.id,
            conversation_inactivity_minutes=validate_conversation_inactivity_minutes(
                command.conversation_inactivity_minutes
            ),
            conversation_retention_days=validate_conversation_retention_days(
                command.conversation_retention_days
            ),
            retrieval_top_k=validate_retrieval_top_k(command.retrieval_top_k),
            reranker_enabled=command.reranker_enabled,
            citations_enabled=command.citations_enabled,
        )
        return self._to_dto(updated)

    def _to_dto(self, settings: PlatformSettings) -> SettingsDto:
        return SettingsDto(
            id=settings.id,
            application_id=settings.application_id,
            conversation_inactivity_minutes=settings.conversation_inactivity_minutes,
            conversation_retention_days=settings.conversation_retention_days,
            retrieval_top_k=settings.retrieval_top_k,
            reranker_enabled=settings.reranker_enabled,
            citations_enabled=settings.citations_enabled,
            created_at=settings.created_at,
            updated_at=settings.updated_at,
        )