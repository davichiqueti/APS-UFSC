from datetime import date
from typing import List, Optional


class Usuario():
    """
    Entidade de usuário do sistema.
    """
    def __init__(
        self,
        cpf: str,
        nome: str,
        email: str,
        foto: str,
        data_nascimento: date,
        senha_criptografada: str,
        # TODO: Atualizar tipo para o modelo de medalhas
        medalhas: List = [],
        amizades: List["Usuario"] = [],
        id: Optional[int] = None
    ):
        self._id = id
        # Para atributos com "setters" não acessamos diretamente com o prefixo '_'
        # Acessamos como público, assim o "setter" do atributo é chamado. E consequentemente, suas validcoes também
        self.cpf = cpf
        self.nome = nome
        self.email = email
        self.foto = foto
        self.data_nascimento = data_nascimento
        self.senha_criptografada = senha_criptografada
        self.medalhas = medalhas
        self.amizades = amizades

    @property
    def id(self) -> int:
        return self._id

    @property
    def cpf(self) -> str:
        return self._cpf

    @cpf.setter
    def cpf(self, value):
        self.validar_cpf(value)
        self._cpf = value

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def data_nascimento(self) -> date:
        return self._data_nascimento

    @data_nascimento.setter
    def data_nascimento(self, value):
        self.validar_data_nascimento(value)
        self._data_nascimento = value

    @property
    def senha_criptografada(self) -> str:
        return self._senha_criptografada

    @senha_criptografada.setter
    def senha_criptografada(self, value):
        self._senha_criptografada = value

    def validar_cpf(self, cpf: str):
        # Lidar com tipo de dado
        if not isinstance(cpf, str):
            raise TypeError(
                "CPF inválido. parâmetro deve ser do tipo string"
            )
        if not cpf.isdigit() or len(cpf) != 11:
            raise ValueError(
                "CPF inválido. Deve conter os exatos 11 caracteres númericos."
            )

    def validar_data_nascimento(self, data_nascimento: date):
        # Lidar com tipo de dado
        if not isinstance(data_nascimento, date):
            raise TypeError(
                "Data de nascimento inválida. parâmetro deve ser do tipo datetime.date"
            )
        today = date.today()
        age = today.year - data_nascimento.year
        age = today.year - data_nascimento.year
        if age == 12 and (today.month, today.day) < (data_nascimento.month, data_nascimento.day):
            # Lidando com usuários que fazem aniversário no ano atual
            age -= 1
        if age < 12:
            raise ValueError(
                "Data de nascimento inválida. Usuário deve ter ao menos 12 anos de idade."
            )
