"""Company model for businesses managed by the platform."""

from __future__ import annotations

from typing import Any

from sqlalchemy import Boolean, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base import UUIDTimestampMixin


class Empresa(UUIDTimestampMixin, Base):
    """Business profile used by the agents to understand brand context."""

    __tablename__ = "empresas"

    nome: Mapped[str] = mapped_column(Text, nullable=False)
    nicho: Mapped[str] = mapped_column(Text, nullable=False)
    publico_alvo: Mapped[str | None] = mapped_column(Text)
    cidade: Mapped[str | None] = mapped_column(Text)
    objetivos: Mapped[str | None] = mapped_column(Text)
    tom_voz: Mapped[str | None] = mapped_column(Text)
    identidade_visual: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
    )
    horario_funcionamento: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
    )
    diferenciais: Mapped[str | None] = mapped_column(Text)
    instagram_handle: Mapped[str | None] = mapped_column(Text)
    telefone: Mapped[str | None] = mapped_column(Text)
    email_contato: Mapped[str | None] = mapped_column(Text)
    ativa: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    usuarios: Mapped[list["Usuario"]] = relationship(
        back_populates="empresa",
        cascade="all, delete-orphan",
    )
    servicos: Mapped[list["Servico"]] = relationship(
        back_populates="empresa",
        cascade="all, delete-orphan",
    )
    calendario_editorial: Mapped[list["CalendarioEditorial"]] = relationship(
        back_populates="empresa",
        cascade="all, delete-orphan",
    )
    posts: Mapped[list["Post"]] = relationship(
        back_populates="empresa",
        cascade="all, delete-orphan",
    )
    midias: Mapped[list["Midia"]] = relationship(
        back_populates="empresa",
        cascade="all, delete-orphan",
    )
    publicacoes: Mapped[list["Publicacao"]] = relationship(
        back_populates="empresa",
        cascade="all, delete-orphan",
    )
    metricas: Mapped[list["Metrica"]] = relationship(
        back_populates="empresa",
        cascade="all, delete-orphan",
    )
    prompts: Mapped[list["Prompt"]] = relationship(
        back_populates="empresa",
        cascade="all, delete-orphan",
    )
    configuracoes: Mapped[list["Configuracao"]] = relationship(
        back_populates="empresa",
        cascade="all, delete-orphan",
    )

