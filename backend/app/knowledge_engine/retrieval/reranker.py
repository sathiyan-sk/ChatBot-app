from __future__ import annotations

from app.knowledge_engine.shared.models import RetrievedChunk


class Reranker:
    def rerank(self, *, query_text: str, chunks: list[RetrievedChunk], top_k: int) -> list[RetrievedChunk]:
        ranked = sorted(chunks, key=lambda item: item.score, reverse=True)
        return ranked[:top_k]