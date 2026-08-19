from app.config.settings import get_settings
from app.infrastructure.providers.embeddings.openrouter_embeddings_provider import (
    OpenRouterEmbeddingsProvider,
)


def main() -> None:
    settings = get_settings()

    provider = OpenRouterEmbeddingsProvider(
        settings=settings.openrouter,
    )

    vector = provider.embed_query(
        "test embedding dimension",
    )

    print("Embedding model:", settings.openrouter.embedding_model)
    print("Actual dimension:", len(vector))


if __name__ == "__main__":
    main()