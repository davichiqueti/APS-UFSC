class Medalha:
    def __init__(self, id, categoria, descricao, valor_base, url_photo):
        self._id = id
        self._categoria = categoria
        self._descricao = descricao
        self._valor_base = valor_base
        self._url_photo = url_photo

    @property
    def id(self):
        """ID da medalha (somente leitura)"""
        return self._id

    @property
    def categoria(self):
        """Categoria da medalha"""
        return self._categoria

    @categoria.setter
    def categoria(self, valor):
        self._categoria = valor

    @property
    def descricao(self):
        """Descrição da medalha"""
        return self._descricao

    @descricao.setter
    def descricao(self, valor):
        self._descricao = valor

    @property
    def valor_base(self):
        """Valor base da medalha"""
        return self._valor_base

    @valor_base.setter
    def valor_base(self, valor):
        self._valor_base = valor

    @property
    def url_photo(self):
        """URL da foto da medalha"""
        return self._url_photo

    @url_photo.setter
    def url_photo(self, valor):
        self._url_photo = valor