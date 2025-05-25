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


# Add these new methods inside the ControladorUsuario class

    def abrir_tela_login(self):
        """
        Solicita à view para exibir a tela de login.
        Passa o método 'efetuar_login' como callback para a tentativa de login
        e 'abrir_tela_cadastro' para o caso do usuário querer se registrar.
        """
        self.tela_usuario.exibir_tela_login(
            callback_login=self.efetuar_login,
            callback_abrir_cadastro=self.abrir_tela_cadastro  # Navigates to existing registration screen
        )

    def efetuar_login(self, nome_usuario: str, senha_digitada: str):
        """
        Responsável por:
        - Buscar usuário por nome de usuário (utilizando o campo 'nome').
        - Verificar se a senha digitada, após criptografada, corresponde à senha armazenada.
        - Atualizar o atributo _usuario_logado em caso de sucesso.
        - Gerar exceções em caso de falha (usuário não encontrado, senha incorreta).
        """
        if not nome_usuario or not senha_digitada:
            raise ValueError("Nome de usuário e senha são obrigatórios.")

        # Utiliza o método existente busca_por_nome para encontrar o usuário
        usuario_encontrado = self._user_repository.busca_por_nome(nome_usuario)

        if not usuario_encontrado:
            raise ValueError(f"Usuário '{nome_usuario}' não encontrado.")

        # Criptografa a senha digitada para comparação, usando o mesmo método da tela de cadastro
        senha_digitada_criptografada = cipher.encrypt(senha_digitada.encode('utf-8')).decode('utf-8')

        if senha_digitada_criptografada != usuario_encontrado.senha_criptografada: #
            raise ValueError("Senha incorreta.")

        self._usuario_logado = usuario_encontrado
        # Você pode adicionar uma mensagem de sucesso ou log aqui, se desejar.
        # Ex: print(f"Login bem-sucedido! Bem-vindo(a), {self._usuario_logado.nome}!")
        # Após o login, a tela de login (view) se encarregará de fechar e
        # o fluxo da aplicação poderá seguir para uma tela principal, se houver.