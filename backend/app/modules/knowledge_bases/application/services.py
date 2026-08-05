from __future__ import annotations

from dataclasses import dataclass

from app.core.exceptions import ApplicationError
from app.modules.knowledge_bases.application.commands import (
    ActivateKnowledgeBaseCommand,
    CreateKnowledgeBaseCommand,
    DeactivateKnowledgeBaseCommand,
    UpdateKnowledgeBaseCommand,
)
from app.modules.knowledge_bases.application.dto import KnowledgeBaseDto
from app.modules.knowledge_bases.application.queries import (
    GetKnowledgeBaseByApplicationIdQuery,
    GetKnowledgeBaseByIdQuery,
    ListKnowledgeBasesQuery,
)
from app.modules.knowledge_bases.domain.entities import KnowledgeBase
from app.modules.knowledge_bases.domain.policies import (
    ensure_single_knowledge_base_per_application,
    normalize_knowledge_base_description,
)
from app.modules.knowledge_bases.domain.repository_interfaces import KnowledgeBaseRepositoryInterface
from app.modules.knowledge_bases.domain.value_objects import KnowledgeBaseName, KnowledgeBaseStatus


@dataclass(slots=True)
class KnowledgeBaseApplicationService:
    knowledge_base_repository: KnowledgeBaseRepositoryInterface

    def create(self, command: CreateKnowledgeBaseCommand) -> KnowledgeBaseDto:
        existing = self.knowledge_base_repository.get_by_application_id(command.application_id)
        ensure_single_knowledge_base_per_application(
            application_id=command.application_id,
            existing_knowledge_base_id=None if existing is None else existing.id,
        )

        created = self.knowledge_base_repository.create(
            application_id=command.application_id,
            name=KnowledgeBaseName(command.name).value,
            description=normalize_knowledge_base_description(command.description),
            status=KnowledgeBaseStatus(command.status).value,
        )
        return self._to_dto(created)

    def get_by_id(self, query: GetKnowledgeBaseByIdQuery) -> KnowledgeBaseDto:
        knowledge_base = self.knowledge_base_repository.get_by_id(query.knowledge_base_id)
        if knowledge_base is None:
            raise ApplicationError(
                message="Knowledge base not found.",
                code="knowledge_base_not_found",
                status_code=404,
            )
        return self._to_dto(knowledge_base)

    def get_by_application_id(
        self,
        query: GetKnowledgeBaseByApplicationIdQuery,
    ) -> KnowledgeBaseDto:
        knowledge_base = self.knowledge_base_repository.get_by_application_id(query.application_id)
        if knowledge_base is None:
            raise ApplicationError(
                message="Knowledge base not found.",
                code="knowledge_base_not_found",
                status_code=404,
            )
        return self._to_dto(knowledge_base)

    def list(self, query: ListKnowledgeBasesQuery) -> list[KnowledgeBaseDto]:
        status = None if query.status is None else KnowledgeBaseStatus(query.status).value
        return [
            self._to_dto(item)
            for item in self.knowledge_base_repository.list(status=status)
        ]

    def update(self, command: UpdateKnowledgeBaseCommand) -> KnowledgeBaseDto:
        existing = self.knowledge_base_repository.get_by_id(command.knowledge_base_id)
        if existing is None:
            raise ApplicationError(
                message="Knowledge base not found.",
                code="knowledge_base_not_found",
                status_code=404,
            )

        updated = self.knowledge_base_repository.update(
            knowledge_base_id=command.knowledge_base_id,
            name=KnowledgeBaseName(command.name).value,
            description=normalize_knowledge_base_description(command.description),
            status=KnowledgeBaseStatus(command.status).value,
        )
        return self._to_dto(updated)

    def activate(self, command: ActivateKnowledgeBaseCommand) -> KnowledgeBaseDto:
        existing = self.knowledge_base_repository.get_by_id(command.knowledge_base_id)
        if existing is None:
            raise ApplicationError(
                message="Knowledge base not found.",
                code="knowledge_base_not_found",
                status_code=404,
            )

        updated = self.knowledge_base_repository.update(
            knowledge_base_id=existing.id,
            name=existing.name,
            description=existing.description,
            status="active",
        )
        return self._to_dto(updated)

    def deactivate(self, command: DeactivateKnowledgeBaseCommand) -> KnowledgeBaseDto:
        existing = self.knowledge_base_repository.get_by_id(command.knowledge_base_id)
        if existing is None:
            raise ApplicationError(
                message="Knowledge base not found.",
                code="knowledge_base_not_found",
                status_code=404,
            )

        updated = self.knowledge_base_repository.update(
            knowledge_base_id=existing.id,
            name=existing.name,
            description=existing.description,
            status="inactive",
        )
        return self._to_dto(updated)

    def _to_dto(self, knowledge_base: KnowledgeBase) -> KnowledgeBaseDto:
        return KnowledgeBaseDto(
            id=knowledge_base.id,
            application_id=knowledge_base.application_id,
            name=knowledge_base.name,
            description=knowledge_base.description,
            status=knowledge_base.status,
            created_at=knowledge_base.created_at,
            updated_at=knowledge_base.updated_at,
        )