import tkinter as tk
from tkinter import messagebox
from typing import Callable, List
from datetime import date

from models.usuario import Usuario
from models.treino import Treino

# --- Mock de Usuários e Treinos (lista normal neste arquivo) ---
usuario_mock_joao = Usuario(cpf="11133333333", nome="João Atleta", email="joao@email.com", foto="joao.png", data_nascimento=date(1990, 5, 15), senha_criptografada="...")
usuario_mock_maria = Usuario(cpf="22233333333", nome="Maria Fitness", email="maria@email.com", foto="maria.png", data_nascimento=date(1995, 8, 20), senha_criptografada="...")
usuario_mock_carlos = Usuario(cpf="33333333333", nome="Carlos Corredor", email="carlos@run.com", foto="carlos.png", data_nascimento=date(1988, 1, 10), senha_criptografada="...")

mock_treinos_obj: List[Treino] = [
    Treino(id_treino=1, descricao="Corrida na Esteira Moderada", duracao=45, usuario=usuario_mock_joao, data_treino=date(2024, 5, 20), curtidas=112, imagem="run.png"),
    Treino(id_treino=2, descricao="Treino Funcional Intenso HIIT", duracao=30, usuario=usuario_mock_maria, data_treino=date(2024, 5, 21), curtidas=250, imagem="hiit.png"),
    Treino(id_treino=3, descricao="Alongamento e Mobilidade Articular", duracao=20, usuario=usuario_mock_carlos, data_treino=date(2024, 5, 22), curtidas=75, imagem="stretch.png"),
    Treino(id_treino=4, descricao="Bicicleta Ergométrica - Foco em Resistência", duracao=60, usuario=usuario_mock_joao, data_treino=date(2024, 5, 23), curtidas=98, imagem="bike.png"),
]


