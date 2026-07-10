# Beauty Content AI - Arquitetura Inicial

## Objetivo da Entrega 1

Esta entrega cria a base executavel do projeto: estrutura modular, FastAPI,
configuracao por ambiente, conexao PostgreSQL via SQLAlchemy e suporte a
migracoes com Alembic.

## Decisoes

- `app/main.py` contem a fabrica da aplicacao FastAPI.
- `main.py` na raiz existe para facilitar `uvicorn main:app --reload`.
- `app/core` concentra configuracao e logging.
- `app/database` concentra engine, sessao e base declarativa do SQLAlchemy.
- `app/models/base.py` define o mixin obrigatorio com `id`, `data_criacao` e
  `data_atualizacao`.
- `alembic/env.py` le a mesma `DATABASE_URL` usada pela aplicacao.
- As tabelas de dominio serao adicionadas em entregas incrementais para manter
  o projeto sempre executavel.

## Proximas Entregas

1. Criar schemas Pydantic e repositorios.
2. Criar endpoints REST de empresas e servicos.
3. Implementar os agentes de conteudo de forma independente.
4. Criar interface HTML + Bootstrap inicial.
