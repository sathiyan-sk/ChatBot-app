from __future__ import annotations

from abc import ABC, abstractmethod

from app.knowledge_engine.contracts.embeddings import EmbeddingsContract
from app.knowledge_engine.contracts.llm import LlmContract
from app.knowledge_engine.domain.models import KnowledgeChunk, RetrievalQuery


class EmbeddingProvider(EmbeddingsContract):
    pass


class VectorSearchProvider(ABC):
    @abstractmethod
    def search(
        self,
        *,
        query: RetrievalQuery,
        query_embedding: list[float],
    ) -> list[KnowledgeChunk]:
        raise NotImplementedError


class KeywordSearchProvider(ABC):
    @abstractmethod
    def search(self, *, query: RetrievalQuery) -> list[KnowledgeChunk]:
        raise NotImplementedError


class RerankingProvider(ABC):
    @abstractmethod
    def rerank(
        self,
        *,
        query_text: str,
        chunks: list[KnowledgeChunk],
        top_k: int,
    ) -> list[KnowledgeChunk]:
        raise NotImplementedError


class LlmProvider(LlmContract):
    pass