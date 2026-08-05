from __future__ import annotations

from app.knowledge_engine.shared.models import RetrievedChunk


class MetadataFilter:
    def apply(self, chunks: list[RetrievedChunk]) -> list[RetrievedChunk]:
        return [item for item in chunks if item.content.strip()]