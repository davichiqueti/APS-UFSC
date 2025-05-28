import tkinter as tk
from tkinter import messagebox
from typing import Callable, List
from datetime import date

# NOVOS IMPORTS PARA A IMAGEM
import io # Para lidar com bytes da imagem
import requests # Para baixar a imagem da URL
from PIL import Image, ImageTk # Para processar e exibir a imagem com Tkinter

from models.usuario import Usuario
from models.treino import Treino

class TelaSistema:
    def __init__(self, controlador_sistema_ref=None):
        self.controlador_sistema_ref = controlador_sistema_ref
        self.treinos: List[Treino] = []
        self.indice_treino_atual = 0
        self.root_sistema: tk.Tk | None = None
        
        self.lbl_autor_treino: tk.Label | None = None
        self.lbl_descricao_treino: tk.Label | None = None
        self.lbl_detalhes_treino: tk.Label | None = None
        self.btn_anterior_feed: tk.Button | None = None
        self.btn_proximo_feed: tk.Button | None = None
        self.btn_curtir_treino: tk.Button | None = None
        
        # NOVO: Label para a imagem do treino
        self.lbl_imagem_treino: tk.Label | None = None
        
        self.controlador_treino_ref = None
        self.usuario_logado_atual = None

    def exibir_tela_principal(self, usuario_logado: Usuario, 
                               lista_de_treinos: List[Treino],
                               controlador_treino_ref, 
                               callback_logout: Callable,
                               callback_abrir_perfil: Callable,
                               callback_abrir_busca: Callable,
                               callback_registrar_treino: Callable):
        
        self.treinos = lista_de_treinos 
        self.indice_treino_atual = 0 
        self.controlador_treino_ref = controlador_treino_ref
        self.usuario_logado_atual = usuario_logado

        self.root_sistema = tk.Tk() 
        self.root_sistema.title(f"Feed - Bem-vindo(a), {usuario_logado.nome}!")
        self.root_sistema.geometry("800x750") # Aumentei um pouco a altura para a imagem

        # --- BARRA DE NAVEGAÇÃO ---
        frame_navegacao = tk.Frame(self.root_sistema, bd=1, relief=tk.RAISED)
        frame_navegacao.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))
        tk.Label(frame_navegacao, text=f"Usuário: {usuario_logado.nome}", padx=10, font=("Arial", 10)).pack(side=tk.LEFT)
        tk.Button(frame_navegacao, text="Meu Perfil", command=callback_abrir_perfil).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(frame_navegacao, text="Buscar", command=callback_abrir_busca).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(frame_navegacao, text="Registrar Treino", command=callback_registrar_treino).pack(side=tk.LEFT, padx=5, pady=5)
        def acao_logout_confirmada():
            if messagebox.askyesno("Logout", "Tem certeza que deseja sair?", parent=self.root_sistema):
                callback_logout()
        tk.Button(frame_navegacao, text="Logout", command=acao_logout_confirmada).pack(side=tk.RIGHT, padx=10, pady=5)

        # --- ÁREA DO FEED ---
        frame_feed_area = tk.Frame(self.root_sistema, padx=10, pady=10)
        frame_feed_area.pack(expand=True, fill=tk.BOTH)
        tk.Label(frame_feed_area, text="FEED DE TREINOS DOS AMIGOS", font=("Arial", 18, "bold")).pack(pady=(5,15))

        # Ajustado para acomodar a imagem primeiro
        frame_treino_display = tk.Frame(frame_feed_area, bd=2, relief=tk.GROOVE, padx=15, pady=15)
        frame_treino_display.pack(pady=10, fill=tk.X)
        # Removido height e pack_propagate para deixar o conteúdo definir a altura

        # NOVO: Label para exibir a imagem do treino
        self.lbl_imagem_treino = tk.Label(frame_treino_display)
        self.lbl_imagem_treino.pack(pady=(0, 10)) # Espaço abaixo da imagem

        self.lbl_autor_treino = tk.Label(frame_treino_display, text="", font=("Arial", 10, "italic"), anchor="w")
        self.lbl_autor_treino.pack(fill=tk.X, pady=(0,2))
        self.lbl_descricao_treino = tk.Label(frame_treino_display, text="", font=("Arial", 14, "bold"), wraplength=750, anchor="w", justify=tk.LEFT)
        self.lbl_descricao_treino.pack(pady=(5,10), fill=tk.X)
        self.lbl_detalhes_treino = tk.Label(frame_treino_display, text="", justify=tk.LEFT, wraplength=750, anchor="w")
        self.lbl_detalhes_treino.pack(pady=5, fill=tk.X)

        # --- BOTÕES DE INTERAÇÃO DO FEED ---
        frame_interacao_feed = tk.Frame(frame_feed_area)
        frame_interacao_feed.pack(pady=10)
        self.btn_anterior_feed = tk.Button(frame_interacao_feed, text="<< Treino Anterior", command=self.acao_treino_anterior)
        self.btn_anterior_feed.pack(side=tk.LEFT, padx=20)
        self.btn_curtir_treino = tk.Button(frame_interacao_feed, text="❤️ Curtir (0)", command=self.acao_curtir_treino)
        self.btn_curtir_treino.pack(side=tk.LEFT, padx=20)
        self.btn_proximo_feed = tk.Button(frame_interacao_feed, text="Próximo Treino >>", command=self.acao_treino_proximo)
        self.btn_proximo_feed.pack(side=tk.LEFT, padx=20)

        if not self.treinos:
            self.exibirMensagemSemTreinos()
        else:
            self.exibirTreino(0)
        
        print("DEBUG [TelaSistema.exibir_tela_principal]: UI configurada. Mainloop será iniciado externamente.")

    def exibirTreino(self, indice: int):
        if not self.treinos or not (0 <= indice < len(self.treinos)):
            self.exibirMensagemSemTreinos()
            return

        self.indice_treino_atual = indice
        treino_atual: Treino = self.treinos[self.indice_treino_atual]

        if not all([self.lbl_autor_treino, self.lbl_descricao_treino, self.lbl_detalhes_treino, 
                    self.btn_curtir_treino, self.btn_anterior_feed, self.btn_proximo_feed,
                    self.lbl_imagem_treino]): # Adicionado lbl_imagem_treino à verificação
            print("WARN [TelaSistema.exibirTreino]: Widgets de display não inicializados.")
            return

        self.btn_anterior_feed.config(state=tk.NORMAL)
        self.btn_proximo_feed.config(state=tk.NORMAL)
        self.btn_curtir_treino.config(state=tk.NORMAL)
        
        # --- CARREGAR E EXIBIR IMAGEM ---
        if hasattr(treino_atual, 'imagem') and treino_atual.imagem:
            try:
                print(f"DEBUG [TelaSistema.exibirTreino]: Carregando imagem de {treino_atual.imagem}")
                # Define um tamanho máximo para a imagem exibida
                max_width = 400
                max_height = 300

                response = requests.get(treino_atual.imagem, stream=True)
                response.raise_for_status() # Levanta um erro para códigos de status ruins (4xx ou 5xx)
                
                image_bytes = response.content
                pil_image = Image.open(io.BytesIO(image_bytes))
                
                # Redimensiona a imagem mantendo a proporção
                pil_image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                
                tk_image = ImageTk.PhotoImage(pil_image)
                
                self.lbl_imagem_treino.config(image=tk_image)
                self.lbl_imagem_treino.image = tk_image # Mantém uma referência para evitar garbage collection
            except Exception as e:
                print(f"ERRO [TelaSistema.exibirTreino]: Não foi possível carregar a imagem {treino_atual.imagem}: {e}")
                self.lbl_imagem_treino.config(image=None, text="Imagem não disponível") # Limpa se houver erro
                self.lbl_imagem_treino.image = None # Limpa referência antiga
        else:
            self.lbl_imagem_treino.config(image=None, text="") # Sem imagem para exibir
            self.lbl_imagem_treino.image = None

        # --- ATUALIZAR OUTROS LABELS ---
        nome_autor = "Autor Desconhecido"
        if treino_atual.usuario and hasattr(treino_atual.usuario, 'nome'):
            nome_autor = treino_atual.usuario.nome
        
        data_formatada = treino_atual.data.strftime('%d/%m/%Y') if treino_atual.data else 'Data não informada'
        self.lbl_autor_treino.config(text=f"Postado por: {nome_autor} em {data_formatada}")
        self.lbl_descricao_treino.config(text=treino_atual.descricao, font=("Arial", 14, "bold"))
        
        detalhes_str = ""
        if hasattr(treino_atual, 'duracao') and treino_atual.duracao is not None:
            detalhes_str += f"Duração: {treino_atual.duracao} min"
        self.lbl_detalhes_treino.config(text=detalhes_str)
        
        self.btn_curtir_treino.config(text=f"❤️ Curtir ({treino_atual.curtidas})")

    def exibirMensagemSemTreinos(self):
        if not all([self.lbl_autor_treino, self.lbl_descricao_treino, self.lbl_detalhes_treino, 
                    self.btn_curtir_treino, self.btn_anterior_feed, self.btn_proximo_feed,
                    self.lbl_imagem_treino]): # Adicionado lbl_imagem_treino
            print("WARN [TelaSistema.exibirMensagemSemTreinos]: Widgets de display não inicializados.")
            return
            
        self.lbl_imagem_treino.config(image=None, text="") # Limpa imagem
        self.lbl_imagem_treino.image = None
        self.lbl_autor_treino.config(text="")
        self.lbl_descricao_treino.config(text="Suas conexões ainda não registraram treinos.", font=("Arial", 12, "italic"))
        self.lbl_detalhes_treino.config(text="")
        self.btn_curtir_treino.config(text="❤️ Curtir", state=tk.DISABLED)
        self.btn_anterior_feed.config(state=tk.DISABLED)
        self.btn_proximo_feed.config(state=tk.DISABLED)

    # ... (seus outros métodos: acao_treino_anterior, acao_treino_proximo, acao_curtir_treino,
    #      fechar_tela, iniciar_loop_eventos) ...
    # Lembre-se que acao_curtir_treino deve usar self.controlador_treino_ref
    # e que os métodos fechar_tela e iniciar_loop_eventos devem usar self.root_sistema.
    def acao_treino_anterior(self):
        if not self.treinos or len(self.treinos) <= 1: return 
        novo_indice = self.indice_treino_atual - 1
        if novo_indice < 0: novo_indice = len(self.treinos) - 1 
        self.exibirTreino(novo_indice)

    def acao_treino_proximo(self):
        if not self.treinos or len(self.treinos) <= 1: return
        novo_indice = self.indice_treino_atual + 1
        if novo_indice >= len(self.treinos): novo_indice = 0
        self.exibirTreino(novo_indice)
        
    def acao_curtir_treino(self):
        if not self.root_sistema: return
        if not self.treinos or not (0 <= self.indice_treino_atual < len(self.treinos)): return 
        treino_atual: Treino = self.treinos[self.indice_treino_atual]
        if self.controlador_treino_ref and hasattr(self.controlador_treino_ref, 'curtir_treino'):
            sucesso_curtida = self.controlador_treino_ref.curtir_treino(treino_atual.id)
            if sucesso_curtida:
                treino_atual.curtidas += 1 
                self.exibirTreino(self.indice_treino_atual)
            else: messagebox.showerror("Erro", "Não foi possível registrar a curtida.", parent=self.root_sistema)
        else: print("ERRO [TelaSistema.acao_curtir_treino]: Referência ao ControladorTreino não configurada.")

    def fechar_tela(self):
        if self.root_sistema and self.root_sistema.winfo_exists():
            self.root_sistema.destroy()
            self.root_sistema = None

    def iniciar_loop_eventos(self):
        if self.root_sistema and self.root_sistema.winfo_exists():
            self.root_sistema.mainloop()
            print("DEBUG [TelaSistema.iniciar_loop_eventos]: Mainloop de root_sistema terminou.")