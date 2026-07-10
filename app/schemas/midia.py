from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class MidiaBase(BaseModel):
    empresa_id: UUID
    post_id: UUID
    prompt_id: UUID | None = None
    tipo: str
    url: str | None = None
    caminho_arquivo: str | None = None
    alt_text: str | None = None
    metadados: dict[str, Any] = Field(default_factory=dict)


class MidiaCreate(MidiaBase):
    pass


class MidiaUpdate(BaseModel):
    empresa_id: UUID | None = None
    post_id: UUID | None = None
    prompt_id: UUID | None = None
    tipo: str | None = None
    url: str | None = None
    caminho_arquivo: str | None = None
    alt_text: str | None = None
    metadados: dict[str, Any] | None = None


class MidiaRead(MidiaBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
