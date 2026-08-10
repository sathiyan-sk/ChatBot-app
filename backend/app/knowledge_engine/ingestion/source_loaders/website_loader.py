from __future__ import annotations

from dataclasses import dataclass

import requests

from app.knowledge_engine.ingestion.source_loaders.base import (
    SourceLoader,
)
from app.knowledge_engine.shared.models import (
    KnowledgeIngestionPipelineRequest,
    RawSource,
)


@dataclass(slots=True)
class WebsiteSourceLoader(SourceLoader):
    def load(
        self,
        request: KnowledgeIngestionPipelineRequest,
    ) -> RawSource:
        source_identifier = (
            request.source_identifier
            or request.source_path
        )

        if not source_identifier:
            raise ValueError(
                "Website URL is required."
            )

        if not (
            source_identifier.startswith("http://")
            or source_identifier.startswith("https://")
        ):
            raise ValueError(
                "Website URL must use http or https."
            )

        response = requests.get(
            source_identifier,
            timeout=30,
            headers={
                "User-Agent": (
                    "AI-Knowledge-Platform/1.0"
                ),
            },
        )

        response.raise_for_status()

        return RawSource(
            source_type="website",
            source_identifier=source_identifier,
            content_text=response.text,
            content_bytes=None,
            metadata={
                **request.metadata,
                "url": source_identifier,
                "status_code": str(
                    response.status_code
                ),
                "content_type": (
                    response.headers.get(
                        "content-type",
                        "",
                    )
                ),
            },
        )