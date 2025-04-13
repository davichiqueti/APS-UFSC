from models.user import User
from repositories.user_repository import UserRepository
from datetime import date
from utils.encryption import cipher


class UserController:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def create_user(self, cpf: str, username: str, email: str, birthdate: date, password: str):
        """
        Responsável por:
        - Instanciar entidade
        - Delegar persistência para o repositório
        - Gerar exceção caso um problema aconteça
        """
        encrypted_password = cipher.encrypt(password.encode('utf-8')).decode('utf-8')
        user = User(
            cpf=cpf,
            username=username,
            email=email,
            birthdate=birthdate,
            encrypted_password=encrypted_password
        )
        self._user_repository.add(user)

    def get_user_by_username(self, username: str) -> dict:
        user = self._user_repository.find_by_username(username)
        # Retornando apenas dados básicos
        return {
            "id": user.id,
            "username": user.username
        }
