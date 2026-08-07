from __future__ import annotations


class OriginValidator:
    def is_allowed(self, origin: str) -> bool:
        value = origin.strip().lower()
        return bool(value.startswith("http://") or value.startswith("https://"))