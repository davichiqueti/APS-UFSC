from repositories.base_repository import BaseRepository
from models.user import User
from sqlalchemy.sql import text
from datetime import date


class UserRepository(BaseRepository):
    def __init__(self, connection):
        super().__init__(connection)

    def add(self, user: User):
        query = text("""
        INSERT INTO users (cpf, username, email, birthdate)
        VALUES (:cpf, :username, :email, :birthdate)
        """)
        self._conn.execute(
            statement=query, 
            parameters={
                "cpf": user.cpf,
                "username": user.username,
                "email": user.email,
                "birthdate": user.birthdate,
                "encrypted_password": user.encrypted_password
            }
        )

    def find_by_username(self, username: str) -> User | None:
        query = text("SELECT cpf, username, email, birthdate FROM users WHERE username = :username")
        row = self._conn.execute(
            statement=query,
            parameters={"username": username}
        ).fetchone()
        if row:
            return User(
                cpf=row[0],
                username=row[1],
                email=row[2],
                birthdate=date.fromisoformat(row[3])
            )
        return None
