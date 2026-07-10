from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PromptBase(BaseModel):
    empresa_id: UUID
    post_id: UUID | None = None
    agente: str
    tipo: str
    conteudo: str
    parametros: dict[str, Any] = Field(default_factory=dict)
    modelo_ia: str | None = None
    resposta: dict[str, Any] | None = None
    status: str = "criado"


class PromptCreate(PromptBase):
    pass


class PromptUpdate(BaseModel):
    empresa_id: UUID | None = None
    post_id: UUID | None = None
    agente: str | None = None
    tipo: str | None = None
    conteudo: str | None = None
    parametros: dict[str, Any] | None = None
    modelo_ia: str | None = None
    resposta: dict[str, Any] | None = None
    status: str | None = None


class PromptRead(PromptBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
