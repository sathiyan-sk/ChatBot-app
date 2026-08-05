from __future__ import annotations

from dataclasses import dataclass

from app.core.exceptions import ApplicationError


@dataclass(frozen=True, slots=True)
class PositiveIntegerSetting:
    value: int
    min_value: int
    max_value: int
    code: str

    def __post_init__(self) -> None:
        if self.value < self.min_value or self.value > self.max_value:
            raise ApplicationError(
                message="Setting value is out of allowed range.",
                code=self.code,
                status_code=400,
            )