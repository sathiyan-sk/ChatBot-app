from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class CreateWidgetRequest(BaseModel):
    application_id: str = Field(..., min_length=1)
    display_name: str = Field(..., min_length=1, max_length=120)
    welcome_message: str = Field(..., min_length=1, max_length=1000)
    placeholder_text: str = Field(..., min_length=1, max_length=255)
    theme_mode: str = Field(default="system", min_length=1)
    primary_color: str = Field(..., min_length=7, max_length=7)
    position: str = Field(default="bottom-right", min_length=1)
    is_enabled: bool = True
    allowed_origins: list[str] = Field(default_factory=list)


class UpdateWidgetRequest(BaseModel):
    display_name: str = Field(..., min_length=1, max_length=120)
    welcome_message: str = Field(..., min_length=1, max_length=1000)
    placeholder_text: str = Field(..., min_length=1, max_length=255)
    theme_mode: str = Field(..., min_length=1)
    primary_color: str = Field(..., min_length=7, max_length=7)
    position: str = Field(..., min_length=1)
    is_enabled: bool
    allowed_origins: list[str] = Field(default_factory=list)


class WidgetResponse(BaseModel):
    id: str
    application_id: str
    display_name: str
    welcome_message: str
    placeholder_text: str
    theme_mode: str
    primary_color: str
    position: str
    is_enabled: bool
    allowed_origins: list[str]
    created_at: datetime
    updated_at: datetime