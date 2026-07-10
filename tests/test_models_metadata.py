"""Tests for ORM metadata registration."""

from app.database.base import Base
import app.models  # noqa: F401


def test_all_initial_tables_are_registered() -> None:
    """Every table required by the first data model should be mapped."""
    expected_tables = {
        "empresas",
        "usuarios",
        "servicos",
        "calendario_editorial",
        "posts",
        "midias",
        "publicacoes",
        "metricas",
        "prompts",
        "configuracoes",
    }

    assert expected_tables.issubset(Base.metadata.tables.keys())

