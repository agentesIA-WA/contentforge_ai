"""CRUD endpoints for prompt resources."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.prompt import Prompt
from app.schemas.prompt import PromptCreate, PromptRead, PromptUpdate
from app.services import llm

router = APIRouter(tags=["Prompts"])


@router.post("/prompts", response_model=PromptRead, status_code=status.HTTP_201_CREATED)
def create_prompt(payload: PromptCreate, db: Session = Depends(get_db)) -> Prompt:
    prompt = Prompt(**payload.model_dump())
    db.add(prompt)
    db.commit()
    db.refresh(prompt)
    return prompt


@router.get("/prompts", response_model=list[PromptRead])
def list_prompts(db: Session = Depends(get_db)) -> list[Prompt]:
    return db.query(Prompt).all()


@router.get("/prompts/{prompt_id}", response_model=PromptRead)
def get_prompt(prompt_id: UUID, db: Session = Depends(get_db)) -> Prompt:
    prompt = db.get(Prompt, prompt_id)
    if prompt is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt não encontrado")
    return prompt


@router.put("/prompts/{prompt_id}", response_model=PromptRead)
def update_prompt(prompt_id: UUID, payload: PromptUpdate, db: Session = Depends(get_db)) -> Prompt:
    prompt = db.get(Prompt, prompt_id)
    if prompt is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt não encontrado")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(prompt, field, value)

    db.add(prompt)
    db.commit()
    db.refresh(prompt)
    return prompt


@router.delete("/prompts/{prompt_id}", status_code=status.HTTP_200_OK)
def delete_prompt(prompt_id: UUID, db: Session = Depends(get_db)) -> dict[str, str]:
    prompt = db.get(Prompt, prompt_id)
    if prompt is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt não encontrado")

    db.delete(prompt)
    db.commit()
    return {"detail": "Prompt removido"}


@router.post("/prompts/{prompt_id}/gerar", response_model=PromptRead)
def gerar_prompt(prompt_id: UUID, db: Session = Depends(get_db)) -> Prompt:
    """Trigger generation for a prompt: call LLM and persist the resposta + status."""
    prompt = db.get(Prompt, prompt_id)
    if prompt is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt não encontrado")

    # mark as sent
    prompt.status = "enviado"
    db.add(prompt)
    db.commit()
    db.refresh(prompt)

    # call LLM service (synchronous). Service will simulate if no API key present.
    result = llm.generate_text(prompt.conteudo, modelo=prompt.modelo_ia, parametros=prompt.parametros)

    if isinstance(result, dict) and result.get("error"):
        prompt.status = "falhou"
        prompt.resposta = {"error": result.get("error")}
    else:
        prompt.status = "respondido"
        prompt.resposta = result

    db.add(prompt)
    db.commit()
    db.refresh(prompt)
    return prompt
