from datetime import date
from models.treino import Treino
from repositories.repositorio_treino import RepositorioTreino
from views.tela_treino import TelaTreino

class ControladorTreino:
    def __init__(self, controlador_sistema, controlador_usuario):
        self.ctrl_sistema = controlador_sistema
        self.ctrl_usuario = controlador_usuario
        self.repositorio = RepositorioTreino()
        self.tela_treino = TelaTreino()

    def abrir_tela_registro(self):
        self.tela_treino.exibir_tela_registro(
            callback_registrar=self.registrar_treino
        )

    def registrar_treino(self, descricao: str, duracao_str: str, imagem_path: str) -> None:
        if not imagem_path:
            raise ValueError("Você deve anexar uma imagem para registrar o treino.")
        # Obtém usuário
        usuario = self.ctrl_usuario.usuario_logado
        # Conversão de duração
        duracao = int(duracao_str) if duracao_str else 0

        # Cria e persiste
        treino = Treino(
            id_treino=None,
            descricao=descricao,
            duracao=duracao,
            imagem=imagem_path,
            usuario=usuario,
            data_treino=date.today(),
            curtidas=0
        )
        novo_id = self.repositorio.criar(treino)
        treino.id = novo_id