"""create initial tables

Revision ID: 20260710_0001
Revises:
Create Date: 2026-07-10 10:30:00.000000
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "20260710_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def uuid_pk() -> sa.Column:
    """Return the standard UUID primary key column."""
    return sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False)


def audit_columns() -> list[sa.Column]:
    """Return standard audit timestamp columns."""
    return [
        sa.Column(
            "data_criacao",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "data_atualizacao",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    ]


def upgrade() -> None:
    """Apply schema changes."""
    op.create_table(
        "empresas",
        uuid_pk(),
        *audit_columns(),
        sa.Column("nome", sa.Text(), nullable=False),
        sa.Column("nicho", sa.Text(), nullable=False),
        sa.Column("publico_alvo", sa.Text(), nullable=True),
        sa.Column("cidade", sa.Text(), nullable=True),
        sa.Column("objetivos", sa.Text(), nullable=True),
        sa.Column("tom_voz", sa.Text(), nullable=True),
        sa.Column(
            "identidade_visual",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
        sa.Column(
            "horario_funcionamento",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
        sa.Column("diferenciais", sa.Text(), nullable=True),
        sa.Column("instagram_handle", sa.Text(), nullable=True),
        sa.Column("telefone", sa.Text(), nullable=True),
        sa.Column("email_contato", sa.Text(), nullable=True),
        sa.Column("ativa", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_empresas")),
    )
    op.create_index(op.f("ix_empresas_nome"), "empresas", ["nome"])

    op.create_table(
        "usuarios",
        uuid_pk(),
        *audit_columns(),
        sa.Column("empresa_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("nome", sa.Text(), nullable=False),
        sa.Column("email", sa.Text(), nullable=False),
        sa.Column("senha_hash", sa.Text(), nullable=False),
        sa.Column("perfil", sa.Text(), server_default="admin", nullable=False),
        sa.Column("ativo", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("ultimo_login_em", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "perfil IN ('admin', 'editor', 'visualizador')",
            name=op.f("ck_usuarios_perfil"),
        ),
        sa.ForeignKeyConstraint(
            ["empresa_id"],
            ["empresas.id"],
            name=op.f("fk_usuarios_empresa_id_empresas"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_usuarios")),
        sa.UniqueConstraint("email", name=op.f("uq_usuarios_email")),
    )
    op.create_index(op.f("ix_usuarios_email"), "usuarios", ["email"])
    op.create_index(op.f("ix_usuarios_empresa_id"), "usuarios", ["empresa_id"])

    op.create_table(
        "servicos",
        uuid_pk(),
        *audit_columns(),
        sa.Column("empresa_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("nome", sa.Text(), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=True),
        sa.Column("categoria", sa.Text(), nullable=True),
        sa.Column("duracao_minutos", sa.Integer(), nullable=True),
        sa.Column("preco_estimado", sa.Numeric(10, 2), nullable=True),
        sa.Column("ativo", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.CheckConstraint(
            "duracao_minutos IS NULL OR duracao_minutos > 0",
            name=op.f("ck_servicos_duracao_positiva"),
        ),
        sa.CheckConstraint(
            "preco_estimado IS NULL OR preco_estimado >= 0",
            name=op.f("ck_servicos_preco_nao_negativo"),
        ),
        sa.ForeignKeyConstraint(
            ["empresa_id"],
            ["empresas.id"],
            name=op.f("fk_servicos_empresa_id_empresas"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_servicos")),
        sa.UniqueConstraint("empresa_id", "nome", name=op.f("uq_servicos_empresa_nome")),
    )
    op.create_index(op.f("ix_servicos_empresa_id"), "servicos", ["empresa_id"])
    op.create_index("ix_servicos_empresa_ativo", "servicos", ["empresa_id", "ativo"])

    op.create_table(
        "calendario_editorial",
        uuid_pk(),
        *audit_columns(),
        sa.Column("empresa_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("titulo", sa.Text(), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=True),
        sa.Column("data_planejada", sa.Date(), nullable=False),
        sa.Column("tema", sa.Text(), nullable=True),
        sa.Column("objetivo", sa.Text(), nullable=True),
        sa.Column("formato", sa.Text(), server_default="feed", nullable=False),
        sa.Column("canal", sa.Text(), server_default="instagram", nullable=False),
        sa.Column("status", sa.Text(), server_default="planejado", nullable=False),
        sa.Column("observacoes", sa.Text(), nullable=True),
        sa.CheckConstraint(
            "status IN ('planejado', 'em_producao', 'aprovado', 'publicado', 'cancelado')",
            name=op.f("ck_calendario_editorial_status"),
        ),
        sa.CheckConstraint(
            "formato IN ('feed', 'story', 'reels', 'carrossel', 'campanha')",
            name=op.f("ck_calendario_editorial_formato"),
        ),
        sa.ForeignKeyConstraint(
            ["empresa_id"],
            ["empresas.id"],
            name=op.f("fk_calendario_editorial_empresa_id_empresas"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_calendario_editorial")),
    )
    op.create_index(
        op.f("ix_calendario_editorial_empresa_id"),
        "calendario_editorial",
        ["empresa_id"],
    )
    op.create_index(
        "ix_calendario_editorial_empresa_data",
        "calendario_editorial",
        ["empresa_id", "data_planejada"],
    )

    op.create_table(
        "posts",
        uuid_pk(),
        *audit_columns(),
        sa.Column("empresa_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("calendario_editorial_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("servico_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("aprovado_por_usuario_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("titulo", sa.Text(), nullable=False),
        sa.Column("formato", sa.Text(), server_default="feed", nullable=False),
        sa.Column("status", sa.Text(), server_default="rascunho", nullable=False),
        sa.Column("legenda", sa.Text(), nullable=True),
        sa.Column("cta", sa.Text(), nullable=True),
        sa.Column(
            "hashtags",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'[]'::jsonb"),
            nullable=False,
        ),
        sa.Column(
            "conteudo_estruturado",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
        sa.Column("prompt_imagem", sa.Text(), nullable=True),
        sa.Column("data_publicacao_sugerida", sa.DateTime(timezone=True), nullable=True),
        sa.Column("aprovado_em", sa.DateTime(timezone=True), nullable=True),
        sa.Column("observacoes", sa.Text(), nullable=True),
        sa.CheckConstraint(
            "status IN ('rascunho', 'em_revisao', 'aprovado', 'agendado', 'publicado', 'rejeitado', 'arquivado')",
            name=op.f("ck_posts_status"),
        ),
        sa.CheckConstraint(
            "formato IN ('feed', 'story', 'reels', 'carrossel')",
            name=op.f("ck_posts_formato"),
        ),
        sa.ForeignKeyConstraint(
            ["aprovado_por_usuario_id"],
            ["usuarios.id"],
            name=op.f("fk_posts_aprovado_por_usuario_id_usuarios"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["calendario_editorial_id"],
            ["calendario_editorial.id"],
            name=op.f("fk_posts_calendario_editorial_id_calendario_editorial"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["empresa_id"],
            ["empresas.id"],
            name=op.f("fk_posts_empresa_id_empresas"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["servico_id"],
            ["servicos.id"],
            name=op.f("fk_posts_servico_id_servicos"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_posts")),
    )
    op.create_index(
        op.f("ix_posts_aprovado_por_usuario_id"),
        "posts",
        ["aprovado_por_usuario_id"],
    )
    op.create_index(
        op.f("ix_posts_calendario_editorial_id"),
        "posts",
        ["calendario_editorial_id"],
    )
    op.create_index(op.f("ix_posts_empresa_id"), "posts", ["empresa_id"])
    op.create_index(op.f("ix_posts_servico_id"), "posts", ["servico_id"])
    op.create_index("ix_posts_empresa_status", "posts", ["empresa_id", "status"])
    op.create_index(
        "ix_posts_empresa_data_sugerida",
        "posts",
        ["empresa_id", "data_publicacao_sugerida"],
    )
    op.create_index(
        "ix_posts_fluxo_pendente",
        "posts",
        ["empresa_id", "data_publicacao_sugerida"],
        postgresql_where=sa.text("status IN ('rascunho', 'em_revisao', 'aprovado')"),
    )

    op.create_table(
        "prompts",
        uuid_pk(),
        *audit_columns(),
        sa.Column("empresa_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("post_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("agente", sa.Text(), nullable=False),
        sa.Column("tipo", sa.Text(), nullable=False),
        sa.Column("conteudo", sa.Text(), nullable=False),
        sa.Column(
            "parametros",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
        sa.Column("modelo_ia", sa.Text(), nullable=True),
        sa.Column("resposta", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("status", sa.Text(), server_default="criado", nullable=False),
        sa.CheckConstraint(
            "agente IN ('brand', 'planner', 'writer', 'designer', 'reviewer', 'publisher', 'analytics')",
            name=op.f("ck_prompts_agente"),
        ),
        sa.CheckConstraint(
            "status IN ('criado', 'enviado', 'respondido', 'falhou')",
            name=op.f("ck_prompts_status"),
        ),
        sa.ForeignKeyConstraint(
            ["empresa_id"],
            ["empresas.id"],
            name=op.f("fk_prompts_empresa_id_empresas"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["post_id"],
            ["posts.id"],
            name=op.f("fk_prompts_post_id_posts"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_prompts")),
    )
    op.create_index(op.f("ix_prompts_empresa_id"), "prompts", ["empresa_id"])
    op.create_index(op.f("ix_prompts_post_id"), "prompts", ["post_id"])
    op.create_index("ix_prompts_empresa_agente", "prompts", ["empresa_id", "agente"])

    op.create_table(
        "midias",
        uuid_pk(),
        *audit_columns(),
        sa.Column("empresa_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("post_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("prompt_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("tipo", sa.Text(), nullable=False),
        sa.Column("url", sa.Text(), nullable=True),
        sa.Column("caminho_arquivo", sa.Text(), nullable=True),
        sa.Column("alt_text", sa.Text(), nullable=True),
        sa.Column(
            "metadados",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "tipo IN ('imagem', 'video', 'audio', 'documento')",
            name=op.f("ck_midias_tipo"),
        ),
        sa.ForeignKeyConstraint(
            ["empresa_id"],
            ["empresas.id"],
            name=op.f("fk_midias_empresa_id_empresas"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["post_id"],
            ["posts.id"],
            name=op.f("fk_midias_post_id_posts"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["prompt_id"],
            ["prompts.id"],
            name=op.f("fk_midias_prompt_id_prompts"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_midias")),
    )
    op.create_index(op.f("ix_midias_empresa_id"), "midias", ["empresa_id"])
    op.create_index(op.f("ix_midias_post_id"), "midias", ["post_id"])
    op.create_index(op.f("ix_midias_prompt_id"), "midias", ["prompt_id"])
    op.create_index("ix_midias_empresa_tipo", "midias", ["empresa_id", "tipo"])

    op.create_table(
        "publicacoes",
        uuid_pk(),
        *audit_columns(),
        sa.Column("empresa_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("post_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("plataforma", sa.Text(), server_default="instagram", nullable=False),
        sa.Column("id_externo", sa.Text(), nullable=True),
        sa.Column("permalink", sa.Text(), nullable=True),
        sa.Column("status", sa.Text(), server_default="pendente", nullable=False),
        sa.Column("agendado_para", sa.DateTime(timezone=True), nullable=True),
        sa.Column("publicado_em", sa.DateTime(timezone=True), nullable=True),
        sa.Column("erro_mensagem", sa.Text(), nullable=True),
        sa.Column(
            "payload_publicacao",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "plataforma IN ('instagram')",
            name=op.f("ck_publicacoes_plataforma"),
        ),
        sa.CheckConstraint(
            "status IN ('pendente', 'agendada', 'publicada', 'falhou', 'cancelada')",
            name=op.f("ck_publicacoes_status"),
        ),
        sa.ForeignKeyConstraint(
            ["empresa_id"],
            ["empresas.id"],
            name=op.f("fk_publicacoes_empresa_id_empresas"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["post_id"],
            ["posts.id"],
            name=op.f("fk_publicacoes_post_id_posts"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_publicacoes")),
        sa.UniqueConstraint(
            "plataforma",
            "id_externo",
            name=op.f("uq_publicacoes_plataforma_id_externo"),
        ),
    )
    op.create_index(op.f("ix_publicacoes_empresa_id"), "publicacoes", ["empresa_id"])
    op.create_index(op.f("ix_publicacoes_post_id"), "publicacoes", ["post_id"])
    op.create_index(
        "ix_publicacoes_empresa_status",
        "publicacoes",
        ["empresa_id", "status"],
    )
    op.create_index(
        "ix_publicacoes_agendadas",
        "publicacoes",
        ["empresa_id", "agendado_para"],
        postgresql_where=sa.text("status = 'agendada'"),
    )

    op.create_table(
        "metricas",
        uuid_pk(),
        *audit_columns(),
        sa.Column("empresa_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("publicacao_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("curtidas", sa.Integer(), server_default="0", nullable=False),
        sa.Column("comentarios", sa.Integer(), server_default="0", nullable=False),
        sa.Column("compartilhamentos", sa.Integer(), server_default="0", nullable=False),
        sa.Column("alcance", sa.Integer(), server_default="0", nullable=False),
        sa.Column("impressoes", sa.Integer(), server_default="0", nullable=False),
        sa.Column("taxa_engajamento", sa.Numeric(8, 4), server_default="0", nullable=False),
        sa.Column(
            "coletado_em",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint("curtidas >= 0", name=op.f("ck_metricas_curtidas_nao_negativo")),
        sa.CheckConstraint(
            "comentarios >= 0",
            name=op.f("ck_metricas_comentarios_nao_negativo"),
        ),
        sa.CheckConstraint(
            "compartilhamentos >= 0",
            name=op.f("ck_metricas_compartilhamentos_nao_negativo"),
        ),
        sa.CheckConstraint("alcance >= 0", name=op.f("ck_metricas_alcance_nao_negativo")),
        sa.CheckConstraint(
            "impressoes >= 0",
            name=op.f("ck_metricas_impressoes_nao_negativo"),
        ),
        sa.CheckConstraint(
            "taxa_engajamento >= 0",
            name=op.f("ck_metricas_taxa_engajamento_nao_negativo"),
        ),
        sa.ForeignKeyConstraint(
            ["empresa_id"],
            ["empresas.id"],
            name=op.f("fk_metricas_empresa_id_empresas"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["publicacao_id"],
            ["publicacoes.id"],
            name=op.f("fk_metricas_publicacao_id_publicacoes"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_metricas")),
    )
    op.create_index(op.f("ix_metricas_empresa_id"), "metricas", ["empresa_id"])
    op.create_index(op.f("ix_metricas_publicacao_id"), "metricas", ["publicacao_id"])
    op.create_index(
        "ix_metricas_empresa_coletado_em",
        "metricas",
        ["empresa_id", "coletado_em"],
    )

    op.create_table(
        "configuracoes",
        uuid_pk(),
        *audit_columns(),
        sa.Column("empresa_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("chave", sa.Text(), nullable=False),
        sa.Column(
            "valor",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
        sa.Column("descricao", sa.Text(), nullable=True),
        sa.Column("sensivel", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("ativa", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.ForeignKeyConstraint(
            ["empresa_id"],
            ["empresas.id"],
            name=op.f("fk_configuracoes_empresa_id_empresas"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_configuracoes")),
        sa.UniqueConstraint(
            "empresa_id",
            "chave",
            name=op.f("uq_configuracoes_empresa_chave"),
        ),
    )
    op.create_index(op.f("ix_configuracoes_empresa_id"), "configuracoes", ["empresa_id"])


def downgrade() -> None:
    """Rollback schema changes."""
    op.drop_index(op.f("ix_configuracoes_empresa_id"), table_name="configuracoes")
    op.drop_table("configuracoes")

    op.drop_index("ix_metricas_empresa_coletado_em", table_name="metricas")
    op.drop_index(op.f("ix_metricas_publicacao_id"), table_name="metricas")
    op.drop_index(op.f("ix_metricas_empresa_id"), table_name="metricas")
    op.drop_table("metricas")

    op.drop_index("ix_publicacoes_agendadas", table_name="publicacoes")
    op.drop_index("ix_publicacoes_empresa_status", table_name="publicacoes")
    op.drop_index(op.f("ix_publicacoes_post_id"), table_name="publicacoes")
    op.drop_index(op.f("ix_publicacoes_empresa_id"), table_name="publicacoes")
    op.drop_table("publicacoes")

    op.drop_index("ix_midias_empresa_tipo", table_name="midias")
    op.drop_index(op.f("ix_midias_prompt_id"), table_name="midias")
    op.drop_index(op.f("ix_midias_post_id"), table_name="midias")
    op.drop_index(op.f("ix_midias_empresa_id"), table_name="midias")
    op.drop_table("midias")

    op.drop_index("ix_prompts_empresa_agente", table_name="prompts")
    op.drop_index(op.f("ix_prompts_post_id"), table_name="prompts")
    op.drop_index(op.f("ix_prompts_empresa_id"), table_name="prompts")
    op.drop_table("prompts")

    op.drop_index("ix_posts_fluxo_pendente", table_name="posts")
    op.drop_index("ix_posts_empresa_data_sugerida", table_name="posts")
    op.drop_index("ix_posts_empresa_status", table_name="posts")
    op.drop_index(op.f("ix_posts_servico_id"), table_name="posts")
    op.drop_index(op.f("ix_posts_empresa_id"), table_name="posts")
    op.drop_index(op.f("ix_posts_calendario_editorial_id"), table_name="posts")
    op.drop_index(op.f("ix_posts_aprovado_por_usuario_id"), table_name="posts")
    op.drop_table("posts")

    op.drop_index(
        "ix_calendario_editorial_empresa_data",
        table_name="calendario_editorial",
    )
    op.drop_index(
        op.f("ix_calendario_editorial_empresa_id"),
        table_name="calendario_editorial",
    )
    op.drop_table("calendario_editorial")

    op.drop_index("ix_servicos_empresa_ativo", table_name="servicos")
    op.drop_index(op.f("ix_servicos_empresa_id"), table_name="servicos")
    op.drop_table("servicos")

    op.drop_index(op.f("ix_usuarios_empresa_id"), table_name="usuarios")
    op.drop_index(op.f("ix_usuarios_email"), table_name="usuarios")
    op.drop_table("usuarios")

    op.drop_index(op.f("ix_empresas_nome"), table_name="empresas")
    op.drop_table("empresas")

