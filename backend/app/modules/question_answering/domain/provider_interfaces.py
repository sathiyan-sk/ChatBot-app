from __future__ import annotations

from abc import ABC, abstractmethod

from app.modules.question_answering.domain.entities import GeneratedAnswer, RetrievedChunk


class RetrievalProvider(ABC):
    @abstractmethod
    def retrieve(
        self,
        *,
        application_id: str,
        knowledge_base_id: str,
        query_text: str,
        conversation_messages: list[dict[str, str]],
        top_k: int,
    ) -> list[RetrievedChunk]:
        raise NotImplementedError


class AnswerGenerationProvider(ABC):
    @abstractmethod
    def generate_answer(
        self,
        *,
        application_id: str,
        query_text: str,
        retrieved_chunks: list[RetrievedChunk],
        conversation_messages: list[dict[str, str]],
    ) -> GeneratedAnswer:
        raise NotImplementedError