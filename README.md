# Beauty Content AI

Beauty Content AI e uma plataforma FastAPI para automatizar planejamento,
criacao, aprovacao e publicacao de conteudo para Instagram de saloes de beleza.

## Entrega 1

Esta primeira entrega inclui:

- Estrutura modular do projeto.
- Configuracao do FastAPI.
- Configuracao por `.env`.
- Logging padrao.
- Conexao PostgreSQL com SQLAlchemy.
- Alembic preparado para migracoes.
- Endpoint de health check.
- Teste inicial da API.

## Requisitos

- Python 3.12+
- PostgreSQL
- Credenciais do banco da Locaweb

Em Ubuntu/Debian, caso `python3 -m venv .venv` falhe por falta de `ensurepip`,
instale o pacote do sistema:

```bash
sudo apt-get install python3.12-venv
```

## Como executar

Crie e ative o ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependencias:

```bash
pip install -r requirements.txt
```

Crie o arquivo de ambiente:

```bash
cp .env.example .env
```

Edite a variavel `DATABASE_URL` com as credenciais do PostgreSQL da Locaweb.
As configuracoes da propria aplicacao usam o prefixo `APP_`, como
`APP_DEBUG` e `APP_API_PREFIX`, para evitar colisao com variaveis do sistema.

Execute a API:

```bash
uvicorn main:app --reload
```

Ou, caso os pacotes tenham sido instalados no `.venv` por `--target`:

```bash
.venv/bin/python -m uvicorn main:app --reload --port 8001
```

Acesse:

- API: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/api/v1/health
- Metadata tables: http://127.0.0.1:8000/api/v1/metadata/tables
- Empresas CRUD:
  - Listar: http://127.0.0.1:8000/api/v1/empresas
  - Criar: `POST http://127.0.0.1:8000/api/v1/empresas`
  - Buscar: http://127.0.0.1:8000/api/v1/empresas/{id}
  - Atualizar: `PUT http://127.0.0.1:8000/api/v1/empresas/{id}`
  - Excluir: `DELETE http://127.0.0.1:8000/api/v1/empresas/{id}`
- Serviços CRUD:
  - Listar: http://127.0.0.1:8000/api/v1/servicos
  - Criar: `POST http://127.0.0.1:8000/api/v1/servicos`
  - Buscar: http://127.0.0.1:8000/api/v1/servicos/{id}
  - Atualizar: `PUT http://127.0.0.1:8000/api/v1/servicos/{id}`
  - Excluir: `DELETE http://127.0.0.1:8000/api/v1/servicos/{id}`
- Posts CRUD:
  - Listar: http://127.0.0.1:8000/api/v1/posts
  - Criar: `POST http://127.0.0.1:8000/api/v1/posts`
  - Buscar: http://127.0.0.1:8000/api/v1/posts/{id}
  - Atualizar: `PUT http://127.0.0.1:8000/api/v1/posts/{id}`
  - Excluir: `DELETE http://127.0.0.1:8000/api/v1/posts/{id}`
- Prompts CRUD:
  - Listar: http://127.0.0.1:8000/api/v1/prompts
  - Criar: `POST http://127.0.0.1:8000/api/v1/prompts`
  - Buscar: http://127.0.0.1:8000/api/v1/prompts/{id}
  - Atualizar: `PUT http://127.0.0.1:8000/api/v1/prompts/{id}`
  - Excluir: `DELETE http://127.0.0.1:8000/api/v1/prompts/{id}`
- Calendário editorial CRUD:
  - Listar: http://127.0.0.1:8000/api/v1/calendario-editorial
  - Criar: `POST http://127.0.0.1:8000/api/v1/calendario-editorial`
  - Buscar: `GET http://127.0.0.1:8000/api/v1/calendario-editorial/{id}`
  - Atualizar: `PUT http://127.0.0.1:8000/api/v1/calendario-editorial/{id}`
  - Excluir: `DELETE http://127.0.0.1:8000/api/v1/calendario-editorial/{id}`
