from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infrastructure.db.models.knowledge_base_model import KnowledgeBaseModel
from app.modules.knowledge_bases.domain.entities import KnowledgeBase
from app.modules.knowledge_bases.domain.repository_interfaces import KnowledgeBaseRepositoryInterface


def _to_knowledge_base_entity(model: KnowledgeBaseModel) -> KnowledgeBase:
    return KnowledgeBase(
        id=model.id,
        application_id=model.application_id,
        name=model.name,
        description=None,
        status=model.status,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


class SqlAlchemyKnowledgeBaseRepository(KnowledgeBaseRepositoryInterface):
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(
        self,
        *,
        application_id: str,
        name: str,
        description: str | None,
        status: str,
    ) -> KnowledgeBase:
        model = KnowledgeBaseModel(
            application_id=application_id,
            name=name,
            status=status,
        )
        self._session.add(model)
        self._session.flush()
        self._session.refresh(model)
        return _to_knowledge_base_entity(model)

    def get_by_id(self, knowledge_base_id: str) -> KnowledgeBase | None:
        statement = select(KnowledgeBaseModel).where(KnowledgeBaseModel.id == knowledge_base_id)
        model = self._session.execute(statement).scalar_one_or_none()
        if model is None:
            return None
        return _to_knowledge_base_entity(model)

    def get_by_application_id(self, application_id: str) -> KnowledgeBase | None:
        statement = select(KnowledgeBaseModel).where(KnowledgeBaseModel.application_id == application_id)
        model = self._session.execute(statement).scalar_one_or_none()
        if model is None:
            return None
        return _to_knowledge_base_entity(model)

    def list(self, *, status: str | None = None) -> list[KnowledgeBase]:
        statement = select(KnowledgeBaseModel).order_by(KnowledgeBaseModel.created_at.desc())
        if status is not None:
            statement = statement.where(KnowledgeBaseModel.status == status)
        models = self._session.execute(statement).scalars().all()
        return [_to_knowledge_base_entity(item) for item in models]

    def update(
        self,
        *,
        knowledge_base_id: str,
        name: str,
        description: str | None,
        status: str,
    ) -> KnowledgeBase:
        statement = select(KnowledgeBaseModel).where(KnowledgeBaseModel.id == knowledge_base_id)
        model = self._session.execute(statement).scalar_one()
        model.name = name
        model.status = status
        self._session.flush()
        self._session.refresh(model)
        return _to_knowledge_base_entity(model)