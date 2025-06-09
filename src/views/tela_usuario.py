import tkinter as tk
from tkinter import messagebox
from typing import Callable
from datetime import datetime
import requests
from PIL import Image, ImageTk
import io
from repositories.repositorio_usuario import RepositorioUsuario
from PIL import ImageDraw

class TelaUsuario():
    def __init__(self):
        pass

    def exibir_tela_cadastro(self, callback_cadastro: Callable, callback_abrir_login: Callable):
        root = tk.Tk()
        root.title("Cadastrar Conta")
        root.geometry("400x550")

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
                return  
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

        def acao_ir_para_login():
            root.destroy()  
            callback_abrir_login() 

        tk.Button(root, text="Já tem uma conta? Entre aqui!", command=acao_ir_para_login).pack(pady=10) 



    def exibir_tela_login(self, callback_login: Callable, callback_abrir_cadastro: Callable, callback_sucesso_proxima_etapa: Callable):

        root = tk.Tk()
        root.title("Login de Usuário")
        root.geometry("350x300")

        tk.Label(root, text="LOGIN", font=("Arial", 20, "bold")).pack(pady=20) 

        tk.Label(root, text="Nome de Usuário:").pack(anchor="w", padx=40)
        nome_usuario_entry = tk.Entry(root, width=30) 
        nome_usuario_entry.pack(pady=5, padx=40, fill="x")

        tk.Label(root, text="Senha:").pack(anchor="w", padx=40)  
        senha_entry = tk.Entry(root, show="*", width=30)  
        senha_entry.pack(pady=5, padx=40, fill="x")

        def acao_tentar_login():
            nome_usuario = nome_usuario_entry.get()
            senha = senha_entry.get()
            try:
                callback_login(nome_usuario, senha)
                messagebox.showinfo("Login", "Login realizado com sucesso!", parent=root) 
                root.destroy()  
                callback_sucesso_proxima_etapa()
            except ValueError as e: 
                messagebox.showerror("Erro de Login", str(e), parent=root)
            except Exception as e: 
                messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}", parent=root) 


        login_button = tk.Button(root, text="Login", command=acao_tentar_login, width=15) 
        login_button.pack(pady=20)

        def acao_ir_para_cadastro():
            root.destroy()  
            callback_abrir_cadastro() 

        cadastro_button = tk.Button(root, text="Não tem uma conta? Cadastre-se", command=acao_ir_para_cadastro) 
        cadastro_button.pack(pady=5)

        root.mainloop()


    def exibir_tela_perfil(self, usuario, callback_voltar, usuario_logado=None, controlador_usuario=None):
        root = tk.Toplevel()
        root.title("Perfil do Usuário")
        root.geometry("500x600")
        # ... resto do código ...
    
        card_frame = tk.Frame(root, bg="#444444")
        card_frame.pack(pady=20)
    
        def comando_editar_perfil():
            pass  # Implemente se necessário
    
        def comando_amizades():
            if controlador_usuario:
                root.destroy()
                controlador_usuario.solicitarVisualizarAmizades(usuario, callback_voltar)
    
        def comando_medalhas():
            if controlador_usuario:
                root.destroy()
                controlador_usuario.solicitarVisualizarMedalhas(usuario, callback_voltar)
    
        # Só mostra "Editar Perfil" se for o usuário logado
        botoes = []
        if usuario_logado and str(usuario_logado.cpf) == str(usuario.cpf):
            botoes.append(("Editar Perfil", comando_editar_perfil))
        botoes.append(("Medalhas", comando_medalhas))
        botoes.append(("Amizades", comando_amizades))
        botoes.append(("Ranking", None))
        botoes.append(("Meus Treinos", None))
    
        for i, (texto, comando) in enumerate(botoes):
            btn = tk.Button(
                card_frame, text=texto, width=22, height=2,
                bg="#333333", fg="#f0f0f0", font=("Arial", 11, "bold"),
                relief="groove", bd=1, cursor="hand2", activebackground="#555555", activeforeground="#f0f0f0",
                command=comando if comando else lambda: None
            )
            btn.grid(row=i // 2, column=i % 2, padx=10, pady=8, sticky="ew")