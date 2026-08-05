from __future__ import annotations

from dataclasses import dataclass

from app.knowledge_engine.contracts.vector_store import VectorStoreContract
from app.knowledge_engine.shared.models import EmbeddedChunk


@dataclass(slots=True)
class VectorIndexer:
    vector_store_contract: VectorStoreContract

    def index(self, embedded_chunks: list[EmbeddedChunk]) -> list[str]:
        indexed_chunk_ids: list[str] = []

        for chunk in embedded_chunks:
            self.vector_store_contract.index_chunk(
                chunk_id=chunk.chunk_id,
                content=chunk.content,
                embedding=chunk.embedding,
                metadata=chunk.metadata,
            )
            indexed_chunk_ids.append(chunk.chunk_id)

        return indexed_chunk_ids