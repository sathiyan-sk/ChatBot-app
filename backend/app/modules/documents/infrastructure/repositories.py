from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.documents.domain.entities import Document
from app.modules.documents.domain.repository_interfaces import DocumentRepositoryInterface
from app.modules.documents.infrastructure.mappers import map_document_model_to_entity
from app.modules.documents.infrastructure.orm_models import DocumentModel


class SqlAlchemyDocumentRepository(DocumentRepositoryInterface):
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(
        self,
        *,
        knowledge_base_id: str,
        title: str,
        description: str | None,
        source_type: str,
        source_uri: str,
        status: str,
    ) -> Document:
        model = DocumentModel(
            knowledge_base_id=knowledge_base_id,
            title=title,
            description=description,
            source_type=source_type,
            source_uri=source_uri,
            status=status,
            failure_reason=None,
        )
        self._session.add(model)
        self._session.flush()
        self._session.refresh(model)
        return map_document_model_to_entity(model)

    def get_by_id(self, document_id: str) -> Document | None:
        statement = select(DocumentModel).where(DocumentModel.id == document_id)
        model = self._session.execute(statement).scalar_one_or_none()
        return None if model is None else map_document_model_to_entity(model)

    def list_by_knowledge_base_id(
        self,
        *,
        knowledge_base_id: str,
        status: str | None = None,
    ) -> list[Document]:
        statement = (
            select(DocumentModel)
            .where(DocumentModel.knowledge_base_id == knowledge_base_id)
            .order_by(DocumentModel.created_at.desc())
        )
        if status is not None:
            statement = statement.where(DocumentModel.status == status)

        models = self._session.execute(statement).scalars().all()
        return [map_document_model_to_entity(model) for model in models]

    def list_by_status(self, *, status: str) -> list[Document]:
        statement = (
            select(DocumentModel)
            .where(DocumentModel.status == status)
            .order_by(DocumentModel.created_at.desc())
        )
        models = self._session.execute(statement).scalars().all()
        return [map_document_model_to_entity(model) for model in models]

    def update(
        self,
        *,
        document_id: str,
        title: str,
        description: str | None,
        status: str,
        failure_reason: str | None,
    ) -> Document:
        statement = select(DocumentModel).where(DocumentModel.id == document_id)
        model = self._session.execute(statement).scalar_one()

        model.title = title
        model.description = description
        model.status = status
        model.failure_reason = failure_reason

        self._session.flush()
        self._session.refresh(model)
        return map_document_model_to_entity(model)