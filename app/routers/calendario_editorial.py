from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.calendario_editorial import CalendarioEditorial
from app.schemas.calendario_editorial import (
    CalendarioEditorialCreate,
    CalendarioEditorialRead,
    CalendarioEditorialUpdate,
)

router = APIRouter(tags=["CalendarioEditorial"])


@router.post("/calendario-editorial", response_model=CalendarioEditorialRead, status_code=status.HTTP_201_CREATED)
def create_calendario_editorial(
    payload: CalendarioEditorialCreate,
    db: Session = Depends(get_db),
) -> CalendarioEditorial:
    calendario = CalendarioEditorial(**payload.model_dump())
    db.add(calendario)
    db.commit()
    db.refresh(calendario)
    return calendario


@router.get("/calendario-editorial", response_model=list[CalendarioEditorialRead])
def list_calendarios_editorial(db: Session = Depends(get_db)) -> list[CalendarioEditorial]:
    return db.query(CalendarioEditorial).all()


@router.get("/calendario-editorial/{calendario_id}", response_model=CalendarioEditorialRead)
def get_calendario_editorial(calendario_id: UUID, db: Session = Depends(get_db)) -> CalendarioEditorial:
    calendario = db.get(CalendarioEditorial, calendario_id)
    if calendario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calendário editorial não encontrado")
    return calendario


@router.put("/calendario-editorial/{calendario_id}", response_model=CalendarioEditorialRead)
def update_calendario_editorial(
    calendario_id: UUID,
    payload: CalendarioEditorialUpdate,
    db: Session = Depends(get_db),
) -> CalendarioEditorial:
    calendario = db.get(CalendarioEditorial, calendario_id)
    if calendario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calendário editorial não encontrado")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(calendario, field, value)

    db.add(calendario)
    db.commit()
    db.refresh(calendario)
    return calendario


@router.delete("/calendario-editorial/{calendario_id}", status_code=status.HTTP_200_OK)
def delete_calendario_editorial(calendario_id: UUID, db: Session = Depends(get_db)) -> dict[str, str]:
    calendario = db.get(CalendarioEditorial, calendario_id)
    if calendario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calendário editorial não encontrado")

    db.delete(calendario)
    db.commit()
    return {"detail": "Calendário editorial removido"}
