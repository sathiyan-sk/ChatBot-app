from __future__ import annotations

import hashlib

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infrastructure.db.models.api_key_model import ApiKeyModel
from app.infrastructure.db.models.application_model import ApplicationModel
from app.modules.security.domain.entities import ClientApplicationContext
from app.modules.security.domain.repository_interfaces import ClientSecurityRepository


class ClientSecuritySqlAlchemyRepository(ClientSecurityRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def resolve_application_context_by_api_key(self, raw_api_key: str) -> ClientApplicationContext | None:
        key_hash = hashlib.sha256(raw_api_key.encode("utf-8")).hexdigest()

        statement = (
            select(ApiKeyModel, ApplicationModel)
            .join(ApplicationModel, ApplicationModel.id == ApiKeyModel.application_id)
            .where(ApiKeyModel.key_hash == key_hash)
            .where(ApiKeyModel.is_active.is_(True))
            .where(ApplicationModel.is_active.is_(True))
        )

        row = self._session.execute(statement).first()
        if row is None:
            return None

        api_key_model, application_model = row

        return ClientApplicationContext(
            application_id=application_model.id,
            application_slug=application_model.slug,
            client_type=application_model.client_type,
            api_key_prefix=api_key_model.key_prefix,
        )