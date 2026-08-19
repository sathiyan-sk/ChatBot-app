from __future__ import annotations

from app.api.dependencies import ResponseFormatter
from app.knowledge_engine.domain.provider_interfaces import LlmProvider


class ResponseGenerator:
    __slots__ = ("llm_contract", "response_formatter")

    def __init__(self, llm_contract: LlmProvider):
        self.llm_contract = llm_contract
        self.response_formatter = ResponseFormatter()

    def generate(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        conversation_context: list[dict[str, str]] | None = None,
    ) -> str:
        return self.llm_contract.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )