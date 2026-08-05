from __future__ import annotations

from app.knowledge_engine.shared.models import Citation, RetrievedChunk


class CitationBuilder:
    def build(self, chunks: list[RetrievedChunk]) -> list[Citation]:
        citations: list[Citation] = []
        seen_keys: set[str] = set()

        for chunk in chunks:
            key = f"{chunk.document_id}:{chunk.chunk_id}"
            if key in seen_keys:
                continue
            seen_keys.add(key)

            citations.append(
                Citation(
                    document_id=chunk.document_id,
                    document_title=chunk.document_title,
                    chunk_id=chunk.chunk_id,
                    source_uri=chunk.source_uri,
                )
            )

        return citations