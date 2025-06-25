from typing import Optional
from .usuario import Usuario


class Solicitacao:
    def __init__(
        self,
        destinatario: Usuario,
        remetente: Usuario,
        status: Optional[str] = "pendente",
    ):
        self.destinatario = destinatario
        self.remetente = remetente
        self.status = status

    @property
    def destinatario(self) -> Usuario:
        return self._destinatario

    @destinatario.setter
    def destinatario(self, value: Usuario):
        if not isinstance(value, Usuario):
            raise TypeError("Destinatário deve ser uma instância da classe Usuario.")
        self._destinatario = value

    @property
    def remetente(self) -> Usuario:
        return self._remetente

    @remetente.setter
    def remetente(self, value: Usuario):
        if not isinstance(value, Usuario):
            raise TypeError("Remetente deve ser uma instância da classe Usuario.")
        self._remetente = value

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        if value not in ["pendente", "aceito", "negado", "excluido"]:
            raise ValueError("Status deve ser 'pendente', 'aceito', 'negado' ou 'excluido'.")
        self._status = value