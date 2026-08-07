from __future__ import annotations

from dataclasses import dataclass

from app.core.exceptions import ApplicationError
from app.knowledge_engine.ingestion.chunker import IntelligentChunkGenerator
from app.knowledge_engine.ingestion.document_parser import DocumentParser
from app.knowledge_engine.ingestion.embedding_generator import EmbeddingGenerator
from app.knowledge_engine.ingestion.metadata_enricher import MetadataEnricher
from app.knowledge_engine.ingestion.normalizer import DocumentNormalizer
from app.knowledge_engine.ingestion.source_loader import SourceLoader
from app.knowledge_engine.ingestion.vector_indexer import VectorIndexer
from app.knowledge_engine.shared.models import (
    KnowledgeIngestionPipelineRequest,
    KnowledgeIngestionPipelineResult,
)


@dataclass(slots=True)
class KnowledgeIngestionPipeline:
    source_loader: SourceLoader
    parser: DocumentParser
    normalizer: DocumentNormalizer
    chunk_generator: IntelligentChunkGenerator
    metadata_enricher: MetadataEnricher
    embedding_generator: EmbeddingGenerator
    vector_indexer: VectorIndexer

    def run(self, request: KnowledgeIngestionPipelineRequest) -> KnowledgeIngestionPipelineResult:
        raw_source = self.source_loader.load(request)
        parsed_document = self.parser.parse(raw_source)
        normalized_document = self.normalizer.normalize(parsed_document)

        if not normalized_document.content.strip():
            raise ApplicationError(
                message="Parsed document content is empty.",
                code="parsed_document_empty",
                status_code=422,
            )

        chunks = self.chunk_generator.generate(
            document_id=request.document_id,
            document=normalized_document,
        )

        enriched_chunks = self.metadata_enricher.enrich(
            chunks=chunks,
            document_id=request.document_id,
            knowledge_base_id=request.knowledge_base_id,
            source_type=request.source_type,
            source_identifier=raw_source.source_identifier,
            document_title=normalized_document.title,
            document_metadata=normalized_document.metadata,
        )
        embedded_chunks = self.embedding_generator.generate(enriched_chunks)
        indexed_chunk_ids = self.vector_indexer.index(embedded_chunks)

        return KnowledgeIngestionPipelineResult(
            document_id=request.document_id,
            knowledge_base_id=request.knowledge_base_id,
            chunk_count=len(indexed_chunk_ids),
            indexed_chunk_ids=indexed_chunk_ids,
            document_title=normalized_document.title,
            metadata=normalized_document.metadata,
        )