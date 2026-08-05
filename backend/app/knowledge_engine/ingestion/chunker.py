from __future__ import annotations

from dataclasses import dataclass

from app.knowledge_engine.shared.helpers import build_chunk_id, split_text_into_paragraphs, truncate_text
from app.knowledge_engine.shared.models import DocumentChunk, NormalizedDocument


@dataclass(slots=True)
class IntelligentChunkGenerator:
    max_chunk_length: int = 1000

    def generate(self, *, document_id: str, document: NormalizedDocument) -> list[DocumentChunk]:
        segments = document.sections or split_text_into_paragraphs(document.content) or [document.content]
        chunks: list[DocumentChunk] = []

        for index, segment in enumerate(segments, start=1):
            content = segment.strip()
            if not content:
                continue

            chunks.append(
                DocumentChunk(
                    chunk_id=build_chunk_id(document_id, f"chunk-{index}"),
                    content=truncate_text(content, self.max_chunk_length),
                    metadata={
                        "chunk_index": str(index),
                        "document_title": document.title,
                    },
                )
            )

        return chunks