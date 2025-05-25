import tkinter as tk
from tkinter import messagebox
from typing import Callable
from datetime import datetime


class TelaUsuario():
    def __init__(self):
        pass

    def exibir_tela_cadastro(self, callback_cadastro: Callable):
        root = tk.Tk()
        root.title("Cadastrar Conta")
        root.geometry("400x500")

        tk.Label(root, text="CADASTRO", font=("Arial", 20, "bold")).pack(pady=10)

        tk.Label(root, text="Nome de Usuário:").pack(anchor="w", padx=20)
        nome_entry = tk.Entry(root)
        nome_entry.pack(pady=5, padx=20, fill="x")

        tk.Label(root, text="Email:").pack(anchor="w", padx=20)
        email_entry = tk.Entry(root)
        email_entry.pack(pady=5, padx=20, fill="x")

        tk.Label(root, text="CPF (Apenas números):").pack(anchor="w", padx=20)
        cpf_entry = tk.Entry(root)
        cpf_entry.pack(pady=5, padx=20, fill="x")

        tk.Label(root, text="Foto de perfil (URL):").pack(anchor="w", padx=20)
        foto_entry = tk.Entry(root)
        foto_entry.pack(pady=5, padx=20, fill="x")

        def abrir_calendario():
            def selecionar_data():
                data_selecionada = calendario.get_date()
                data_nascimento_entry.delete(0, "end")
                data_nascimento_entry.insert(0, data_selecionada)
                calendario_window.destroy()

            calendario_window = tk.Toplevel(root)
            calendario_window.title("Selecionar Data")
            from tkcalendar import Calendar
            calendario = Calendar(calendario_window, date_pattern="dd/mm/yyyy")
            calendario.pack(pady=10)
            tk.Button(calendario_window, text="Selecionar", command=selecionar_data).pack(pady=10)

        tk.Label(root, text="Data de Nascimento (Formato 01/12/2000):").pack(anchor="w", padx=20)
        data_nascimento_entry = tk.Entry(root)
        data_nascimento_entry.pack(pady=5, padx=20, fill="x")
        tk.Button(root, text="Selecionar por Calendário", command=abrir_calendario).pack(pady=5)

        tk.Label(root, text="Senha:").pack(anchor="w", padx=20)
        senha_entry = tk.Entry(root, show="*")
        senha_entry.pack(pady=5, padx=20, fill="x")

        tk.Label(root, text="Confirmar Senha:").pack(anchor="w", padx=20)
        confirmar_senha_entry = tk.Entry(root, show="*")
        confirmar_senha_entry.pack(pady=5, padx=20, fill="x")

        def cadastrar_usuario():
            if senha_entry.get() != confirmar_senha_entry.get():
                messagebox.showerror("Erro", "As senhas não coincidem!")
                return  # Apenas retorna, sem recriar a tela
            try:
                data_nascimento = datetime.strptime(data_nascimento_entry.get(), "%d/%m/%Y").date()
                callback_cadastro(
                    cpf=cpf_entry.get(),
                    nome=nome_entry.get(),
                    email=email_entry.get(),
                    foto=foto_entry.get(),
                    data_nascimento=data_nascimento,
                    senha=senha_entry.get()
                )
                root.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro no cadastro: {e}")

        tk.Button(
            root,
            text="Cadastrar",
            command=cadastrar_usuario
        ).pack(pady=10)


# Ensure you have 'import tkinter as tk', 'from tkinter import messagebox',
# and 'from typing import Callable' at the top of your tela_usuario.py file.

    def exibir_tela_login(self, callback_login: Callable, callback_abrir_cadastro: Callable):
        """
        Cria e exibe a janela de login.

        Args:
            callback_login: Função a ser chamada ao tentar fazer login.
            callback_abrir_cadastro: Função a ser chamada para navegar para a tela de cadastro.
        """
        root = tk.Tk()  # Changed from root_login
        root.title("Login de Usuário")  # Changed from root_login
        root.geometry("350x300") # Largura x Altura

        tk.Label(root, text="LOGIN", font=("Arial", 20, "bold")).pack(pady=20)  # Changed from root_login

        tk.Label(root, text="Nome de Usuário:").pack(anchor="w", padx=40)  # Changed from root_login
        nome_usuario_entry = tk.Entry(root, width=30)  # Changed from root_login
        nome_usuario_entry.pack(pady=5, padx=40, fill="x")

        tk.Label(root, text="Senha:").pack(anchor="w", padx=40)  # Changed from root_login
        senha_entry = tk.Entry(root, show="*", width=30)  # Changed from root_login
        senha_entry.pack(pady=5, padx=40, fill="x")

        def acao_tentar_login():
            nome_usuario = nome_usuario_entry.get()
            senha = senha_entry.get()
            try:
                callback_login(nome_usuario, senha)
                messagebox.showinfo("Login", "Login realizado com sucesso!", parent=root)  # Changed from root_login
                root.destroy()  # Changed from root_login
            except ValueError as e: # Captura exceções levantadas pelo controlador
                messagebox.showerror("Erro de Login", str(e), parent=root)  # Changed from root_login
            except Exception as e: # Captura outras exceções inesperadas
                messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}", parent=root)  # Changed from root_login


        login_button = tk.Button(root, text="Login", command=acao_tentar_login, width=15)  # Changed from root_login
        login_button.pack(pady=20)

        def acao_ir_para_cadastro():
            root.destroy()  # Fecha a janela de login # Changed from root_login
            callback_abrir_cadastro() # Chama o callback para abrir a tela de cadastro

        cadastro_button = tk.Button(root, text="Não tem uma conta? Cadastre-se", command=acao_ir_para_cadastro)  # Changed from root_login
        cadastro_button.pack(pady=5)


        

        # TODO: Criar botão que muda para tela de login
        #tk.Button(root, text="Já tem uma conta? Faça login", command=...).pack()
        root.mainloop()
