"""Health-check endpoints for application and database monitoring."""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.database.session import check_database_connection

router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    """Response returned by health-check endpoints."""

    status: str
    service: str


@router.get("/health", response_model=HealthResponse, summary="Application health")
async def health_check() -> HealthResponse:
    """Confirm that the API process is running."""
    return HealthResponse(status="ok", service="Beauty Content AI")


@router.get(
    "/health/database",
    response_model=HealthResponse,
    summary="Database health",
    responses={status.HTTP_503_SERVICE_UNAVAILABLE: {"description": "Unavailable"}},
)
async def database_health_check() -> HealthResponse:
    """Confirm that the configured PostgreSQL database is reachable."""
    if not check_database_connection():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection unavailable",
        )

    return HealthResponse(status="ok", service="PostgreSQL")
