from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.base import Base, TimestampMixin, UuidPrimaryKeyMixin


class WidgetModel(UuidPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "widgets"
    __table_args__ = (
        Index("ix_widgets_application_id", "application_id"),
        Index("ix_widgets_is_enabled", "is_enabled"),
    )

    application_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=False,
    )
    display_name: Mapped[str] = mapped_column(String(150), nullable=False)
    theme: Mapped[str] = mapped_column(String(50), nullable=False, default="light", server_default="light")
    launcher_label: Mapped[str | None] = mapped_column(String(100), nullable=True)
    welcome_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    placeholder_text: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")

    application = relationship("ApplicationModel", back_populates="widgets")