"""ORM model package.

Importing this module registers every mapped table in ``Base.metadata`` so
Alembic can detect schema changes.
"""

from app.models.base import UUIDTimestampMixin
from app.models.calendario_editorial import CalendarioEditorial
from app.models.configuracao import Configuracao
from app.models.empresa import Empresa
from app.models.metrica import Metrica
from app.models.midia import Midia
from app.models.post import Post
from app.models.prompt import Prompt
from app.models.publicacao import Publicacao
from app.models.servico import Servico
from app.models.usuario import Usuario

__all__ = [
    "CalendarioEditorial",
    "Configuracao",
    "Empresa",
    "Metrica",
    "Midia",
    "Post",
    "Prompt",
    "Publicacao",
    "Servico",
    "UUIDTimestampMixin",
    "Usuario",
]
