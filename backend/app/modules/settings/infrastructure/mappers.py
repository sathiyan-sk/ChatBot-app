from __future__ import annotations

from app.modules.settings.domain.entities import PlatformSettings
from app.modules.settings.infrastructure.orm_models import SettingsModel


def map_settings_model_to_entity(model: SettingsModel) -> PlatformSettings:
    return PlatformSettings(
        id=model.id,
        application_id=model.application_id,
        conversation_inactivity_minutes=model.conversation_inactivity_minutes,
        conversation_retention_days=model.conversation_retention_days,
        retrieval_top_k=model.retrieval_top_k,
        reranker_enabled=model.reranker_enabled,
        citations_enabled=model.citations_enabled,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )