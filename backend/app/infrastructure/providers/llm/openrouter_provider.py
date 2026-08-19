from __future__ import annotations

from dataclasses import dataclass

import httpx

from app.core.exceptions import ApplicationError
from app.knowledge_engine.domain.provider_interfaces import LlmProvider


@dataclass(slots=True)
class OpenRouterLlmProvider(LlmProvider):
    settings: object

    def generate(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        normalized_system = system_prompt.strip()
        normalized_user = user_prompt.strip()

        if not normalized_user:
            raise ApplicationError(
                message="LLM user prompt cannot be empty.",
                code="llm_prompt_empty",
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
            "model",
            "google/gemma-4-26b-a4b-it:free",
        )

        temperature = float(
            getattr(
                self.settings,
                "temperature",
                0.2,
            )
        )

        messages: list[dict[str, str]] = []
        if normalized_system:
            messages.append({"role": "system", "content": normalized_system})
        messages.append({"role": "user", "content": normalized_user})

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "stream": False,
        }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "AI Knowledge Platform",
        }

        timeout = float(
            getattr(
                self.settings,
                "provider_timeout_seconds",
                30.0,
            )
        )

        try:
            response = httpx.post(
                f"{base_url}/chat/completions",
                json=payload,
                headers=headers,
                timeout=timeout,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise ApplicationError(
                message="OpenRouter LLM provider request failed.",
                code="openrouter_provider_failed",
                status_code=502,
            ) from exc

        try:
            response_payload = response.json()
            generated_text = (
                response_payload["choices"][0]
                ["message"]["content"]
            )
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise ApplicationError(
                message="OpenRouter provider returned an invalid response.",
                code="openrouter_provider_invalid_response",
                status_code=502,
            ) from exc

        if not isinstance(generated_text, str) or not generated_text.strip():
            raise ApplicationError(
                message="OpenRouter provider returned empty response text.",
                code="openrouter_provider_empty_response",
                status_code=502,
            )

        return generated_text.strip()