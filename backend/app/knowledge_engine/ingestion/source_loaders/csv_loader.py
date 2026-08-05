from __future__ import annotations

from dataclasses import dataclass

from app.knowledge_engine.contracts.storage import StorageContract
from app.knowledge_engine.ingestion.source_loaders.base import SourceLoader
from app.knowledge_engine.shared.models import KnowledgeIngestionPipelineRequest, RawSource


@dataclass(slots=True)
class CsvSourceLoader(SourceLoader):
    storage_contract: StorageContract

    def load(self, request: KnowledgeIngestionPipelineRequest) -> RawSource:
        content_text = self.storage_contract.download_text(request.source_path)
        return RawSource(
            source_type="csv",
            source_identifier=request.source_path,
            content_text=content_text,
            metadata=request.metadata,
        )