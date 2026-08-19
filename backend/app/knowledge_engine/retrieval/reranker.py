from __future__ import annotations

import re

from app.knowledge_engine.domain.models import KnowledgeChunk


class Reranker:
    def rerank(
        self,
        *,
        query_text: str,
        chunks: list[KnowledgeChunk],
        top_k: int,
    ) -> list[KnowledgeChunk]:
        if not chunks:
            return []

        query_tokens = self._tokenize(query_text)
        query_token_set = set(query_tokens)

        scored_chunks: list[tuple[KnowledgeChunk, float]] = []

        for chunk in chunks:
            chunk_tokens = self._tokenize(chunk.content)
            chunk_token_set = set(chunk_tokens)

            # Keyword overlap ratio
            overlap = len(query_token_set & chunk_token_set)
            overlap_ratio = overlap / max(len(query_token_set), 1)

            # Original retrieval score (from vector or keyword search)
            original_score = chunk.score

            # Hybrid score: 60% original retrieval score, 40% keyword overlap
            # Adjust weights based on your testing
            rerank_score = (0.6 * original_score) + (0.4 * overlap_ratio)

            scored_chunks.append((chunk, rerank_score))

        # Sort by rerank score descending
        scored_chunks.sort(key=lambda x: x[1], reverse=True)

        # Return top_k chunks with updated scores
        reranked = []
        for chunk, score in scored_chunks[:top_k]:
            # Create a new chunk with updated score
            reranked.append(
                KnowledgeChunk(
                    chunk_id=chunk.chunk_id,
                    document_id=chunk.document_id,
                    document_title=chunk.document_title,
                    content=chunk.content,
                    source_uri=chunk.source_uri,
                    score=score,  # Updated rerank score
                    metadata=chunk.metadata,
                )
            )

        return reranked[:top_k]

    def _tokenize(self, text: str) -> list[str]:
        # Simple tokenization: lowercase, remove punctuation, split
        text = text.lower()
        tokens = re.findall(r'\b[a-z0-9]+\b', text)
        # Remove common stopwords
        stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'need',
            'it', 'its', 'this', 'that', 'these', 'those', 'i', 'you', 'he',
            'she', 'we', 'they', 'what', 'which', 'who', 'whom', 'whose',
        }
        return [t for t in tokens if t not in stopwords]