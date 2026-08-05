from __future__ import annotations

from abc import ABC, abstractmethod

from app.modules.knowledge_bases.domain.entities import KnowledgeBase


class KnowledgeBaseRepositoryInterface(ABC):
    @abstractmethod
    def create(
        self,
        *,
        application_id: str,
        name: str,
        description: str | None,
        status: str,
    ) -> KnowledgeBase:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, knowledge_base_id: str) -> KnowledgeBase | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_application_id(self, application_id: str) -> KnowledgeBase | None:
        raise NotImplementedError

    @abstractmethod
    def list(self, *, status: str | None = None) -> list[KnowledgeBase]:
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        *,
        knowledge_base_id: str,
        name: str,
        description: str | None,
        status: str,
    ) -> KnowledgeBase:
        raise NotImplementedError