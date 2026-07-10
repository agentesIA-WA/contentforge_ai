"""Tests for the Usuario CRUD API."""

from uuid import UUID, uuid4

from fastapi import status
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.database.session import get_db
from app.models.usuario import Usuario


class FakeQuery:
    def __init__(self, items: list[Usuario]) -> None:
        self._items = items

    def all(self) -> list[Usuario]:
        return list(self._items)

    def filter(self, condition):
        if hasattr(condition, "right") and condition.right is not None:
            value = condition.right.value
            key = condition.left.key
            if key == "email":
                for item in self._items:
                    if getattr(item, key) == value:
                        return FakeQuery([item])
        return FakeQuery([])

    def first(self) -> Usuario | None:
        return self._items[0] if self._items else None


class FakeSession:
    def __init__(self) -> None:
        self._storage: dict[UUID, Usuario] = {}

    def add(self, entity: Usuario) -> None:
        if entity.id is None:
            entity.id = uuid4()
        self._storage[entity.id] = entity

    def commit(self) -> None:
        pass

    def refresh(self, entity: Usuario) -> None:
        pass

    def query(self, model):
        if model is Usuario:
            return FakeQuery(list(self._storage.values()))
        raise TypeError("Unsupported model")

    def get(self, model, entity_id: UUID) -> Usuario | None:
        if model is Usuario:
            return self._storage.get(entity_id)
        raise TypeError("Unsupported model")

    def delete(self, entity: Usuario) -> None:
        self._storage.pop(entity.id, None)


def test_usuario_crud_flow() -> None:
    fake_db = FakeSession()

    async def get_fake_db():
        yield fake_db

    app.dependency_overrides[get_db] = get_fake_db
    transport = ASGITransport(app=app)

    async def run_test() -> None:
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            create_response = await client.post(
                "/api/v1/usuarios",
                json={
                    "nome": "Maria",
                    "email": "maria@example.com",
                    "senha": "senha-segura",
                    "perfil": "editor",
                },
            )
            assert create_response.status_code == status.HTTP_201_CREATED
            usuario = create_response.json()
            assert usuario["nome"] == "Maria"
            assert usuario["email"] == "maria@example.com"
            usuario_id = usuario["id"]

            get_response = await client.get(f"/api/v1/usuarios/{usuario_id}")
            assert get_response.status_code == status.HTTP_200_OK
            assert get_response.json()["id"] == usuario_id

            list_response = await client.get("/api/v1/usuarios")
            assert list_response.status_code == status.HTTP_200_OK
            assert len(list_response.json()) == 1

            update_response = await client.put(
                f"/api/v1/usuarios/{usuario_id}",
                json={"nome": "Maria Clara", "ativo": False},
            )
            assert update_response.status_code == status.HTTP_200_OK
            assert update_response.json()["nome"] == "Maria Clara"
            assert update_response.json()["ativo"] is False

            delete_response = await client.delete(f"/api/v1/usuarios/{usuario_id}")
            assert delete_response.status_code == status.HTTP_200_OK

            not_found_response = await client.get(f"/api/v1/usuarios/{usuario_id}")
            assert not_found_response.status_code == status.HTTP_404_NOT_FOUND

    import asyncio

    asyncio.run(run_test())
    app.dependency_overrides.pop(get_db, None)
