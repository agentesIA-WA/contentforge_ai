"""User model for authentication and approval workflows."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base import UUIDTimestampMixin


class Usuario(UUIDTimestampMixin, Base):
    """Application user associated with a managed company."""

    __tablename__ = "usuarios"
    __table_args__ = (
        CheckConstraint(
            "perfil IN ('admin', 'editor', 'visualizador')",
            name="ck_usuarios_perfil",
        ),
    )

    empresa_id: Mapped[UUID | None] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("empresas.id", ondelete="CASCADE"),
        index=True,
    )
    nome: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(Text, nullable=False, unique=True, index=True)
    senha_hash: Mapped[str] = mapped_column(Text, nullable=False)
    perfil: Mapped[str] = mapped_column(Text, default="admin", nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    ultimo_login_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    empresa: Mapped["Empresa | None"] = relationship(back_populates="usuarios")
    posts_aprovados: Mapped[list["Post"]] = relationship(
        back_populates="aprovado_por",
        foreign_keys="Post.aprovado_por_usuario_id",
    )

