import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable, List
from models.usuario import Usuario

class TelaSolicitacao:
    def __init__(self):
        pass

    def exibir_solicitacoes_pendentes(
        self,
        lista_solicitacoes: List[Usuario],
        callback_aceitar: Callable[[Usuario], None],
        callback_negar: Callable[[Usuario], None],
        callback_voltar: Callable[[], None]
    ):
        root = tk.Toplevel()
        root.title("Solicitações de Amizade")
        root.geometry("500x450")
        root.resizable(False, False)

        style = ttk.Style(root)
        style.configure("TLabel", font=("Arial", 10))
        style.configure("TButton", font=("Arial", 9, "bold"), padding=5)
        style.configure("Header.TLabel", font=("Arial", 14, "bold"))
        style.configure("Accept.TButton", background="green", foreground="white")
        style.configure("Deny.TButton", background="red", foreground="white")

        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(main_frame, text="SOLICITAÇÕES PENDENTES", style="Header.TLabel").pack(pady=(0, 20))

        if not lista_solicitacoes:
            ttk.Label(main_frame, text="Nenhuma solicitação pendente.").pack(pady=20)
        else:
            for solicitacao in lista_solicitacoes:
                self._criar_card_solicitacao(main_frame, solicitacao, callback_aceitar, callback_negar, root)
        
        btn_voltar = ttk.Button(main_frame, text="Voltar", command=lambda: [root.destroy(), callback_voltar()])
        btn_voltar.pack(side=tk.BOTTOM, pady=10)

        root.mainloop()

    def _criar_card_solicitacao(
        self,
        parent: tk.Widget,
        remetente: Usuario,
        callback_aceitar: Callable[[Usuario], None],
        callback_negar: Callable[[Usuario], None],
        root_window: tk.Toplevel
    ):
        card_frame = ttk.Frame(parent, borderwidth=1, relief="solid", padding=10)
        card_frame.pack(fill=tk.X, pady=5)

        info_label = ttk.Label(card_frame, text=f"{remetente.nome} quer ser seu amigo(a).", font=("Arial", 11))
        info_label.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        btn_aceitar = ttk.Button(
            card_frame,
            text="Aceitar",
            style="Accept.TButton",
            command=lambda r=remetente: [root_window.destroy(), callback_aceitar(r)]
        )
        btn_aceitar.pack(side=tk.RIGHT, padx=5)
        
        btn_negar = ttk.Button(
            card_frame,
            text="Negar",
            style="Deny.TButton",
            command=lambda r=remetente: [root_window.destroy(), callback_negar(r)]
        )
        btn_negar.pack(side=tk.RIGHT, padx=5)

    def exibir_mensagem(self, titulo: str, mensagem: str):
        messagebox.showinfo(titulo, mensagem)