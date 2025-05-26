from datetime import date
from ..repositories.repositorio_treino import RepositorioTreino
from ..models.usuario import Usuario
from ..views.tela_treino import ViewTreino

class ControladorTreino:
    def __init__(self):
        self.repositorio_treino = RepositorioTreino()

    def validaSeImagemFoiAnexada(self, imagem_path: str) -> bool:
        return bool(imagem_path)

    def registrarTreino(self, descricao: str, duracao: int, imagem_path: str,
                        usuario: Usuario, data_registro: date, view_callback: ViewTreino) -> None: # Usando string para forward reference
        imagem_anexada_e_valida = self.validaImagemFoiAnexada(imagem_path)
        if not imagem_anexada_e_valida:
            if hasattr(view_callback, 'erroImagemNaoAnexada'):
                view_callback.erroImagemNaoAnexada()
            return