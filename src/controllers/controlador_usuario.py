from models.usuario import Usuario
from repositories.repositorio_usuario import RepositorioUsuario
from views.tela_usuario import TelaUsuario
from datetime import date
from utils.encryption import cipher


class ControladorUsuario:
    def __init__(self):
        user_repository = RepositorioUsuario()
        self.tela_usuario = TelaUsuario()
        self._user_repository = user_repository
        self._usuario_logado = None

    @property
    def usuario_logado(self) -> None | Usuario:
        return self._usuario_logado

    def iniciar(self):
        return

    def abrir_tela_cadastro(self):
        self.tela_usuario.exibir_tela_cadastro(callback_cadastro=self.cadastrar_conta)

    def cadastrar_conta(
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
        self._user_repository.criar(user)
        self._usuario_logado = user
