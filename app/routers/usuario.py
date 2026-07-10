from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.database.session import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioRead, UsuarioUpdate

router = APIRouter(tags=["Usuarios"])


@router.post("/usuarios", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def create_usuario(payload: UsuarioCreate, db: Session = Depends(get_db)) -> Usuario:
    usuario = Usuario(
        empresa_id=payload.empresa_id,
        nome=payload.nome,
        email=payload.email,
        senha_hash=get_password_hash(payload.senha),
        perfil=payload.perfil,
        ativo=payload.ativo,
    )

    db.add(usuario)
    try:
        db.commit()
        db.refresh(usuario)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário já existe ou dados inválidos") from exc

    return usuario


@router.get("/usuarios", response_model=list[UsuarioRead])
def list_usuarios(db: Session = Depends(get_db)) -> list[Usuario]:
    return db.query(Usuario).all()


@router.get("/usuarios/{usuario_id}", response_model=UsuarioRead)
def get_usuario(usuario_id: UUID, db: Session = Depends(get_db)) -> Usuario:
    usuario = db.get(Usuario, usuario_id)
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return usuario


@router.put("/usuarios/{usuario_id}", response_model=UsuarioRead)
def update_usuario(usuario_id: UUID, payload: UsuarioUpdate, db: Session = Depends(get_db)) -> Usuario:
    usuario = db.get(Usuario, usuario_id)
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    update_data = payload.model_dump(exclude_unset=True)
    if "senha" in update_data and update_data["senha"] is not None:
        update_data["senha_hash"] = get_password_hash(update_data.pop("senha"))

    for field, value in update_data.items():
        setattr(usuario, field, value)

    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.delete("/usuarios/{usuario_id}", status_code=status.HTTP_200_OK)
def delete_usuario(usuario_id: UUID, db: Session = Depends(get_db)) -> dict[str, str]:
    usuario = db.get(Usuario, usuario_id)
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    db.delete(usuario)
    db.commit()
    return {"detail": "Usuário removido"}
