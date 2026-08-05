from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.knowledge_bases.domain.entities import KnowledgeBase
from app.modules.knowledge_bases.domain.repository_interfaces import KnowledgeBaseRepositoryInterface
from app.modules.knowledge_bases.infrastructure.mappers import map_knowledge_base_model_to_entity
from app.modules.knowledge_bases.infrastructure.orm_models import KnowledgeBaseModel


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
            description=description,
            status=status,
        )
        self._session.add(model)
        self._session.flush()
        self._session.refresh(model)
        return map_knowledge_base_model_to_entity(model)

    def get_by_id(self, knowledge_base_id: str) -> KnowledgeBase | None:
        statement = select(KnowledgeBaseModel).where(KnowledgeBaseModel.id == knowledge_base_id)
        model = self._session.execute(statement).scalar_one_or_none()
        return None if model is None else map_knowledge_base_model_to_entity(model)

    def get_by_application_id(self, application_id: str) -> KnowledgeBase | None:
        statement = select(KnowledgeBaseModel).where(KnowledgeBaseModel.application_id == application_id)
        model = self._session.execute(statement).scalar_one_or_none()
        return None if model is None else map_knowledge_base_model_to_entity(model)

    def list(self, *, status: str | None = None) -> list[KnowledgeBase]:
        statement = select(KnowledgeBaseModel).order_by(KnowledgeBaseModel.created_at.desc())
        if status is not None:
            statement = statement.where(KnowledgeBaseModel.status == status)

        models = self._session.execute(statement).scalars().all()
        return [map_knowledge_base_model_to_entity(model) for model in models]

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
        model.description = description
        model.status = status

        self._session.flush()
        self._session.refresh(model)
        return map_knowledge_base_model_to_entity(model)