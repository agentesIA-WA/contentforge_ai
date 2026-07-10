"""Editorial calendar model for planned content slots."""

from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import CheckConstraint, Date, ForeignKey, Index, Text
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base import UUIDTimestampMixin


class CalendarioEditorial(UUIDTimestampMixin, Base):
    """Planned editorial item for campaigns and recurring content."""

    __tablename__ = "calendario_editorial"
    __table_args__ = (
        CheckConstraint(
            "status IN ('planejado', 'em_producao', 'aprovado', 'publicado', 'cancelado')",
            name="ck_calendario_editorial_status",
        ),
        CheckConstraint(
            "formato IN ('feed', 'story', 'reels', 'carrossel', 'campanha')",
            name="ck_calendario_editorial_formato",
        ),
        Index("ix_calendario_editorial_empresa_data", "empresa_id", "data_planejada"),
    )

    empresa_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("empresas.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    titulo: Mapped[str] = mapped_column(Text, nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text)
    data_planejada: Mapped[date] = mapped_column(Date, nullable=False)
    tema: Mapped[str | None] = mapped_column(Text)
    objetivo: Mapped[str | None] = mapped_column(Text)
    formato: Mapped[str] = mapped_column(Text, default="feed", nullable=False)
    canal: Mapped[str] = mapped_column(Text, default="instagram", nullable=False)
    status: Mapped[str] = mapped_column(Text, default="planejado", nullable=False)
    observacoes: Mapped[str | None] = mapped_column(Text)

    empresa: Mapped["Empresa"] = relationship(back_populates="calendario_editorial")
    posts: Mapped[list["Post"]] = relationship(back_populates="calendario_editorial")

