"""Tests for the Post CRUD API."""

from datetime import datetime
from uuid import UUID, uuid4

from fastapi import status
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.database.session import get_db
from app.models.post import Post


class FakeQuery:
    def __init__(self, items: list[Post]) -> None:
        self._items = items

    def all(self) -> list[Post]:
        return list(self._items)


class FakeSession:
    def __init__(self) -> None:
        self._storage: dict[UUID, Post] = {}

    def add(self, entity: Post) -> None:
        if entity.id is None:
            entity.id = uuid4()
        self._storage[entity.id] = entity

    def commit(self) -> None:
        pass

    def refresh(self, entity: Post) -> None:
        pass

    def query(self, model):
        if model is Post:
            return FakeQuery(list(self._storage.values()))
        raise TypeError("Unsupported model")

    def get(self, model, entity_id: UUID) -> Post | None:
        if model is Post:
            return self._storage.get(entity_id)
        raise TypeError("Unsupported model")

    def delete(self, entity: Post) -> None:
        self._storage.pop(entity.id, None)


def test_post_crud_flow() -> None:
    """A post can be created, fetched, updated, listed, and deleted."""
    fake_db = FakeSession()

    async def get_fake_db():
        yield fake_db

    app.dependency_overrides[get_db] = get_fake_db
    transport = ASGITransport(app=app)

    async def run_test() -> None:
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            create_response = await client.post(
                "/api/v1/posts",
                json={
                    "empresa_id": str(uuid4()),
                    "titulo": "Post Teste",
                    "formato": "feed",
                    "status": "rascunho",
                    "hashtags": ["#teste"],
                    "conteudo_estruturado": {"texto": "ola"},
                    "data_publicacao_sugerida": datetime.utcnow().isoformat(),
                },
            )
            assert create_response.status_code == status.HTTP_201_CREATED
            post = create_response.json()
            assert post["titulo"] == "Post Teste"
            assert post["status"] == "rascunho"
            post_id = post["id"]

            get_response = await client.get(f"/api/v1/posts/{post_id}")
            assert get_response.status_code == status.HTTP_200_OK
            assert get_response.json()["id"] == post_id

            list_response = await client.get("/api/v1/posts")
            assert list_response.status_code == status.HTTP_200_OK
            assert len(list_response.json()) == 1

            update_response = await client.put(
                f"/api/v1/posts/{post_id}",
                json={"status": "aprovado", "legenda": "Atualizado"},
            )
            assert update_response.status_code == status.HTTP_200_OK
            assert update_response.json()["status"] == "aprovado"
            assert update_response.json()["legenda"] == "Atualizado"

            delete_response = await client.delete(f"/api/v1/posts/{post_id}")
            assert delete_response.status_code == status.HTTP_200_OK

            not_found_response = await client.get(f"/api/v1/posts/{post_id}")
            assert not_found_response.status_code == status.HTTP_404_NOT_FOUND

    import asyncio

    asyncio.run(run_test())
    app.dependency_overrides.pop(get_db, None)
