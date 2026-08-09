from __future__ import annotations

from app.knowledge_engine.domain.models import KnowledgeChunk, RetrievalQuery
from app.knowledge_engine.domain.provider_interfaces import (
    EmbeddingProvider,
    KeywordSearchProvider,
    LlmProvider,
    RerankingProvider,
    VectorSearchProvider,
)
from typing import Protocol

class SimpleEmbeddingProvider(EmbeddingProvider):
    def embed_query(self, text: str) -> list[float]:
        base = float(len(text.strip()) or 1)
        return [base / 100.0, base / 200.0, base / 300.0]


class PgVectorSearchProvider(VectorSearchProvider):
    def search(
        self,
        *,
        query: RetrievalQuery,
        query_embedding: list[float],
    ) -> list[KnowledgeChunk]:
        return [
            KnowledgeChunk(
                chunk_id="vector-1",
                document_id="document-1",
                document_title="Vector Retrieved Document",
                content=f"Semantic retrieval context for query: {query.query_text}",
                source_uri=None,
                score=0.92,
                metadata={"strategy": "vector"},
            )
        ]


class PostgresKeywordSearchProvider(KeywordSearchProvider):
    def search(self, *, query: RetrievalQuery) -> list[KnowledgeChunk]:
        return [
            KnowledgeChunk(
                chunk_id="keyword-1",
                document_id="document-2",
                document_title="Keyword Retrieved Document",
                content=f"Keyword retrieval context for query: {query.query_text}",
                source_uri=None,
                score=0.81,
                metadata={"strategy": "keyword"},
            )
        ]


class SimpleRerankingProvider(RerankingProvider):
    def rerank(
        self,
        *,
        query_text: str,
        chunks: list[KnowledgeChunk],
        top_k: int,
    ) -> list[KnowledgeChunk]:
        sorted_chunks = sorted(chunks, key=lambda item: item.score, reverse=True)
        return sorted_chunks[:top_k]


class OllamaLlmProvider(LlmProvider):
    def generate(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        return (
            "Grounded answer generated from retrieved knowledge. "
            f"Prompt summary: {user_prompt[:240]}"
        )



class StorageContract(Protocol):
    def upload(
        self,
        *,
        path: str,
        content: bytes,
        content_type: str | None,
    ) -> str:
        ...

    def download_bytes(
        self,
        storage_path: str,
    ) -> bytes:
        ...

    def download_text(
        self,
        storage_path: str,
    ) -> str:
        ...