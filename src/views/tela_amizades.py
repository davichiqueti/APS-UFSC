import tkinter as tk

class TelaAmizades:
    def __init__(self):
        pass

    def exibir_amizades(self, lista_amigos, callback_voltar, callback_abrir_perfil=None):
        root = tk.Tk()
        root.title("Amizades")
        root.geometry("500x400")
        tk.Label(root, text="Amizades", font=("Arial", 18, "bold")).pack(pady=15)
    
        if not lista_amigos:
            tk.Label(root, text="Nenhuma amizade encontrada.", font=("Arial", 12, "italic")).pack(pady=20)
        else:
            frame = tk.Frame(root)
            frame.pack(pady=10, fill=tk.BOTH, expand=True)
            for amigo in lista_amigos:
                self._exibir_card_amigo(
                    frame,
                    amigo,
                    callback_abrir_perfil=(lambda a=amigo: [root.destroy(), callback_abrir_perfil(a)]) if callback_abrir_perfil else None
                )
    
        tk.Button(root, text="Voltar", command=lambda: [root.destroy(), callback_voltar()]).pack(pady=15)
        root.mainloop()

    def _exibir_card_amigo(self, parent, amigo, callback_abrir_perfil=None):
        frame = tk.Frame(parent, bd=2, relief="groove", padx=10, pady=10, bg="#f7f7f7", cursor="hand2")
        frame.pack(padx=10, pady=8, fill="x", expand=True)

        nome = getattr(amigo, "nome", "Usuário")
        email = getattr(amigo, "email", "")
        tk.Label(frame, text=nome, font=("Arial", 12, "bold"), bg="#f7f7f7").pack(anchor="w")
        tk.Label(frame, text=email, font=("Arial", 10), bg="#f7f7f7").pack(anchor="w")

        if callback_abrir_perfil:
            frame.bind("<Button-1>", lambda e: callback_abrir_perfil(amigo))
            for widget in frame.winfo_children():
                widget.bind("<Button-1>", lambda e: callback_abrir_perfil(amigo))