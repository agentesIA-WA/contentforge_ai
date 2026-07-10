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
