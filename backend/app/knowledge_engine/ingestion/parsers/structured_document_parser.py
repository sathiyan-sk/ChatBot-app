from __future__ import annotations

from dataclasses import dataclass

from app.knowledge_engine.contracts.parsing import ParsingContract
from app.knowledge_engine.ingestion.parsers.base import DocumentParser
from app.knowledge_engine.shared.models import ParsedDocument, RawSource


@dataclass(slots=True)
class StructuredDocumentParser(DocumentParser):
    parsing_contract: ParsingContract

    def parse(self, source: RawSource) -> ParsedDocument:
        return self.parsing_contract.parse(source)