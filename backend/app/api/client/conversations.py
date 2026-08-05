from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_container
from app.api.schemas.conversations import (
    AppendMessageRequest,
    ConversationDetailResponse,
    ConversationResponse,
    MessageResponse,
    ResolveConversationRequest,
)
from app.composition import ApplicationContainer
from app.modules.conversations.application.commands import (
    AppendMessageCommand,
    ResolveConversationCommand,
)
from app.modules.conversations.application.services import ConversationServices
from app.modules.conversations.infrastructure.repositories import (
    ConversationSqlAlchemyRepository,
    MessageSqlAlchemyRepository,
)

router = APIRouter(prefix="/client/conversations", tags=["Client Conversations"])


def _build_conversation_services(container: ApplicationContainer) -> tuple[Session, ConversationServices]:
    session = container.session_factory()
    service = ConversationServices(
        session=session,
        conversation_repository=ConversationSqlAlchemyRepository(session),
        message_repository=MessageSqlAlchemyRepository(session),
    )
    return session, service


@router.post("/resolve", response_model=ConversationResponse, status_code=201)
def resolve_client_conversation(
    payload: ResolveConversationRequest,
    container: ApplicationContainer = Depends(get_container),
) -> ConversationResponse:
    session, service = _build_conversation_services(container)
    try:
        result = service.resolve_active_conversation(
            ResolveConversationCommand(
                application_id=payload.application_id,
                conversation_identity=payload.conversation_identity,
                title=payload.title,
            )
        )
        return ConversationResponse(**result.__dict__)
    finally:
        session.close()


@router.get("/{conversation_id}", response_model=ConversationDetailResponse)
def get_client_conversation_detail(
    conversation_id: str,
    container: ApplicationContainer = Depends(get_container),
) -> ConversationDetailResponse:
    session, service = _build_conversation_services(container)
    try:
        result = service.get_conversation_detail(conversation_id)
        return ConversationDetailResponse(
            conversation=ConversationResponse(**result.conversation.__dict__),
            messages=[MessageResponse(**item.__dict__) for item in result.messages],
        )
    finally:
        session.close()


@router.post("/{conversation_id}/messages", response_model=MessageResponse, status_code=201)
def append_client_message(
    conversation_id: str,
    payload: AppendMessageRequest,
    container: ApplicationContainer = Depends(get_container),
) -> MessageResponse:
    session, service = _build_conversation_services(container)
    try:
        result = service.append_message(
            AppendMessageCommand(
                conversation_id=conversation_id,
                role=payload.role,
                content=payload.content,
                citation_payload=payload.citation_payload,
            )
        )
        return MessageResponse(**result.__dict__)
    finally:
        session.close()