class TelaSistema:
    def __init__(self):
        self.treinos: List[Treino] = mock_treinos_obj # Usando a lista de objetos Treino
        self.indice_treino_atual = 0
        self.root_sistema = None

    def exibir_tela_principal(self, usuario_logado: Usuario, callback_logout: Callable,
                               callback_abrir_perfil: Callable,
                               callback_abrir_busca: Callable,
                               callback_registrar_treino: Callable):
        
        

        self.root_sistema = tk.Tk()
        self.root_sistema.title(f"Feed - Bem-vindo(a), {usuario_logado.nome}!")
        self.root_sistema.geometry("800x650")

        frame_navegacao = tk.Frame(self.root_sistema, bd=1, relief=tk.RAISED)
        frame_navegacao.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))
        tk.Label(frame_navegacao, text=f"Usuário: {usuario_logado.nome}", padx=10, font=("Arial", 10)).pack(side=tk.LEFT)
        tk.Button(frame_navegacao, text="Meu Perfil", command=callback_abrir_perfil).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(frame_navegacao, text="Buscar", command=callback_abrir_busca).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(frame_navegacao, text="Registrar Treino", command=callback_registrar_treino).pack(side=tk.LEFT, padx=5, pady=5)


        frame_feed_area = tk.Frame(self.root_sistema, padx=10, pady=10)
        frame_feed_area.pack(expand=True, fill=tk.BOTH)
        tk.Label(frame_feed_area, text="FEED DE TREINOS", font=("Arial", 18, "bold")).pack(pady=(5,15))

        self.frame_treino_display = tk.Frame(frame_feed_area, bd=2, relief=tk.GROOVE, padx=15, pady=15)
        self.frame_treino_display.pack(pady=10, fill=tk.X)

        self.lbl_autor_treino = tk.Label(self.frame_treino_display, text="", font=("Arial", 10, "italic"), anchor="w")
        self.lbl_autor_treino.pack(fill=tk.X)
        self.lbl_descricao_treino = tk.Label(self.frame_treino_display, text="", font=("Arial", 14, "bold"), wraplength=700, anchor="w", justify=tk.LEFT)
        self.lbl_descricao_treino.pack(pady=(5,10), fill=tk.X)
        self.lbl_detalhes_treino = tk.Label(self.frame_treino_display, text="", justify=tk.LEFT, wraplength=700, anchor="w") # Usaremos para duração por enquanto
        self.lbl_detalhes_treino.pack(pady=5, fill=tk.X)

        frame_interacao_feed = tk.Frame(frame_feed_area)
        frame_interacao_feed.pack(pady=10)
        tk.Button(frame_interacao_feed, text="<< Treino Anterior", command=self.acao_treino_anterior).pack(side=tk.LEFT, padx=20)
        self.btn_curtir_treino = tk.Button(frame_interacao_feed, text="❤️ Curtir (0)", command=self.acao_curtir_treino)
        self.btn_curtir_treino.pack(side=tk.LEFT, padx=20)
        tk.Button(frame_interacao_feed, text="Próximo Treino >>", command=self.acao_treino_proximo).pack(side=tk.LEFT, padx=20)

        self._atualizar_exibicao_treino()
        self.root_sistema.mainloop()

    def _atualizar_exibicao_treino(self):
        if not self.treinos:
            self.lbl_autor_treino.config(text="")
            self.lbl_descricao_treino.config(text="Suas amizades ainda não registraram treinos.")
            self.lbl_detalhes_treino.config(text="")
            self.btn_curtir_treino.config(text="❤️ Curtir (-)", state=tk.DISABLED)
            return

        if 0 <= self.indice_treino_atual < len(self.treinos):
            treino_atual: Treino = self.treinos[self.indice_treino_atual] # Agora é um objeto Treino

            nome_autor = "Desconhecido"
            if treino_atual.usuario: # Verifica se o treino tem um usuário associado
                nome_autor = treino_atual.usuario.nome # Acessa o nome do usuário diretamente
                # Ou: nome_autor = treino_atual.getUsuario().getNome() # Usando getters

            self.lbl_autor_treino.config(text=f"Postado por: {nome_autor} em {treino_atual.data.strftime('%d/%m/%Y') if treino_atual.data else 'Data não informada'}")
            self.lbl_descricao_treino.config(text=treino_atual.descricao) # Acesso direto
            # Ou: self.lbl_descricao_treino.config(text=treino_atual.getDescricao()) # Usando getter
            
            detalhes_str = ""
            if treino_atual.duracao is not None:
                detalhes_str += f"Duração: {treino_atual.duracao} min"
            # Você pode adicionar mais informações do treino aqui, como a imagem (se for exibir)
            # ou outros detalhes que sua classe Treino possa ter e que você queira mostrar.
            self.lbl_detalhes_treino.config(text=detalhes_str)
            
            self.btn_curtir_treino.config(text=f"❤️ Curtir ({treino_atual.curtidas})", state=tk.NORMAL)
            # Ou: self.btn_curtir_treino.config(text=f"❤️ Curtir ({treino_atual.getCurtidas()})", state=tk.NORMAL)
        else:
            self.lbl_autor_treino.config(text="")
            self.lbl_descricao_treino.config(text="Erro ao carregar treino.")
            self.lbl_detalhes_treino.config(text="")
            self.btn_curtir_treino.config(text="❤️ Curtir (-)", state=tk.DISABLED)

    def acao_treino_anterior(self):
        # ... (lógica idêntica à anterior) ...
        if not self.treinos: return
        if self.indice_treino_atual > 0:
            self.indice_treino_atual -= 1
            self._atualizar_exibicao_treino()
        else:
            messagebox.showinfo("Feed", "Você já está no primeiro treino.", parent=self.root_sistema)


    def acao_treino_proximo(self):
        # ... (lógica idêntica à anterior) ...
        if not self.treinos: return
        if self.indice_treino_atual < len(self.treinos) - 1:
            self.indice_treino_atual += 1
            self._atualizar_exibicao_treino()
        else:
            messagebox.showinfo("Feed", "Você já está no último treino.", parent=self.root_sistema)


    def acao_curtir_treino(self):
        if not self.treinos or not (0 <= self.indice_treino_atual < len(self.treinos)):
             messagebox.showerror("Erro", "Nenhum treino selecionado para curtir.", parent=self.root_sistema)
             return

        treino_atual: Treino = self.treinos[self.indice_treino_atual]
        
        # Incrementa a curtida no objeto Treino
        novas_curtidas = treino_atual.curtidas + 1
        treino_atual.curtidas = novas_curtidas # Acesso direto
        # Ou: treino_atual.setCurtidas(novas_curtidas) # Usando setter
        
        # No futuro, você chamaria seu controlador aqui para persistir essa curtida no banco de dados.
        # Ex: self.controlador_geral.controlador_treino.registrar_curtida(treino_atual.id, usuario_logado.id)
        
        self._atualizar_exibicao_treino()

    def fechar_tela(self):
        if self.root_sistema and self.root_sistema.winfo_exists():
            self.root_sistema.destroy()
            self.root_sistema = None
