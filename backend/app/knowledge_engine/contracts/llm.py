from __future__ import annotations

from abc import ABC, abstractmethod


class LlmContract(ABC):
    @abstractmethod
    def generate_text(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        raise NotImplementedError