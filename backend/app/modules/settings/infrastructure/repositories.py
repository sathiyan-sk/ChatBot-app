from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.settings.domain.entities import PlatformSettings
from app.modules.settings.domain.repository_interfaces import SettingsRepositoryInterface
from app.modules.settings.infrastructure.mappers import map_settings_model_to_entity
from app.modules.settings.infrastructure.orm_models import SettingsModel


class SqlAlchemySettingsRepository(SettingsRepositoryInterface):
    def __init__(self, session: Session) -> None:
        self._session = session

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
        model = SettingsModel(
            application_id=application_id,
            conversation_inactivity_minutes=conversation_inactivity_minutes,
            conversation_retention_days=conversation_retention_days,
            retrieval_top_k=retrieval_top_k,
            reranker_enabled=reranker_enabled,
            citations_enabled=citations_enabled,
        )
        self._session.add(model)
        self._session.flush()
        self._session.refresh(model)
        return map_settings_model_to_entity(model)

    def get_by_application_id(self, application_id: str) -> PlatformSettings | None:
        statement = select(SettingsModel).where(SettingsModel.application_id == application_id)
        model = self._session.execute(statement).scalar_one_or_none()
        return None if model is None else map_settings_model_to_entity(model)

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
        statement = select(SettingsModel).where(SettingsModel.id == settings_id)
        model = self._session.execute(statement).scalar_one()

        model.conversation_inactivity_minutes = conversation_inactivity_minutes
        model.conversation_retention_days = conversation_retention_days
        model.retrieval_top_k = retrieval_top_k
        model.reranker_enabled = reranker_enabled
        model.citations_enabled = citations_enabled

        self._session.flush()
        self._session.refresh(model)
        return map_settings_model_to_entity(model)