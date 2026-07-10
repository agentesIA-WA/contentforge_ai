"""CRUD endpoints for company resources."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.empresa import Empresa
from app.schemas.configuracao import ConfiguracaoRead
from app.schemas.metrica import MetricaRead
from app.schemas.post import PostRead
from app.schemas.prompt import PromptRead
from app.schemas.publicacao import PublicacaoRead
from app.schemas.empresa import EmpresaCreate, EmpresaRead, EmpresaUpdate
from app.schemas.servico import ServicoRead

router = APIRouter(tags=["Empresas"])


@router.post("/empresas", response_model=EmpresaRead, status_code=status.HTTP_201_CREATED)
def create_empresa(
    payload: EmpresaCreate,
    db: Session = Depends(get_db),
) -> Empresa:
    empresa = Empresa(**payload.model_dump())
    db.add(empresa)
    db.commit()
    db.refresh(empresa)
    return empresa


@router.get("/empresas", response_model=list[EmpresaRead])
def list_empresas(db: Session = Depends(get_db)) -> list[Empresa]:
    return db.query(Empresa).all()


@router.get("/empresas/{empresa_id}", response_model=EmpresaRead)
def get_empresa(empresa_id: UUID, db: Session = Depends(get_db)) -> Empresa:
    empresa = db.get(Empresa, empresa_id)
    if empresa is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada")
    return empresa


@router.get("/empresas/{empresa_id}/posts", response_model=list[PostRead])
def get_empresa_posts(empresa_id: UUID, db: Session = Depends(get_db)) -> list[PostRead]:
    empresa = db.get(Empresa, empresa_id)
    if empresa is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada")
    return empresa.posts


@router.get("/empresas/{empresa_id}/publicacoes", response_model=list[PublicacaoRead])
def get_empresa_publicacoes(empresa_id: UUID, db: Session = Depends(get_db)) -> list[PublicacaoRead]:
    empresa = db.get(Empresa, empresa_id)
    if empresa is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada")
    return empresa.publicacoes


@router.get("/empresas/{empresa_id}/prompts", response_model=list[PromptRead])
def get_empresa_prompts(empresa_id: UUID, db: Session = Depends(get_db)) -> list[PromptRead]:
    empresa = db.get(Empresa, empresa_id)
    if empresa is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada")
    return empresa.prompts


@router.get("/empresas/{empresa_id}/servicos", response_model=list[ServicoRead])
def get_empresa_servicos(empresa_id: UUID, db: Session = Depends(get_db)) -> list[ServicoRead]:
    empresa = db.get(Empresa, empresa_id)
    if empresa is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada")
    return empresa.servicos


@router.get("/empresas/{empresa_id}/configuracoes", response_model=list[ConfiguracaoRead])
def get_empresa_configuracoes(empresa_id: UUID, db: Session = Depends(get_db)) -> list[ConfiguracaoRead]:
    empresa = db.get(Empresa, empresa_id)
    if empresa is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada")
    return empresa.configuracoes


@router.get("/empresas/{empresa_id}/metricas", response_model=list[MetricaRead])
def get_empresa_metricas(empresa_id: UUID, db: Session = Depends(get_db)) -> list[MetricaRead]:
    empresa = db.get(Empresa, empresa_id)
    if empresa is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada")
    return empresa.metricas


@router.put("/empresas/{empresa_id}", response_model=EmpresaRead)
def update_empresa(
    empresa_id: UUID,
    payload: EmpresaUpdate,
    db: Session = Depends(get_db),
) -> Empresa:
    empresa = db.get(Empresa, empresa_id)
    if empresa is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(empresa, field, value)

    db.add(empresa)
    db.commit()
    db.refresh(empresa)
    return empresa


@router.delete("/empresas/{empresa_id}", status_code=status.HTTP_200_OK)
def delete_empresa(empresa_id: UUID, db: Session = Depends(get_db)) -> dict[str, str]:
    empresa = db.get(Empresa, empresa_id)
    if empresa is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa não encontrada")

    db.delete(empresa)
    db.commit()
    return {"detail": "Empresa removida"}
