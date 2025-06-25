import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable, List
from models.usuario import Usuario
from PIL import Image, ImageTk
import requests
import io

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

        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(main_frame, text="SOLICITAÇÕES PENDENTES", style="Header.TLabel").pack(pady=(0, 20))

        if not lista_solicitacoes:
            ttk.Label(main_frame, text="Nenhuma solicitação pendente.").pack(pady=20)
        else:
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

            # Carregar imagens dos ícones com novas URLs
            try:
                # NOVAS URLs para os ícones
                accept_icon_url = "https://uxwing.com/wp-content/themes/uxwing/download/checkmark-cross/success-green-check-mark-icon.png"
                deny_icon_url = "https://uxwing.com/wp-content/themes/uxwing/download/checkmark-cross/red-x-icon.png"

                accept_response = requests.get(accept_icon_url)
                deny_response = requests.get(deny_icon_url)
                
                # Garante que a requisição foi bem sucedida antes de tentar abrir a imagem
                accept_response.raise_for_status()
                deny_response.raise_for_status()

                accept_image = Image.open(io.BytesIO(accept_response.content)).resize((20, 20), Image.Resampling.LANCZOS)
                deny_image = Image.open(io.BytesIO(deny_response.content)).resize((20, 20), Image.Resampling.LANCZOS)

                self.accept_icon = ImageTk.PhotoImage(accept_image)
                self.deny_icon = ImageTk.PhotoImage(deny_image)

            except Exception as e:
                print(f"Erro ao carregar imagens dos ícones: {e}")
                self.accept_icon = None
                self.deny_icon = None

            for solicitacao in lista_solicitacoes:
                self._criar_card_solicitacao(scrollable_frame, solicitacao, callback_aceitar, callback_negar, root)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

        btn_voltar = ttk.Button(root, text="Voltar", command=lambda: [root.destroy(), callback_voltar()])
        btn_voltar.pack(side=tk.BOTTOM, pady=10)

        root.protocol("WM_DELETE_WINDOW", lambda: [root.destroy(), callback_voltar()])
        root.mainloop()

    def _criar_card_solicitacao(
        self,
        parent: tk.Widget,
        remetente: Usuario,
        callback_aceitar: Callable[[Usuario], None],
        callback_negar: Callable[[Usuario], None],
        root_window: tk.Tk
    ):
        card_frame = ttk.Frame(parent, borderwidth=1, relief="solid", padding=10)
        card_frame.pack(fill=tk.X, pady=5, padx=10)

        info_label = ttk.Label(card_frame, text=f"{remetente.nome} quer ser seu amigo(a).", font=("Arial", 11))
        info_label.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        # Apenas cria os botões se os ícones foram carregados com sucesso
        if self.accept_icon and self.deny_icon:
            btn_aceitar = ttk.Button(
                card_frame,
                image=self.accept_icon,
                command=lambda r=remetente: [root_window.destroy(), callback_aceitar(r)]
            )
            btn_aceitar.pack(side=tk.RIGHT, padx=5)
            # É crucial manter uma referência da imagem para evitar que ela seja coletada pelo garbage collector
            btn_aceitar.image = self.accept_icon
            
            btn_negar = ttk.Button(
                card_frame,
                image=self.deny_icon,
                command=lambda r=remetente: [root_window.destroy(), callback_negar(r)]
            )
            btn_negar.pack(side=tk.RIGHT, padx=5)
            # Referência da imagem
            btn_negar.image = self.deny_icon
        else:
            # Fallback para botões de texto se os ícones falharem
            btn_aceitar = ttk.Button(card_frame, text="Aceitar", command=lambda r=remetente: [root_window.destroy(), callback_aceitar(r)])
            btn_aceitar.pack(side=tk.RIGHT, padx=5)
            btn_negar = ttk.Button(card_frame, text="Negar", command=lambda r=remetente: [root_window.destroy(), callback_negar(r)])
            btn_negar.pack(side=tk.RIGHT, padx=5)


    def exibir_mensagem(self, titulo: str, mensagem: str):
        messagebox.showinfo(titulo, mensagem)