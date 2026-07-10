"""Service model for offerings sold by each business."""

from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Integer, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base import UUIDTimestampMixin


class Servico(UUIDTimestampMixin, Base):
    """Beauty service used as source material for content generation."""

    __tablename__ = "servicos"
    __table_args__ = (
        CheckConstraint("duracao_minutos IS NULL OR duracao_minutos > 0", name="ck_servicos_duracao_positiva"),
        CheckConstraint("preco_estimado IS NULL OR preco_estimado >= 0", name="ck_servicos_preco_nao_negativo"),
    )

    empresa_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("empresas.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    nome: Mapped[str] = mapped_column(Text, nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text)
    categoria: Mapped[str | None] = mapped_column(Text)
    duracao_minutos: Mapped[int | None] = mapped_column(Integer)
    preco_estimado: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    empresa: Mapped["Empresa"] = relationship(back_populates="servicos")
    posts: Mapped[list["Post"]] = relationship(back_populates="servico")

