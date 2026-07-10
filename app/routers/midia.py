"""CRUD API for media assets."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.midia import Midia
from app.schemas.midia import MidiaCreate, MidiaRead, MidiaUpdate

router = APIRouter(tags=["Mídias"])


@router.post("/midias", response_model=MidiaRead, status_code=status.HTTP_201_CREATED)
def create_midia(
    payload: MidiaCreate,
    db: Session = Depends(get_db),
) -> Midia:
    midia = Midia(**payload.model_dump())
    db.add(midia)
    db.commit()
    db.refresh(midia)
    return midia


@router.get("/midias", response_model=list[MidiaRead])
def list_midias(db: Session = Depends(get_db)) -> list[Midia]:
    return db.query(Midia).all()


@router.get("/midias/{midia_id}", response_model=MidiaRead)
def get_midia(midia_id: UUID, db: Session = Depends(get_db)) -> Midia:
    midia = db.get(Midia, midia_id)
    if midia is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mídia não encontrada")
    return midia


@router.put("/midias/{midia_id}", response_model=MidiaRead)
def update_midia(
    midia_id: UUID,
    payload: MidiaUpdate,
    db: Session = Depends(get_db),
) -> Midia:
    midia = db.get(Midia, midia_id)
    if midia is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mídia não encontrada")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(midia, field, value)

    db.add(midia)
    db.commit()
    db.refresh(midia)
    return midia


@router.delete("/midias/{midia_id}", status_code=status.HTTP_200_OK)
def delete_midia(midia_id: UUID, db: Session = Depends(get_db)) -> dict[str, str]:
    midia = db.get(Midia, midia_id)
    if midia is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mídia não encontrada")

    db.delete(midia)
    db.commit()
    return {"detail": "Mídia removida"}
