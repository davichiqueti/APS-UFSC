from repositories.repositorio_base import RepositorioBase
from models.medalha import Medalha
from sqlalchemy.sql import text
import sqlalchemy
from typing import List

class repositoryMedalha(RepositorioBase):
    def __init__(self, connection: sqlalchemy.engine.Connection | None = None):
        super().__init__(connection)

    def adicionar(self, medalha: Medalha) -> None:
        query = text("""
        INSERT INTO medalhas (categoria, descricao, valor_base, url_photo)
        VALUES (:categoria, :descricao, :valor_base, :url_photo)
        """)
        with self._conn.begin():
            self._conn.execute(
                statement=query,
                parameters={
                    "categoria": medalha.categoria,
                    "descricao": medalha.descricao,
                    "valor_base": medalha.valor_base,
                    "url_photo": medalha.url_photo
                }
            )

    def buscar_por_id(self, medalha_id: int) -> Medalha | None:
        query = text("""
        SELECT id, categoria, descricao, valor_base, url_photo
        FROM medalhas
        WHERE id = :id
        """)
        row = self._conn.execute(query, {"id": medalha_id}).fetchone()
        if row:
            return Medalha(
                id=row[0],
                categoria=row[1],
                descricao=row[2],
                valor_base=row[3],
                url_photo=row[4]
            )
        return None

    def obterTodasMedalhas(self) -> List[Medalha]:
        query = text("""
        SELECT id, categoria, descricao, valor_base, url_photo
        FROM medalhas
        ORDER BY id
        """)
        resultado = self._conn.execute(query).fetchall()
        medalhas = []
        for row in resultado:
            medalhas.append(
                Medalha(
                    id=row[0],
                    categoria=row[1],
                    descricao=row[2],
                    valor_base=row[3],
                    url_photo=row[4]
                )
            )
        return medalhas

    def atualizar(self, medalha: Medalha) -> bool:
        query = text("""
        UPDATE medalhas
        SET categoria = :categoria,
            descricao = :descricao,
            valor_base = :valor_base,
            url_photo = :url_photo
        WHERE id = :id
        """)
        with self._conn.begin():
            result = self._conn.execute(
                statement=query,
                parameters={
                    "id": medalha.id,
                    "categoria": medalha.categoria,
                    "descricao": medalha.descricao,
                    "valor_base": medalha.valor_base,
                    "url_photo": medalha.url_photo
                }
            )
            return result.rowcount > 0

    def deletar(self, medalha_id: int) -> bool:
        query = text("""
        DELETE FROM medalhas WHERE id = :id
        """)
        with self._conn.begin():
            result = self._conn.execute(query, {"id": medalha_id})
            return result.rowcount > 0
        
    def obterMedalhasPorUsuario(self, usuario_id: int) -> List[Medalha]:
        query = text("""
        SELECT m.id, m.categoria, m.descricao, m.valor_base, m.url_photo
        FROM medalhas m
        JOIN medalhas_usuario mu ON m.id = mu.medalha
        WHERE mu.usuario = :usuario_id
        """)
        resultado = self._conn.execute(query, {"usuario_id": usuario_id}).fetchall()
        medalhas = []
        for row in resultado:
            medalhas.append(
                Medalha(
                    id=row[0],
                    categoria=row[1],
                    descricao=row[2],
                    valor_base=row[3],
                    url_photo=row[4]
                )
            )
        return medalhas
        
