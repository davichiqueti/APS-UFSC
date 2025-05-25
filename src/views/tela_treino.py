import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import date
from controllers.controlador_usuario import ControladorUsuario
from controllers.controlador_treino import ControladorTreino

class ViewTreino(tk.Tk):
    def __init__(self, controlador_treino: ControladorTreino, controlador_usuario: ControladorUsuario):
        super().__init__()
        self.controlador_treino = controlador_treino
        self.controlador_usuario = controlador_usuario
        self._imagem_path = ""

        self.title("FitUp - Registrar Treino")
        self.geometry("400x380")
        self.resizable(False, False)

        style = ttk.Style(self)
        style.configure("TLabel", font=("Arial", 10))
        style.configure("TButton", font=("Arial", 10, "bold"), padding=5)
        style.configure("TEntry", font=("Arial", 10), padding=5)
        style.configure("Header.TLabel", font=("Arial", 14, "bold"))

        main_frame = ttk.Frame(self, padding="20 20 20 20")
        main_frame.pack(expand=True, fill=tk.BOTH)

        self.lbl_title = ttk.Label(main_frame, text="REGISTRAR TREINO", style="Header.TLabel")
        self.lbl_title.pack(pady=(0, 20))

        frm_descricao = ttk.Frame(main_frame)
        frm_descricao.pack(fill=tk.X, pady=5)
        self.lbl_descricao_txt = ttk.Label(frm_descricao, text="DESCRIÇÃO:")
        self.lbl_descricao_txt.pack(side=tk.LEFT, padx=(0,10))
        self.entry_descricao = ttk.Entry(frm_descricao)
        self.entry_descricao.pack(side=tk.LEFT, expand=True, fill=tk.X)

        frm_duracao = ttk.Frame(main_frame)
        frm_duracao.pack(fill=tk.X, pady=5)
        self.lbl_duracao_txt = ttk.Label(frm_duracao, text="DURAÇÃO (MINUTOS):")
        self.lbl_duracao_txt.pack(side=tk.LEFT, padx=(0,10))
        self.entry_duracao = ttk.Entry(frm_duracao)
        self.entry_duracao.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.btn_carregar_imagem_ui = ttk.Button(main_frame, text="CARREGUE SUA IMAGEM", command=self._carregar_imagem_pelo_dialog)
        self.btn_carregar_imagem_ui.pack(pady=10, fill=tk.X)
        self.lbl_imagem_selecionada = ttk.Label(main_frame, text="Nenhuma imagem selecionada.")
        self.lbl_imagem_selecionada.pack(pady=(0,10))

        self.btn_confirmar_ui = ttk.Button(main_frame, text="CONFIRMAR", command=self.confirmarRegistro)
        self.btn_confirmar_ui.pack(pady=20, fill=tk.X)

        self.registrarTreino()

    def registrarTreino(self):
        """Prepara a view para um novo registro, limpando os campos."""
        print("[ViewTreino] Método registrarTreino() chamado - limpando campos.")
        if hasattr(self, 'entry_descricao'):
            self.entry_descricao.delete(0, tk.END)
            self.entry_duracao.delete(0, tk.END)
            self._imagem_path = ""
            self.lbl_imagem_selecionada.config(text="Nenhuma imagem selecionada.")
        return self 
    
    def informarDescricao(self, descricao_texto: str):
        """Define programaticamente o campo de descrição."""
        print(f"[ViewTreino] Método informarDescricao('{descricao_texto}') chamado.")
        self.entry_descricao.delete(0, tk.END)
        self.entry_descricao.insert(0, descricao_texto)

    def informarDuracao(self, duracao_valor: int):
        """Define programaticamente o campo de duração."""
        print(f"[ViewTreino] Método informarDuracao({duracao_valor}) chamado.")
        self.entry_duracao.delete(0, tk.END)
        self.entry_duracao.insert(0, str(duracao_valor))

    def anexarImagem(self, imagem_caminho: str):
        """Define programaticamente o caminho da imagem e atualiza o label."""
        print(f"[ViewTreino] Método anexarImagem('{imagem_caminho}') chamado.")
        self._imagem_path = imagem_caminho
        if imagem_caminho:
            filename = imagem_caminho.split("/")[-1].split("\\")[-1]
            self.lbl_imagem_selecionada.config(text=f"Imagem: {filename}")
        else:
            self.lbl_imagem_selecionada.config(text="Nenhuma imagem selecionada.")

    def _carregar_imagem_pelo_dialog(self):
        """Método interno para lidar com o diálogo de carregar imagem via UI."""
        file_path = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=(("Arquivos de Imagem", "*.jpg *.jpeg *.png *.gif"), ("Todos os arquivos", "*.*"))
        )
        self.anexarImagem(file_path if file_path else "")


    def confirmarRegistro(self):
        """Coleta os dados da view e aciona o controlador para registrar o treino."""
        print("[ViewTreino] Método confirmarRegistro() chamado.")
        descricao = self.entry_descricao.get()
        duracao_str = self.entry_duracao.get()
        duracao = 0

        if duracao_str:
            try:
                duracao_val = int(duracao_str)
                if duracao_val < 0:
                    messagebox.showwarning("Aviso de Validação", "A 'DURAÇÃO' não pode ser negativa. Será considerada como 0.")
                    duracao = 0
                else:
                    duracao = duracao_val
            except ValueError:
                messagebox.showwarning("Aviso de Validação", "A 'DURAÇÃO' informada não é um número válido. Será considerada como 0.")
                duracao = 0
        
        usuario_logado = self.controlador_usuario._usuario_logado()

        data_atual = date.today()

        self.controlador_treino.registrarTreino(
            descricao=descricao,
            duracao=duracao,
            imagem_path=self._imagem_path,
            usuario=usuario_logado,
            data_registro=data_atual,
            view_callback=self
        )

    def sucessoRegistro(self):
        messagebox.showinfo("Treino registrado com sucesso!")
        self.registrarTreino() 

    def erroImagemNaoAnexada(self):
        messagebox.showerror("Você deve anexar uma imagem para registrar o treino.")