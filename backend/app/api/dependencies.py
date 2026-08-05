from __future__ import annotations

from collections.abc import Generator

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from app.config.settings import Settings
from app.infrastructure.providers.embeddings.nomic_provider import NomicEmbeddingsProvider
from app.infrastructure.providers.llm.ollama_provider import OllamaLlmProvider
from app.infrastructure.providers.parsing.docling_provider import DoclingParsingProvider
from app.infrastructure.providers.parsing.html_parsing_provider import HtmlParsingProvider
from app.infrastructure.providers.parsing.ocr_provider import OcrParsingProvider
from app.infrastructure.providers.storage.supabase_storage_provider import SupabaseStorageProvider
from app.infrastructure.providers.vector.pgvector_provider import PgVectorProvider
from app.modules.chat.application.services import ChatApplicationService
from app.modules.conversations.application.services import ConversationApplicationService
from app.modules.conversations.infrastructure.repositories import (
    SqlAlchemyConversationRepository,
    SqlAlchemyMessageRepository,
)
from app.modules.documents.application.services import DocumentApplicationService
from app.modules.documents.infrastructure.repositories import SqlAlchemyDocumentRepository
from app.modules.knowledge_bases.application.services import KnowledgeBaseApplicationService
from app.modules.knowledge_bases.infrastructure.repositories import SqlAlchemyKnowledgeBaseRepository
from app.modules.settings.application.services import SettingsApplicationService
from app.modules.settings.infrastructure.repositories import SqlAlchemySettingsRepository
from app.modules.widgets.application.services import WidgetApplicationService
from app.modules.widgets.infrastructure.repositories import SqlAlchemyWidgetRepository
from app.knowledge_engine.generation.citation_builder import CitationBuilder
from app.knowledge_engine.generation.prompt_builder import PromptBuilder
from app.knowledge_engine.generation.response_formatter import ResponseFormatter
from app.knowledge_engine.generation.response_generator import ResponseGenerator
from app.knowledge_engine.ingestion.chunker import IntelligentChunkGenerator
from app.knowledge_engine.ingestion.embedding_generator import EmbeddingGenerator
from app.knowledge_engine.ingestion.metadata_enricher import MetadataEnricher
from app.knowledge_engine.ingestion.normalizer import DocumentNormalizer
from app.knowledge_engine.ingestion.parsers.html_parser import HtmlDocumentParser
from app.knowledge_engine.ingestion.parsers.ocr_parser import OcrDocumentParser
from app.knowledge_engine.ingestion.parsers.structured_document_parser import StructuredDocumentParser
from app.knowledge_engine.ingestion.source_loaders.csv_loader import CsvSourceLoader
from app.knowledge_engine.ingestion.source_loaders.file_loader import FileSourceLoader
from app.knowledge_engine.ingestion.source_loaders.website_loader import WebsiteSourceLoader
from app.knowledge_engine.ingestion.vector_indexer import VectorIndexer
from app.knowledge_engine.pipelines.knowledge_ingestion_pipeline import KnowledgeIngestionPipeline
from app.knowledge_engine.pipelines.question_answering_pipeline import QuestionAnsweringPipeline
from app.knowledge_engine.retrieval.conversation_context_builder import ConversationContextBuilder
from app.knowledge_engine.retrieval.hybrid_retriever import HybridRetriever
from app.knowledge_engine.retrieval.metadata_filter import MetadataFilter
from app.knowledge_engine.retrieval.query_embedder import QueryEmbedder
from app.knowledge_engine.retrieval.reranker import Reranker


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


def get_session(request: Request) -> Generator[Session, None, None]:
    session_factory = request.app.state.session_factory
    session: Session = session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_knowledge_base_application_service(
    session: Session = Depends(get_session),
) -> KnowledgeBaseApplicationService:
    return KnowledgeBaseApplicationService(
        knowledge_base_repository=SqlAlchemyKnowledgeBaseRepository(session=session),
    )


