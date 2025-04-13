from datetime import date
from typing import Optional


class User:
    """
    Entidade de usuário do sistema.

    O campo `id` é opcional, pois será preenchido apenas após a persistência no banco de dados.
    
    """

    def __init__(
        self,
        cpf: str,
        username: str,
        email: str,
        birthdate: date,
        encrypted_password: str,
        # ID opcional, usado apenas após a inserção no banco (gerado automaticamente)
        id: Optional[int] = None,
    ):
        self._id = id
        # Para atributos com "setters" não acessamos diretamente com o prefixo '_'
        # Acessamos como público, assim o "setter" do atributo é chamado. E consequentemente, suas validcoes também
        self.cpf = cpf
        self.username = username
        self.email = email
        self.birthdate = birthdate
        self.encrypted_password = encrypted_password

    @property
    def id(self) -> int:
        return self._id

    @property
    def cpf(self) -> str:
        return self._cpf

    @cpf.setter
    def cpf(self, value):
        self.validate_cpf(value)
        self._cpf = value

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def birthdate(self) -> date:
        return self._birthdate

    @birthdate.setter
    def birthdate(self, value):
        self.validate_birthdate(value)
        self._birthdate = value

    @property
    def encrypted_password(self) -> str:
        return self._encrypted_password

    @encrypted_password.setter
    def encrypted_password(self, value):
        self._encrypted_password = value

    def validate_cpf(self, cpf: str):
        # Lidar com tipo de dado
        if not isinstance(cpf, str):
            raise TypeError(
                "CPF inválido. parâmetro deve ser do tipo string"
            )
        if not cpf.isdigit() or len(cpf) != 11:
            raise ValueError(
                "CPF inválido. Deve conter os exatos 11 caracteres númericos."
            )

    def validate_birthdate(self, birthdate: date):
        # Lidar com tipo de dado
        if not isinstance(birthdate, date):
            raise TypeError(
                "Data de nascimento inválida. parâmetro deve ser do tipo datetime.date"
            )
        today = date.today()
        age = today.year - birthdate.year
        age = today.year - birthdate.year
        if age == 12 and (today.month, today.day) < (birthdate.month, birthdate.day):
            # Lidando com usuários que fazem aniversário no ano atual
            age -= 1
        if age < 12:
            raise ValueError(
                "Data de nascimento inválida. Usuário deve ter ao menos 12 anos de idade."
            )
