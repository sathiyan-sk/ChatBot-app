from __future__ import annotations

from dataclasses import dataclass

from app.modules.question_answering.contracts.response_models import CitationItem


@dataclass(slots=True, frozen=True)
class AskChatQuestionResultDto:
    conversation_id: str
    user_message_id: str
    assistant_message_id: str
    answer_text: str
    citations: list[CitationItem]