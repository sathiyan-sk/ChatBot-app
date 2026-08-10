from __future__ import annotations

from app.modules.widgets.domain.entities import Widget
from app.modules.widgets.infrastructure.orm_models import WidgetModel


def map_widget_model_to_entity(model: WidgetModel) -> Widget:
    return Widget(
        id=model.id,
        application_id=model.application_id,
        display_name=model.display_name,
        welcome_message=model.welcome_message,
        placeholder_text=model.placeholder_text,
        launcher_label=model.launcher_label,
        theme=model.theme,
        is_enabled=model.is_enabled,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )