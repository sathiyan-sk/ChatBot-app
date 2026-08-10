from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(slots=True, frozen=True)
class AppSettings:
    app_name: str
    app_version: str
    app_env: str


@dataclass(slots=True, frozen=True)
class DatabaseSettings:
    url: str


@dataclass(slots=True, frozen=True)
class StorageSettings:
    supabase_url: str
    supabase_bucket_name: str
    supabase_service_role_key: str
    provider_timeout_seconds: float


@dataclass(slots=True, frozen=True)
class OllamaSettings:
    base_url: str
    embedding_model_name: str
    llm_model_name: str
    provider_timeout_seconds: float


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
    storage: StorageSettings
    ollama: OllamaSettings

    # These fields are intentionally on the root Settings
    # object because PgVectorProvider expects:
    # settings.vector_store_table_name
    # settings.vector_store_dimension
    vector_store_table_name: str
    vector_store_dimension: int

    provider_timeout_seconds: float = 30.0
    http_user_agent: str = (
        "AI-Knowledge-Platform/1.0"
    )

def load_settings() -> Settings:
    provider_timeout_seconds = float(
        os.getenv(
            "PROVIDER_TIMEOUT_SECONDS",
            "30",
        )
    )

    ollama_timeout_seconds = float(
        os.getenv(
            "OLLAMA_TIMEOUT_SECONDS",
            str(provider_timeout_seconds),
        )
    )

    return Settings(
        app=AppSettings(
            app_name=os.getenv(
                "APP_NAME",
                "AI Knowledge Platform Backend",
            ),
            app_version=os.getenv(
                "APP_VERSION",
                "0.1.0",
            ),
            app_env=os.getenv(
                "APP_ENV",
                "development",
            ),
        ),
        database=DatabaseSettings(
            url=os.getenv(
                "DATABASE_URL",
                (
                    "postgresql+psycopg2://"
                    "postgres:pfEuZ2Zz3OII0oiN@"
                    "db.qrmoeqkwmglnsjzacmox.supabase.co:"
                    "5432/postgres?sslmode=require"
                ),
            ),
        ),
        providers=ProviderSettings(
            llm=os.getenv(
                "LLM_PROVIDER",
                "ollama",
            ),
            embeddings=os.getenv(
                "EMBEDDING_PROVIDER",
                "ollama",
            ),
            vector=os.getenv(
                "VECTOR_PROVIDER",
                "pgvector",
            ),
            storage=os.getenv(
                "STORAGE_PROVIDER",
                "supabase",
            ),
            parsing=os.getenv(
                "PARSING_PROVIDER",
                "pymupdf",
            ),
        ),
        storage=StorageSettings(
            supabase_url=os.environ[
                "SUPABASE_URL"
            ],
            supabase_bucket_name=os.environ[
                "SUPABASE_BUCKET_NAME"
            ],
            supabase_service_role_key=os.environ[
                "SUPABASE_SERVICE_ROLE_KEY"
            ],
            provider_timeout_seconds=(
                provider_timeout_seconds
            ),
        ),
        ollama=OllamaSettings(
            base_url=os.getenv(
                "OLLAMA_BASE_URL",
                "http://127.0.0.1:11434",
            ),
            embedding_model_name=os.getenv(
                "EMBEDDING_MODEL_NAME",
                "nomic-embed-text",
            ),
            llm_model_name=os.getenv(
                "LLM_MODEL_NAME",
                "qwen2.5:7b",
            ),
            provider_timeout_seconds=(
                ollama_timeout_seconds
            ),
        ),
        vector_store_table_name=os.getenv(
            "VECTOR_STORE_TABLE_NAME",
            "document_chunks",
        ),
        vector_store_dimension=int(
            os.getenv(
                "VECTOR_STORE_DIMENSION",
                "768",
            )
        ),
        provider_timeout_seconds=provider_timeout_seconds,
        http_user_agent=os.getenv("HTTP_USER_AGENT", "AI-Knowledge-Platform/1.0",),
    )


def get_settings() -> Settings:
    return load_settings()