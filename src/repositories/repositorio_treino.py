# repositories/repositorio_treino.py

from repositories.repositorio_base import RepositorioBase
from models.treino import Treino
from sqlalchemy.sql import text
import sqlalchemy

class RepositorioTreino(RepositorioBase):
    def __init__(self, connection: sqlalchemy.engine.Connection | None = None):
        super().__init__(connection)

    def criar(self, treino: Treino) -> None:
        """
        Insere um novo treino na tabela 'treinos', cujos campos são:
          id SERIAL PK,
          curtidas INTEGER NOT NULL DEFAULT 0,
          "data" DATE NOT NULL DEFAULT CURRENT_DATE,
          descricao TEXT,
          foto TEXT NOT NULL,
          usuario INTEGER REFERENCES usuarios
        """
        query = text("""
        INSERT INTO treinos (descricao, foto, usuario, curtidas, "data")
        VALUES (:descricao, :foto, :usuario, :curtidas, :data)
        """)
        with self._conn.begin():
            self._conn.execute(
                statement = query,
                parameters = {
                    "descricao": treino.descricao,
                    "foto": treino.imagem,                          # no model é 'imagem'
                    "usuario": treino.usuario.id if treino.usuario else None,
                    "curtidas": treino.curtidas,
                    "data": treino.data.isoformat() if treino.data else None
                }
            )
