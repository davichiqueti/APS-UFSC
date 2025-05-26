#from views.tela_sistema import TelaSistema
from controllers.controlador_usuario import ControladorUsuario
from controllers.controlador_treino import ControladorTreino
from views.tela_sistema import TelaSistema
from views.tela_treino import ViewTreino

class ControladorSistema:
    def __init__(self):
        self.tela_sistema = TelaSistema()
        self.controlador_treino = ControladorTreino()
        self.controlador_usuario = ControladorUsuario(self)
        self.view_treino_atual = None

    def abrir_tela_usuario(self):
        self.controlador_usuario.iniciar()

    def iniciar(self):
        self.controlador_usuario.abrir_tela_login()

    def inicializarFeed(self):
        usuario_atual = self.controlador_usuario.usuario_logado
        if usuario_atual:
            print(f"\nControladorSistema: Login bem-sucedido para {usuario_atual.nome}!")
            print("ControladorSistema: Abrindo a tela principal do sistema (feed)...")
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

        self.view_treino_atual = ViewTreino(self.controlador_treino, self.controlador_usuario)

        # self.inicializarFeed() # Exemplo: voltar para o feed depois
