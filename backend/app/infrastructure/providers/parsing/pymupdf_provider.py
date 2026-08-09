from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO

import pymupdf

from app.core.exceptions import ApplicationError
from app.knowledge_engine.contracts.parsing import (
    ParsingContract,
)
from app.knowledge_engine.shared.helpers import (
    normalize_whitespace,
    split_text_into_paragraphs,
)
from app.knowledge_engine.shared.models import (
    ParsedDocument,
    RawSource,
)


@dataclass(slots=True)
class PyMuPDFParsingProvider(ParsingContract):
    def parse(
        self,
        source: RawSource,
    ) -> ParsedDocument:
        if source.content_bytes is None:
            raise ApplicationError(
                message="PDF content is missing.",
                code="pdf_content_missing",
                status_code=422,
            )

        try:
            pdf = pymupdf.open(
                stream=BytesIO(
                    source.content_bytes,
                ),
                filetype="pdf",
            )

            page_text = []

            for page in pdf:
                text = page.get_text(
                    "text",
                    sort=True,
                )

                if text.strip():
                    page_text.append(text)

            pdf.close()

        except Exception as exc:
            raise ApplicationError(
                message=f"PDF extraction failed: {exc}",
                code="pdf_extraction_failed",
                status_code=422,
            ) from exc

        extracted_text = "\n\n".join(page_text)

        normalized_text = normalize_whitespace(
            extracted_text,
        )

        if not normalized_text:
            raise ApplicationError(
                message=(
                    "No selectable text was found in "
                    "the PDF. It may be scanned."
                ),
                code="pdf_text_not_found",
                status_code=422,
            )

        paragraphs = split_text_into_paragraphs(
            normalized_text,
        )

        source_name = (
            source.source_identifier.rsplit(
                "/",
                1,
            )[-1]
            or "document.pdf"
        )

        title = (
            source.metadata.get("document_title")
            or source_name
        )

        return ParsedDocument(
            title=title,
            content=normalized_text,
            sections=paragraphs or [normalized_text],
            metadata={
                **source.metadata,
                "parser": "pymupdf",
            },
        )