from __future__ import annotations

from dataclasses import dataclass

from app.knowledge_engine.contracts.storage import StorageContract
from app.knowledge_engine.ingestion.source_loaders.base import SourceLoader
from app.knowledge_engine.shared.models import KnowledgeIngestionPipelineRequest, RawSource


@dataclass(slots=True)
class FileSourceLoader(SourceLoader):
    storage_contract: StorageContract

    def load(self, request: KnowledgeIngestionPipelineRequest) -> RawSource:
        content_bytes = self.storage_contract.download_bytes(request.source_path)
        return RawSource(
            source_type="file",
            source_identifier=request.source_path,
            content_bytes=content_bytes,
            metadata=request.metadata,
        )