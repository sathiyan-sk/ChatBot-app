from __future__ import annotations

from dataclasses import dataclass

from app.knowledge_engine.contracts.llm import LlmContract


@dataclass(slots=True)
class ResponseGenerator:
    llm_contract: LlmContract

    def generate(self, *, system_prompt: str, user_prompt: str) -> str:
        return self.llm_contract.generate_text(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )