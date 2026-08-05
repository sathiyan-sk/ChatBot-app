from __future__ import annotations

from abc import ABC, abstractmethod

from app.knowledge_engine.shared.models import RetrievedChunk


class VectorStoreContract(ABC):
    @abstractmethod
    def index_chunk(
        self,
        *,
        chunk_id: str,
        content: str,
        embedding: list[float],
        metadata: dict[str, str],
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def similarity_search(
        self,
        *,
        knowledge_base_id: str,
        query_embedding: list[float],
        top_k: int,
    ) -> list[RetrievedChunk]:
        raise NotImplementedError

    @abstractmethod
    def keyword_search(
        self,
        *,
        knowledge_base_id: str,
        query_text: str,
        top_k: int,
    ) -> list[RetrievedChunk]:
        raise NotImplementedError