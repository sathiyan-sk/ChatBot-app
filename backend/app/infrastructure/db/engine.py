from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from app.config.database import build_database_url, is_sqlite_database
from app.config.settings import DatabaseSettings


def create_database_engine(settings: DatabaseSettings) -> Engine:
    engine_kwargs: dict[str, object] = {
        "echo": settings.database_echo,
        "pool_pre_ping": True,
    }

    if not is_sqlite_database(settings):
        engine_kwargs.update(
            {
                "pool_size": settings.database_pool_size,
                "max_overflow": settings.database_max_overflow,
                "pool_timeout": settings.database_pool_timeout,
                "pool_recycle": settings.database_pool_recycle,
            }
        )

    return create_engine(build_database_url(settings), **engine_kwargs)
    