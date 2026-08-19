from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.dependencies import get_knowledge_ingestion_pipeline
from app.api.error_handlers import register_exception_handlers
from app.api.router import api_router
from app.composition import build_application_container
from app.config.settings import get_settings
from app.infrastructure.db.session import create_session_factory
from app.infrastructure.providers.vector.pgvector_provider import PgVectorProvider


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    session_factory = create_session_factory(settings.database.url)

    app.state.settings = settings
    app.state.session_factory = session_factory

    # Ensure vector store schema exists before serving requests
    session = app.state.session_factory()
    try:
        vector_provider = PgVectorProvider(settings=settings, session=session)
        vector_provider.ensure_schema()
    finally:
        session.close()

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

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "https://growthsphere.online",
            "http://localhost:5500",
            "http://localhost:3000",
            "http://localhost:5173",
            "http://localhost:5174",
            # file:// pages send "Origin: null" — allowed so the embeddable
            # widget can be tested directly from a local HTML file on disk.
            "null",
        ],
        allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "X-Widget-Key", "X-API-Key", "Authorization"],
        expose_headers=["Content-Type", "X-Widget-Key"],
    )

    register_exception_handlers(app)
    app.include_router(api_router)
    # Serve the embeddable widget static assets (widget.js, widget.css) so that
    # client websites can load the widget from the backend origin - the same
    # origin they already use for API calls.
    static_dir = Path(__file__).resolve().parent.parent / "static"
    if static_dir.exists():
        app.mount("/widget", StaticFiles(directory=static_dir / "widget"), name="widget")

    @app.get("/health", tags=["Health"])
    def health_check() -> dict[str, str]:
        return {"status": "OK"}

    return app


app = create_app()