from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PostBase(BaseModel):
    empresa_id: UUID
    calendario_editorial_id: UUID | None = None
    servico_id: UUID | None = None
    aprovado_por_usuario_id: UUID | None = None
    titulo: str
    formato: str = "feed"
    status: str = "rascunho"
    legenda: str | None = None
    cta: str | None = None
    hashtags: list[str] = Field(default_factory=list)
    conteudo_estruturado: dict[str, Any] = Field(default_factory=dict)
    prompt_imagem: str | None = None
    data_publicacao_sugerida: datetime | None = None
    aprovado_em: datetime | None = None
    observacoes: str | None = None


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    empresa_id: UUID | None = None
    calendario_editorial_id: UUID | None = None
    servico_id: UUID | None = None
    aprovado_por_usuario_id: UUID | None = None
    titulo: str | None = None
    formato: str | None = None
    status: str | None = None
    legenda: str | None = None
    cta: str | None = None
    hashtags: list[str] | None = None
    conteudo_estruturado: dict[str, Any] | None = None
    prompt_imagem: str | None = None
    data_publicacao_sugerida: datetime | None = None
    aprovado_em: datetime | None = None
    observacoes: str | None = None


class PostRead(PostBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
