import tkinter as tk
from tkinter import ttk
from typing import Callable, List
from models.usuario import Usuario

class TelaBusca:
    def __init__(self):
        self.root = None
        self.frame_resultados = None
        self.entry_busca = None

    def exibir_tela_busca(
        self,
        callback_buscar: Callable[[str], None],
        callback_abrir_perfil: Callable[[Usuario], None],
        callback_voltar: Callable[[], None]
    ):
        self.root = tk.Tk()
        self.root.title("Buscar Usuários")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        # Centralizar a janela
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

        style = ttk.Style(self.root)
        style.configure("TLabel", font=("Arial", 10))
        style.configure("TButton", font=("Arial", 9, "bold"), padding=5)
        style.configure("Header.TLabel", font=("Arial", 14, "bold"))

        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Frame de busca
        frame_busca = ttk.Frame(main_frame)
        frame_busca.pack(fill=tk.X, pady=(0, 20))

        self.entry_busca = ttk.Entry(frame_busca, font=("Arial", 12))
        self.entry_busca.pack(side=tk.LEFT, expand=True, fill=tk.X, ipady=4)
        self.entry_busca.bind("<Return>", lambda event: callback_buscar(self.entry_busca.get()))

        btn_buscar = ttk.Button(frame_busca, text="Buscar", command=lambda: callback_buscar(self.entry_busca.get()))
        btn_buscar.pack(side=tk.RIGHT, padx=(10, 0))

        # Frame de resultados com scroll
        canvas = tk.Canvas(main_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        self.frame_resultados = ttk.Frame(canvas)

        self.frame_resultados.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.frame_resultados, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        btn_voltar = ttk.Button(self.root, text="Voltar", command=lambda: [self.root.destroy(), callback_voltar()])
        btn_voltar.pack(side=tk.BOTTOM, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", lambda: [self.root.destroy(), callback_voltar()])
        self.root.mainloop()

    def atualizar_resultados(self, resultados: List[Usuario], callback_abrir_perfil: Callable[[Usuario], None]):
        # Limpa resultados antigos
        for widget in self.frame_resultados.winfo_children():
            widget.destroy()

        if not resultados:
            ttk.Label(self.frame_resultados, text="Nenhum usuário encontrado.", font=("Arial", 11, "italic")).pack(pady=20)
        else:
            for usuario in resultados:
                self._criar_card_usuario(self.frame_resultados, usuario, callback_abrir_perfil)

    def _criar_card_usuario(self, parent: tk.Widget, usuario: Usuario, callback_abrir_perfil: Callable[[Usuario], None]):
        card_frame = ttk.Frame(parent, borderwidth=1, relief="solid", padding=10, style="Card.TFrame")
        card_frame.pack(fill=tk.X, pady=5, padx=10)
        card_frame.bind("<Button-1>", lambda e: [self.root.destroy(), callback_abrir_perfil(usuario)])

        info_label = ttk.Label(card_frame, text=f"{usuario.nome}", font=("Arial", 12, "bold"))
        info_label.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        info_label.bind("<Button-1>", lambda e: [self.root.destroy(), callback_abrir_perfil(usuario)])

        email_label = ttk.Label(card_frame, text=f"{usuario.email}", font=("Arial", 9))
        email_label.pack(side=tk.RIGHT, padx=5)
        email_label.bind("<Button-1>", lambda e: [self.root.destroy(), callback_abrir_perfil(usuario)])