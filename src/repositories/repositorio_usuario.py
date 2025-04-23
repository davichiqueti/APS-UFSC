from repositories.repositorio_base import RepositorioBase
from models.usuario import Usuario
from sqlalchemy.sql import text
import sqlalchemy


class RepositorioUsuario(RepositorioBase):
    def __init__(self, connection: sqlalchemy.engine.Connection | None = None):
        super().__init__(connection)

    def criar(self, user: Usuario):
        query = text("""
        INSERT INTO users (cpf, username, email, birthdate, encrypted_password)
        VALUES (:cpf, :username, :email, :birthdate, :encrypted_password)
        """)
        self._conn.execute(
            statement=query, 
            parameters={
                "cpf": user.cpf,
                "nome": user.nome,
                "email": user.email,
                "data_nascimento": user.data_nascimento.isoformat(),  # Convertendo objeto de data para ISO formato aceito pelo banco
                "senha_criptografada": user.senha_criptografada
            }
        )

    def busca_por_nome(self, nome: str) -> Usuario | None:
        query = text("""
        SELECT
            id,
            cpf,
            nome,
            email,
            foto,
            data_nascimento,
            senha_criptografada
        FROM usuarios
        WHERE nome = :nome"
        """)
        row = self._conn.execute(
            statement=query,
            parameters={"nome": nome}
        ).fetchone()
        if row:
            return Usuario(
                id=row[0],
                cpf=row[1],
                nome=row[2],
                email=row[3],
                foto=row[4],
                data_nascimento=row[5],
                senha_criptografada=row[6]
            )
        return None