- Configurações CRUD:
  - Listar: http://127.0.0.1:8000/api/v1/configuracoes
  - Criar: `POST http://127.0.0.1:8000/api/v1/configuracoes`
  - Buscar: `GET http://127.0.0.1:8000/api/v1/configuracoes/{id}`
  - Atualizar: `PUT http://127.0.0.1:8000/api/v1/configuracoes/{id}`
  - Excluir: `DELETE http://127.0.0.1:8000/api/v1/configuracoes/{id}`
- Métricas CRUD:
  - Listar: http://127.0.0.1:8000/api/v1/metricas
  - Criar: `POST http://127.0.0.1:8000/api/v1/metricas`
  - Buscar: `GET http://127.0.0.1:8000/api/v1/metricas/{id}`
  - Atualizar: `PUT http://127.0.0.1:8000/api/v1/metricas/{id}`
  - Excluir: `DELETE http://127.0.0.1:8000/api/v1/metricas/{id}`
- Mídias CRUD:
  - Listar: http://127.0.0.1:8000/api/v1/midias
  - Criar: `POST http://127.0.0.1:8000/api/v1/midias`
  - Buscar: `GET http://127.0.0.1:8000/api/v1/midias/{id}`
  - Atualizar: `PUT http://127.0.0.1:8000/api/v1/midias/{id}`
  - Excluir: `DELETE http://127.0.0.1:8000/api/v1/midias/{id}`
- Publicações CRUD:
  - Listar: http://127.0.0.1:8000/api/v1/publicacoes
  - Criar: `POST http://127.0.0.1:8000/api/v1/publicacoes`
  - Buscar: http://127.0.0.1:8000/api/v1/publicacoes/{id}
  - Atualizar: `PUT http://127.0.0.1:8000/api/v1/publicacoes/{id}`
  - Excluir: `DELETE http://127.0.0.1:8000/api/v1/publicacoes/{id}`
- Usuários CRUD:
  - Listar: http://127.0.0.1:8000/api/v1/usuarios
  - Criar: `POST http://127.0.0.1:8000/api/v1/usuarios`
  - Buscar: http://127.0.0.1:8000/api/v1/usuarios/{id}
  - Atualizar: `PUT http://127.0.0.1:8000/api/v1/usuarios/{id}`
  - Excluir: `DELETE http://127.0.0.1:8000/api/v1/usuarios/{id}`
- Empresa nested resources:
  - Posts: `GET http://127.0.0.1:8000/api/v1/empresas/{id}/posts`
  - Publicações: `GET http://127.0.0.1:8000/api/v1/empresas/{id}/publicacoes`
  - Prompts: `GET http://127.0.0.1:8000/api/v1/empresas/{id}/prompts`
  - Serviços: `GET http://127.0.0.1:8000/api/v1/empresas/{id}/servicos`
  - Configurações: `GET http://127.0.0.1:8000/api/v1/empresas/{id}/configuracoes`
  - Métricas: `GET http://127.0.0.1:8000/api/v1/empresas/{id}/metricas`
- Autenticação:
  - Login: `POST http://127.0.0.1:8000/api/v1/login` (form data `username`, `password`)
  - Perfil atual: http://127.0.0.1:8000/api/v1/me

Se a porta `8000` já estiver em uso, você também pode iniciar em `8001`:

```bash
.venv/bin/python -m uvicorn main:app --reload --port 8001
```

## Alembic

Aplicar a migration inicial:

```bash
alembic upgrade head
```

Criar uma migracao:

```bash
alembic revision --autogenerate -m "create initial tables"
```

Aplicar migracoes:

```bash
alembic upgrade head
```

## Testes

```bash
pytest
```

Alternativa pelo Python do `.venv`:

```bash
.venv/bin/python -m pytest
```
