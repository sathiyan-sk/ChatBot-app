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
        # Retrieve from both sources
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

        # Normalize scores to 0-1 range for fair comparison
        def normalize_score(chunks: list[RetrievedChunk]) -> list[tuple[RetrievedChunk, float]]:
            if not chunks:
                return []
            max_score = max(c.score for c in chunks)
            min_score = min(c.score for c in chunks)
            score_range = max_score - min_score if max_score != min_score else 1.0
            return [
                (chunk, (chunk.score - min_score) / score_range)
                for chunk in chunks
            ]

        normalized_semantic = normalize_score(semantic_chunks)
        normalized_keyword = normalize_score(keyword_chunks)

        # Merge with weighted combination (60% semantic, 40% keyword)
        merged: dict[str, tuple[RetrievedChunk, float]] = {}

        for chunk, norm_score in normalized_semantic:
            key = f"{chunk.document_id}:{chunk.chunk_id}"
            merged[key] = (chunk, 0.6 * norm_score)

        for chunk, norm_score in normalized_keyword:
            key = f"{chunk.document_id}:{chunk.chunk_id}"
            existing = merged.get(key)
            if existing:
                # Add keyword score to existing semantic score
                existing_chunk, existing_score = existing
                combined_score = existing_score + (0.4 * norm_score)
                merged[key] = (existing_chunk, combined_score)
            else:
                merged[key] = (chunk, 0.4 * norm_score)

        # Sort by combined score and return top_k
        sorted_chunks = sorted(merged.values(), key=lambda x: x[1], reverse=True)
        return [chunk for chunk, _ in sorted_chunks[:top_k]]