"""Tests for the Prompt CRUD API."""

from uuid import UUID, uuid4

from fastapi import status
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.database.session import get_db
from app.models.prompt import Prompt


class FakeQuery:
    def __init__(self, items: list[Prompt]) -> None:
        self._items = items

    def all(self) -> list[Prompt]:
        return list(self._items)


class FakeSession:
    def __init__(self) -> None:
        self._storage: dict[UUID, Prompt] = {}

    def add(self, entity: Prompt) -> None:
        if entity.id is None:
            entity.id = uuid4()
        self._storage[entity.id] = entity

    def commit(self) -> None:
        pass

    def refresh(self, entity: Prompt) -> None:
        pass

    def query(self, model):
        if model is Prompt:
            return FakeQuery(list(self._storage.values()))
        raise TypeError("Unsupported model")

    def get(self, model, entity_id: UUID) -> Prompt | None:
        if model is Prompt:
            return self._storage.get(entity_id)
        raise TypeError("Unsupported model")

    def delete(self, entity: Prompt) -> None:
        self._storage.pop(entity.id, None)


def test_prompt_crud_flow() -> None:
    """A prompt can be created, fetched, updated, listed, and deleted."""
    fake_db = FakeSession()

    async def get_fake_db():
        yield fake_db

    app.dependency_overrides[get_db] = get_fake_db
    transport = ASGITransport(app=app)

    async def run_test() -> None:
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            create_response = await client.post(
                "/api/v1/prompts",
                json={
                    "empresa_id": str(uuid4()),
                    "agente": "writer",
                    "tipo": "conteudo",
                    "conteudo": "Escreva um post sobre salão de beleza.",
                    "parametros": {"tom": "amigavel"},
                    "modelo_ia": "gpt-4",
                },
            )
            assert create_response.status_code == status.HTTP_201_CREATED
            prompt = create_response.json()
            assert prompt["agente"] == "writer"
            assert prompt["tipo"] == "conteudo"
            prompt_id = prompt["id"]

            get_response = await client.get(f"/api/v1/prompts/{prompt_id}")
            assert get_response.status_code == status.HTTP_200_OK
            assert get_response.json()["id"] == prompt_id

            list_response = await client.get("/api/v1/prompts")
            assert list_response.status_code == status.HTTP_200_OK
            assert len(list_response.json()) == 1

            update_response = await client.put(
                f"/api/v1/prompts/{prompt_id}",
                json={"status": "respondido", "resposta": {"texto": "Aqui está o post."}},
            )
            assert update_response.status_code == status.HTTP_200_OK
            assert update_response.json()["status"] == "respondido"
            assert update_response.json()["resposta"]["texto"] == "Aqui está o post."

            delete_response = await client.delete(f"/api/v1/prompts/{prompt_id}")
            assert delete_response.status_code == status.HTTP_200_OK

            not_found_response = await client.get(f"/api/v1/prompts/{prompt_id}")
            assert not_found_response.status_code == status.HTTP_404_NOT_FOUND

    import asyncio

    asyncio.run(run_test())
    app.dependency_overrides.pop(get_db, None)
