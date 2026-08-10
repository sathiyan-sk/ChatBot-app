from __future__ import annotations

from dataclasses import dataclass

from app.core.exceptions import ApplicationError
from app.modules.widgets.application.commands import CreateWidgetCommand, UpdateWidgetCommand
from app.modules.widgets.application.dto import WidgetDto
from app.modules.widgets.application.queries import GetWidgetByApplicationQuery
from app.modules.widgets.domain.entities import Widget
from app.modules.widgets.domain.policies import (
    normalize_widget_text,
)
from app.modules.widgets.domain.repository_interfaces import WidgetRepositoryInterface
from app.modules.widgets.domain.value_objects import WidgetThemeMode


@dataclass(slots=True)
class WidgetApplicationService:
    widget_repository: WidgetRepositoryInterface

    def create(self, command: CreateWidgetCommand) -> WidgetDto:
        existing = self.widget_repository.get_by_application_id(command.application_id)
        if existing is not None:
            raise ApplicationError(
                message="Widget already exists for application.",
                code="widget_already_exists",
                status_code=409,
            )

        created = self.widget_repository.create(
    application_id=command.application_id,
    display_name=command.display_name,
    theme=command.theme,
    launcher_label=command.launcher_label,
    welcome_message=command.welcome_message,
    placeholder_text=command.placeholder_text,
    is_enabled=command.is_enabled,
        )
        return self._to_dto(created)

    def get_by_application(self, query: GetWidgetByApplicationQuery) -> WidgetDto:
        widget = self.widget_repository.get_by_application_id(query.application_id)
        if widget is None:
            raise ApplicationError(
                message="Widget not found.",
                code="widget_not_found",
                status_code=404,
            )
        return self._to_dto(widget)

    def update(self, command: UpdateWidgetCommand) -> WidgetDto:
        existing = self.widget_repository.get_by_application_id(command.application_id)
        if existing is None:
            raise ApplicationError(
                message="Widget not found.",
                code="widget_not_found",
                status_code=404,
            )

        updated = self.widget_repository.update(
            widget_id=existing.id,
            display_name=normalize_widget_text(command.display_name, field_name="display_name", max_length=120),
            welcome_message=normalize_widget_text(command.welcome_message, field_name="welcome_message", max_length=1000),
            placeholder_text=normalize_widget_text(command.placeholder_text, field_name="placeholder_text", max_length=255),
            theme=WidgetThemeMode(command.theme).value,
            is_enabled=command.is_enabled,
        )
        return self._to_dto(updated)

    def _to_dto(self, widget: Widget) -> WidgetDto:
        return WidgetDto(
            id=widget.id,
            application_id=widget.application_id,
            display_name=widget.display_name,
            welcome_message=widget.welcome_message,
            placeholder_text=widget.placeholder_text,
            theme=widget.theme,
            is_enabled=widget.is_enabled,
            created_at=widget.created_at,
            updated_at=widget.updated_at,
        )