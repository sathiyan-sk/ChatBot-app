from __future__ import annotations

from abc import ABC, abstractmethod

from app.knowledge_engine.domain.models import GeneratedResponse, KnowledgeChunk, RetrievalQuery


class EmbeddingProvider(ABC):
    @abstractmethod
    def embed_query(self, text: str) -> list[float]:
        raise NotImplementedError


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


class LlmProvider(ABC):
    @abstractmethod
    def generate(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        raise NotImplementedError