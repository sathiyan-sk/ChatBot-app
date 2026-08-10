from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.widgets.domain.entities import Widget
from app.modules.widgets.domain.repository_interfaces import WidgetRepositoryInterface
from app.modules.widgets.infrastructure.mappers import map_widget_model_to_entity
from app.modules.widgets.infrastructure.orm_models import WidgetModel


class SqlAlchemyWidgetRepository(WidgetRepositoryInterface):
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(
        self,
        *,
        application_id: str,
        display_name: str,
        welcome_message: str,
        placeholder_text: str,
        launcher_label: str,
        theme: str| None,
        is_enabled: bool,
    ) -> Widget:
        model = WidgetModel(
            application_id=application_id,
            display_name=display_name,
            welcome_message=welcome_message,
            placeholder_text=placeholder_text,
            launcher_label=launcher_label,
            theme=theme,
            is_enabled=is_enabled,
        )
        self._session.add(model)
        self._session.flush()
        self._session.refresh(model)
        return map_widget_model_to_entity(model)

    def get_by_application_id(self, application_id: str) -> Widget | None:
        statement = select(WidgetModel).where(WidgetModel.application_id == application_id)
        model = self._session.execute(statement).scalar_one_or_none()
        return None if model is None else map_widget_model_to_entity(model)

    def update(
        self,
        *,
        widget_id: str,
        display_name: str,
        welcome_message: str,
        placeholder_text: str,
        theme: str,
        is_enabled: bool,
    ) -> Widget:
        statement = select(WidgetModel).where(WidgetModel.id == widget_id)
        model = self._session.execute(statement).scalar_one()

        model.display_name = display_name
        model.welcome_message = welcome_message
        model.placeholder_text = placeholder_text
        model.theme = theme
        model.is_enabled = is_enabled

        self._session.flush()
        self._session.refresh(model)
        return map_widget_model_to_entity(model)