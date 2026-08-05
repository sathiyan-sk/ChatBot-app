from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Header, HTTPException, status

from app.api.dependencies import get_chat_application_service
from app.api.schemas.chat import (
    ChatMessageRequest,
    ChatMessageResponse,
    CitationResponse,
)
from app.modules.chat.application.services import ChatApplicationService

router = APIRouter(prefix="/client/chat", tags=["Client Chat"])


@router.post("/messages", response_model=ChatMessageResponse, status_code=status.HTTP_200_OK)
def create_chat_message(
    request: ChatMessageRequest,
    service: ChatApplicationService = Depends(get_chat_application_service),
    x_application_api_key: str | None = Header(default=None, alias="X-Application-Api-Key"),
) -> ChatMessageResponse:
    if not x_application_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Application API key is required.",
        )

    result = service.answer_question(
        api_key=x_application_api_key,
        conversation_id=request.conversation_id,
        conversation_identity=request.conversation_identity,
        message=request.message,
    )

    citations = [
        CitationResponse(
            source_id=item.source_id,
            title=getattr(item, "title", None),
            snippet=getattr(item, "snippet", None),
        )
        for item in result.citations
    ]

    return ChatMessageResponse(
        conversation_id=result.conversation_id,
        answer=result.answer,
        citations=citations,
        created_at=getattr(result, "created_at", datetime.now(timezone.utc)),
    )