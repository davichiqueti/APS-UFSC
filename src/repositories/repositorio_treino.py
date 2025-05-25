# repositories/repositorio_treino.py
from sqlalchemy.sql import text
import sqlalchemy

# Supondo que RepositorioBase está em um arquivo acessível, como no exemplo
from repositories.repositorio_base import RepositorioBase
# Supondo que o modelo Treino está definido em models.treino
from models.treino import Treino


class RepositorioTreino(RepositorioBase):
    def __init__(self, connection: sqlalchemy.engine.Connection | None = None):
        super().__init__(connection)

    def adicionar(self, treino: Treino):
        """
        Adiciona um novo treino ao banco de dados.

        Args:
            treino: Um objeto Treino contendo os dados a serem persistidos.
        """
        # Assumindo que 'treino.usuario' é um objeto Usuario e queremos armazenar seu ID.
        # Se 'treino.usuario_id' já for o ID, ajuste conforme necessário.
        usuario_id_para_db = None
        if treino.usuario:
            usuario_id_para_db = treino.usuario.id # Ou treino.usuario_id se for direto

        # Os atributos do treino.data e treino.curtidas precisam ser tratados.
        # treino.data deve ser um objeto date/datetime.
        # treino.curtidas é um int.
        query = text("""
        INSERT INTO treinos (descricao, duracao, imagem, usuario_id, data, curtidas)
        VALUES (:descricao, :duracao, :imagem, :usuario_id, :data, :curtidas)
        """)
        with self._conn.begin() as transaction:
            self._conn.execute(
                statement=query,
                parameters={
                    "descricao": treino.descricao,
                    "duracao": treino.duracao,
                    "imagem": treino.imagem,
                    "usuario_id": usuario_id_para_db,
                    "data": treino.data.isoformat() if treino.data else None, # Convertendo data para formato ISO
                    "curtidas": treino.curtidas if hasattr(treino, 'curtidas') else 0 # Default para 0 se não existir
                }
            )
            # Se você precisar retornar o ID do treino inserido,
            # a forma de fazer isso pode variar dependendo do dialeto do banco de dados (ex: RETURNING id).
            # Por simplicidade, este método não retorna o objeto inserido ou seu ID.