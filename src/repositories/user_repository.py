from repositories.base_repository import BaseRepository
from models.user import User
from sqlalchemy.sql import text
from datetime import date


class UserRepository(BaseRepository):
    def __init__(self, connection):
        super().__init__(connection)

    def add(self, user: User):
        query = text("""
        INSERT INTO users (cpf, username, email, birthdate, encrypted_password)
        VALUES (:cpf, :username, :email, :birthdate, :encrypted_password)
        """)
        self._conn.execute(
            statement=query, 
            parameters={
                "cpf": user.cpf,
                "username": user.username,
                "email": user.email,
                "birthdate": user.birthdate.isoformat(),  # Convertendo objeto de data para ISO formato aceito pelo banco
                "encrypted_password": user.encrypted_password
            }
        )

    def find_by_username(self, username: str) -> User | None:
        query = text("SELECT id, cpf, username, email, birthdate, encrypted_password FROM users WHERE username = :username")
        row = self._conn.execute(
            statement=query,
            parameters={"username": username}
        ).fetchone()
        if row:
            return User(
                id=row[0],
                cpf=row[1],
                username=row[2],
                email=row[3],
                birthdate=row[4],
                encrypted_password=row[5]
            )
        return None
