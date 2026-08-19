from __future__ import annotations

from dataclasses import dataclass

import httpx

from app.core.exceptions import ApplicationError
from app.knowledge_engine.domain.provider_interfaces import EmbeddingProvider


@dataclass(slots=True)
class OpenRouterEmbeddingsProvider(EmbeddingProvider):
    settings: object

    def embed_query(self, text: str) -> list[float]:
        normalized = text.strip()
        if not normalized:
            raise ApplicationError(
                message="Embedding text cannot be empty.",
                code="embedding_text_empty",
                status_code=400,
            )

        api_key = getattr(self.settings, "api_key", "").strip()
        if not api_key:
            raise ApplicationError(
                message="OpenRouter API key is not configured.",
                code="openrouter_api_key_missing",
                status_code=500,
            )

        base_url = getattr(
            self.settings,
            "base_url",
            "https://openrouter.ai/api/v1",
        ).rstrip("/")

        model = getattr(
            self.settings,
            "embedding_model",
            "qwen/qwen3-embedding-8b",
        )

        dimensions = int(
            getattr(
                self.settings,
                "embedding_dimensions",
                1024,
            )
        )

        timeout = float(
            getattr(
                self.settings,
                "provider_timeout_seconds",
                30.0,
            )
        )

        url = f"{base_url}/embeddings"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": model,
            "input": normalized,
        }

        try:
            response = httpx.post(
                url,
                json=payload,
                headers=headers,
                timeout=timeout,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise ApplicationError(
                message="OpenRouter embeddings request failed.",
                code="embedding_provider_failed",
                status_code=502,
            ) from exc

        try:
            response_payload = response.json()
            embedding = response_payload["data"][0]["embedding"]
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise ApplicationError(
                message="OpenRouter embeddings returned an invalid response.",
                code="embedding_provider_invalid_response",
                status_code=502,
            ) from exc

        if not isinstance(embedding, list) or not embedding:
            raise ApplicationError(
                message="OpenRouter embeddings returned an empty vector.",
                code="embedding_provider_empty_response",
                status_code=502,
            )

        return embedding