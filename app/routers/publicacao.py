"""CRUD endpoints for publication resources."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.publicacao import Publicacao
from app.schemas.publicacao import PublicacaoCreate, PublicacaoRead, PublicacaoUpdate

router = APIRouter(tags=["Publicacoes"])


@router.post("/publicacoes", response_model=PublicacaoRead, status_code=status.HTTP_201_CREATED)
def create_publicacao(payload: PublicacaoCreate, db: Session = Depends(get_db)) -> Publicacao:
    publicacao = Publicacao(**payload.model_dump())
    db.add(publicacao)
    db.commit()
    db.refresh(publicacao)
    return publicacao


@router.get("/publicacoes", response_model=list[PublicacaoRead])
def list_publicacoes(db: Session = Depends(get_db)) -> list[Publicacao]:
    return db.query(Publicacao).all()


@router.get("/publicacoes/{publicacao_id}", response_model=PublicacaoRead)
def get_publicacao(publicacao_id: UUID, db: Session = Depends(get_db)) -> Publicacao:
    publicacao = db.get(Publicacao, publicacao_id)
    if publicacao is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Publicacao não encontrada")
    return publicacao


@router.put("/publicacoes/{publicacao_id}", response_model=PublicacaoRead)
def update_publicacao(
    publicacao_id: UUID,
    payload: PublicacaoUpdate,
    db: Session = Depends(get_db),
) -> Publicacao:
    publicacao = db.get(Publicacao, publicacao_id)
    if publicacao is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Publicacao não encontrada")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(publicacao, field, value)

    db.add(publicacao)
    db.commit()
    db.refresh(publicacao)
    return publicacao


@router.delete("/publicacoes/{publicacao_id}", status_code=status.HTTP_200_OK)
def delete_publicacao(publicacao_id: UUID, db: Session = Depends(get_db)) -> dict[str, str]:
    publicacao = db.get(Publicacao, publicacao_id)
    if publicacao is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Publicacao não encontrada")

    db.delete(publicacao)
    db.commit()
    return {"detail": "Publicacao removida"}
