from __future__ import annotations

from datetime import datetime, timezone

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from app.api.client.dependencies import (
    get_client_application_context,
)
from app.api.dependencies import (
    get_chat_application_service,
)
from app.api.schemas.chat import (
    ChatMessageRequest,
    ChatMessageResponse,
    CitationResponse,
)
from app.modules.question_answering.application.commands import (
    AskChatQuestionCommand,
)
from app.modules.question_answering.application.services import (
    ChatApplicationService,
)
from app.modules.security.domain.entities import (
    ClientApplicationContext,
)


router = APIRouter(
    prefix="/client/chat",
    tags=["Client Chat"],
)


@router.post(
    "/messages",
    response_model=ChatMessageResponse,
    status_code=status.HTTP_200_OK,
)
def create_chat_message(
    request: ChatMessageRequest,
    application_context: ClientApplicationContext = Depends(
        get_client_application_context,
    ),
    service: ChatApplicationService = Depends(
        get_chat_application_service,
    ),
) -> ChatMessageResponse:
    if not application_context.application_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid application context.",
        )

    result = service.ask(
        AskChatQuestionCommand(
            application_id=str(
                application_context.application_id,
            ),
            conversation_identity=(
                request.conversation_identity
            ),
            message_text=request.message,
            conversation_title=(
                request.conversation_title
            ),
        )
    )

    citations = [
        CitationResponse(
            document_id=item.document_id,
            title=item.document_title,
            chunk_id=item.chunk_id,
            source_uri=item.source_uri,
        )
        for item in result.citations
    ]

    return ChatMessageResponse(
    conversation_id=(
        str(result.conversation_id)
        if result.conversation_id is not None
        else ""
    ),
    answer=result.answer_text,
    citations=citations,
    created_at=datetime.now(timezone.utc),
)