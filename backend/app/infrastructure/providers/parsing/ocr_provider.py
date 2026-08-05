from __future__ import annotations

from dataclasses import dataclass

import httpx

from app.core.exceptions import ApplicationError
from app.knowledge_engine.contracts.parsing import ParsingContract
from app.knowledge_engine.shared.helpers import normalize_whitespace, split_text_into_paragraphs
from app.knowledge_engine.shared.models import ParsedDocument, RawSource


@dataclass(slots=True)
class OcrParsingProvider(ParsingContract):
    settings: object

    def parse(self, source: RawSource) -> ParsedDocument:
        if source.content_bytes is None:
            raise ApplicationError(
                message="OCR source bytes are required.",
                code="ocr_source_bytes_required",
                status_code=422,
            )

        extracted_text = self._extract_text(source.content_bytes)
        normalized_text = normalize_whitespace(extracted_text)

        if not normalized_text:
            raise ApplicationError(
                message="OCR parser extracted no readable text.",
                code="ocr_parsed_content_empty",
                status_code=422,
            )

        title = source.metadata.get("document_title") or source.source_identifier.split("/")[-1] or "Untitled Image"
        sections = split_text_into_paragraphs(extracted_text) or [normalized_text]

        return ParsedDocument(
            title=title,
            content=normalized_text,
            sections=sections,
            metadata={
                **source.metadata,
                "parser_type": "ocr",
            },
        )

    def _extract_text(self, content_bytes: bytes) -> str:
        ocr_endpoint = getattr(self.settings, "ocr_service_url", None)
        if not ocr_endpoint:
            raise ApplicationError(
                message="OCR service is not configured.",
                code="ocr_service_not_configured",
                status_code=500,
            )

        files = {
            "file": ("document-image", content_bytes, "application/octet-stream"),
        }

        try:
            response = httpx.post(
                ocr_endpoint.rstrip("/"),
                files=files,
                timeout=self.settings.provider_timeout_seconds,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise ApplicationError(
                message="OCR provider request failed.",
                code="ocr_provider_failed",
                status_code=502,
            ) from exc

        payload = response.json()
        extracted_text = payload.get("text")
        if not isinstance(extracted_text, str):
            raise ApplicationError(
                message="OCR provider returned invalid response text.",
                code="ocr_provider_invalid_response",
                status_code=502,
            )

        return extracted_text