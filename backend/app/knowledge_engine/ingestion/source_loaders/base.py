from __future__ import annotations

from abc import ABC, abstractmethod

from app.knowledge_engine.shared.models import KnowledgeIngestionPipelineRequest, RawSource


class SourceLoader(ABC):
    @abstractmethod
    def load(self, request: KnowledgeIngestionPipelineRequest) -> RawSource:
        raise NotImplementedError