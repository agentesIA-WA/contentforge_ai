"""Configuration model for company-scoped settings."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base import UUIDTimestampMixin


class Configuracao(UUIDTimestampMixin, Base):
    """Company setting stored as a JSON value."""

    __tablename__ = "configuracoes"
    __table_args__ = (
        UniqueConstraint("empresa_id", "chave", name="uq_configuracoes_empresa_chave"),
    )

    empresa_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("empresas.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    chave: Mapped[str] = mapped_column(Text, nullable=False)
    valor: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text)
    sensivel: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    ativa: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    empresa: Mapped["Empresa"] = relationship(back_populates="configuracoes")

