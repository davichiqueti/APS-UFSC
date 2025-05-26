from models.usuario import Usuario
from repositories.repositorio_usuario import RepositorioUsuario
from views.tela_usuario import TelaUsuario
from datetime import date
from utils.encryption import cipher
from typing import List
from models.treino import Treino


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
            callback_abrir_cadastro=self.abrir_tela_cadastro,
            callback_sucesso_proxima_etapa=self.chama_sistema
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

        try:
            # A senha armazenada é uma string (token Fernet), precisamos encodá-la para bytes
            senha_armazenada_token_bytes = usuario_encontrado.senha_criptografada.encode('utf-8')
            
            # Descriptografar a senha armazenada no banco
            senha_descriptografada_bytes = cipher.decrypt(senha_armazenada_token_bytes)
            senha_descriptografada_str = senha_descriptografada_bytes.decode('utf-8')

            # Comparar a senha digitada (em texto plano) com a senha descriptografada
            if senha_digitada != senha_descriptografada_str:
                raise ValueError("Senha incorreta.")

        except ValueError as e: # Captura o ValueError de "Senha incorreta."
            raise e 
        except Exception as e:
            # cryptography.fernet.InvalidToken será uma das exceções se o token for inválido/corrompido
            # Ou se a chave de criptografia mudou desde que a senha foi criptografada.
            print(f"Erro ao descriptografar a senha ou token inválido: {e}")
            raise ValueError("Erro ao verificar a senha. Contate o suporte.")

        self._usuario_logado = usuario_encontrado
        print(usuario_encontrado)

        #self.chama_sistema()

    def chama_sistema(self):
        self._controlador_sistema.inicializarFeed()


        # Você pode adicionar uma mensagem de sucesso ou log aqui, se desejar.
        # Ex: print(f"Login bem-sucedido! Bem-vindo(a), {self._usuario_logado.nome}!")
        # Após o login, a tela de login (view) se encarregará de fechar e
        # o fluxo da aplicação poderá seguir para uma tela principal, se houver.

    
    def buscar_treinos_das_amizades(self) -> List[Treino]:
        """
        Busca os treinos de todos os amigos do usuário logado,
        ordena-os por data (mais recentes primeiro) e os retorna.
        """
        if not self._usuario_logado or not hasattr(self._usuario_logado, 'amizades') or not self._usuario_logado.amizades:
            print("DEBUG [ControladorUsuario.buscar_treinos_das_amizades]: Usuário não logado ou sem amigos.")
            return []

        print(f"DEBUG [ControladorUsuario.buscar_treinos_das_amizades]: Buscando treinos para amigos de {self._usuario_logado.nome}.")
        todos_os_treinos: List[Treino] = []
        
        # Acessa o controlador_treino através do controlador_sistema
        controlador_treino = self._controlador_sistema.controlador_treino
        if not controlador_treino:
            print("ERRO [ControladorUsuario.buscar_treinos_das_amizades]: ControladorTreino não encontrado via ControladorSistema.")
            return []

        for amigo in self._usuario_logado.amizades:
            if amigo and hasattr(amigo, 'id') and amigo.id is not None:
                print(f"DEBUG [ControladorUsuario.buscar_treinos_das_amizades]: Obtendo treinos do amigo {amigo.nome} (ID: {amigo.id}).")
                treinos_do_amigo = controlador_treino.obter_treinos_do_usuario(amigo)
                todos_os_treinos.extend(treinos_do_amigo)
            else:
                print(f"WARN [ControladorUsuario.buscar_treinos_das_amizades]: Amigo inválido ou sem ID na lista.")
        
        if todos_os_treinos:
            # Ordena pela data do treino, do mais recente para o mais antigo
            # Garante que treino.data seja um objeto 'date'
            todos_os_treinos.sort(key=lambda treino: treino.data if treino.data else date.min, reverse=True)
            print(f"DEBUG [ControladorUsuario.buscar_treinos_das_amizades]: {len(todos_os_treinos)} treinos de amigos encontrados e ordenados.")
        else:
            print("DEBUG [ControladorUsuario.buscar_treinos_das_amizades]: Nenhum treino encontrado nas conexões.")
            
        return todos_os_treinos