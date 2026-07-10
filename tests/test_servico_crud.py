"""Tests for the Servico CRUD API."""

from decimal import Decimal
from uuid import UUID, uuid4

from fastapi import status
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.database.session import get_db
from app.models.servico import Servico


class FakeQuery:
    def __init__(self, items: list[Servico]) -> None:
        self._items = items

    def all(self) -> list[Servico]:
        return list(self._items)


class FakeSession:
    def __init__(self) -> None:
        self._storage: dict[UUID, Servico] = {}

    def add(self, entity: Servico) -> None:
        if entity.id is None:
            entity.id = uuid4()
        self._storage[entity.id] = entity

    def commit(self) -> None:
        pass

    def refresh(self, entity: Servico) -> None:
        pass

    def query(self, model):
        if model is Servico:
            return FakeQuery(list(self._storage.values()))
        raise TypeError("Unsupported model")

    def get(self, model, entity_id: UUID) -> Servico | None:
        if model is Servico:
            return self._storage.get(entity_id)
        raise TypeError("Unsupported model")

    def delete(self, entity: Servico) -> None:
        self._storage.pop(entity.id, None)


async def get_fake_db() -> FakeSession:
    yield FakeSession()


def test_servico_crud_flow() -> None:
    """A service can be created, fetched, updated, listed, and deleted."""
    fake_db = FakeSession()

    async def get_fake_db_override():
        yield fake_db

    app.dependency_overrides[get_db] = get_fake_db_override

    transport = ASGITransport(app=app)

    async def run_test() -> None:
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            create_response = await client.post(
                "/api/v1/servicos",
                json={
                    "empresa_id": str(uuid4()),
                    "nome": "Corte de Cabelo",
                    "descricao": "Corte masculino com acabamento",
                    "categoria": "Cabelo",
                    "duracao_minutos": 45,
                    "preco_estimado": "120.00",
                },
            )
            assert create_response.status_code == status.HTTP_201_CREATED
            servico = create_response.json()
            assert servico["nome"] == "Corte de Cabelo"
            assert servico["categoria"] == "Cabelo"
            servico_id = servico["id"]

            get_response = await client.get(f"/api/v1/servicos/{servico_id}")
            assert get_response.status_code == status.HTTP_200_OK
            assert get_response.json()["id"] == servico_id

            list_response = await client.get("/api/v1/servicos")
            assert list_response.status_code == status.HTTP_200_OK
            assert len(list_response.json()) == 1

            update_response = await client.put(
                f"/api/v1/servicos/{servico_id}",
                json={"duracao_minutos": 60, "ativo": False},
            )
            assert update_response.status_code == status.HTTP_200_OK
            assert update_response.json()["duracao_minutos"] == 60
            assert update_response.json()["ativo"] is False

            delete_response = await client.delete(f"/api/v1/servicos/{servico_id}")
            assert delete_response.status_code == status.HTTP_200_OK

            not_found_response = await client.get(f"/api/v1/servicos/{servico_id}")
            assert not_found_response.status_code == status.HTTP_404_NOT_FOUND

    import asyncio

    asyncio.run(run_test())
    app.dependency_overrides.pop(get_db, None)
