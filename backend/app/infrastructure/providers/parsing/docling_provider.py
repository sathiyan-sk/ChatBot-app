from __future__ import annotations

from dataclasses import dataclass

from app.core.exceptions import ApplicationError
from app.knowledge_engine.contracts.parsing import ParsingContract
from app.knowledge_engine.shared.helpers import normalize_whitespace, split_text_into_paragraphs
from app.knowledge_engine.shared.models import ParsedDocument, RawSource


@dataclass(slots=True)
class DoclingParsingProvider(ParsingContract):
    def parse(self, source: RawSource) -> ParsedDocument:
        if source.content_bytes is None and source.content_text is None:
            raise ApplicationError(
                message="Parsing source content is missing.",
                code="parsing_source_missing_content",
                status_code=422,
            )

        if source.content_text is not None:
            extracted_text = source.content_text
        else:
            try:
                extracted_text = source.content_bytes.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise ApplicationError(
                    message="Binary document parsing requires a real Docling integration.",
                    code="docling_binary_parsing_not_available",
                    status_code=501,
                ) from exc

        normalized_text = normalize_whitespace(extracted_text)
        if not normalized_text:
            raise ApplicationError(
                message="Parsed document content is empty.",
                code="docling_parsed_content_empty",
                status_code=422,
            )

        paragraphs = split_text_into_paragraphs(extracted_text)
        title = source.metadata.get("document_title") or source.source_identifier.split("/")[-1] or "Untitled Document"

        return ParsedDocument(
            title=title,
            content=normalized_text,
            sections=paragraphs or [normalized_text],
            metadata=source.metadata,
        )