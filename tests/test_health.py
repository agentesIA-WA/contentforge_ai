"""Tests for basic API health endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
def anyio_backend() -> str:
    """Run async tests with asyncio only."""
    return "asyncio"


@pytest.mark.anyio
async def test_health_check_returns_ok() -> None:
    """The API health endpoint should confirm the service is alive."""
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "Beauty Content AI"}
