"""Publication model for scheduled and completed social posts."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base import UUIDTimestampMixin


class Publicacao(UUIDTimestampMixin, Base):
    """Publication attempt for a post on a social platform."""

    __tablename__ = "publicacoes"
    __table_args__ = (
        CheckConstraint(
            "plataforma IN ('instagram')",
            name="ck_publicacoes_plataforma",
        ),
        CheckConstraint(
            "status IN ('pendente', 'agendada', 'publicada', 'falhou', 'cancelada')",
            name="ck_publicacoes_status",
        ),
        UniqueConstraint("plataforma", "id_externo", name="uq_publicacoes_plataforma_id_externo"),
        Index("ix_publicacoes_empresa_status", "empresa_id", "status"),
        Index(
            "ix_publicacoes_agendadas",
            "empresa_id",
            "agendado_para",
            postgresql_where=text("status = 'agendada'"),
        ),
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
    plataforma: Mapped[str] = mapped_column(Text, default="instagram", nullable=False)
    id_externo: Mapped[str | None] = mapped_column(Text)
    permalink: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Text, default="pendente", nullable=False)
    agendado_para: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    publicado_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    erro_mensagem: Mapped[str | None] = mapped_column(Text)
    payload_publicacao: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
    )

    empresa: Mapped["Empresa"] = relationship(back_populates="publicacoes")
    post: Mapped["Post"] = relationship(back_populates="publicacoes")
    metricas: Mapped[list["Metrica"]] = relationship(
        back_populates="publicacao",
        cascade="all, delete-orphan",
    )

