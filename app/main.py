"""FastAPI application factory."""

from pathlib import Path
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.config import get_settings
from app.core.logging import configure_logging
from app.routers import health
from app.routers.metadata import router as metadata_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Configure application resources during startup and shutdown."""
    settings = get_settings()
    configure_logging(settings.log_level)
    logger.info("Starting %s in %s mode", settings.app_name, settings.environment)
    yield
    logger.info("Stopping %s", settings.app_name)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        description="Social Media inteligente para saloes de beleza.",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url=f"{settings.api_prefix}/openapi.json",
        lifespan=lifespan,
    )

    static_path = Path(__file__).resolve().parents[1] / "static"
    app.mount("/static", StaticFiles(directory=static_path), name="static")
    app.include_router(health.router, prefix=settings.api_prefix)
    app.include_router(metadata_router, prefix=settings.api_prefix)

    @app.get("/", include_in_schema=False)
    async def root() -> dict[str, str]:
        """Return basic navigation metadata for humans and monitors."""
        return {
            "service": settings.app_name,
            "docs": "/docs",
            "health": f"{settings.api_prefix}/health",
        }

    return app


app = create_app()
