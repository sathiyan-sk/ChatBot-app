from __future__ import annotations

from dataclasses import dataclass

from app.core.exceptions import ApplicationError
from app.modules.widgets.application.commands import CreateWidgetCommand, UpdateWidgetCommand
from app.modules.widgets.application.dto import WidgetDto
from app.modules.widgets.application.queries import GetWidgetByApplicationQuery
from app.modules.widgets.domain.entities import Widget
from app.modules.widgets.domain.policies import (
    normalize_allowed_origins,
    normalize_color_hex,
    normalize_widget_text,
)
from app.modules.widgets.domain.repository_interfaces import WidgetRepositoryInterface
from app.modules.widgets.domain.value_objects import WidgetPosition, WidgetThemeMode


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
            display_name=normalize_widget_text(command.display_name, field_name="display_name", max_length=120),
            welcome_message=normalize_widget_text(command.welcome_message, field_name="welcome_message", max_length=1000),
            placeholder_text=normalize_widget_text(command.placeholder_text, field_name="placeholder_text", max_length=255),
            theme_mode=WidgetThemeMode(command.theme_mode).value,
            primary_color=normalize_color_hex(command.primary_color),
            position=WidgetPosition(command.position).value,
            is_enabled=command.is_enabled,
            allowed_origins=normalize_allowed_origins(command.allowed_origins),
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
            theme_mode=WidgetThemeMode(command.theme_mode).value,
            primary_color=normalize_color_hex(command.primary_color),
            position=WidgetPosition(command.position).value,
            is_enabled=command.is_enabled,
            allowed_origins=normalize_allowed_origins(command.allowed_origins),
        )
        return self._to_dto(updated)

    def _to_dto(self, widget: Widget) -> WidgetDto:
        return WidgetDto(
            id=widget.id,
            application_id=widget.application_id,
            display_name=widget.display_name,
            welcome_message=widget.welcome_message,
            placeholder_text=widget.placeholder_text,
            theme_mode=widget.theme_mode,
            primary_color=widget.primary_color,
            position=widget.position,
            is_enabled=widget.is_enabled,
            allowed_origins=widget.allowed_origins,
            created_at=widget.created_at,
            updated_at=widget.updated_at,
        )