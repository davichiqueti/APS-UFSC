from views.tela_busca import TelaBusca
from repositories.repositorio_usuario import RepositorioUsuario
from models.usuario import Usuario
from typing import Callable

class ControladorBusca:
    def __init__(self, controlador_sistema):
        self._controlador_sistema = controlador_sistema
        self._tela_busca = TelaBusca()
        self._repositorio_usuario = RepositorioUsuario()
        self._callback_voltar_principal = None

    def abrir_tela_busca(self, callback_voltar: Callable[[], None]):
        """Abre a tela de busca e define o callback para voltar ao menu principal."""
        self._callback_voltar_principal = callback_voltar
        self._tela_busca.exibir_tela_busca(
            callback_buscar=self.buscar_usuarios,
            callback_abrir_perfil=self.abrir_perfil_usuario,
            callback_voltar=self._callback_voltar_principal
        )

    def buscar_usuarios(self, nome_parcial: str):
        """Busca usuários no repositório e atualiza a tela."""
        if not nome_parcial.strip():
            resultados = []
        else:
            resultados = self._repositorio_usuario.buscar_por_nome_parcial(nome_parcial)
        
        # Filtra o próprio usuário logado dos resultados
        usuario_logado = self._controlador_sistema.buscar_usuario_logado()
        if usuario_logado:
            resultados = [user for user in resultados if user.id != usuario_logado.id]

        self._tela_busca.atualizar_resultados(resultados, self.abrir_perfil_usuario)

    def abrir_perfil_usuario(self, usuario: Usuario):
        """
        Navega para a tela de perfil do usuário selecionado.
        O callback de 'voltar' do perfil será reabrir a tela de busca.
        """
        self._controlador_sistema.controlador_usuario.abrir_tela_perfil(
            usuario=usuario,
            callback_voltar=lambda: self.abrir_tela_busca(self._callback_voltar_principal)
        )