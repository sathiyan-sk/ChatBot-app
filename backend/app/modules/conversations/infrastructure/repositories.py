from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.infrastructure.db.models.conversation_model import ConversationModel
from app.infrastructure.db.models.message_model import MessageModel
from app.modules.conversations.domain.entities import Conversation, Message
from app.modules.conversations.domain.repository_interfaces import (
    ConversationRepositoryInterface,
    MessageRepositoryInterface,
)
from app.modules.conversations.infrastructure.mappers import (
    map_conversation_model_to_entity,
    map_message_model_to_entity,
)


class SqlAlchemyConversationRepository(ConversationRepositoryInterface):
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(
        self,
        *,
        application_id: str,
        conversation_identity: str,
        title: str | None,
        summary: str | None,
        is_active: bool,
    ) -> Conversation:
        model = ConversationModel(
            application_id=application_id,
            conversation_identity=conversation_identity,
            title=title,
            summary=summary,
            is_active=is_active,
        )
        self._session.add(model)
        self._session.flush()
        self._session.refresh(model)
        return map_conversation_model_to_entity(model)

    def get_by_id(self, conversation_id: str) -> Conversation | None:
        statement = select(ConversationModel).where(ConversationModel.id == conversation_id)
        model = self._session.execute(statement).scalar_one_or_none()
        if model is None:
            return None
        return map_conversation_model_to_entity(model)

    def get_active_by_identity(
        self,
        *,
        application_id: str,
        conversation_identity: str,
    ) -> Conversation | None:
        statement = (
            select(ConversationModel)
            .where(ConversationModel.application_id == application_id)
            .where(ConversationModel.conversation_identity == conversation_identity)
            .where(ConversationModel.is_active.is_(True))
            .order_by(ConversationModel.created_at.desc())
        )
        model = self._session.execute(statement).scalar_one_or_none()
        if model is None:
            return None
        return map_conversation_model_to_entity(model)

    def list_by_application_id(self, application_id: str) -> list[Conversation]:
        statement = (
            select(ConversationModel)
            .where(ConversationModel.application_id == application_id)
            .order_by(ConversationModel.created_at.desc())
        )
        models = self._session.execute(statement).scalars().all()
        return [map_conversation_model_to_entity(item) for item in models]

    def list_by_identity(
        self,
        *,
        application_id: str,
        conversation_identity: str,
    ) -> list[Conversation]:
        statement = (
            select(ConversationModel)
            .where(ConversationModel.application_id == application_id)
            .where(ConversationModel.conversation_identity == conversation_identity)
            .order_by(ConversationModel.created_at.desc())
        )
        models = self._session.execute(statement).scalars().all()
        return [map_conversation_model_to_entity(item) for item in models]

    def update(
        self,
        *,
        conversation_id: str,
        title: str | None,
        summary: str | None,
        is_active: bool,
    ) -> Conversation:
        statement = select(ConversationModel).where(ConversationModel.id == conversation_id)
        model = self._session.execute(statement).scalar_one()
        model.title = title
        model.summary = summary
        model.is_active = is_active
        self._session.flush()
        self._session.refresh(model)
        return map_conversation_model_to_entity(model)


class SqlAlchemyMessageRepository(MessageRepositoryInterface):
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(
        self,
        *,
        conversation_id: str,
        role: str,
        content: str,
        sequence_number: int,
        citation_payload: str | None,
    ) -> Message:
        model = MessageModel(
            conversation_id=conversation_id,
            role=role,
            content=content,
            sequence_number=sequence_number,
            citations_json=citation_payload,
            metadata_json=None,
        )
        self._session.add(model)
        self._session.flush()
        self._session.refresh(model)
        return map_message_model_to_entity(model)

    def list_by_conversation_id(self, conversation_id: str) -> list[Message]:
        statement = (
            select(MessageModel)
            .where(MessageModel.conversation_id == conversation_id)
            .order_by(MessageModel.sequence_number.asc())
        )
        models = self._session.execute(statement).scalars().all()
        return [map_message_model_to_entity(item) for item in models]

    def get_latest_sequence_number(self, conversation_id: str) -> int:
        statement = select(func.max(MessageModel.sequence_number)).where(
            MessageModel.conversation_id == conversation_id
        )
        value = self._session.execute(statement).scalar_one_or_none()
        return int(value or 0)