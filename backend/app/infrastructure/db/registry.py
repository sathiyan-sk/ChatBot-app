from __future__ import annotations

from app.infrastructure.db.base import Base

# Import all SQLAlchemy models here so Base.metadata is fully populated.
from app.infrastructure.db.models import (  # noqa: F401
    ApiKeyModel,
    ApplicationModel,
    ConversationModel,
    DocumentModel,
    KnowledgeBaseModel,
    MessageModel,
    SettingsModel,
    WidgetModel,
)


def import_model_registry() -> type[Base]:
    return Base