from __future__ import annotations

from abc import ABC, abstractmethod


class StorageContract(ABC):
    @abstractmethod
    def download_text(self, storage_path: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def download_bytes(self, storage_path: str) -> bytes:
        raise NotImplementedError