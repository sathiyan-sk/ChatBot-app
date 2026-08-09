from __future__ import annotations

from dataclasses import asdict
from typing import Any

from fastapi import APIRouter, Depends

from app.api.client.dependencies import (
    get_client_application_context,
)
from app.api.dependencies import (
    get_conversation_application_service,
)
from app.api.schemas.conversations import (
    ConversationDetailResponse,
    ConversationResponse,
    MessageResponse,
)
from app.modules.conversations.application.queries import (
    GetConversationDetailQuery,
)
from app.modules.conversations.application.services import (
    ConversationApplicationService,
)
from app.modules.security.domain.entities import (
    ClientApplicationContext,
)


router = APIRouter(
    prefix="/client/conversations",
    tags=["Client Conversations"],
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


@router.get(
    "/{conversation_id}",
    response_model=ConversationDetailResponse,
)
def get_client_conversation_detail(
    conversation_id: str,
    application_context: ClientApplicationContext = Depends(
        get_client_application_context,
    ),
    service: ConversationApplicationService = Depends(
        get_conversation_application_service,
    ),
) -> ConversationDetailResponse:
    result = service.get_conversation_detail(
        GetConversationDetailQuery(
            conversation_id=conversation_id,
            application_id=str(
                application_context.application_id,
            ),
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