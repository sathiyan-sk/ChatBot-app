from __future__ import annotations

from abc import ABC, abstractmethod

from app.knowledge_engine.shared.models import ParsedDocument, RawSource


class DocumentParser(ABC):
    @abstractmethod
    def parse(self, source: RawSource) -> ParsedDocument:
        raise NotImplementedError