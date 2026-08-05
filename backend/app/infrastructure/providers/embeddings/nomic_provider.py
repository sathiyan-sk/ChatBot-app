from __future__ import annotations

from dataclasses import dataclass

import httpx

from app.core.exceptions import ApplicationError
from app.knowledge_engine.contracts.embeddings import EmbeddingsContract


@dataclass(slots=True)
class NomicEmbeddingsProvider(EmbeddingsContract):
    settings: object

    def embed_query(self, text: str) -> list[float]:
        normalized_text = text.strip()
        if not normalized_text:
            raise ApplicationError(
                message="Embedding text cannot be empty.",
                code="embedding_text_empty",
                status_code=400,
            )

        url = f"{self.settings.ollama_base_url.rstrip('/')}/api/embeddings"
        payload = {
            "model": self.settings.embedding_model_name,
            "prompt": normalized_text,
        }

        try:
            response = httpx.post(
                url,
                json=payload,
                timeout=self.settings.provider_timeout_seconds,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise ApplicationError(
                message="Embedding provider request failed.",
                code="embedding_provider_failed",
                status_code=502,
            ) from exc

        response_payload = response.json()
        embedding = response_payload.get("embedding")
        if not isinstance(embedding, list) or not embedding:
            raise ApplicationError(
                message="Embedding provider returned invalid embedding output.",
                code="embedding_provider_invalid_response",
                status_code=502,
            )

        return [float(value) for value in embedding]