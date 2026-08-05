from __future__ import annotations

from dataclasses import dataclass

from app.knowledge_engine.contracts.embeddings import EmbeddingsContract


@dataclass(slots=True)
class QueryEmbedder:
    embeddings_contract: EmbeddingsContract

    def embed(self, query_text: str) -> list[float]:
        return self.embeddings_contract.embed_query(query_text)