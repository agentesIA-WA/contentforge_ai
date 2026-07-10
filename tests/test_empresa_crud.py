"""Tests for the Empresa CRUD API."""

from uuid import UUID, uuid4

from fastapi import status
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.database.session import get_db
from app.models.empresa import Empresa
from app.models.post import Post
from app.models.publicacao import Publicacao


class FakeQuery:
    def __init__(self, items: list[Empresa]) -> None:
        self._items = items

    def all(self) -> list[Empresa]:
        return list(self._items)


class FakeSession:
    def __init__(self) -> None:
        self._storage: dict[UUID, Empresa] = {}

    def add(self, entity: Empresa) -> None:
        if entity.id is None:
            entity.id = uuid4()
        self._storage[entity.id] = entity

    def commit(self) -> None:
        pass

    def refresh(self, entity: Empresa) -> None:
        pass

    def query(self, model):
        if model is Empresa:
            return FakeQuery(list(self._storage.values()))
        raise TypeError("Unsupported model")

    def get(self, model, entity_id: UUID) -> Empresa | None:
        if model is Empresa:
            return self._storage.get(entity_id)
        raise TypeError("Unsupported model")

    def delete(self, entity: Empresa) -> None:
        self._storage.pop(entity.id, None)


def test_empresa_crud_flow() -> None:
    """A company can be created, fetched, updated, listed, and deleted."""
    fake_db = FakeSession()

    async def get_fake_db():
        yield fake_db

    app.dependency_overrides[get_db] = get_fake_db

    transport = ASGITransport(app=app)

    async def run_test() -> None:
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            create_response = await client.post(
                "/api/v1/empresas",
                json={
                    "nome": "Salão Exemplo",
                    "nicho": "Cabeleireiro",
                    "email_contato": "contato@example.com",
                },
            )
            assert create_response.status_code == status.HTTP_201_CREATED
            empresa = create_response.json()
            assert empresa["nome"] == "Salão Exemplo"
            assert empresa["nicho"] == "Cabeleireiro"
            empresa_id = empresa["id"]

            get_response = await client.get(f"/api/v1/empresas/{empresa_id}")
            assert get_response.status_code == status.HTTP_200_OK
            assert get_response.json()["id"] == empresa_id

            list_response = await client.get("/api/v1/empresas")
            assert list_response.status_code == status.HTTP_200_OK
            assert len(list_response.json()) == 1

            update_response = await client.put(
                f"/api/v1/empresas/{empresa_id}",
                json={"cidade": "São Paulo", "ativa": False},
            )
            assert update_response.status_code == status.HTTP_200_OK
            assert update_response.json()["cidade"] == "São Paulo"
            assert update_response.json()["ativa"] is False

            delete_response = await client.delete(f"/api/v1/empresas/{empresa_id}")
            assert delete_response.status_code == status.HTTP_200_OK

            not_found_response = await client.get(f"/api/v1/empresas/{empresa_id}")
            assert not_found_response.status_code == status.HTTP_404_NOT_FOUND

    import asyncio

    asyncio.run(run_test())
    app.dependency_overrides.pop(get_db, None)


def test_empresa_nested_relations_are_exposed() -> None:
    fake_db = FakeSession()
    empresa_id = uuid4()
    post_id = uuid4()
    publicacao_id = uuid4()

    empresa = Empresa(
        id=empresa_id,
        nome="Salão Relacionado",
        nicho="Estética",
        email_contato="contato2@example.com",
        identidade_visual={},
        horario_funcionamento={},
        ativa=True,
    )
    empresa.posts = [
        Post(
            id=post_id,
            empresa_id=empresa_id,
            titulo="Post Relacionado",
            formato="feed",
            status="rascunho",
            hashtags=["#relacionado"],
            conteudo_estruturado={"texto": "Teste"},
        )
    ]
    empresa.publicacoes = [
        Publicacao(
            id=publicacao_id,
            empresa_id=empresa_id,
            post_id=post_id,
            plataforma="instagram",
            status="pendente",
            payload_publicacao={},
        )
    ]
    fake_db._storage[empresa_id] = empresa

    async def get_fake_db():
        yield fake_db

    app.dependency_overrides[get_db] = get_fake_db
    transport = ASGITransport(app=app)

    async def run_test() -> None:
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            posts_response = await client.get(f"/api/v1/empresas/{empresa_id}/posts")
            assert posts_response.status_code == status.HTTP_200_OK
            assert posts_response.json()[0]["id"] == str(post_id)

            publicacoes_response = await client.get(f"/api/v1/empresas/{empresa_id}/publicacoes")
            assert publicacoes_response.status_code == status.HTTP_200_OK
            assert publicacoes_response.json()[0]["id"] == str(publicacao_id)

    import asyncio

    asyncio.run(run_test())
    app.dependency_overrides.pop(get_db, None)
