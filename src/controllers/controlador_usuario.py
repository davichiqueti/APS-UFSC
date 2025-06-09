from models.usuario import Usuario
from repositories.repositorio_usuario import RepositorioUsuario
from views.tela_usuario import TelaUsuario
from datetime import date
from utils.encryption import cipher
from controllers.controlador_medalha import ControladorMedalha
from views.tela_amizades import TelaAmizades

class ControladorUsuario:
    def __init__(self, controlador_sistema):
        self._controlador_sistema = controlador_sistema
        self.tela_usuario = TelaUsuario()
        self._user_repository = RepositorioUsuario()
        self._usuario_logado = None

    @property
    def usuario_logado(self) -> None | Usuario:
        return self._usuario_logado

    def iniciar(self):
        return

    def abrir_tela_cadastro(self):
        self.tela_usuario.exibir_tela_cadastro(
            callback_cadastro=self.cadastrar_conta,
            callback_abrir_login=self.abrir_tela_login
        )

    def cadastrar_conta(
        self,
        cpf: str,
        nome: str,
        email: str,
        foto: str,
        data_nascimento: date,
        senha: str
    ):

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




    def abrir_tela_login(self):

        self.tela_usuario.exibir_tela_login(
            callback_login=self.efetuar_login,
            callback_abrir_cadastro=self.abrir_tela_cadastro,
            callback_sucesso_proxima_etapa=self.chama_sistema
        )

    def efetuar_login(self, nome_usuario: str, senha_digitada: str):

        if not nome_usuario or not senha_digitada:
            raise ValueError("Nome de usuário e senha são obrigatórios.")

        usuario_encontrado = self._user_repository.busca_por_nome(nome_usuario)

        if not usuario_encontrado:
            raise ValueError(f"Usuário '{nome_usuario}' não encontrado.")

        try:
            senha_armazenada_token_bytes = usuario_encontrado.senha_criptografada.encode('utf-8')
            
            senha_descriptografada_bytes = cipher.decrypt(senha_armazenada_token_bytes)
            senha_descriptografada_str = senha_descriptografada_bytes.decode('utf-8')

            if senha_digitada != senha_descriptografada_str:
                raise ValueError("Senha incorreta.")

        except ValueError as e:
            raise e 
        except Exception as e:
            print(f"Erro ao descriptografar a senha ou token inválido: {e}")
            raise ValueError("Erro ao verificar a senha. Contate o suporte.")

        self._usuario_logado = usuario_encontrado
        print(usuario_encontrado.amizades)


    def chama_sistema(self):
        self._controlador_sistema.inicializarFeed()

    
    def solicitarVisualizarMedalhas(self, usuario, callback_voltar):
        is_logado = self.verificarIdentidade(usuario)
        controlador_medalha = ControladorMedalha(self._controlador_sistema)
        if is_logado:
            todas = controlador_medalha.buscarTodasMedalhas()
            conquistadas = controlador_medalha.buscarMedalhasConquistadas(usuario)
            self.tela_medalha = controlador_medalha.tela_medalha
            self.tela_medalha.exibir_todas_medalhas(todas, callback_voltar, conquistadas=conquistadas)
        else:
            conquistadas = controlador_medalha.buscarMedalhasConquistadas(usuario)
            self.tela_medalha = controlador_medalha.tela_medalha
            if conquistadas:
                self.tela_medalha.exibir_medalhas_conquistadas(conquistadas, callback_voltar)
            else:
                self.tela_medalha.exibir_mensagem("Usuário não possui medalhas")

    def verificarIdentidade(self, usuario):
        return self._usuario_logado and usuario.cpf == self._usuario_logado.cpf
    
    def solicitarVisualizarAmizades(self, usuario, callback_voltar):
        lista_amigos = self._user_repository.buscar_amizades_aceitas(usuario.id)
        self.tela_amizades = TelaAmizades()
        def abrir_perfil_amigo(amigo):
            self.tela_usuario.exibir_tela_perfil(
                usuario=amigo,
                callback_voltar=lambda: self.solicitarVisualizarAmizades(usuario, callback_voltar),
                controlador_usuario=self,
                usuario_logado=self._usuario_logado
            )
        self.tela_amizades.exibir_amizades(
            lista_amigos,
            callback_voltar,
            callback_abrir_perfil=abrir_perfil_amigo
        )
    
    