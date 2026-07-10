"""Media model for generated or uploaded creative assets."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey, Index, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base import UUIDTimestampMixin


class Midia(UUIDTimestampMixin, Base):
    """Image, video, or other asset attached to a post."""

    __tablename__ = "midias"
    __table_args__ = (
        CheckConstraint(
            "tipo IN ('imagem', 'video', 'audio', 'documento')",
            name="ck_midias_tipo",
        ),
        Index("ix_midias_empresa_tipo", "empresa_id", "tipo"),
    )

    empresa_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("empresas.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    post_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("posts.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    prompt_id: Mapped[UUID | None] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("prompts.id", ondelete="SET NULL"),
        index=True,
    )
    tipo: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[str | None] = mapped_column(Text)
    caminho_arquivo: Mapped[str | None] = mapped_column(Text)
    alt_text: Mapped[str | None] = mapped_column(Text)
    metadados: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
    )

    empresa: Mapped["Empresa"] = relationship(back_populates="midias")
    post: Mapped["Post"] = relationship(back_populates="midias")
    prompt: Mapped["Prompt | None"] = relationship(back_populates="midias")

