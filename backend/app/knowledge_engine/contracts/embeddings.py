from __future__ import annotations

from abc import ABC, abstractmethod


class EmbeddingsContract(ABC):
    @abstractmethod
    def embed_query(self, text: str) -> list[float]:
        raise NotImplementedError