def get_document_application_service(
    session: Session = Depends(get_session),
) -> DocumentApplicationService:
    return DocumentApplicationService(
        document_repository=SqlAlchemyDocumentRepository(session=session),
        knowledge_base_repository=SqlAlchemyKnowledgeBaseRepository(session=session),
    )


def get_widget_application_service(
    session: Session = Depends(get_session),
) -> WidgetApplicationService:
    return WidgetApplicationService(
        widget_repository=SqlAlchemyWidgetRepository(session=session),
    )


def get_settings_application_service(
    session: Session = Depends(get_session),
) -> SettingsApplicationService:
    return SettingsApplicationService(
        settings_repository=SqlAlchemySettingsRepository(session=session),
    )


def get_conversation_application_service(
    session: Session = Depends(get_session),
) -> ConversationApplicationService:
    return ConversationApplicationService(
        conversation_repository=SqlAlchemyConversationRepository(session=session),
        message_repository=SqlAlchemyMessageRepository(session=session),
    )


def get_question_answering_pipeline(
    request: Request,
    session: Session = Depends(get_session),
) -> QuestionAnsweringPipeline:
    settings = get_settings(request)
    embeddings_provider = NomicEmbeddingsProvider(settings=settings)
    llm_provider = OllamaLlmProvider(settings=settings)
    vector_provider = PgVectorProvider(settings=settings, session=session)

    return QuestionAnsweringPipeline(
        conversation_context_builder=ConversationContextBuilder(),
        query_embedder=QueryEmbedder(embeddings_contract=embeddings_provider),
        hybrid_retriever=HybridRetriever(vector_store_contract=vector_provider),
        metadata_filter=MetadataFilter(),
        reranker=Reranker(),
        prompt_builder=PromptBuilder(),
        response_generator=ResponseGenerator(llm_contract=llm_provider),
        citation_builder=CitationBuilder(),
        response_formatter=ResponseFormatter(),
    )


def get_chat_application_service(
    request: Request,
    session: Session = Depends(get_session),
    conversation_service: ConversationApplicationService = Depends(get_conversation_application_service),
    question_answering_pipeline: QuestionAnsweringPipeline = Depends(get_question_answering_pipeline),
) -> ChatApplicationService:
    return ChatApplicationService(
        knowledge_base_repository=SqlAlchemyKnowledgeBaseRepository(session=session),
        document_repository=SqlAlchemyDocumentRepository(session=session),
        conversation_service=conversation_service,
        question_answering_pipeline=question_answering_pipeline,
    )


def get_knowledge_ingestion_pipeline(
    source_type: str,
    request: Request,
    session: Session = Depends(get_session),
) -> KnowledgeIngestionPipeline:
    settings = get_settings(request)
    storage_provider = SupabaseStorageProvider(settings=settings)
    embeddings_provider = NomicEmbeddingsProvider(settings=settings)
    vector_provider = PgVectorProvider(settings=settings, session=session)

    if source_type == "website":
        source_loader = WebsiteSourceLoader()
        parser = HtmlDocumentParser(parsing_contract=HtmlParsingProvider(settings=settings))
    elif source_type == "csv":
        source_loader = CsvSourceLoader(storage_contract=storage_provider)
        parser = StructuredDocumentParser(parsing_contract=DoclingParsingProvider())
    elif source_type == "image":
        source_loader = FileSourceLoader(storage_contract=storage_provider)
        parser = OcrDocumentParser(parsing_contract=OcrParsingProvider(settings=settings))
    else:
        source_loader = FileSourceLoader(storage_contract=storage_provider)
        parser = StructuredDocumentParser(parsing_contract=DoclingParsingProvider())

    return KnowledgeIngestionPipeline(
        source_loader=source_loader,
        parser=parser,
        normalizer=DocumentNormalizer(),
        chunk_generator=IntelligentChunkGenerator(),
        metadata_enricher=MetadataEnricher(),
        embedding_generator=EmbeddingGenerator(embeddings_contract=embeddings_provider),
        vector_indexer=VectorIndexer(vector_store_contract=vector_provider),
    )