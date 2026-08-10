from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


class CreateWidgetRequest(BaseModel):
    application_id: str = Field(..., min_length=1)
    display_name: str = Field(..., min_length=1, max_length=150)
    theme: str = Field(default="light", min_length=1, max_length=50)
    launcher_label: str | None = Field(default=None, max_length=100)
    welcome_message: str | None = Field(default=None, max_length=4000)
    placeholder_text: str | None = Field(default=None, max_length=255)
    is_enabled: bool = True


class UpdateWidgetRequest(BaseModel):
    display_name: str = Field(..., min_length=1, max_length=150)
    theme: str = Field(..., min_length=1, max_length=50)
    launcher_label: str | None = Field(default=None, max_length=100)
    welcome_message: str | None = Field(default=None, max_length=4000)
    placeholder_text: str | None = Field(default=None, max_length=255)
    is_enabled: bool


class WidgetResponse(BaseModel):
    id: str
    application_id: str
    display_name: str
    theme: str
    launcher_label: str | None
    welcome_message: str | None
    placeholder_text: str | None
    is_enabled: bool
    created_at: datetime
    updated_at: datetime