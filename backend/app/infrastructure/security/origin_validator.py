from __future__ import annotations


class OriginValidator:
    def is_allowed(
        self,
        origin: str | None,
        allowed_origins: list[str] | tuple[str, ...] | set[str] | None = None,
    ) -> bool:
        value = (origin or "").strip()
        if not value:
            return False

        normalized_origin = self._normalize(value)
        allowed = [
            self._normalize(item)
            for item in (allowed_origins or [])
            if item and item.strip()
        ]

        if not allowed:
            return False

        if normalized_origin == "null":
            return "null" in allowed

        return normalized_origin in allowed

    @staticmethod
    def _normalize(value: str) -> str:
        return value.strip().rstrip("/").lower()