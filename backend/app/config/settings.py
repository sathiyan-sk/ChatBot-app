from __future__ import annotations

from dataclasses import dataclass
import os
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


def load_settings() -> Settings:
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
                "postgresql+psycopg2://postgres:pfEuZ2Zz3OII0oiN@db.qrmoeqkwmglnsjzacmox.supabase.co:5432/postgres?sslmode=require",
            ),
        ),
        providers=ProviderSettings(
            llm=os.getenv("LLM_PROVIDER", "ollama"),
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
                "docling",
            ),
        ),
        storage=StorageSettings(
            supabase_url=os.environ["SUPABASE_URL"],
            supabase_bucket_name=os.environ[
                "SUPABASE_BUCKET_NAME"
            ],
            supabase_service_role_key=os.environ[
                "SUPABASE_SERVICE_ROLE_KEY"
            ],
            provider_timeout_seconds=float(
                os.getenv(
                    "PROVIDER_TIMEOUT_SECONDS",
                    "30",
                )
            ),
        ),
    )


def get_settings() -> Settings:
    return load_settings()