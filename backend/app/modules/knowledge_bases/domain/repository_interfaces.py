from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.knowledge_bases.domain.entities import (
    KnowledgeBase,
)


class KnowledgeBaseRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(
        self,
        knowledge_base_id: UUID | str,
    ) -> KnowledgeBase | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_slug(
        self,
        slug: str,
    ) -> KnowledgeBase | None:
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        knowledge_base: KnowledgeBase,
    ) -> KnowledgeBase:
        raise NotImplementedError

    @abstractmethod
    def get_by_application_id(
        self,
        application_id: UUID | str,
    ) -> KnowledgeBase | None:
        raise NotImplementedError

    @abstractmethod
    def list(
        self,
        application_id: UUID | str | None = None,
        status: str | None = None,
    ) -> list[KnowledgeBase]:
        raise NotImplementedError