import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import io


class TelaMedalha:
    def __init__(self):
        pass

    def exibir_mensagem(self, mensagem: str):
        root = tk.Tk()
        root.title("Medalhas")
        tk.Label(root, text=mensagem, font=("Arial", 14, "italic")).pack(padx=30, pady=30)
        tk.Button(root, text="Voltar", command=root.destroy).pack(pady=10)
        root.mainloop()

    def exibir_medalhas_conquistadas(self, lista_medalhas, callback_voltar):
        root = tk.Tk()
        root.title("Medalhas Conquistadas")
        root.geometry("600x400")
        tk.Label(root, text="Medalhas Conquistadas", font=("Arial", 18, "bold")).pack(pady=15)

        if not lista_medalhas:
            tk.Label(root, text="Nenhuma medalha conquistada ainda.", font=("Arial", 12, "italic")).pack(pady=20)
        else:
            frame = tk.Frame(root)
            frame.pack(pady=10, fill=tk.BOTH, expand=True)
            for medalha in lista_medalhas:
                self._exibir_card_medalha(frame, medalha, conquistada=True)

        tk.Button(root, text="Voltar", command=lambda: [root.destroy(), callback_voltar()]).pack(pady=15)
        root.mainloop()

    def exibir_todas_medalhas(self, lista_medalhas, callback_voltar, conquistadas=None):
        root = tk.Tk()
        root.title("Todas as Medalhas")
        root.geometry("700x500")
        tk.Label(root, text="Todas as Medalhas", font=("Arial", 18, "bold")).pack(pady=15)

        if not lista_medalhas:
            tk.Label(root, text="Nenhuma medalha cadastrada.", font=("Arial", 12, "italic")).pack(pady=20)
        else:
            canvas = tk.Canvas(root)
            scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
            scroll_frame = tk.Frame(canvas)

            scroll_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # Prepare lista de IDs das conquistadas para facilitar a checagem
            conquistadas_ids = set()
            if conquistadas:
                conquistadas_ids = {m.id for m in conquistadas}

            for medalha in lista_medalhas:
                foi_conquistada = medalha.id in conquistadas_ids
                self._exibir_card_medalha(scroll_frame, medalha, conquistada=foi_conquistada)

        tk.Button(root, text="Voltar", command=lambda: [root.destroy(), callback_voltar()]).pack(pady=15)
        root.mainloop()

    def _exibir_card_medalha(self, parent, medalha, conquistada=False):
        cor_fundo = "#d0ffd0" if conquistada else "#f7f7f7"
        frame = tk.Frame(parent, bd=2, relief="groove", padx=10, pady=10, bg=cor_fundo)
        frame.pack(padx=10, pady=8, fill="x", expand=True)

        # Imagem da medalha
        img_label = tk.Label(frame, bg=cor_fundo)
        img_label.pack(side="left", padx=10)
        if hasattr(medalha, "url_photo") and medalha.url_photo:
            try:
                response = requests.get(medalha.url_photo, timeout=5)
                response.raise_for_status()
                img = Image.open(io.BytesIO(response.content)).convert("RGBA")
                img = img.resize((60, 60), Image.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                img_label.configure(image=img_tk)
                img_label.image = img_tk
            except Exception:
                img_label.configure(text="[img]", font=("Arial", 10, "bold"))
        else:
            img_label.configure(text="[img]", font=("Arial", 10, "bold"))

        # Informações da medalha
        info_frame = tk.Frame(frame, bg=cor_fundo)
        info_frame.pack(side="left", padx=10, fill="x", expand=True)
        tk.Label(info_frame, text=f"Descrição: {getattr(medalha, 'descricao', '')}", font=("Arial", 12, "bold"), bg=cor_fundo).pack(anchor="w")
        tk.Label(info_frame, text=f"Valor Base: {getattr(medalha, 'valor_base', '')}", font=("Arial", 10), bg=cor_fundo).pack(anchor="w")
        status = "Conquistada" if conquistada else "Não conquistada"
        tk.Label(info_frame, text=f"Status: {status}", font=("Arial", 10, "italic"), bg=cor_fundo, fg="#228B22" if conquistada else "#888888").pack(anchor="w")