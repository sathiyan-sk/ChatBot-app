from __future__ import annotations

from app.modules.documents.domain.entities import Document
from app.modules.documents.infrastructure.orm_models import DocumentModel


def map_document_model_to_entity(model: DocumentModel) -> Document:
    return Document(
        id=model.id,
        knowledge_base_id=model.knowledge_base_id,
        title=model.title,
        description=model.description,
        source_type=model.source_type,
        source_uri=model.source_uri,
        status=model.status,
        failure_reason=model.failure_reason,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )