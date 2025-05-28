import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Callable

class TelaTreino:
    def __init__(self):
        pass

    def exibir_tela_registro(self, callback_registrar: Callable[[str, str, str], None]):
        root = tk.Tk()
        root.title("FitUp - Registrar Treino")
        root.geometry("400x380")
        root.resizable(False, False)

        style = ttk.Style(root)
        style.configure("TLabel", font=("Arial", 10))
        style.configure("TButton", font=("Arial", 10, "bold"), padding=5)
        style.configure("TEntry", font=("Arial", 10), padding=5)
        style.configure("Header.TLabel", font=("Arial", 14, "bold"))

        main_frame = ttk.Frame(root, padding="20 20 20 20")
        main_frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(main_frame, text="REGISTRAR TREINO", style="Header.TLabel").pack(pady=(0, 20))

        # Descrição
        frm_desc = ttk.Frame(main_frame)
        frm_desc.pack(fill=tk.X, pady=5)
        ttk.Label(frm_desc, text="DESCRIÇÃO:").pack(side=tk.LEFT, padx=(0, 10))
        entry_descricao = ttk.Entry(frm_desc)
        entry_descricao.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Duração
        frm_dur = ttk.Frame(main_frame)
        frm_dur.pack(fill=tk.X, pady=5)
        ttk.Label(frm_dur, text="DURAÇÃO (MIN):").pack(side=tk.LEFT, padx=(0, 10))
        entry_duracao = ttk.Entry(frm_dur)
        entry_duracao.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Imagem
        imagem_path = {'value': ''}
        def carregar_imagem():
            path = filedialog.askopenfilename(
                title="Selecione uma imagem",
                filetypes=(("Imagens", "*.jpg *.jpeg *.png *.gif"), ("Todos", "*.*"))
            )
            imagem_path['value'] = path or ''
            nome = path.split('/')[-1].split('\\')[-1] if path else 'Nenhuma imagem selecionada.'
            lbl_imagem.config(text=f"Imagem: {nome}")

        btn_imagem = ttk.Button(main_frame, text="CARREGAR IMAGEM", command=carregar_imagem)
        btn_imagem.pack(pady=10, fill=tk.X)
        lbl_imagem = ttk.Label(main_frame, text="Nenhuma imagem selecionada.")
        lbl_imagem.pack(pady=(0, 10))

        # Botão Confirmar
        def on_confirmar():
            desc = entry_descricao.get().strip()
            dur = entry_duracao.get().strip()
            img = imagem_path['value']
            try:
                callback_registrar(desc, dur, img)
                messagebox.showinfo("Sucesso", "Treino registrado com sucesso.", parent=root)
                root.destroy()
            except Exception as e:
                messagebox.showerror("Erro", str(e), parent=root)

        btn_confirmar = ttk.Button(main_frame, text="CONFIRMAR", command=on_confirmar)
        btn_confirmar.pack(pady=20, fill=tk.X)

        root.mainloop()
#teste
