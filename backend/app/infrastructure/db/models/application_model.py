from __future__ import annotations

from sqlalchemy import Boolean, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.base import Base, TimestampMixin, UuidPrimaryKeyMixin


class ApplicationModel(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "applications"
    __table_args__ = (
        Index("ix_applications_name", "name"),
        Index("ix_applications_slug", "slug"),
        Index("ix_applications_is_active", "is_active"),
    )

    name: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    client_type: Mapped[str] = mapped_column(String(50), nullable=False)
    allowed_origins: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")

    knowledge_base = relationship(
        "KnowledgeBaseModel",
        back_populates="application",
        uselist=False,
        cascade="all, delete-orphan",
    )
    api_keys = relationship(
        "ApiKeyModel",
        back_populates="application",
        cascade="all, delete-orphan",
    )
    documents = relationship(
        "DocumentModel",
        back_populates="application",
        cascade="all, delete-orphan",
    )
    conversations = relationship(
        "ConversationModel",
        back_populates="application",
        cascade="all, delete-orphan",
    )
    widgets = relationship(
        "WidgetModel",
        back_populates="application",
        cascade="all, delete-orphan",
    )
    settings = relationship(
        "SettingsModel",
        back_populates="application",
        uselist=False,
        cascade="all, delete-orphan",
    )