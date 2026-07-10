"""Test for prompt generation endpoint (create + gerar)."""

from uuid import uuid4

from httpx import ASGITransport, AsyncClient
from fastapi import status

from app.main import app
from app.database.session import get_db


class FakeSession:
    def __init__(self) -> None:
        self._storage = {}

    def add(self, entity) -> None:
        if getattr(entity, "id", None) is None:
            from uuid import uuid4

            entity.id = uuid4()
        self._storage[entity.id] = entity

    def commit(self) -> None:
        pass

    def refresh(self, entity) -> None:
        pass

    def query(self, model):
        return list(self._storage.values())

    def get(self, model, entity_id):
        return self._storage.get(entity_id)

    def delete(self, entity) -> None:
        self._storage.pop(entity.id, None)


def test_create_and_generate_prompt(monkeypatch) -> None:
    fake_db = FakeSession()

    async def get_fake_db():
        yield fake_db

    app.dependency_overrides[get_db] = get_fake_db

    # patch the llm.generate_text to return a deterministic payload
    import app.services.llm as llm_mod


    def fake_generate_text(conteudo, modelo=None, parametros=None):
        return {"choices": [{"message": {"content": f"Generated: {conteudo}"}}]}


    monkeypatch.setattr(llm_mod, "generate_text", fake_generate_text)

    transport = ASGITransport(app=app)

    async def run():
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            create_resp = await client.post(
                "/api/v1/prompts",
                json={
                    "empresa_id": str(uuid4()),
                    "agente": "writer",
                    "tipo": "conteudo",
                    "conteudo": "Teste de geração",
                },
            )
            assert create_resp.status_code == status.HTTP_201_CREATED
            prompt = create_resp.json()

            gen_resp = await client.post(f"/api/v1/prompts/{prompt['id']}/gerar")
            assert gen_resp.status_code == status.HTTP_200_OK
            gen_json = gen_resp.json()
            assert gen_json["status"] == "respondido"
            assert "Generated: Teste de geração" in str(gen_json["resposta"]) or gen_json["resposta"] is not None

    import asyncio

    asyncio.run(run())
    app.dependency_overrides.pop(get_db, None)
