from models.medalha import Medalha
from repositories.repositorio_medalha import repositoryMedalha
from views.tela_medalha import TelaMedalha
from typing import List

class ControladorMedalha:
    def __init__(self, controlador_sistema):
        self._controlador_sistema = controlador_sistema
        self.tela_medalha = TelaMedalha()
        self._repositorio_medalha = repositoryMedalha()

    def buscarMedalhasConquistadas(self, usuario) -> List[Medalha]:
        return self._repositorio_medalha.obterMedalhasPorUsuario(usuario.id)
        

    def buscarTodasMedalhas(self) -> List[Medalha]:
        """
        Retorna todas as medalhas cadastradas no sistema.
        Usado para o usuário logado ver as medalhas que pode conquistar e as já conquistadas.
        """
        return self._repositorio_medalha.obterTodasMedalhas()