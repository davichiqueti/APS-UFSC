import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable, List
from models.usuario import Usuario

class TelaSolicitacao:
    def __init__(self):
        # Nenhuma mudança aqui
        pass

    def exibir_solicitacoes_pendentes(
        self,
        lista_solicitacoes: List[Usuario],
        callback_aceitar: Callable[[Usuario], None],
        callback_negar: Callable[[Usuario], None],
        callback_voltar: Callable[[], None]
    ):
        # AQUI ESTÁ A MUDANÇA: tk.Toplevel() foi trocado por tk.Tk()
        root = tk.Tk()
        root.title("Solicitações de Amizade")
        root.geometry("500x450")
        root.resizable(False, False)

        # Para centralizar a janela
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')

        style = ttk.Style(root)
        style.configure("TLabel", font=("Arial", 10))
        style.configure("TButton", font=("Arial", 9, "bold"), padding=5)
        style.configure("Header.TLabel", font=("Arial", 14, "bold"))
        style.configure("Accept.TButton", background="#4CAF50", foreground="#4CAF50") # Verde
        style.map("Accept.TButton", background=[('active', '#45a049')])
        style.configure("Deny.TButton", background="#f44336", foreground="#f44336") # Vermelho
        style.map("Deny.TButton", background=[('active', '#e53935')])


        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(main_frame, text="SOLICITAÇÕES PENDENTES", style="Header.TLabel").pack(pady=(0, 20))

        if not lista_solicitacoes:
            ttk.Label(main_frame, text="Nenhuma solicitação pendente.").pack(pady=20)
        else:
            # Frame com scroll para a lista de solicitações
            canvas = tk.Canvas(main_frame)
            scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            for solicitacao in lista_solicitacoes:
                self._criar_card_solicitacao(scrollable_frame, solicitacao, callback_aceitar, callback_negar, root)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

        # O botão voltar agora destrói a janela e chama o callback
        btn_voltar = ttk.Button(root, text="Voltar", command=lambda: [root.destroy(), callback_voltar()])
        btn_voltar.pack(side=tk.BOTTOM, pady=10)

        # Garantir que a janela seja destruída ao fechar no "X"
        root.protocol("WM_DELETE_WINDOW", lambda: [root.destroy(), callback_voltar()])

        root.mainloop()

    def _criar_card_solicitacao(
        self,
        parent: tk.Widget,
        remetente: Usuario,
        callback_aceitar: Callable[[Usuario], None],
        callback_negar: Callable[[Usuario], None],
        root_window: tk.Tk # Mudado para tk.Tk
    ):
        card_frame = ttk.Frame(parent, borderwidth=1, relief="solid", padding=10)
        card_frame.pack(fill=tk.X, pady=5, padx=10)

        info_label = ttk.Label(card_frame, text=f"{remetente.nome} quer ser seu amigo(a).", font=("Arial", 11))
        info_label.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        # A lógica de destruir a janela e chamar o callback é crucial
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