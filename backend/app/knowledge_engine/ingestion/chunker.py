from __future__ import annotations

import re

from app.knowledge_engine.shared.models import DocumentChunk


class IntelligentChunkGenerator:
    def __init__(
        self,
        chunk_size: int = 400,  # tokens or characters
        chunk_overlap: int = 100,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def generate(self, text: str) -> list[DocumentChunk]:
        # Split into sentences (simple heuristic)
        sentences = re.split(r'(?<=[.!?])\s+', text)

        chunks: list[DocumentChunk] = []
        current_chunk_text = ""
        current_chunk_index = 0

        for sentence in sentences:
            if len(current_chunk_text) + len(sentence) <= self.chunk_size:
                current_chunk_text += " " + sentence if current_chunk_text else sentence
            else:
                # Save current chunk
                chunks.append(
                    DocumentChunk(
                        chunk_index=current_chunk_index,
                        content=current_chunk_text.strip(),
                    )
                )
                current_chunk_index += 1

                # Start new chunk with overlap
                overlap_sentences = self._get_overlap_sentences(
                    current_chunk_text, sentence, self.chunk_overlap
                )
                current_chunk_text = " ".join(overlap_sentences)

        # Don't forget the last chunk
        if current_chunk_text.strip():
            chunks.append(
                DocumentChunk(
                    chunk_index=current_chunk_index,
                    content=current_chunk_text.strip(),
                )
            )

        return chunks

    def _get_overlap_sentences(
        self,
        current_text: str,
        next_sentence: str,
        overlap_size: int,
    ) -> list[str]:
        # Keep last N characters from current chunk as overlap
        sentences = re.split(r'(?<=[.!?])\s+', current_text)
        overlap_text = current_text[-overlap_size:] if len(current_text) > overlap_size else current_text
        overlap_sentences = re.split(r'(?<=[.!?])\s+', overlap_text)
        return [s for s in overlap_sentences if s.strip()] + [next_sentence]