from __future__ import annotations

from app.modules.knowledge_bases.application.commands import (
    ActivateKnowledgeBaseCommand,
    DeactivateKnowledgeBaseCommand,
    UpdateKnowledgeBaseCommand,
)
from app.modules.knowledge_bases.application.dto import (
    KnowledgeBaseDto,
)
from app.modules.knowledge_bases.application.queries import (
    GetKnowledgeBaseByApplicationIdQuery,
    GetKnowledgeBaseByIdQuery,
    ListKnowledgeBasesQuery,
)
from app.modules.knowledge_bases.domain.entities import (
    KnowledgeBase,
)


class KnowledgeBaseApplicationService:
    def __init__(
        self,
        knowledge_base_repository,
    ) -> None:
        self.knowledge_base_repository = (
            knowledge_base_repository
        )

    def list(
        self,
        query: ListKnowledgeBasesQuery,
    ) -> list[KnowledgeBaseDto]:
        status_value = getattr(query, "status", None)
        application_id = getattr(
            query,
            "application_id",
            None,
        )

        results = (
            self.knowledge_base_repository.list(
                application_id=application_id,
                status=status_value,
            )
        )

        return [
            self._to_dto(item)
            for item in results
        ]

    def get_by_id(
        self,
        query: GetKnowledgeBaseByIdQuery,
    ) -> KnowledgeBaseDto | None:
        result = (
            self.knowledge_base_repository.get_by_id(
                query.knowledge_base_id,
            )
        )

        if result is None:
            return None

        return self._to_dto(result)

    def get_by_application_id(
        self,
        query: GetKnowledgeBaseByApplicationIdQuery,
    ) -> KnowledgeBaseDto | None:
        result = (
            self.knowledge_base_repository
            .get_by_application_id(
                query.application_id,
            )
        )

        if result is None:
            return None

        return self._to_dto(result)

    def update(
        self,
        command: UpdateKnowledgeBaseCommand,
    ) -> KnowledgeBaseDto:
        knowledge_base = (
            self.knowledge_base_repository.get_by_id(
                command.knowledge_base_id,
            )
        )

        if knowledge_base is None:
            raise LookupError(
                "Knowledge base not found.",
            )

        updated = KnowledgeBase(
            id=knowledge_base.id,
            application_id=knowledge_base.application_id,
            name=command.name,
            slug=knowledge_base.slug,
            status=command.status,
            is_active=knowledge_base.is_active,
            created_at=knowledge_base.created_at,
            updated_at=knowledge_base.updated_at,
        )

        result = (
            self.knowledge_base_repository.update(
                updated,
            )
        )

        return self._to_dto(result)

    def activate(
        self,
        command: ActivateKnowledgeBaseCommand,
    ) -> KnowledgeBaseDto:
        knowledge_base = (
            self.knowledge_base_repository.get_by_id(
                command.knowledge_base_id,
            )
        )

        if knowledge_base is None:
            raise LookupError(
                "Knowledge base not found.",
            )

        updated = KnowledgeBase(
            id=knowledge_base.id,
            application_id=knowledge_base.application_id,
            name=knowledge_base.name,
            slug=knowledge_base.slug,
            status=knowledge_base.status,
            is_active=True,
            created_at=knowledge_base.created_at,
            updated_at=knowledge_base.updated_at,
        )

        result = (
            self.knowledge_base_repository.update(
                updated,
            )
        )

        return self._to_dto(result)

    def deactivate(
        self,
        command: DeactivateKnowledgeBaseCommand,
    ) -> KnowledgeBaseDto:
        knowledge_base = (
            self.knowledge_base_repository.get_by_id(
                command.knowledge_base_id,
            )
        )

        if knowledge_base is None:
            raise LookupError(
                "Knowledge base not found.",
            )

        updated = KnowledgeBase(
            id=knowledge_base.id,
            application_id=knowledge_base.application_id,
            name=knowledge_base.name,
            slug=knowledge_base.slug,
            status=knowledge_base.status,
            is_active=False,
            created_at=knowledge_base.created_at,
            updated_at=knowledge_base.updated_at,
        )

        result = (
            self.knowledge_base_repository.update(
                updated,
            )
        )

        return self._to_dto(result)

    @staticmethod
    def _to_dto(
        knowledge_base: KnowledgeBase,
    ) -> KnowledgeBaseDto:
        return KnowledgeBaseDto(
            id=knowledge_base.id,
            application_id=knowledge_base.application_id,
            name=knowledge_base.name,
            slug=knowledge_base.slug,
            status=knowledge_base.status,
            is_active=knowledge_base.is_active,
            created_at=knowledge_base.created_at,
            updated_at=knowledge_base.updated_at,
        )