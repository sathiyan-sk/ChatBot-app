from __future__ import annotations

from dataclasses import dataclass

from app.config.settings import ProviderSettings


@dataclass(frozen=True, slots=True)
class ActiveProviders:
    llm: str
    embeddings: str
    vector: str
    storage: str
    parsing: str


def build_active_providers(settings: ProviderSettings) -> ActiveProviders:
    return ActiveProviders(
        llm=settings.active_llm_provider,
        embeddings=settings.active_embedding_provider,
        vector=settings.active_vector_provider,
        storage=settings.active_storage_provider,
        parsing=settings.active_parsing_provider,
    )