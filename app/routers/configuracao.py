"""CRUD API for configuration settings."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.configuracao import Configuracao
from app.schemas.configuracao import (
    ConfiguracaoCreate,
    ConfiguracaoRead,
    ConfiguracaoUpdate,
)

router = APIRouter(tags=["Configurações"])


@router.post("/configuracoes", response_model=ConfiguracaoRead, status_code=status.HTTP_201_CREATED)
def create_configuracao(
    payload: ConfiguracaoCreate,
    db: Session = Depends(get_db),
) -> Configuracao:
    configuracao = Configuracao(**payload.model_dump())
    db.add(configuracao)
    db.commit()
    db.refresh(configuracao)
    return configuracao


@router.get("/configuracoes", response_model=list[ConfiguracaoRead])
def list_configuracoes(db: Session = Depends(get_db)) -> list[Configuracao]:
    return db.query(Configuracao).all()


@router.get("/configuracoes/{configuracao_id}", response_model=ConfiguracaoRead)
def get_configuracao(configuracao_id: UUID, db: Session = Depends(get_db)) -> Configuracao:
    configuracao = db.get(Configuracao, configuracao_id)
    if configuracao is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Configuração não encontrada")
    return configuracao


@router.put("/configuracoes/{configuracao_id}", response_model=ConfiguracaoRead)
def update_configuracao(
    configuracao_id: UUID,
    payload: ConfiguracaoUpdate,
    db: Session = Depends(get_db),
) -> Configuracao:
    configuracao = db.get(Configuracao, configuracao_id)
    if configuracao is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Configuração não encontrada")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(configuracao, field, value)

    db.add(configuracao)
    db.commit()
    db.refresh(configuracao)
    return configuracao


@router.delete("/configuracoes/{configuracao_id}", status_code=status.HTTP_200_OK)
def delete_configuracao(configuracao_id: UUID, db: Session = Depends(get_db)) -> dict[str, str]:
    configuracao = db.get(Configuracao, configuracao_id)
    if configuracao is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Configuração não encontrada")

    db.delete(configuracao)
    db.commit()
    return {"detail": "Configuração removida"}
