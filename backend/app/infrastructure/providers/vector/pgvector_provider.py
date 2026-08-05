from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.exceptions import ApplicationError
from app.knowledge_engine.contracts.vector_store import VectorStoreContract
from app.knowledge_engine.shared.models import RetrievedChunk


@dataclass(slots=True)
class PgVectorProvider(VectorStoreContract):
    settings: object
    session: Session

    def index_chunk(
        self,
        *,
        chunk_id: str,
        content: str,
        embedding: list[float],
        metadata: dict[str, str],
    ) -> None:
        knowledge_base_id = metadata.get("knowledge_base_id")
        document_id = metadata.get("document_id")
        document_title = metadata.get("document_title")

        if not knowledge_base_id or not document_id or not document_title:
            raise ApplicationError(
                message="Indexed chunk metadata is incomplete.",
                code="vector_index_metadata_invalid",
                status_code=422,
            )

        source_uri = metadata.get("source_identifier")
        embedding_literal = self._to_pgvector_literal(embedding)

        statement = text(
            f"""
            insert into {self.settings.vector_store_table_name} (
                chunk_id,
                knowledge_base_id,
                document_id,
                document_title,
                content,
                source_uri,
                metadata_json,
                embedding
            )
            values (
                :chunk_id,
                :knowledge_base_id,
                :document_id,
                :document_title,
                :content,
                :source_uri,
                cast(:metadata_json as jsonb),
                cast(:embedding as vector)
            )
            on conflict (chunk_id)
            do update set
                knowledge_base_id = excluded.knowledge_base_id,
                document_id = excluded.document_id,
                document_title = excluded.document_title,
                content = excluded.content,
                source_uri = excluded.source_uri,
                metadata_json = excluded.metadata_json,
                embedding = excluded.embedding
            """
        )

        self.session.execute(
            statement,
            {
                "chunk_id": chunk_id,
                "knowledge_base_id": knowledge_base_id,
                "document_id": document_id,
                "document_title": document_title,
                "content": content,
                "source_uri": source_uri,
                "metadata_json": self._to_json(metadata),
                "embedding": embedding_literal,
            },
        )

    def similarity_search(
        self,
        *,
        knowledge_base_id: str,
        query_embedding: list[float],
        top_k: int,
    ) -> list[RetrievedChunk]:
        statement = text(
            f"""
            select
                chunk_id,
                document_id,
                document_title,
                content,
                source_uri,
                metadata_json,
                1 - (embedding <=> cast(:query_embedding as vector)) as score
            from {self.settings.vector_store_table_name}
            where knowledge_base_id = :knowledge_base_id
            order by embedding <=> cast(:query_embedding as vector)
            limit :top_k
            """
        )

        result = self.session.execute(
            statement,
            {
                "knowledge_base_id": knowledge_base_id,
                "query_embedding": self._to_pgvector_literal(query_embedding),
                "top_k": top_k,
            },
        )
        return [self._map_row_to_retrieved_chunk(row) for row in result.mappings().all()]

    def keyword_search(
        self,
        *,
        knowledge_base_id: str,
        query_text: str,
        top_k: int,
    ) -> list[RetrievedChunk]:
        statement = text(
            f"""
            select
                chunk_id,
                document_id,
                document_title,
                content,
                source_uri,
                metadata_json,
                ts_rank_cd(
                    to_tsvector('english', content),
                    plainto_tsquery('english', :query_text)
                ) as score
            from {self.settings.vector_store_table_name}
            where knowledge_base_id = :knowledge_base_id
              and to_tsvector('english', content) @@ plainto_tsquery('english', :query_text)
            order by score desc
            limit :top_k
            """
        )

        result = self.session.execute(
            statement,
            {
                "knowledge_base_id": knowledge_base_id,
                "query_text": query_text,
                "top_k": top_k,
            },
        )
        return [self._map_row_to_retrieved_chunk(row) for row in result.mappings().all()]

    def _map_row_to_retrieved_chunk(self, row: dict) -> RetrievedChunk:
        metadata = row.get("metadata_json") or {}
        return RetrievedChunk(
            chunk_id=row["chunk_id"],
            document_id=row["document_id"],
            document_title=row["document_title"],
            content=row["content"],
            score=float(row["score"]),
            source_uri=row.get("source_uri"),
            metadata=metadata,
        )

    def _to_pgvector_literal(self, embedding: list[float]) -> str:
        if not embedding:
            raise ApplicationError(
                message="Embedding vector cannot be empty.",
                code="vector_embedding_empty",
                status_code=422,
            )
        return "[" + ",".join(str(float(value)) for value in embedding) + "]"

    def _to_json(self, metadata: dict[str, str]) -> str:
        import json
        return json.dumps(metadata)