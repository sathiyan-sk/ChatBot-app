from __future__ import annotations

from dataclasses import dataclass

from app.knowledge_engine.contracts.vector_store import VectorStoreContract
from app.knowledge_engine.shared.models import RetrievedChunk


@dataclass(slots=True)
class HybridRetriever:
    vector_store_contract: VectorStoreContract

    def retrieve(
        self,
        *,
        knowledge_base_id: str,
        query_text: str,
        query_embedding: list[float],
        top_k: int,
    ) -> list[RetrievedChunk]:
        semantic_chunks = self.vector_store_contract.similarity_search(
            knowledge_base_id=knowledge_base_id,
            query_embedding=query_embedding,
            top_k=top_k,
        )
        keyword_chunks = self.vector_store_contract.keyword_search(
            knowledge_base_id=knowledge_base_id,
            query_text=query_text,
            top_k=top_k,
        )

        merged: dict[str, RetrievedChunk] = {}
        for chunk in semantic_chunks + keyword_chunks:
            key = f"{chunk.document_id}:{chunk.chunk_id}"
            existing = merged.get(key)
            if existing is None or chunk.score > existing.score:
                merged[key] = chunk

        return sorted(merged.values(), key=lambda item: item.score, reverse=True)