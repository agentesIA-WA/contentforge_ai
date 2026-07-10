"""Prompt model for tracking agent instructions and AI responses."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey, Index, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base import UUIDTimestampMixin


class Prompt(UUIDTimestampMixin, Base):
    """Prompt sent or prepared by an agent during content generation."""

    __tablename__ = "prompts"
    __table_args__ = (
        CheckConstraint(
            "agente IN ('brand', 'planner', 'writer', 'designer', 'reviewer', 'publisher', 'analytics')",
            name="ck_prompts_agente",
        ),
        CheckConstraint(
            "status IN ('criado', 'enviado', 'respondido', 'falhou')",
            name="ck_prompts_status",
        ),
        Index("ix_prompts_empresa_agente", "empresa_id", "agente"),
    )

    empresa_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("empresas.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    post_id: Mapped[UUID | None] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("posts.id", ondelete="SET NULL"),
        index=True,
    )
    agente: Mapped[str] = mapped_column(Text, nullable=False)
    tipo: Mapped[str] = mapped_column(Text, nullable=False)
    conteudo: Mapped[str] = mapped_column(Text, nullable=False)
    parametros: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
    )
    modelo_ia: Mapped[str | None] = mapped_column(Text)
    resposta: Mapped[dict[str, Any] | None] = mapped_column(JSONB)
    status: Mapped[str] = mapped_column(Text, default="criado", nullable=False)

    empresa: Mapped["Empresa"] = relationship(back_populates="prompts")
    post: Mapped["Post | None"] = relationship(back_populates="prompts")
    midias: Mapped[list["Midia"]] = relationship(back_populates="prompt")

