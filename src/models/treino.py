from datetime import date
from .usuario import Usuario

class Treino:
    def __init__(
        self,
        id_treino: int = None,
        descricao: str = None,
        duracao: int = None,
        imagem: str = None,
        usuario: Usuario = None,
        data_treino: date = None,
        curtidas: int = 0
    ):
        # Atributos privados internos
        self._id: int = id_treino
        self._descricao: str = descricao
        self._duracao: int = duracao  # Em minutos
        self._imagem: str = imagem
        self._usuario: Usuario = usuario
        self._data: date = data_treino
        self._curtidas: int = curtidas

    @property
    def id(self) -> int:
        """ID do treino (somente leitura)"""
        return self._id

    @property
    def descricao(self) -> str:
        """Descrição do treino"""
        return self._descricao

    @descricao.setter
    def descricao(self, valor: str) -> None:
        self._descricao = valor

    @property
    def duracao(self) -> int:
        """Duração do treino em minutos"""
        return self._duracao

    @duracao.setter
    def duracao(self, valor: int) -> None:
        self._duracao = valor

    @property
    def imagem(self) -> str:
        """Caminho ou nome da imagem associada ao treino"""
        return self._imagem

    @imagem.setter
    def imagem(self, valor: str) -> None:
        self._imagem = valor

    @property
    def usuario(self) -> Usuario:
        """Usuário que realizou o treino"""
        return self._usuario

    @usuario.setter
    def usuario(self, valor: Usuario) -> None:
        self._usuario = valor

    @property
    def data(self) -> date:
        """Data em que o treino foi realizado"""
        return self._data

    @data.setter
    def data(self, valor: date) -> None:
        self._data = valor

    @property
    def curtidas(self) -> int:
        """Número de curtidas recebidas pelo treino"""
        return self._curtidas

    @curtidas.setter
    def curtidas(self, valor: int) -> None:
        self._curtidas = valor

    def __str__(self) -> str:
        """Representação em string do objeto Treino."""
        nome_usuario = self.usuario.getNome() if self.usuario else 'N/A'
        return (
            f"Treino(ID: {self.id}, Descrição: '{self.descricao}', "
            f"Duração: {self.duracao} mins, Imagem: '{self.imagem}', "
            f"Usuário: {nome_usuario}, Data: {self.data}, Curtidas: {self.curtidas})"
        )
