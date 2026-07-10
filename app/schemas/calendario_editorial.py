from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CalendarioEditorialBase(BaseModel):
    empresa_id: UUID
    titulo: str
    descricao: str | None = None
    data_planejada: date
    tema: str | None = None
    objetivo: str | None = None
    formato: str = "feed"
    canal: str = "instagram"
    status: str = "planejado"
    observacoes: str | None = None


class CalendarioEditorialCreate(CalendarioEditorialBase):
    pass


class CalendarioEditorialUpdate(BaseModel):
    empresa_id: UUID | None = None
    titulo: str | None = None
    descricao: str | None = None
    data_planejada: date | None = None
    tema: str | None = None
    objetivo: str | None = None
    formato: str | None = None
    canal: str | None = None
    status: str | None = None
    observacoes: str | None = None


class CalendarioEditorialRead(CalendarioEditorialBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
