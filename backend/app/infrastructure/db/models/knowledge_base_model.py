from __future__ import annotations

from uuid import UUID as PyUUID

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Index,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.infrastructure.db.base import (
    Base,
    TimestampMixin,
    UuidPrimaryKeyMixin,
)


class KnowledgeBaseModel(
    UuidPrimaryKeyMixin,
    TimestampMixin,
    Base,
):
    __tablename__ = "knowledge_bases"

    __table_args__ = (
        Index(
            "ix_knowledge_bases_application_id",
            "application_id",
        ),
        Index(
            "ix_knowledge_bases_status",
            "status",
        ),
        Index(
            "ix_knowledge_bases_is_active",
            "is_active",
        ),
        Index(
            "ux_knowledge_bases_slug",
            "slug",
            unique=True,
        ),
    )

    application_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "applications.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(180),
        nullable=False,
        unique=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="ready",
        server_default="ready",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )

    application = relationship(
        "ApplicationModel",
        back_populates="knowledge_base",
    )

    documents = relationship(
        "DocumentModel",
        back_populates="knowledge_base",
        cascade="all, delete-orphan",
    )