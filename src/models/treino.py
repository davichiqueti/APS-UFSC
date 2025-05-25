from datetime import date
from .usuario import Usuario

class Treino:
    def __init__(self, id_treino: int = None, descricao: str = None, duracao: int = None,
                 imagem: str = None, usuario: Usuario = None, data_treino: date = None,
                 curtidas: int = 0):
        # Atributos conforme o diagrama [cite: 1]
        self.id: int = id_treino
        self.descricao: str = descricao
        self.duracao: int = duracao # Em minutos, por exemplo
        self.imagem: str = imagem
        self.usuario: Usuario = usuario
        self.data: date = data_treino
        self.curtidas: int = curtidas

    # --- Getters ---
    def getCurtidas(self) -> int: # [cite: 1]
        return self.curtidas

    def getData(self) -> date: # [cite: 1]
        return self.data

    def getDescricao(self) -> str: # [cite: 1]
        return self.descricao

    def getDuracao(self) -> int: # [cite: 1]
        return self.duracao

    def getImagem(self) -> str: # Nome corrigido de getimagem para getImagem [cite: 1]
        return self.imagem

    def getUsuario(self) -> Usuario: # [cite: 1]
        return self.usuario

    # --- Setters ---
    def setCurtidas(self, curtidas: int) -> None: # [cite: 1]
        self.curtidas = curtidas

    def setData(self, data_treino: date) -> None: # [cite: 1]
        self.data = data_treino

    def setDescricao(self, descricao: str) -> None: # [cite: 1]
        self.descricao = descricao

    def setDuracao(self, duracao: int) -> None: # [cite: 1]
        self.duracao = duracao

    def setImagem(self, imagem: str) -> None: # Nome corrigido de setimagem para setImagem [cite: 2]
        self.imagem = imagem

    def setUsuario(self, usuario: Usuario) -> None: # [cite: 2]
        self.usuario = usuario

    def __str__(self) -> str:
        """ Retorna uma representação em string do objeto Treino. """
        return (
            f"Treino(ID: {self.id}, Descrição: '{self.descricao}', Duração: {self.duracao} mins, "
            f"Imagem: '{self.imagem}', Usuário: {self.usuario.getNome() if self.usuario else 'N/A'}, "
            f"Data: {self.data}, Curtidas: {self.curtidas})"
        )