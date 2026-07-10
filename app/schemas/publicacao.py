from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PublicacaoBase(BaseModel):
    empresa_id: UUID
    post_id: UUID
    plataforma: str = "instagram"
    id_externo: str | None = None
    permalink: str | None = None
    status: str = "pendente"
    agendado_para: datetime | None = None
    publicado_em: datetime | None = None
    erro_mensagem: str | None = None
    payload_publicacao: dict[str, Any] = Field(default_factory=dict)


class PublicacaoCreate(PublicacaoBase):
    pass


class PublicacaoUpdate(BaseModel):
    empresa_id: UUID | None = None
    post_id: UUID | None = None
    plataforma: str | None = None
    id_externo: str | None = None
    permalink: str | None = None
    status: str | None = None
    agendado_para: datetime | None = None
    publicado_em: datetime | None = None
    erro_mensagem: str | None = None
    payload_publicacao: dict[str, Any] | None = None


class PublicacaoRead(PublicacaoBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
