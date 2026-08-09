from __future__ import annotations

from dataclasses import asdict
from typing import Any

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from app.api.dependencies import (
    get_conversation_application_service,
    require_admin,
)
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
from app.modules.conversations.application.queries import (
    GetConversationDetailQuery,
    ListApplicationConversationsQuery,
)
from app.modules.conversations.application.services import (
    ConversationApplicationService,
)


router = APIRouter(
    prefix="/admin/conversations",
    tags=["Admin Conversations"],
    dependencies=[
        Depends(require_admin),
    ],
)


def _conversation_response_payload(
    conversation: Any,
) -> dict[str, Any]:
    payload = asdict(conversation)

    payload["id"] = str(
        payload["id"],
    )

    payload["application_id"] = str(
        payload["application_id"],
    )

    return payload


def _message_response_payload(
    message: Any,
) -> dict[str, Any]:
    payload = asdict(message)

    payload["id"] = str(
        payload["id"],
    )

    payload["conversation_id"] = str(
        payload["conversation_id"],
    )

    return payload


@router.post(
    "/resolve",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
)
def resolve_conversation(
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
        )
    )

    return ConversationResponse.model_validate(
        _conversation_response_payload(result),
    )


@router.get(
    "/application/{application_id}",
    response_model=list[ConversationResponse],
)
def list_application_conversations(
    application_id: str,
    service: ConversationApplicationService = Depends(
        get_conversation_application_service,
    ),
) -> list[ConversationResponse]:
    result = (
        service.list_application_conversations(
            query=ListApplicationConversationsQuery(
                application_id=application_id,
            ),
        )
    )

    return [
        ConversationResponse.model_validate(
            _conversation_response_payload(item),
        )
        for item in result
    ]


@router.get(
    "/{conversation_id}",
    response_model=ConversationDetailResponse,
)
def get_conversation_detail(
    conversation_id: str,
    service: ConversationApplicationService = Depends(
        get_conversation_application_service,
    ),
) -> ConversationDetailResponse:
    result = service.get_conversation_detail(
        GetConversationDetailQuery(
            conversation_id=conversation_id,
            application_id=None,
        )
    )

    return ConversationDetailResponse(
        conversation=ConversationResponse.model_validate(
            _conversation_response_payload(
                result.conversation,
            ),
        ),
        messages=[
            MessageResponse.model_validate(
                _message_response_payload(item),
            )
            for item in result.messages
        ],
    )


@router.put(
    "/{conversation_id}",
    response_model=ConversationResponse,
)
def update_conversation(
    conversation_id: str,
    payload: UpdateConversationRequest,
    service: ConversationApplicationService = Depends(
        get_conversation_application_service,
    ),
) -> ConversationResponse:
    result = service.update_conversation(
        UpdateConversationCommand(
            conversation_id=conversation_id,
            title=payload.title,
            summary=payload.summary,
            is_active=payload.is_active,
        )
    )

    return ConversationResponse.model_validate(
        _conversation_response_payload(result),
    )


@router.delete(
    "/{conversation_id}",
    response_model=ConversationResponse,
)
def close_conversation(
    conversation_id: str,
    service: ConversationApplicationService = Depends(
        get_conversation_application_service,
    ),
) -> ConversationResponse:
    result = service.update_conversation(
        UpdateConversationCommand(
            conversation_id=conversation_id,
            title=None,
            summary=None,
            is_active=False,
        )
    )

    return ConversationResponse.model_validate(
        _conversation_response_payload(result),
    )


@router.post(
    "/{conversation_id}/messages",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def append_message(
    conversation_id: str,
    payload: AppendMessageRequest,
    service: ConversationApplicationService = Depends(
        get_conversation_application_service,
    ),
) -> MessageResponse:
    allowed_roles = {
        "user",
        "assistant",
        "system",
    }

    if payload.role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Unsupported message role.",
                "code": "message_role_invalid",
            },
        )

    result = service.append_message(
        AppendMessageCommand(
            conversation_id=conversation_id,
            role=payload.role,
            content=payload.content,
            citation_payload=(
                payload.citation_payload
            ),
        )
    )

    return MessageResponse.model_validate(
        _message_response_payload(result),
    )