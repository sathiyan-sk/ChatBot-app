from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infrastructure.db.models.knowledge_base_model import (
    KnowledgeBaseModel,
)
from app.modules.knowledge_bases.domain.entities import (
    KnowledgeBase,
)
from app.modules.knowledge_bases.domain.repository_interfaces import (
    KnowledgeBaseRepositoryInterface,
)


class SqlAlchemyKnowledgeBaseRepository(
    KnowledgeBaseRepositoryInterface,
):
    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def get_by_application_id(
        self,
        application_id: UUID | str,
    ) -> KnowledgeBase | None:
        statement = select(
            KnowledgeBaseModel,
        ).where(
            KnowledgeBaseModel.application_id
            == str(application_id),
        )

        model = self._session.execute(
            statement,
        ).scalar_one_or_none()

        if model is None:
            return None

        return self._to_entity(model)

    def get_by_id(
        self,
        knowledge_base_id: UUID | str,
    ) -> KnowledgeBase | None:
        statement = select(
            KnowledgeBaseModel,
        ).where(
            KnowledgeBaseModel.id
            == str(knowledge_base_id),
        )

        model = self._session.execute(
            statement,
        ).scalar_one_or_none()

        if model is None:
            return None

        return self._to_entity(model)

    def get_by_slug(
        self,
        slug: str,
    ) -> KnowledgeBase | None:
        statement = select(
            KnowledgeBaseModel,
        ).where(
            KnowledgeBaseModel.slug == slug,
        )

        model = self._session.execute(
            statement,
        ).scalar_one_or_none()

        if model is None:
            return None

        return self._to_entity(model)

    def list(
        self,
        application_id: UUID | str | None = None,
        status: str | None = None,
    ) -> list[KnowledgeBase]:
        statement = select(
            KnowledgeBaseModel,
        )

        if application_id is not None:
            statement = statement.where(
                KnowledgeBaseModel.application_id
                == str(application_id),
            )

        if status is not None:
            statement = statement.where(
                KnowledgeBaseModel.status == status,
            )

        statement = statement.order_by(
            KnowledgeBaseModel.created_at.desc(),
        )

        models = self._session.execute(
            statement,
        ).scalars().all()

        return [
            self._to_entity(model)
            for model in models
        ]

    def update(
        self,
        knowledge_base: KnowledgeBase,
    ) -> KnowledgeBase:
        statement = select(
            KnowledgeBaseModel,
        ).where(
            KnowledgeBaseModel.id
            == str(knowledge_base.id),
        )

        model = self._session.execute(
            statement,
        ).scalar_one_or_none()

        if model is None:
            raise LookupError(
                "Knowledge base not found.",
            )

        model.name = knowledge_base.name
        model.status = knowledge_base.status
        model.is_active = knowledge_base.is_active

        self._session.flush()
        self._session.refresh(model)

        return self._to_entity(model)

    @staticmethod
    def _to_entity(
        model: KnowledgeBaseModel,
    ) -> KnowledgeBase:
        return KnowledgeBase(
            id=model.id,
            application_id=model.application_id,
            name=model.name,
            slug=model.slug,
            status=model.status,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )