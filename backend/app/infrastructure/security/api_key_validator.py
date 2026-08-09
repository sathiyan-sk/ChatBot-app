from __future__ import annotations

import hashlib
import hmac
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import AuthenticationError
from app.infrastructure.db.models.api_key_model import (
    ApiKeyModel,
)


@dataclass(slots=True)
class ApiKeyValidator:
    session: Session

    def validate_presence(
        self,
        api_key: str | None,
    ) -> str:
        if api_key is None or not api_key.strip():
            raise AuthenticationError(
                "Missing application API key."
            )

        return api_key.strip()

    def is_valid(
        self,
        api_key: str,
    ) -> bool:
        normalized_key = api_key.strip()

        if not normalized_key:
            return False

        # Application creation stores the first 16
        # characters as key_prefix.
        key_prefix = normalized_key[:32]

        statement = (
            select(ApiKeyModel)
            .where(
                ApiKeyModel.key_prefix == key_prefix,
            )
            .where(
                ApiKeyModel.is_active.is_(True),
            )
        )

        candidates = list(
            self.session.scalars(statement)
        )

        actual_hash = hashlib.sha256(
            normalized_key.encode("utf-8")
        ).hexdigest()

        for candidate in candidates:
            if hmac.compare_digest(
                actual_hash,
                candidate.key_hash,
            ):
                return True

        return False