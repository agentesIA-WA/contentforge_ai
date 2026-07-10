from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class EmpresaBase(BaseModel):
    nome: str
    nicho: str
    publico_alvo: str | None = None
    cidade: str | None = None
    objetivos: str | None = None
    tom_voz: str | None = None
    identidade_visual: dict[str, Any] = Field(default_factory=dict)
    horario_funcionamento: dict[str, Any] = Field(default_factory=dict)
    diferenciais: str | None = None
    instagram_handle: str | None = None
    telefone: str | None = None
    email_contato: str | None = None
    ativa: bool = True


class EmpresaCreate(EmpresaBase):
    pass


class EmpresaUpdate(BaseModel):
    nome: str | None = None
    nicho: str | None = None
    publico_alvo: str | None = None
    cidade: str | None = None
    objetivos: str | None = None
    tom_voz: str | None = None
    identidade_visual: dict[str, Any] | None = None
    horario_funcionamento: dict[str, Any] | None = None
    diferenciais: str | None = None
    instagram_handle: str | None = None
    telefone: str | None = None
    email_contato: str | None = None
    ativa: bool | None = None


class EmpresaRead(EmpresaBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
