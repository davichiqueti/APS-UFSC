from repositories.repositorio_base import RepositorioBase
from models.solicitacao import Solicitacao
from models.usuario import Usuario
from sqlalchemy.sql import text
import sqlalchemy
from typing import Optional, List

class RepositorioSolicitacao(RepositorioBase):
    def __init__(self, connection: sqlalchemy.engine.Connection | None = None):
        super().__init__(connection)

    def criar(self, solicitacao: Solicitacao) -> None:
        """
        Cria uma nova solicitação de amizade com status 'pendente'.
        """
        query = text("""
        INSERT INTO solicitacoes_amizade (remetente, destinatario, status)
        VALUES (:remetente, :destinatario, 'pendente')
        """)
        with self._conn.begin():
            self._conn.execute(
                statement=query,
                parameters={
                    "remetente": solicitacao.remetente.id,
                    "destinatario": solicitacao.destinatario.id,
                }
            )

    def buscar_solicitacao(self, remetente_id: int, destinatario_id: int) -> Optional[dict]:
        """
        Busca uma solicitação específica entre dois usuários para verificar seu status.
        """
        query = text("""
        SELECT remetente, destinatario, status
        FROM solicitacoes_amizade
        WHERE (remetente = :remetente_id AND destinatario = :destinatario_id)
           OR (remetente = :destinatario_id AND destinatario = :remetente_id)
        """)
        with self._conn.begin():
            result = self._conn.execute(
                statement=query,
                parameters={"remetente_id": remetente_id, "destinatario_id": destinatario_id}
            ).fetchone()
        
        return result._asdict() if result else None

    def atualizar_status(self, remetente_id: int, destinatario_id: int, novo_status: str) -> bool:
        """
        Atualiza o status de uma solicitação de amizade existente.
        Retorna True se a atualização foi bem-sucedida, False caso contrário.
        """
        query = text("""
        UPDATE solicitacoes_amizade
        SET status = :novo_status
        WHERE remetente = :remetente_id AND destinatario = :destinatario_id
        """)
        with self._conn.begin():
            result = self._conn.execute(
                statement=query,
                parameters={
                    "remetente_id": remetente_id,
                    "destinatario_id": destinatario_id,
                    "novo_status": novo_status
                }
            )
            return result.rowcount > 0
            
    def listar_pendentes(self, usuario_id: int) -> List[Usuario]:
        """
        Lista todos os usuários que enviaram uma solicitação pendente para o usuário logado.
        """
        query = text("""
            SELECT u.*
            FROM usuarios u
            JOIN solicitacoes_amizade s ON u.id = s.remetente
            WHERE s.destinatario = :usuario_id AND s.status = 'pendente'
        """)
        with self._conn.begin():
            resultados = self._conn.execute(query, {"usuario_id": usuario_id}).fetchall()
        
        remetentes = []
        for row in resultados:
            remetentes.append(Usuario(
                id=row[0], cpf=row[1], nome=row[2], email=row[3],
                foto=row[4], data_nascimento=row[5], senha_criptografada=row[6]
            ))
            
        return remetentes