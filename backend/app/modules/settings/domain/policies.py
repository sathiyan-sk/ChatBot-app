from __future__ import annotations

from app.modules.settings.domain.value_objects import PositiveIntegerSetting


def validate_conversation_inactivity_minutes(value: int) -> int:
    return PositiveIntegerSetting(
        value=value,
        min_value=5,
        max_value=10080,
        code="invalid_conversation_inactivity_minutes",
    ).value


def validate_conversation_retention_days(value: int) -> int:
    return PositiveIntegerSetting(
        value=value,
        min_value=1,
        max_value=3650,
        code="invalid_conversation_retention_days",
    ).value


def validate_retrieval_top_k(value: int) -> int:
    return PositiveIntegerSetting(
        value=value,
        min_value=1,
        max_value=50,
        code="invalid_retrieval_top_k",
    ).value