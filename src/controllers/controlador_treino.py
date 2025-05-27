from datetime import date
from models.treino import Treino
from repositories.repositorio_treino import RepositorioTreino
from views.tela_treino import TelaTreino
from models.usuario import Usuario
from typing import List

class ControladorTreino:
    def __init__(self, controlador_sistema):
        self.ctrl_sistema = controlador_sistema
        self.repositorio = RepositorioTreino()
        self.tela_treino = TelaTreino()

    def abrir_tela_registro(self):
        self.tela_treino.exibir_tela_registro(
            callback_registrar=self.registrar_treino
        )
    
    def pega_usuario_logado(self):
        self.ctrl_sistema.buscar_usuario_logado()

    def registrar_treino(self, descricao: str, duracao_str: str, imagem_path: str) -> None:
        if not imagem_path:
            raise ValueError("Você deve anexar uma imagem para registrar o treino.")
        # Obtém usuário
        usuario = self.pega_usuario_logado()
        # Conversão de duração
        try:
            duracao = int(duracao_str) if duracao_str else 0
        except:
            duracao = 0
        # Cria e persiste
        treino = Treino(
            descricao=descricao,
            duracao=duracao,
            imagem=imagem_path,
            usuario=usuario,
            data_treino=date.today(),
            curtidas=0
        )
        novo_id = self.repositorio.criar(treino)
        treino.id = novo_id

    
    def obter_treinos_do_usuario(self, usuario: Usuario) -> list[Treino]:
        """
        Obtém todos os treinos de um usuário específico.
        """
        if not usuario or not hasattr(usuario, 'id') or usuario.id is None:
            print(f"WARN [ControladorTreino]: Tentativa de buscar treinos para usuário inválido: {usuario}")
            return []
        # print(f"DEBUG [ControladorTreino]: Buscando treinos para usuário ID: {usuario.id} ({usuario.nome if hasattr(usuario, 'nome') else 'Nome não disponível'})")
        return self.repositorio.buscar_por_usuario_id(usuario.id)
    

    def buscar_treinos_amizades(self, usuario: Usuario):

        self.repositorio.
        return List[Treino]