from __future__ import annotations

from dataclasses import dataclass

import httpx

from app.core.exceptions import ApplicationError
from app.knowledge_engine.contracts.llm import LlmContract


@dataclass(slots=True)
class OllamaLlmProvider(LlmContract):
    settings: object

    def generate_text(self, prompt: str) -> str:
        normalized_prompt = prompt.strip()
        if not normalized_prompt:
            raise ApplicationError(
                message="LLM prompt cannot be empty.",
                code="llm_prompt_empty",
                status_code=400,
            )

        url = f"{self.settings.ollama_base_url.rstrip('/')}/api/generate"
        payload = {
            "model": self.settings.llm_model_name,
            "prompt": normalized_prompt,
            "stream": False,
            "options": {
                "temperature": self.settings.llm_temperature,
            },
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
                message="LLM provider request failed.",
                code="llm_provider_failed",
                status_code=502,
            ) from exc

        response_payload = response.json()
        generated_text = response_payload.get("response")
        if not isinstance(generated_text, str) or not generated_text.strip():
            raise ApplicationError(
                message="LLM provider returned invalid response text.",
                code="llm_provider_invalid_response",
                status_code=502,
            )

        return generated_text.strip()