from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class MetricaBase(BaseModel):
    empresa_id: UUID
    publicacao_id: UUID
    curtidas: int = 0
    comentarios: int = 0
    compartilhamentos: int = 0
    alcance: int = 0
    impressoes: int = 0
    taxa_engajamento: Decimal = Decimal("0")
    coletado_em: datetime | None = None


class MetricaCreate(MetricaBase):
    pass


class MetricaUpdate(BaseModel):
    empresa_id: UUID | None = None
    publicacao_id: UUID | None = None
    curtidas: int | None = None
    comentarios: int | None = None
    compartilhamentos: int | None = None
    alcance: int | None = None
    impressoes: int | None = None
    taxa_engajamento: Decimal | None = None
    coletado_em: datetime | None = None


class MetricaRead(MetricaBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
