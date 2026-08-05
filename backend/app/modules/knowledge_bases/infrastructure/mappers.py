from __future__ import annotations

from app.modules.knowledge_bases.domain.entities import KnowledgeBase
from app.modules.knowledge_bases.infrastructure.orm_models import KnowledgeBaseModel


def map_knowledge_base_model_to_entity(model: KnowledgeBaseModel) -> KnowledgeBase:
    return KnowledgeBase(
        id=model.id,
        application_id=model.application_id,
        name=model.name,
        description=model.description,
        status=model.status,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )