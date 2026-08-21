from __future__ import annotations

from app.infrastructure.db.models.application_model import ApplicationModel
from app.modules.applications.domain.entities import Application


def map_application_model_to_entity(model: ApplicationModel) -> Application:
    raw_allowed_origins = model.allowed_origins or []
    if isinstance(raw_allowed_origins, str):
        allowed_origins = [origin.strip() for origin in raw_allowed_origins.split(",") if origin and origin.strip()]
    else:
        allowed_origins = [origin.strip() for origin in raw_allowed_origins if origin and origin.strip()]

    return Application(
        id=model.id,
        name=model.name,
        slug=model.slug,
        description=model.description,
        client_type=model.client_type,
        allowed_origins=allowed_origins,
        is_active=model.is_active,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )