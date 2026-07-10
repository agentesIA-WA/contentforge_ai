from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import create_access_token, get_current_user, verify_password
from app.database.session import get_db
from app.models.usuario import Usuario
from app.schemas.token import Token
from app.schemas.usuario import UsuarioRead

router = APIRouter(tags=["Auth"])


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Token:
    user = db.query(Usuario).filter(Usuario.email == form_data.username).first()
    if user is None or not verify_password(form_data.password, user.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.ativo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário inativo")

    access_token = create_access_token(data={"sub": str(user.id)})
    user.ultimo_login_em = datetime.now(timezone.utc)
    db.add(user)
    db.commit()
    db.refresh(user)

    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UsuarioRead)
def read_current_user(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    return current_user
