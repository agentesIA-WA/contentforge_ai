from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UsuarioBase(BaseModel):
    empresa_id: UUID | None = None
    nome: str
    email: str
    perfil: str = "admin"
    ativo: bool = True


class UsuarioCreate(UsuarioBase):
    senha: str


class UsuarioUpdate(BaseModel):
    empresa_id: UUID | None = None
    nome: str | None = None
    email: str | None = None
    senha: str | None = None
    perfil: str | None = None
    ativo: bool | None = None


class UsuarioRead(UsuarioBase):
    id: UUID
    ultimo_login_em: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
