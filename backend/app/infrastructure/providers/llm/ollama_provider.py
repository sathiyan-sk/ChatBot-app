from __future__ import annotations

from dataclasses import dataclass

import httpx

from app.core.exceptions import ApplicationError
from app.knowledge_engine.contracts.llm import (
    LlmContract,
)


@dataclass(slots=True)
class OllamaLlmProvider(LlmContract):
    settings: object

    def generate_text(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        normalized_system_prompt = (
            system_prompt.strip()
        )

        normalized_user_prompt = (
            user_prompt.strip()
        )

        if not normalized_user_prompt:
            raise ApplicationError(
                message="LLM user prompt cannot be empty.",
                code="llm_prompt_empty",
                status_code=400,
            )

        ollama_settings = getattr(
            self.settings,
            "ollama",
            None,
        )

        if ollama_settings is None:
            raise ApplicationError(
                message="Ollama settings are missing.",
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
            "llm_model_name",
            None,
        )

        timeout_seconds = getattr(
            ollama_settings,
            "provider_timeout_seconds",
            120.0,
        )

        if not base_url:
            raise ApplicationError(
                message="Ollama base URL is missing.",
                code="ollama_base_url_missing",
                status_code=503,
            )

        if not model_name:
            raise ApplicationError(
                message="Ollama LLM model is missing.",
                code="ollama_model_name_missing",
                status_code=503,
            )

        url = (
            f"{base_url.rstrip('/')}"
            "/api/chat"
        )

        payload = {
            "model": model_name,
            "stream": False,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        normalized_system_prompt
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        normalized_user_prompt
                    ),
                },
            ],
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
                    "Ollama chat request failed with "
                    f"status {exc.response.status_code}."
                ),
                code="llm_provider_failed",
                status_code=502,
            ) from exc

        except httpx.HTTPError as exc:
            raise ApplicationError(
                message=(
                    "Could not connect to Ollama "
                    "chat provider."
                ),
                code="llm_provider_unavailable",
                status_code=502,
            ) from exc

        try:
            response_payload = response.json()

        except ValueError as exc:
            raise ApplicationError(
                message=(
                    "Ollama returned invalid JSON."
                ),
                code="llm_provider_invalid_json",
                status_code=502,
            ) from exc

        message = response_payload.get(
            "message",
        )

        generated_text = (
            message.get("content")
            if isinstance(message, dict)
            else None
        )

        if not isinstance(
            generated_text,
            str,
        ) or not generated_text.strip():
            raise ApplicationError(
                message=(
                    "Ollama returned empty response text."
                ),
                code="llm_provider_invalid_response",
                status_code=502,
            )

        return generated_text.strip()