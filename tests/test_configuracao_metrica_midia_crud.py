"""Tests for CRUD APIs of configurações, métricas, and mídias."""

from decimal import Decimal
from uuid import UUID, uuid4

from fastapi import status
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.database.session import get_db
from app.models.configuracao import Configuracao
from app.models.metrica import Metrica
from app.models.midia import Midia


class FakeQuery:
    def __init__(self, items: list[object]) -> None:
        self._items = items

    def all(self) -> list[object]:
        return list(self._items)


class FakeSession:
    def __init__(self) -> None:
        self._storage: dict[type, dict[UUID, object]] = {}

    def add(self, entity: object) -> None:
        if getattr(entity, "id", None) is None:
            entity.id = uuid4()
        container = self._storage.setdefault(type(entity), {})
        container[entity.id] = entity

    def commit(self) -> None:
        pass

    def refresh(self, entity: object) -> None:
        pass

    def query(self, model):
        return FakeQuery(list(self._storage.get(model, {}).values()))

    def get(self, model, entity_id: UUID):
        return self._storage.get(model, {}).get(entity_id)

    def delete(self, entity: object) -> None:
        self._storage.get(type(entity), {}).pop(entity.id, None)


def test_configuracao_crud_flow() -> None:
    fake_db = FakeSession()

    async def get_fake_db():
        yield fake_db

    app.dependency_overrides[get_db] = get_fake_db
    transport = ASGITransport(app=app)

    async def run_test() -> None:
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            create_response = await client.post(
                "/api/v1/configuracoes",
                json={
                    "empresa_id": str(uuid4()),
                    "chave": "fuso_horario",
                    "valor": {"timezone": "America/Sao_Paulo"},
                    "descricao": "Fuso horário padrão",
                    "sensivel": False,
                    "ativa": True,
                },
            )
            assert create_response.status_code == status.HTTP_201_CREATED
            configuracao = create_response.json()
            assert configuracao["chave"] == "fuso_horario"
            configuracao_id = configuracao["id"]

            get_response = await client.get(f"/api/v1/configuracoes/{configuracao_id}")
            assert get_response.status_code == status.HTTP_200_OK
            assert get_response.json()["id"] == configuracao_id

            list_response = await client.get("/api/v1/configuracoes")
            assert list_response.status_code == status.HTTP_200_OK
            assert len(list_response.json()) == 1

            update_response = await client.put(
                f"/api/v1/configuracoes/{configuracao_id}",
                json={"descricao": "Fuso horário do salão", "ativa": False},
            )
            assert update_response.status_code == status.HTTP_200_OK
            assert update_response.json()["descricao"] == "Fuso horário do salão"
            assert update_response.json()["ativa"] is False

            delete_response = await client.delete(f"/api/v1/configuracoes/{configuracao_id}")
            assert delete_response.status_code == status.HTTP_200_OK

            not_found_response = await client.get(f"/api/v1/configuracoes/{configuracao_id}")
            assert not_found_response.status_code == status.HTTP_404_NOT_FOUND

    import asyncio

    asyncio.run(run_test())
    app.dependency_overrides.pop(get_db, None)


def test_metrica_crud_flow() -> None:
    fake_db = FakeSession()

    async def get_fake_db():
        yield fake_db

    app.dependency_overrides[get_db] = get_fake_db
    transport = ASGITransport(app=app)

    async def run_test() -> None:
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            create_response = await client.post(
                "/api/v1/metricas",
                json={
                    "empresa_id": str(uuid4()),
                    "publicacao_id": str(uuid4()),
                    "curtidas": 100,
                    "comentarios": 10,
                    "compartilhamentos": 5,
                    "alcance": 2500,
                    "impressoes": 6000,
                    "taxa_engajamento": "0.0417",
                },
            )
            assert create_response.status_code == status.HTTP_201_CREATED
            metrica = create_response.json()
            assert metrica["curtidas"] == 100
            assert Decimal(metrica["taxa_engajamento"]) == Decimal("0.0417")
            metrica_id = metrica["id"]

            get_response = await client.get(f"/api/v1/metricas/{metrica_id}")
            assert get_response.status_code == status.HTTP_200_OK
            assert get_response.json()["id"] == metrica_id

            list_response = await client.get("/api/v1/metricas")
            assert list_response.status_code == status.HTTP_200_OK
            assert len(list_response.json()) == 1

            update_response = await client.put(
                f"/api/v1/metricas/{metrica_id}",
                json={"comentarios": 12, "alcance": 3000},
            )
            assert update_response.status_code == status.HTTP_200_OK
            assert update_response.json()["comentarios"] == 12
            assert update_response.json()["alcance"] == 3000

            delete_response = await client.delete(f"/api/v1/metricas/{metrica_id}")
            assert delete_response.status_code == status.HTTP_200_OK

            not_found_response = await client.get(f"/api/v1/metricas/{metrica_id}")
            assert not_found_response.status_code == status.HTTP_404_NOT_FOUND

    import asyncio

    asyncio.run(run_test())
    app.dependency_overrides.pop(get_db, None)


def test_midia_crud_flow() -> None:
    fake_db = FakeSession()

    async def get_fake_db():
        yield fake_db

    app.dependency_overrides[get_db] = get_fake_db
    transport = ASGITransport(app=app)

    async def run_test() -> None:
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            create_response = await client.post(
                "/api/v1/midias",
                json={
                    "empresa_id": str(uuid4()),
                    "post_id": str(uuid4()),
                    "prompt_id": str(uuid4()),
                    "tipo": "imagem",
                    "url": "https://example.com/asset.png",
                    "caminho_arquivo": "/tmp/asset.png",
                    "alt_text": "Imagem de teste",
                    "metadados": {"resolucao": "1080x1080"},
                },
            )
            assert create_response.status_code == status.HTTP_201_CREATED
            midia = create_response.json()
            assert midia["tipo"] == "imagem"
            midia_id = midia["id"]

            get_response = await client.get(f"/api/v1/midias/{midia_id}")
            assert get_response.status_code == status.HTTP_200_OK
            assert get_response.json()["id"] == midia_id

            list_response = await client.get("/api/v1/midias")
            assert list_response.status_code == status.HTTP_200_OK
            assert len(list_response.json()) == 1

            update_response = await client.put(
                f"/api/v1/midias/{midia_id}",
                json={"url": "https://example.com/asset-updated.png", "alt_text": "Imagem atualizada"},
            )
            assert update_response.status_code == status.HTTP_200_OK
            assert update_response.json()["url"] == "https://example.com/asset-updated.png"
            assert update_response.json()["alt_text"] == "Imagem atualizada"

            delete_response = await client.delete(f"/api/v1/midias/{midia_id}")
            assert delete_response.status_code == status.HTTP_200_OK

            not_found_response = await client.get(f"/api/v1/midias/{midia_id}")
            assert not_found_response.status_code == status.HTTP_404_NOT_FOUND

    import asyncio

    asyncio.run(run_test())
    app.dependency_overrides.pop(get_db, None)
