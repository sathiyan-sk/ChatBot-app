from __future__ import annotations

from app.knowledge_engine.shared.helpers import normalize_whitespace
from app.knowledge_engine.shared.models import NormalizedDocument, ParsedDocument


class DocumentNormalizer:
    def normalize(self, document: ParsedDocument) -> NormalizedDocument:
        normalized_sections = [
            normalize_whitespace(section)
            for section in document.sections
            if normalize_whitespace(section)
        ]

        normalized_content = normalize_whitespace(document.content)

        return NormalizedDocument(
            title=normalize_whitespace(document.title) or "Untitled Document",
            content=normalized_content,
            sections=normalized_sections,
            metadata=document.metadata,
        )