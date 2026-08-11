from __future__ import annotations

from app.infrastructure.db.models.knowledge_base_model import (
    KnowledgeBaseModel,
)
from app.modules.knowledge_bases.domain.entities import (
    KnowledgeBase,
)


def map_knowledge_base_model_to_entity(
    model: KnowledgeBaseModel,
) -> KnowledgeBase:
    return KnowledgeBase(
        id=model.id,
        application_id=model.application_id,
        name=model.name,
        status=model.status,
        is_active=model.is_active,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )