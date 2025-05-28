#from views.tela_sistema import TelaSistema
from controllers.controlador_usuario import ControladorUsuario
from controllers.controlador_treino import ControladorTreino
from views.tela_sistema import TelaSistema
from views.tela_treino import TelaTreino

class ControladorSistema:
    def __init__(self):
        self.tela_sistema = TelaSistema()
        self.controlador_usuario = ControladorUsuario(self)
        self.controlador_treino = ControladorTreino(self)
        self.view_treino_atual = None

    def abrir_tela_usuario(self):
        self.controlador_usuario.iniciar()

    def buscar_usuario_logado(self):
        self.controlador_usuario.usuario_logado

    def iniciar(self):
        self.controlador_usuario.abrir_tela_login()

    def inicializarFeed(self):
        usuario_atual = self.controlador_usuario.usuario_logado
        if usuario_atual:
            print(f"\nDEBUG [ControladorSistema.inicializarFeed]: Usuário {usuario_atual.nome} logado.")
            
            # 1. Pede ao ControladorUsuario para buscar os treinos dos amigos
            print("DEBUG [ControladorSistema.inicializarFeed]: Solicitando treinos das amizades ao ControladorUsuario...")

            usuario = self.controlador_usuario.usuario_logado

            if usuario:
                lista_de_treinos_para_o_feed = self.controlador_treino.buscar_treinos_amizades(usuario)


            # 2. Define a lista de treinos na TelaSistema
            self.tela_sistema.treinos = lista_de_treinos_para_o_feed # type: ignore
            self.tela_sistema.indice_treino_atual = 0 # Reseta o índice ao carregar novo feed
            
            print("DEBUG [ControladorSistema.inicializarFeed]: Configurando e exibindo a tela principal do sistema (feed)...")
            self.tela_sistema.exibir_tela_principal(
                usuario_logado=usuario_atual,
                callback_logout=self.efetuar_logout,
                callback_abrir_perfil=self.navegar_para_perfil,
                callback_abrir_busca=self.navegar_para_busca,
                callback_registrar_treino=self.navegar_para_registrar_treino
            )
            
        else:
            self.iniciar()

    def efetuar_logout(self):
        """Processa o logout do usuário."""
        print("ControladorSistema: Efetuando logout...")
        self.tela_sistema.fechar_tela() # Garante que a tela do sistema seja fechada

        if self.controlador_usuario:
            self.controlador_usuario._usuario_logado = None 

        self.controlador_usuario.abrir_tela_login() # Redireciona para a tela de login

    # --- Métodos de Callback para Navegação (placeholders) ---
    def navegar_para_perfil(self):
        print("ControladorSistema: Navegando para Tela de Perfil.")
        self.tela_sistema.fechar_tela() 
        
        # Após fechar a tela de perfil, você pode querer reabrir o feed ou o login
        # self.inicializarFeed() # Para voltar ao feed
        # self.controlador_usuario.abrir_tela_login() # Ou para login

    def navegar_para_busca(self):
        print("ControladorSistema: Navegando para Tela de Busca.")
        self.tela_sistema.fechar_tela()
        # self.inicializarFeed() # Exemplo: voltar para o feed depois

    def navegar_para_registrar_treino(self):
        print("ControladorSistema: Navegando para Tela de Registrar Treino.")
        self.tela_sistema.fechar_tela()
        self.controlador_treino.abrir_tela_registro()
        # self.inicializarFeed() # Exemplo: voltar para o feed depois
