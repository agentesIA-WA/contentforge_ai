"""CRUD endpoints for post resources."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.post import Post
from app.schemas.post import PostCreate, PostRead, PostUpdate

router = APIRouter(tags=["Posts"])


@router.post("/posts", response_model=PostRead, status_code=status.HTTP_201_CREATED)
def create_post(payload: PostCreate, db: Session = Depends(get_db)) -> Post:
    post = Post(**payload.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.get("/posts", response_model=list[PostRead])
def list_posts(db: Session = Depends(get_db)) -> list[Post]:
    return db.query(Post).all()


@router.get("/posts/{post_id}", response_model=PostRead)
def get_post(post_id: UUID, db: Session = Depends(get_db)) -> Post:
    post = db.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post não encontrado")
    return post


@router.put("/posts/{post_id}", response_model=PostRead)
def update_post(post_id: UUID, payload: PostUpdate, db: Session = Depends(get_db)) -> Post:
    post = db.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post não encontrado")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(post, field, value)

    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.delete("/posts/{post_id}", status_code=status.HTTP_200_OK)
def delete_post(post_id: UUID, db: Session = Depends(get_db)) -> dict[str, str]:
    post = db.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post não encontrado")

    db.delete(post)
    db.commit()
    return {"detail": "Post removido"}
