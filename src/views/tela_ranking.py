import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Callable


class TelaRanking:
    def __init__(self, controlador_ranking):
        self.controlador_ranking = controlador_ranking

        self._tipo: str | None = None
        self._periodo: int | None = None
        self._ranking_table: ttk.Treeview = None
        self._ranking_subtitulo: ttk.Label = None

    def exibir(self):
        tipos_aceitos = (
            "Número de Treinos",
            "Tempo em Atividade",
            "Sequência de Treinos",
        )

        periodos = {
            "Semana atual": 7,
            "Mês atual": 30,
            "Últimos 3 meses": 90,
            "Últimos 6 meses": 180
        }

        # Basico da tela
        root = tk.Tk()
        root.title("FitUp - Rankings")
        root.resizable(False, False)
        root.geometry("800x650")

        style = ttk.Style(root)
        style.configure("TLabel", font=("Arial", 10))
        style.configure("TButton", font=("Arial", 10, "bold"), padding=5)
        style.configure("TEntry", font=("Arial", 10), padding=5)
        style.configure("Header.TLabel", font=("Arial", 14, "bold"))

        self.main_frame = ttk.Frame(root, padding="20 20 20 20")
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        # Componentes
        ttk.Label(self.main_frame, text="Rankings", style="Header.TLabel").pack(pady=(0, 20))

        ttk.Label(self.main_frame, text="Tipo de ranking:").pack(pady=5)
        selecao_tipo = ttk.Combobox(
            self.main_frame,
            values=tipos_aceitos,
            state="readonly"
        )
        selecao_tipo.pack(pady=1)

        ttk.Label(self.main_frame, text="Período:").pack(pady=5)
        selecao_periodo = ttk.Combobox(
            self.main_frame,
            values=list(periodos.keys()),
            state="disabled"
        )
        selecao_periodo.pack(pady=1)

        def atualizar_ranking():
            listagem = self.controlador_ranking.gerarListagemRanking(
                self._tipo,
                self._periodo
            )
            self.exibirRanking(listagem)

        def evento_tipo_definido(event=None):
            tipo_selecionado = selecao_tipo.get()
            self.definirTipo(tipo_selecionado)
            if tipo_selecionado == "Sequência de Treinos":
                selecao_periodo.config(state="disabled")
                atualizar_ranking()
            else:
                selecao_periodo.config(state="readonly")
                if self._periodo and not selecao_periodo.get().isspace():
                    atualizar_ranking()

        def evento_periodo_definido(event=None):
            periodo_selecionado = selecao_periodo.get()
            valor_correspondente = periodos[periodo_selecionado]
            self.definirPeriodo(valor_correspondente)
            atualizar_ranking()

        selecao_tipo.bind("<<ComboboxSelected>>", evento_tipo_definido)
        selecao_periodo.bind("<<ComboboxSelected>>", evento_periodo_definido)

        root.mainloop()

    def definirTipo(self, tipo: str):
        self._tipo = tipo

    def definirPeriodo(self, periodo: int):
        self._periodo = periodo

    def exibirRanking(self, listagem):
        if self._ranking_table is not None:
            try:
                if self._ranking_table.winfo_exists():
                    self._ranking_table.destroy()
            except tk.TclError:
                pass
            self._ranking_table = None

        if self._ranking_subtitulo is not None:
            try:
                if self._ranking_subtitulo.winfo_exists():
                    self._ranking_subtitulo.destroy()
            except tk.TclError:
                pass
            self._ranking_subtitulo = None

        self._ranking_subtitulo = ttk.Label(
            self.main_frame,
            text=f"Ranking de {self._tipo}",
            font=("Arial", 13, "bold")
        )
        self._ranking_subtitulo.pack(pady=(10, 0))

        # Definindo estilo da tabela
        style = ttk.Style()
        style.configure("Ranking.Treeview", font=("Arial", 12))
        style.configure("Ranking.Treeview.Heading", font=("Arial", 12, "bold"))

        # Cria Treeview para exibir ranking
        tree = ttk.Treeview(
            self.main_frame,
            columns=("pos", "nome", "pontuacao"),
            show="headings",
            height=15,
            style="Ranking.Treeview"
        )
        tree.heading("pos", text="Posição")
        tree.heading("nome", text="Nome")
        tree.heading("pontuacao", text="Pontuação")
        tree.column("pos", width=80, anchor="center")
        tree.column("nome", width=300, anchor="center")
        tree.column("pontuacao", width=120, anchor="center")

        # Definindo tags para estilizar linhas forma facilmente alteravel
        tree.tag_configure(1, background='#FFD700')
        tree.tag_configure(2, background='#C0C0C0')
        tree.tag_configure(3, background='#CD7F32')

        # Insere os dados
        for index in range(len(listagem)):
            posicao = index + 1
            usuario, pontuacao = listagem[index]
            tree.insert(
                parent="",
                index=index,
                values=(posicao, usuario, pontuacao),
                tags=(posicao, )
            )

        tree.pack(pady=20)
        self._ranking_table = tree
