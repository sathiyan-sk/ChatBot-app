from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
from urllib.parse import urlparse

import httpx

from app.core.exceptions import ApplicationError
from app.knowledge_engine.contracts.parsing import ParsingContract
from app.knowledge_engine.shared.helpers import normalize_whitespace, split_text_into_paragraphs
from app.knowledge_engine.shared.models import ParsedDocument, RawSource


class _HtmlTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._title_parts: list[str] = []
        self._text_parts: list[str] = []
        self._inside_title = False
        self._ignored_tags = {"script", "style", "noscript"}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "title":
            self._inside_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._inside_title = False

    def handle_data(self, data: str) -> None:
        normalized = normalize_whitespace(data)
        if not normalized:
            return
        if self._inside_title:
            self._title_parts.append(normalized)
            return
        self._text_parts.append(normalized)

    @property
    def title(self) -> str:
        return normalize_whitespace(" ".join(self._title_parts))

    @property
    def text(self) -> str:
        return "\n\n".join(self._text_parts)


@dataclass(slots=True)
class HtmlParsingProvider(ParsingContract):
    settings: object

    def parse(self, source: RawSource) -> ParsedDocument:
        source_identifier = source.source_identifier.strip()
        if not source_identifier:
            raise ApplicationError(
                message="Website source identifier is required.",
                code="html_source_identifier_required",
                status_code=400,
            )

        html_content = source.content_text
        if self._looks_like_url(source_identifier):
            html_content = self._download_html(source_identifier)
        elif not html_content:
            raise ApplicationError(
                message="HTML content is missing.",
                code="html_content_missing",
                status_code=422,
            )

        extractor = _HtmlTextExtractor()
        extractor.feed(html_content)
        body_text = normalize_whitespace(extractor.text)

        if not body_text:
            raise ApplicationError(
                message="HTML parser extracted no readable text.",
                code="html_parsed_content_empty",
                status_code=422,
            )

        resolved_title = extractor.title or self._derive_title_from_source(source_identifier)
        sections = split_text_into_paragraphs(extractor.text) or [body_text]

        return ParsedDocument(
            title=resolved_title,
            content=body_text,
            sections=sections,
            metadata={
                **source.metadata,
                "source_uri": source_identifier,
                "parser_type": "html",
            },
        )

    def _download_html(self, url: str) -> str:
        try:
            response = httpx.get(
                url,
                timeout=self.settings.provider_timeout_seconds,
                follow_redirects=True,
                headers={"User-Agent": self.settings.http_user_agent},
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise ApplicationError(
                message="Website download failed.",
                code="html_download_failed",
                status_code=502,
            ) from exc

        return response.text

    def _looks_like_url(self, value: str) -> bool:
        parsed = urlparse(value)
        return bool(parsed.scheme and parsed.netloc)

    def _derive_title_from_source(self, value: str) -> str:
        parsed = urlparse(value)
        if parsed.netloc:
            return parsed.netloc
        return value.rsplit("/", maxsplit=1)[-1] or "Untitled Website"