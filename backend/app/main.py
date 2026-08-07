from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.dependencies import get_knowledge_ingestion_pipeline
from app.api.error_handlers import register_exception_handlers
from app.api.router import api_router
from app.composition import build_application_container
from app.config.settings import get_settings
from app.infrastructure.db.session import create_session_factory


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    session_factory = create_session_factory(settings.database.url)

    app.state.settings = settings
    app.state.session_factory = session_factory
    app.state.container = build_application_container(
        settings=settings,
        session_factory=session_factory,
    )
    app.state.knowledge_ingestion_pipeline_factory = (
        get_knowledge_ingestion_pipeline
    )

    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="AI Knowledge Platform Backend",
        version="1.0.0",
        lifespan=lifespan,
    )

    register_exception_handlers(app)
    app.include_router(api_router)

    @app.get("/health", tags=["Health"])
    def health_check() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()