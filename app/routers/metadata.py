"""Metadata endpoints for schema inspection."""

from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

import app.models  # noqa: F401
from app.database.base import Base

router = APIRouter(tags=["Metadata"])


class MetadataResponse(BaseModel):
    """Response returned by metadata endpoints."""

    tables: List[str]


@router.get("/metadata/tables", response_model=MetadataResponse, summary="List database tables")
async def list_database_tables() -> MetadataResponse:
    """Return the names of the tables defined by the current ORM models."""
    return MetadataResponse(tables=sorted(Base.metadata.tables.keys()))
