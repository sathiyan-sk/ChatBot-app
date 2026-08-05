from __future__ import annotations

from dataclasses import dataclass

from app.knowledge_engine.contracts.embeddings import EmbeddingsContract
from app.knowledge_engine.shared.models import DocumentChunk, EmbeddedChunk


@dataclass(slots=True)
class EmbeddingGenerator:
    embeddings_contract: EmbeddingsContract

    def generate(self, chunks: list[DocumentChunk]) -> list[EmbeddedChunk]:
        embedded_chunks: list[EmbeddedChunk] = []

        for chunk in chunks:
            embedding = self.embeddings_contract.embed_query(chunk.content)
            embedded_chunks.append(
                EmbeddedChunk(
                    chunk_id=chunk.chunk_id,
                    content=chunk.content,
                    embedding=embedding,
                    metadata=chunk.metadata,
                )
            )

        return embedded_chunks