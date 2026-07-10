"""Tests for the Calendario Editorial CRUD API."""

from datetime import date
from uuid import UUID, uuid4

from fastapi import status
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.database.session import get_db
from app.models.calendario_editorial import CalendarioEditorial


class FakeQuery:
    def __init__(self, items: list[CalendarioEditorial]) -> None:
        self._items = items

    def all(self) -> list[CalendarioEditorial]:
        return list(self._items)


class FakeSession:
    def __init__(self) -> None:
        self._storage: dict[UUID, CalendarioEditorial] = {}

    def add(self, entity: CalendarioEditorial) -> None:
        if entity.id is None:
            entity.id = uuid4()
        self._storage[entity.id] = entity

    def commit(self) -> None:
        pass

    def refresh(self, entity: CalendarioEditorial) -> None:
        pass

    def query(self, model):
        if model is CalendarioEditorial:
            return FakeQuery(list(self._storage.values()))
        raise TypeError("Unsupported model")

    def get(self, model, entity_id: UUID) -> CalendarioEditorial | None:
        if model is CalendarioEditorial:
            return self._storage.get(entity_id)
        raise TypeError("Unsupported model")

    def delete(self, entity: CalendarioEditorial) -> None:
        self._storage.pop(entity.id, None)


def test_calendario_editorial_crud_flow() -> None:
    fake_db = FakeSession()

    async def get_fake_db():
        yield fake_db

    app.dependency_overrides[get_db] = get_fake_db
    transport = ASGITransport(app=app)

    async def run_test() -> None:
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            create_response = await client.post(
                "/api/v1/calendario-editorial",
                json={
                    "empresa_id": str(uuid4()),
                    "titulo": "Conteúdo de Verão",
                    "descricao": "Planejamento de post para campanha",
                    "data_planejada": date.today().isoformat(),
                    "tema": "promoção",
                },
            )
            assert create_response.status_code == status.HTTP_201_CREATED
            calendario = create_response.json()
            assert calendario["titulo"] == "Conteúdo de Verão"
            calendario_id = calendario["id"]

            get_response = await client.get(f"/api/v1/calendario-editorial/{calendario_id}")
            assert get_response.status_code == status.HTTP_200_OK
            assert get_response.json()["id"] == calendario_id

            list_response = await client.get("/api/v1/calendario-editorial")
            assert list_response.status_code == status.HTTP_200_OK
            assert len(list_response.json()) == 1

            update_response = await client.put(
                f"/api/v1/calendario-editorial/{calendario_id}",
                json={"status": "aprovado", "observacoes": "Revisado e aprovado"},
            )
            assert update_response.status_code == status.HTTP_200_OK
            assert update_response.json()["status"] == "aprovado"
            assert update_response.json()["observacoes"] == "Revisado e aprovado"

            delete_response = await client.delete(f"/api/v1/calendario-editorial/{calendario_id}")
            assert delete_response.status_code == status.HTTP_200_OK

            not_found_response = await client.get(f"/api/v1/calendario-editorial/{calendario_id}")
            assert not_found_response.status_code == status.HTTP_404_NOT_FOUND

    import asyncio

    asyncio.run(run_test())
    app.dependency_overrides.pop(get_db, None)
