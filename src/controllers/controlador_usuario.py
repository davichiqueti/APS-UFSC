from models.usuario import Usuario
from repositories.repositorio_usuario import UserRepository
from datetime import date
from utils.encryption import cipher


class ControladorUsuario:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def create_user(
        self,
        cpf: str,
        nome: str,
        email: str,
        foto: str,
        data_nascimento: date,
        senha: str
    ):
        """
        Responsável por:
        - Instanciar entidade
        - Delegar persistência para o repositório
        - Gerar exceção caso um problema aconteça
        """
        senha_criptografada = cipher.encrypt(senha.encode('utf-8')).decode('utf-8')
        user = Usuario(
            cpf=cpf,
            nome=nome,
            email=email,
            foto=foto,
            data_nascimento=data_nascimento,
            senha_criptografada=senha_criptografada
        )
        self._user_repository.add(user)

    def get_user_by_username(self, nome: str) -> dict:
        usuario = self._user_repository.busca_por_nome(nome)
        # Retornando apenas dados básicos
        return {
            "id": usuario.id,
            "nome": usuario.nome
        }
