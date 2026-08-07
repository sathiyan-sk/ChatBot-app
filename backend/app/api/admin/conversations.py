from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_conversation_application_service, get_session
from app.api.schemas.conversations import (
    AppendMessageRequest,
    ConversationDetailResponse,
    ConversationResponse,
    MessageResponse,
    ResolveConversationRequest,
    UpdateConversationRequest,
)
from app.modules.conversations.application.commands import (
    AppendMessageCommand,
    ResolveConversationCommand,
    UpdateConversationCommand,
)
from app.modules.conversations.application.queries import GetConversationDetailQuery
from app.modules.conversations.application.services import ConversationApplicationService

router = APIRouter(prefix="/admin/conversations", tags=["Admin Conversations"])


@router.post("/resolve", response_model=ConversationResponse, status_code=201)
def resolve_conversation(
    payload: ResolveConversationRequest,
    service: ConversationApplicationService = Depends(get_conversation_application_service),
) -> ConversationResponse:
    result = service.resolve_conversation(
        ResolveConversationCommand(
            application_id=payload.application_id,
            conversation_identity=payload.conversation_identity,
            title=payload.title,
        )
    )
    return ConversationResponse.model_validate(result.__dict__)


@router.get("/application/{application_id}", response_model=list[ConversationResponse])
def list_application_conversations(
    application_id: str,
    service: ConversationApplicationService = Depends(get_conversation_application_service),
) -> list[ConversationResponse]:
    result = service.list_application_conversations(
        query=type("Query", (), {"application_id": application_id})()
    )
    return [ConversationResponse.model_validate(item.__dict__) for item in result]


@router.get("/{conversation_id}", response_model=ConversationDetailResponse)
def get_conversation_detail(
    conversation_id: str,
    service: ConversationApplicationService = Depends(get_conversation_application_service),
) -> ConversationDetailResponse:
    result = service.get_conversation_detail(GetConversationDetailQuery(conversation_id=conversation_id))
    return ConversationDetailResponse(
        conversation=ConversationResponse.model_validate(result.conversation.__dict__),
        messages=[MessageResponse.model_validate(item.__dict__) for item in result.messages],
    )


@router.put("/{conversation_id}", response_model=ConversationResponse)
def update_conversation(
    conversation_id: str,
    payload: UpdateConversationRequest,
    service: ConversationApplicationService = Depends(get_conversation_application_service),
) -> ConversationResponse:
    result = service.update_conversation(
        UpdateConversationCommand(
            conversation_id=conversation_id,
            title=payload.title,
            summary=payload.summary,
            is_active=payload.is_active,
        )
    )
    return ConversationResponse.model_validate(result.__dict__)


@router.delete("/{conversation_id}", response_model=ConversationResponse)
def close_conversation(
    conversation_id: str,
    service: ConversationApplicationService = Depends(get_conversation_application_service),
) -> ConversationResponse:
    result = service.update_conversation(
        UpdateConversationCommand(
            conversation_id=conversation_id,
            title=None,
            summary=None,
            is_active=False,
        )
    )
    return ConversationResponse.model_validate(result.__dict__)


@router.post("/{conversation_id}/messages", response_model=MessageResponse, status_code=201)
def append_message(
    conversation_id: str,
    payload: AppendMessageRequest,
    service: ConversationApplicationService = Depends(get_conversation_application_service),
) -> MessageResponse:
    result = service.append_message(
        AppendMessageCommand(
            conversation_id=conversation_id,
            role=payload.role,
            content=payload.content,
            citation_payload=payload.citation_payload,
        )
    )
    return MessageResponse.model_validate(result.__dict__)