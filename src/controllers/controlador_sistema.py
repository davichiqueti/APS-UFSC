from tkinter import messagebox
from views.tela_sistema import TelaSistema
from controllers.controlador_usuario import ControladorUsuario
from controllers.controlador_treino import ControladorTreino
from controllers.controlador_ranking import ControladorRanking


class ControladorSistema:
    def __init__(self):
        self.tela_sistema = TelaSistema(self) 
        self.controlador_usuario = ControladorUsuario(self)
        # Mantendo a instanciação conforme seu pedido.
        # O __init__ do ControladorTreino deve ser def __init__(self, controlador_sistema):
        self.controlador_treino = ControladorTreino(self) 
        self.controlador_ranking = ControladorRanking(self)

    def buscar_usuario_logado(self):
        return self.controlador_usuario.usuario_logado # Adicionado return

    def iniciar(self):
        print("DEBUG [ControladorSistema.iniciar]: Iniciando fluxo de login.")
        self.controlador_usuario.abrir_tela_login()
        print("DEBUG [ControladorSistema.iniciar]: Fluxo principal (login/sistema) aparentemente concluído.")

    def inicializarFeed(self):
        usuario_atual = self.buscar_usuario_logado()
        if usuario_atual:
            print(f"\nDEBUG [ControladorSistema.inicializarFeed]: Usuário {usuario_atual.nome} logado.")
            print("DEBUG [ControladorSistema.inicializarFeed]: Solicitando treinos das amizades ao ControladorTreino...")
            
            lista_de_treinos_para_o_feed = self.controlador_treino.buscar_treinos_amizades(usuario_atual)

            # O método em TelaSistema que monta a UI e recebe os dados
            # é chamado de exibir_tela_principal no seu diagrama (Controlador -> Tela)
            print("DEBUG [ControladorSistema.inicializarFeed]: Configurando UI da TelaSistema via exibir_tela_principal...")
            self.tela_sistema.exibir_tela_principal(
                usuario_logado=usuario_atual,
                lista_de_treinos=lista_de_treinos_para_o_feed, # Passa a lista de treinos
                controlador_treino_ref=self.controlador_treino,
                callback_logout=self.efetuar_logout,
                callback_abrir_perfil=self.navegar_para_perfil,
                callback_abrir_busca=self.navegar_para_busca,
                callback_registrar_treino=self.navegar_para_registrar_treino,
                callback_rankings=self.navegar_para_rankings
            )
            
            print("DEBUG [ControladorSistema.inicializarFeed]: Iniciando loop de eventos da TelaSistema...")
            if self.tela_sistema.root_sistema and self.tela_sistema.root_sistema.winfo_exists():
                self.tela_sistema.iniciar_loop_eventos() # BLOQUEANTE até TelaSistema fechar
                print("DEBUG [ControladorSistema.inicializarFeed]: TelaSistema foi fechada.")
            else:
                print("ERROR [ControladorSistema.inicializarFeed]: Não foi possível iniciar a TelaSistema.")
                self.iniciar() 
        else:
            print("ERROR [ControladorSistema.inicializarFeed]: Usuário não logado. Voltando para tela de login.")
            self.iniciar()

    def efetuar_logout(self):
        # ... (como antes) ...
        print("DEBUG [ControladorSistema.efetuar_logout]: Processando logout...")
        if self.tela_sistema: self.tela_sistema.fechar_tela()
        if self.controlador_usuario: self.controlador_usuario._usuario_logado = None 
        print("DEBUG [ControladorSistema.efetuar_logout]: Redirecionando para login.")
        self.controlador_usuario.abrir_tela_login()

    def navegar_para_perfil(self):
        # ... (como antes, mas chamando inicializarFeed ou iniciar após) ...
        print("DEBUG [ControladorSistema]: Navegando para Tela de Perfil.")
        if self.tela_sistema: self.tela_sistema.fechar_tela() 
        messagebox.showinfo("Navegação", "Tela de Perfil ainda não implementada.")
        if self.controlador_usuario.usuario_logado: self.inicializarFeed()
        else: self.iniciar()

    def navegar_para_busca(self):
        # ... (como antes) ...
        print("DEBUG [ControladorSistema]: Navegando para Tela de Busca.")
        if self.tela_sistema: self.tela_sistema.fechar_tela()
        messagebox.showinfo("Navegação", "Tela de Busca ainda não implementada.")
        if self.controlador_usuario.usuario_logado: self.inicializarFeed()
        else: self.iniciar()

    def navegar_para_registrar_treino(self):
        # ... (como antes) ...
        print("DEBUG [ControladorSistema]: Navegando para Tela de Registrar Treino.")
        if self.tela_sistema: self.tela_sistema.fechar_tela()
        self.controlador_treino.abrir_tela_registro()
        print("DEBUG [ControladorSistema]: Retornou de abrir_tela_registro.")
        if self.controlador_usuario.usuario_logado: self.inicializarFeed()
        else: self.iniciar()

    def navegar_para_rankings(self):
        print("DEBUG [ControladorSistema]: Navegando para Tela de Rankings.")
        self.tela_sistema.fechar_tela()
        self.controlador_ranking.tela_ranking.exibir()
        print("DEBUG [ControladorSistema]: Retornou de da tela de rankings.")
        if self.controlador_usuario.usuario_logado:
            self.inicializarFeed()
        else:
            self.iniciar()
