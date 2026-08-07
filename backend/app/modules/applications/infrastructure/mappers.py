from __future__ import annotations

from app.infrastructure.db.models.application_model import ApplicationModel
from app.modules.applications.domain.entities import Application


def map_application_model_to_entity(model: ApplicationModel) -> Application:
    return Application(
        id=model.id,
        name=model.name,
        slug=model.slug,
        description=model.description,
        client_type=model.client_type,
        allowed_origins=model.allowed_origins,
        is_active=model.is_active,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )