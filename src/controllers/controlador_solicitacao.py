from models.usuario import Usuario
from repositories.repositorio_solicitacao import RepositorioSolicitacao
from views.tela_solicitacao import TelaSolicitacao

class ControladorSolicitacao:
    def __init__(self, controlador_sistema):
        self._controlador_sistema = controlador_sistema
        self.repositorio_solicitacao = RepositorioSolicitacao()
        self.tela_solicitacao = TelaSolicitacao()

    def pega_usuario_logado(self) -> Usuario:
        """Busca o usuário logado no sistema."""
        return self._controlador_sistema.buscar_usuario_logado()

    def abrir_tela_solicitacoes(self, callback_voltar):
        """
        Busca as solicitações pendentes e exibe na tela.
        """
        usuario_logado = self.pega_usuario_logado()
        if not usuario_logado:
            self.tela_solicitacao.exibir_mensagem("Erro", "Usuário não logado!")
            callback_voltar()
            return

        solicitacoes_pendentes = self.repositorio_solicitacao.listar_pendentes(usuario_logado.id)
        
        self.tela_solicitacao.exibir_solicitacoes_pendentes(
            lista_solicitacoes=solicitacoes_pendentes,
            callback_aceitar=self.aceitar_solicitacao,
            callback_negar=self.negar_solicitacao,
            callback_voltar=callback_voltar
        )

    def aceitar_solicitacao(self, remetente: Usuario):
        """
        Lógica para aceitar uma solicitação de amizade.
        """
        destinatario = self.pega_usuario_logado()
        if not destinatario:
            self.tela_solicitacao.exibir_mensagem("Erro", "Usuário não logado!")
            return

        sucesso = self.repositorio_solicitacao.atualizar_status(
            remetente_id=remetente.id,
            destinatario_id=destinatario.id,
            novo_status="aceito"
        )
        
        if sucesso:
            self.tela_solicitacao.exibir_mensagem("Sucesso", f"Você e {remetente.nome} agora são amigos!")
        else:
            self.tela_solicitacao.exibir_mensagem("Erro", "Não foi possível aceitar a solicitação.")
        
        # Recarregar a tela
        self.abrir_tela_solicitacoes(self._controlador_sistema.navegar_para_perfil)


    def negar_solicitacao(self, remetente: Usuario):
        """
        Lógica para negar uma solicitação de amizade.
        """
        destinatario = self.pega_usuario_logado()
        if not destinatario:
            self.tela_solicitacao.exibir_mensagem("Erro", "Usuário não logado!")
            return

        # No seu repositório, o status 'negado' atualiza a solicitação.
        # Se quisesse remover, poderia adaptar para um método `deletar`.
        sucesso = self.repositorio_solicitacao.atualizar_status(
            remetente_id=remetente.id,
            destinatario_id=destinatario.id,
            novo_status="negado"
        )

        if sucesso:
            self.tela_solicitacao.exibir_mensagem("Aviso", f"Solicitação de {remetente.nome} negada.")
        else:
            self.tela_solicitacao.exibir_mensagem("Erro", "Não foi possível negar a solicitação.")

        # Recarregar a tela
        self.abrir_tela_solicitacoes(self._controlador_sistema.navegar_para_perfil)