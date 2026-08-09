from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.orm import Session, sessionmaker

from app.config.settings import Settings
from app.infrastructure.providers.embeddings.nomic_provider import NomicEmbeddingsProvider
from app.infrastructure.providers.llm.ollama_provider import OllamaLlmProvider
from app.infrastructure.providers.vector.pgvector_provider import PgVectorProvider
from app.modules.applications.infrastructure.repositories import (
    ApplicationSqlAlchemyRepository,
)
from app.modules.question_answering.application.services import ChatApplicationService
from app.modules.conversations.application.services import ConversationApplicationService
from app.modules.conversations.infrastructure.repositories import (
    SqlAlchemyConversationRepository,
    SqlAlchemyMessageRepository,
)
from app.modules.documents.infrastructure.repositories import SqlAlchemyDocumentRepository
from app.modules.knowledge_bases.infrastructure.repositories import SqlAlchemyKnowledgeBaseRepository
from app.knowledge_engine.generation.citation_builder import CitationBuilder
from app.knowledge_engine.generation.prompt_builder import PromptBuilder
from app.knowledge_engine.generation.response_formatter import ResponseFormatter
from app.knowledge_engine.generation.response_generator import ResponseGenerator
from app.knowledge_engine.pipelines.question_answering_pipeline import QuestionAnsweringPipeline
from app.knowledge_engine.retrieval.conversation_context_builder import ConversationContextBuilder
from app.knowledge_engine.retrieval.hybrid_retriever import HybridRetriever
from app.knowledge_engine.retrieval.metadata_filter import MetadataFilter
from app.knowledge_engine.retrieval.query_embedder import QueryEmbedder
from app.knowledge_engine.retrieval.reranker import Reranker


@dataclass(slots=True)
class ApplicationContainer:
    settings: Settings
    session_factory: sessionmaker
    application_repository: ApplicationSqlAlchemyRepository
    knowledge_base_repository: SqlAlchemyKnowledgeBaseRepository
    document_repository: SqlAlchemyDocumentRepository
    conversation_repository: SqlAlchemyConversationRepository
    message_repository: SqlAlchemyMessageRepository
    conversation_application_service: ConversationApplicationService
    question_answering_pipeline: QuestionAnsweringPipeline
    chat_application_service: ChatApplicationService


def build_application_container(
    *,
    settings: Settings,
    session_factory: sessionmaker,
) -> ApplicationContainer:
    session: Session = session_factory()

    application_repository = ApplicationSqlAlchemyRepository(session=session)
    knowledge_base_repository = SqlAlchemyKnowledgeBaseRepository(session=session)
    document_repository = SqlAlchemyDocumentRepository(session=session)
    conversation_repository = SqlAlchemyConversationRepository(session=session)
    message_repository = SqlAlchemyMessageRepository(session=session)

    conversation_application_service = ConversationApplicationService(
        conversation_repository=conversation_repository,
        message_repository=message_repository,
    )

    embeddings_contract = NomicEmbeddingsProvider(settings=settings)
    vector_store_contract = PgVectorProvider(settings=settings, session=session)
    llm_contract = OllamaLlmProvider(settings=settings)

    question_answering_pipeline = QuestionAnsweringPipeline(
        conversation_context_builder=ConversationContextBuilder(),
        query_embedder=QueryEmbedder(embeddings_contract=embeddings_contract),
        hybrid_retriever=HybridRetriever(vector_store_contract=vector_store_contract),
        metadata_filter=MetadataFilter(),
        reranker=Reranker(),
        prompt_builder=PromptBuilder(),
        response_generator=ResponseGenerator(llm_contract=llm_contract),
        citation_builder=CitationBuilder(),
        response_formatter=ResponseFormatter(),
    )

    chat_application_service = ChatApplicationService(
        knowledge_base_repository=knowledge_base_repository,
        document_repository=document_repository,
        conversation_service=conversation_application_service,
        question_answering_pipeline=question_answering_pipeline,
    )

    return ApplicationContainer(
        settings=settings,
        session_factory=session_factory,
        application_repository=application_repository,
        knowledge_base_repository=knowledge_base_repository,
        document_repository=document_repository,
        conversation_repository=conversation_repository,
        message_repository=message_repository,
        conversation_application_service=conversation_application_service,
        question_answering_pipeline=question_answering_pipeline,
        chat_application_service=chat_application_service,
    )