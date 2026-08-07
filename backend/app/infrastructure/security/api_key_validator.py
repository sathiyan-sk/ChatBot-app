from __future__ import annotations


class ApiKeyValidator:
    def is_valid(self, api_key: str) -> bool:
        token = api_key.strip()
        return bool(token and token.startswith("akp_"))