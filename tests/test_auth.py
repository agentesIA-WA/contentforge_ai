"""Tests for authentication endpoints."""

from uuid import UUID, uuid4

from fastapi import status
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.core.security import get_password_hash
from app.database.session import get_db
from app.models.usuario import Usuario


class FakeQuery:
    def __init__(self, items: list[Usuario]) -> None:
        self._items = items

    def filter(self, condition):
        if hasattr(condition, "right") and condition.right is not None:
            value = condition.right.value
            key = condition.left.key
            return FakeQuery([user for user in self._items if getattr(user, key) == value])
        return FakeQuery([])

    def first(self) -> Usuario | None:
        return self._items[0] if self._items else None


class FakeSession:
    def __init__(self, initial_users: list[Usuario] | None = None) -> None:
        self._storage: dict[UUID, Usuario] = {}
        for user in initial_users or []:
            self._storage[user.id] = user

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


def test_invalid_login_returns_401() -> None:
    fake_db = FakeSession()

    async def get_fake_db():
        yield fake_db

    app.dependency_overrides[get_db] = get_fake_db
    transport = ASGITransport(app=app)

    async def run_test() -> None:
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/login",
                data={"username": "naoexiste@example.com", "password": "senha"},
            )
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

    import asyncio

    asyncio.run(run_test())
    app.dependency_overrides.pop(get_db, None)


def test_login_returns_token_and_me_endpoint_works() -> None:
    user = Usuario(
        id=uuid4(),
        nome="João",
        email="joao@example.com",
        senha_hash=get_password_hash("senha-segura"),
        perfil="admin",
        ativo=True,
    )
    fake_db = FakeSession(initial_users=[user])

    async def get_fake_db():
        yield fake_db

    app.dependency_overrides[get_db] = get_fake_db
    transport = ASGITransport(app=app)

    async def run_test() -> None:
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            login_response = await client.post(
                "/api/v1/login",
                data={"username": "joao@example.com", "password": "senha-segura"},
            )
            assert login_response.status_code == status.HTTP_200_OK
            token_data = login_response.json()
            assert token_data["token_type"] == "bearer"
            assert "access_token" in token_data

            bearer = f"Bearer {token_data['access_token']}"
            me_response = await client.get("/api/v1/me", headers={"Authorization": bearer})
            assert me_response.status_code == status.HTTP_200_OK
            assert me_response.json()["email"] == "joao@example.com"

    import asyncio

    asyncio.run(run_test())
    app.dependency_overrides.pop(get_db, None)
