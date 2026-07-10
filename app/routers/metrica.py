"""CRUD API for publication performance metrics."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.metrica import Metrica
from app.schemas.metrica import MetricaCreate, MetricaRead, MetricaUpdate

router = APIRouter(tags=["Métricas"])


@router.post("/metricas", response_model=MetricaRead, status_code=status.HTTP_201_CREATED)
def create_metrica(
    payload: MetricaCreate,
    db: Session = Depends(get_db),
) -> Metrica:
    metrica = Metrica(**payload.model_dump())
    db.add(metrica)
    db.commit()
    db.refresh(metrica)
    return metrica


@router.get("/metricas", response_model=list[MetricaRead])
def list_metricas(db: Session = Depends(get_db)) -> list[Metrica]:
    return db.query(Metrica).all()


@router.get("/metricas/{metrica_id}", response_model=MetricaRead)
def get_metrica(metrica_id: UUID, db: Session = Depends(get_db)) -> Metrica:
    metrica = db.get(Metrica, metrica_id)
    if metrica is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Métrica não encontrada")
    return metrica


@router.put("/metricas/{metrica_id}", response_model=MetricaRead)
def update_metrica(
    metrica_id: UUID,
    payload: MetricaUpdate,
    db: Session = Depends(get_db),
) -> Metrica:
    metrica = db.get(Metrica, metrica_id)
    if metrica is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Métrica não encontrada")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(metrica, field, value)

    db.add(metrica)
    db.commit()
    db.refresh(metrica)
    return metrica


@router.delete("/metricas/{metrica_id}", status_code=status.HTTP_200_OK)
def delete_metrica(metrica_id: UUID, db: Session = Depends(get_db)) -> dict[str, str]:
    metrica = db.get(Metrica, metrica_id)
    if metrica is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Métrica não encontrada")

    db.delete(metrica)
    db.commit()
    return {"detail": "Métrica removida"}
