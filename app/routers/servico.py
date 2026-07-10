"""CRUD endpoints for service resources."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.servico import Servico
from app.schemas.servico import ServicoCreate, ServicoRead, ServicoUpdate

router = APIRouter(tags=["Servicos"])


@router.post("/servicos", response_model=ServicoRead, status_code=status.HTTP_201_CREATED)
def create_servico(payload: ServicoCreate, db: Session = Depends(get_db)) -> Servico:
    servico = Servico(**payload.model_dump())
    db.add(servico)
    db.commit()
    db.refresh(servico)
    return servico


@router.get("/servicos", response_model=list[ServicoRead])
def list_servicos(db: Session = Depends(get_db)) -> list[Servico]:
    return db.query(Servico).all()


@router.get("/servicos/{servico_id}", response_model=ServicoRead)
def get_servico(servico_id: UUID, db: Session = Depends(get_db)) -> Servico:
    servico = db.get(Servico, servico_id)
    if servico is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Servico não encontrado")
    return servico


@router.put("/servicos/{servico_id}", response_model=ServicoRead)
def update_servico(
    servico_id: UUID,
    payload: ServicoUpdate,
    db: Session = Depends(get_db),
) -> Servico:
    servico = db.get(Servico, servico_id)
    if servico is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Servico não encontrado")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(servico, field, value)

    db.add(servico)
    db.commit()
    db.refresh(servico)
    return servico


@router.delete("/servicos/{servico_id}", status_code=status.HTTP_200_OK)
def delete_servico(servico_id: UUID, db: Session = Depends(get_db)) -> dict[str, str]:
    servico = db.get(Servico, servico_id)
    if servico is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Servico não encontrado")

    db.delete(servico)
    db.commit()
    return {"detail": "Servico removido"}
