"""Tests for the Publicacao CRUD API."""

from datetime import datetime
from uuid import UUID, uuid4

from fastapi import status
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.database.session import get_db
from app.models.publicacao import Publicacao


class FakeQuery:
    def __init__(self, items: list[Publicacao]) -> None:
        self._items = items

    def all(self) -> list[Publicacao]:
        return list(self._items)


class FakeSession:
    def __init__(self) -> None:
        self._storage: dict[UUID, Publicacao] = {}

    def add(self, entity: Publicacao) -> None:
        if entity.id is None:
            entity.id = uuid4()
        self._storage[entity.id] = entity

    def commit(self) -> None:
        pass

    def refresh(self, entity: Publicacao) -> None:
        pass

    def query(self, model):
        if model is Publicacao:
            return FakeQuery(list(self._storage.values()))
        raise TypeError("Unsupported model")

    def get(self, model, entity_id: UUID) -> Publicacao | None:
        if model is Publicacao:
            return self._storage.get(entity_id)
        raise TypeError("Unsupported model")

    def delete(self, entity: Publicacao) -> None:
        self._storage.pop(entity.id, None)


def test_publicacao_crud_flow() -> None:
    """A publication can be created, fetched, updated, listed, and deleted."""
    fake_db = FakeSession()

    async def get_fake_db():
        yield fake_db

    app.dependency_overrides[get_db] = get_fake_db
    transport = ASGITransport(app=app)

    async def run_test() -> None:
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            create_response = await client.post(
                "/api/v1/publicacoes",
                json={
                    "empresa_id": str(uuid4()),
                    "post_id": str(uuid4()),
                    "plataforma": "instagram",
                    "status": "pendente",
                    "agendado_para": datetime.utcnow().isoformat(),
                    "payload_publicacao": {"texto": "Publicar hoje"},
                },
            )
            assert create_response.status_code == status.HTTP_201_CREATED
            publicacao = create_response.json()
            assert publicacao["plataforma"] == "instagram"
            assert publicacao["status"] == "pendente"
            publicacao_id = publicacao["id"]

            get_response = await client.get(f"/api/v1/publicacoes/{publicacao_id}")
            assert get_response.status_code == status.HTTP_200_OK
            assert get_response.json()["id"] == publicacao_id

            list_response = await client.get("/api/v1/publicacoes")
            assert list_response.status_code == status.HTTP_200_OK
            assert len(list_response.json()) == 1

            update_response = await client.put(
                f"/api/v1/publicacoes/{publicacao_id}",
                json={"status": "agendada", "permalink": "http://instagram.com/post"},
            )
            assert update_response.status_code == status.HTTP_200_OK
            assert update_response.json()["status"] == "agendada"
            assert update_response.json()["permalink"] == "http://instagram.com/post"

            delete_response = await client.delete(f"/api/v1/publicacoes/{publicacao_id}")
            assert delete_response.status_code == status.HTTP_200_OK

            not_found_response = await client.get(f"/api/v1/publicacoes/{publicacao_id}")
            assert not_found_response.status_code == status.HTTP_404_NOT_FOUND

    import asyncio

    asyncio.run(run_test())
    app.dependency_overrides.pop(get_db, None)
