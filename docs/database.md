# Beauty Content AI - Modelo de Dados Inicial

## Objetivo da Entrega 2

Esta entrega cria os modelos ORM e a primeira migration Alembic para as dez
tabelas iniciais do produto:

- `empresas`
- `usuarios`
- `servicos`
- `calendario_editorial`
- `posts`
- `midias`
- `publicacoes`
- `metricas`
- `prompts`
- `configuracoes`

Todas as tabelas possuem `id`, `data_criacao` e `data_atualizacao`.

## Decisoes de Modelagem

- As chaves primarias usam UUID, conforme requisito do produto.
- Os timestamps usam `DateTime(timezone=True)` para armazenar valores com fuso.
- Campos estruturados flexiveis usam `JSONB`, como identidade visual, hashtags,
  parametros de prompts e payloads de publicacao.
- Status e tipos usam `TEXT` com `CHECK CONSTRAINT`, evitando migrations
  complexas de enum no inicio do projeto.
- Toda foreign key recebeu indice explicito, pois o PostgreSQL nao cria esses
  indices automaticamente.
- Foram adicionados indices compostos para os fluxos mais provaveis:
  calendario por empresa/data, posts por empresa/status, publicacoes agendadas
  e metricas por empresa/data de coleta.

## Relacionamentos Principais

- Uma `empresa` possui usuarios, servicos, calendario, posts, midias,
  publicacoes, metricas, prompts e configuracoes.
- Um `post` pode nascer de um item de `calendario_editorial` e de um `servico`.
- Um `post` pode possuir midias, prompts e publicacoes.
- Uma `publicacao` pode possuir varias coletas de `metricas`.
- Uma `configuracao` e unica por `empresa_id` e `chave`.

## Como Aplicar a Migration

Com o ambiente virtual ativo e a `DATABASE_URL` configurada:

```bash
alembic upgrade head
```

Para desfazer:

```bash
alembic downgrade base
```

