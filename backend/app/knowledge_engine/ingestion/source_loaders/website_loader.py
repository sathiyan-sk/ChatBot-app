from __future__ import annotations

from dataclasses import dataclass

from app.knowledge_engine.ingestion.source_loaders.base import SourceLoader
from app.knowledge_engine.shared.models import KnowledgeIngestionPipelineRequest, RawSource


@dataclass(slots=True)
class WebsiteSourceLoader(SourceLoader):
    def load(self, request: KnowledgeIngestionPipelineRequest) -> RawSource:
        return RawSource(
            source_type="website",
            source_identifier=request.source_url or request.source_path,
            content_text=request.source_url or request.source_path,
            metadata=request.metadata,
        )