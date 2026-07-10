from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ServicoBase(BaseModel):
    empresa_id: UUID
    nome: str
    descricao: str | None = None
    categoria: str | None = None
    duracao_minutos: int | None = None
    preco_estimado: Decimal | None = None
    ativo: bool = True


class ServicoCreate(ServicoBase):
    pass


class ServicoUpdate(BaseModel):
    nome: str | None = None
    descricao: str | None = None
    categoria: str | None = None
    duracao_minutos: int | None = None
    preco_estimado: Decimal | None = None
    ativo: bool | None = None


class ServicoRead(ServicoBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
