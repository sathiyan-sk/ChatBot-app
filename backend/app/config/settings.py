from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(slots=True, frozen=True)
class AppSettings:
    app_name: str
    app_version: str
    app_env: str


@dataclass(slots=True, frozen=True)
class DatabaseSettings:
    url: str


@dataclass(slots=True, frozen=True)
class ProviderSettings:
    llm: str
    embeddings: str
    vector: str
    storage: str
    parsing: str


@dataclass(slots=True, frozen=True)
class Settings:
    app: AppSettings
    database: DatabaseSettings
    providers: ProviderSettings


def load_settings() -> Settings:
    return Settings(
        app=AppSettings(
            app_name=os.getenv("APP_NAME", "AI Knowledge Platform Backend"),
            app_version=os.getenv("APP_VERSION", "0.1.0"),
            app_env=os.getenv("APP_ENV", "development"),
        ),
        database=DatabaseSettings(
            url=os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/ai_knowledge_platform"),
        ),
        providers=ProviderSettings(
            llm=os.getenv("LLM_PROVIDER", "ollama"),
            embeddings=os.getenv("EMBEDDING_PROVIDER", "ollama"),
            vector=os.getenv("VECTOR_PROVIDER", "pgvector"),
            storage=os.getenv("STORAGE_PROVIDER", "supabase"),
            parsing=os.getenv("PARSING_PROVIDER", "docling"),
        ),
    )