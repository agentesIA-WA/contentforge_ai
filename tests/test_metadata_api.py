"""Tests for metadata API endpoints."""

from httpx import ASGITransport, AsyncClient

from app.main import app


def test_metadata_tables_includes_expected_tables() -> None:
    """The metadata endpoint should expose the registered ORM tables."""
    transport = ASGITransport(app=app)

    async def run_test() -> None:
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/metadata/tables")

        assert response.status_code == 200
        data = response.json()
        assert "tables" in data
        assert "empresas" in data["tables"]
        assert "usuarios" in data["tables"]
        assert "posts" in data["tables"]

    import asyncio

    asyncio.run(run_test())
