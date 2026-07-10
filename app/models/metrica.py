"""Analytics model for publication performance metrics."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Integer, Numeric, func
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base import UUIDTimestampMixin


class Metrica(UUIDTimestampMixin, Base):
    """Collected metrics for a publication on a social platform."""

    __tablename__ = "metricas"
    __table_args__ = (
        CheckConstraint("curtidas >= 0", name="ck_metricas_curtidas_nao_negativo"),
        CheckConstraint("comentarios >= 0", name="ck_metricas_comentarios_nao_negativo"),
        CheckConstraint("compartilhamentos >= 0", name="ck_metricas_compartilhamentos_nao_negativo"),
        CheckConstraint("alcance >= 0", name="ck_metricas_alcance_nao_negativo"),
        CheckConstraint("impressoes >= 0", name="ck_metricas_impressoes_nao_negativo"),
        CheckConstraint("taxa_engajamento >= 0", name="ck_metricas_taxa_engajamento_nao_negativo"),
        Index("ix_metricas_empresa_coletado_em", "empresa_id", "coletado_em"),
    )

    empresa_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("empresas.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    publicacao_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("publicacoes.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    curtidas: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    comentarios: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    compartilhamentos: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    alcance: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    impressoes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    taxa_engajamento: Mapped[Decimal] = mapped_column(
        Numeric(8, 4),
        default=0,
        nullable=False,
    )
    coletado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    empresa: Mapped["Empresa"] = relationship(back_populates="metricas")
    publicacao: Mapped["Publicacao"] = relationship(back_populates="metricas")

