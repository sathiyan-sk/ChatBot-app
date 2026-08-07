from __future__ import annotations

from app.infrastructure.db.models.conversation_model import ConversationModel
from app.infrastructure.db.models.message_model import MessageModel
from app.modules.conversations.domain.entities import Conversation, Message


def map_conversation_model_to_entity(model: ConversationModel) -> Conversation:
    return Conversation(
        id=model.id,
        application_id=model.application_id,
        conversation_identity=model.conversation_identity,
        title=model.title,
        summary=model.summary,
        is_active=model.is_active,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def map_message_model_to_entity(model: MessageModel) -> Message:
    return Message(
        id=model.id,
        conversation_id=model.conversation_id,
        role=model.role,
        content=model.content,
        sequence_number=model.sequence_number,
        citation_payload=model.citations_json,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )