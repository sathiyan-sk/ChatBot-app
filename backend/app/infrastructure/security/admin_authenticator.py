from __future__ import annotations


class AdminAuthenticator:
    def is_valid(self, authorization_header: str) -> bool:
        token = authorization_header.strip()
        return bool(token and token.lower().startswith("bearer "))