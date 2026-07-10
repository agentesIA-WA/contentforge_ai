from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ConfiguracaoBase(BaseModel):
    empresa_id: UUID
    chave: str
    valor: dict[str, Any] = Field(default_factory=dict)
    descricao: str | None = None
    sensivel: bool = False
    ativa: bool = True


class ConfiguracaoCreate(ConfiguracaoBase):
    pass


class ConfiguracaoUpdate(BaseModel):
    empresa_id: UUID | None = None
    chave: str | None = None
    valor: dict[str, Any] | None = None
    descricao: str | None = None
    sensivel: bool | None = None
    ativa: bool | None = None


class ConfiguracaoRead(ConfiguracaoBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
