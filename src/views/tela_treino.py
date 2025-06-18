import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Callable
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Configure o Cloudinary com suas credenciais AQUI
# SUBSTITUA com seu cloud_name, api_key e api_secret
cloudinary.config(
  cloud_name = "dlugl1sww",
  api_key = "126437426144361",
  api_secret = "n7qzsbIKxct-MStresJxJkuVmYc"
)

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
        imagem_path = {'value': ''} # Irá armazenar a URL da imagem do Cloudinary

        def carregar_imagem():
            path = filedialog.askopenfilename(
                title="Selecione uma imagem",
                filetypes=(("Imagens", "*.jpg *.jpeg *.png *.gif"), ("Todos", "*.*"))
            )
            if path:
                # Faz o upload para o Cloudinary
                upload_result = cloudinary.uploader.upload(path)
                # Armazena a URL segura da imagem
                imagem_path['value'] = upload_result['secure_url']
                # Atualiza o label para mostrar o public_id da imagem no Cloudinary
                lbl_imagem.config(text=f"Imagem enviada: {upload_result['public_id']}")
            else:
                imagem_path['value'] = ''
                lbl_imagem.config(text="Nenhuma imagem selecionada.")

        btn_imagem = ttk.Button(main_frame, text="CARREGAR IMAGEM", command=carregar_imagem)
        btn_imagem.pack(pady=10, fill=tk.X)
        lbl_imagem = ttk.Label(main_frame, text="Nenhuma imagem selecionada.")
        lbl_imagem.pack(pady=(0, 10))

        # Botão Confirmar
        def on_confirmar():
            desc = entry_descricao.get().strip()
            dur = entry_duracao.get().strip()
            img_url = imagem_path['value'] # Agora é a URL do Cloudinary
            try:
                callback_registrar(desc, dur, img_url)
                messagebox.showinfo("Sucesso", "Treino registrado com sucesso.", parent=root)
                root.destroy()
            except Exception as e:
                messagebox.showerror("Erro", str(e), parent=root)

        btn_confirmar = ttk.Button(main_frame, text="CONFIRMAR", command=on_confirmar)
        btn_confirmar.pack(pady=20, fill=tk.X)

        root.mainloop()