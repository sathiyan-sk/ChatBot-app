from __future__ import annotations

from dataclasses import dataclass

import httpx

from app.core.exceptions import ApplicationError
from app.knowledge_engine.contracts.embeddings import (
    EmbeddingsContract,
)


@dataclass(slots=True)
class NomicEmbeddingsProvider(
    EmbeddingsContract,
):
    settings: object

    def embed_query(
        self,
        text: str,
    ) -> list[float]:
        normalized_text = text.strip()

        if not normalized_text:
            raise ApplicationError(
                message="Embedding text cannot be empty.",
                code="embedding_text_empty",
                status_code=400,
            )

        ollama_settings = getattr(
            self.settings,
            "ollama",
            None,
        )

        if ollama_settings is None:
            raise ApplicationError(
                message=(
                    "Ollama settings are not configured."
                ),
                code="ollama_settings_missing",
                status_code=503,
            )

        base_url = getattr(
            ollama_settings,
            "base_url",
            None,
        )

        model_name = getattr(
            ollama_settings,
            "embedding_model_name",
            None,
        )

        timeout_seconds = getattr(
            ollama_settings,
            "provider_timeout_seconds",
            120.0,
        )

        if not base_url:
            raise ApplicationError(
                message=(
                    "Ollama base URL is not configured."
                ),
                code="ollama_base_url_missing",
                status_code=503,
            )

        if not model_name:
            raise ApplicationError(
                message=(
                    "Embedding model name is not configured."
                ),
                code="embedding_model_name_missing",
                status_code=503,
            )

        url = (
            f"{base_url.rstrip('/')}"
            "/api/embeddings"
        )

        payload = {
            "model": model_name,
            "prompt": normalized_text,
        }

        try:
            response = httpx.post(
                url,
                json=payload,
                timeout=timeout_seconds,
            )
            response.raise_for_status()

        except httpx.HTTPStatusError as exc:
            raise ApplicationError(
                message=(
                    "Ollama embedding request failed "
                    f"with status "
                    f"{exc.response.status_code}."
                ),
                code="embedding_provider_failed",
                status_code=502,
            ) from exc

        except httpx.HTTPError as exc:
            raise ApplicationError(
                message=(
                    "Could not connect to Ollama "
                    "embedding provider."
                ),
                code="embedding_provider_unavailable",
                status_code=502,
            ) from exc

        try:
            response_payload = response.json()

        except ValueError as exc:
            raise ApplicationError(
                message=(
                    "Embedding provider returned "
                    "invalid JSON."
                ),
                code="embedding_provider_invalid_json",
                status_code=502,
            ) from exc

        embedding = response_payload.get(
            "embedding",
        )

        if not isinstance(embedding, list):
            raise ApplicationError(
                message=(
                    "Embedding provider returned "
                    "invalid embedding output."
                ),
                code="embedding_provider_invalid_response",
                status_code=502,
            )

        if not embedding:
            raise ApplicationError(
                message=(
                    "Embedding provider returned "
                    "an empty embedding."
                ),
                code="embedding_provider_empty_response",
                status_code=502,
            )

        try:
            return [
                float(value)
                for value in embedding
            ]

        except (TypeError, ValueError) as exc:
            raise ApplicationError(
                message=(
                    "Embedding provider returned "
                    "non-numeric values."
                ),
                code="embedding_provider_invalid_values",
                status_code=502,
            ) from exc