from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.dependencies import (
    get_conversation_application_service,
)
from app.api.schemas.conversations import (
    AppendMessageRequest,
    ConversationDetailResponse,
    ConversationResponse,
    MessageResponse,
    ResolveConversationRequest,
)
from app.modules.conversations.application.commands import (
    AppendMessageCommand,
    ResolveConversationCommand,
)
from app.modules.conversations.application.queries import (
    GetConversationDetailQuery,
)
from app.modules.conversations.application.services import (
    ConversationApplicationService,
)


router = APIRouter(
    prefix="/client/conversations",
    tags=["Client Conversations"],
)


@router.post(
    "/resolve",
    response_model=ConversationResponse,
    status_code=201,
)
def resolve_client_conversation(
    payload: ResolveConversationRequest,
    service: ConversationApplicationService = Depends(
        get_conversation_application_service,
    ),
) -> ConversationResponse:
    result = service.resolve_conversation(
        ResolveConversationCommand(
            application_id=payload.application_id,
            conversation_identity=(
                payload.conversation_identity
            ),
            title=payload.title,
        ),
    )

    return ConversationResponse.model_validate(
        result,
        from_attributes=True,
    )


@router.get(
    "/{conversation_id}",
    response_model=ConversationDetailResponse,
)
def get_client_conversation_detail(
    conversation_id: str,
    service: ConversationApplicationService = Depends(
        get_conversation_application_service,
    ),
) -> ConversationDetailResponse:
    result = service.get_conversation_detail(
        GetConversationDetailQuery(
            conversation_id=conversation_id,
        ),
    )

    return ConversationDetailResponse(
        conversation=ConversationResponse.model_validate(
            result.conversation,
            from_attributes=True,
        ),
        messages=[
            MessageResponse.model_validate(
                message,
                from_attributes=True,
            )
            for message in result.messages
        ],
    )


@router.post(
    "/{conversation_id}/messages",
    response_model=MessageResponse,
    status_code=201,
)
def append_client_message(
    conversation_id: str,
    payload: AppendMessageRequest,
    service: ConversationApplicationService = Depends(
        get_conversation_application_service,
    ),
) -> MessageResponse:
    result = service.append_message(
        AppendMessageCommand(
            conversation_id=conversation_id,
            role=payload.role,
            content=payload.content,
            citation_payload=payload.citation_payload,
        ),
    )

    return MessageResponse.model_validate(
        result,
        from_attributes=True,
    )