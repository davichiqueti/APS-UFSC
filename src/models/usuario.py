from datetime import date
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


class Usuario(BaseModel):
    """
    Entidade de usuário do sistema.

    O campo `id` é opcional, pois será preenchido apenas após a persistência no banco de dados.
    """

    cpf: str
    nome: str
    email: EmailStr
    foto: str
    data_nascimento: date
    senha_criptografada: str
    # TODO: Atualizar tipo para o modelo de medalhas
    medalhas: List = Field(default_factory=list)
    amizades: List["Usuario"] = Field(default_factory=list)
    id: Optional[int] = None

    @field_validator("cpf")
    def validar_cpf(cls, cpf: str) -> str:
        if not cpf.isdigit() or len(cpf) != 11:
            raise ValueError("CPF inválido. Deve conter os exatos 11 caracteres numéricos.")
        return cpf

    @field_validator("data_nascimento")
    def validar_data_nascimento(cls, data_nascimento: date) -> date:
        today = date.today()
        age = today.year - data_nascimento.year
        if (today.month, today.day) < (data_nascimento.month, data_nascimento.day):
            age -= 1
        if age < 12:
            raise ValueError("Data de nascimento inválida. Usuário deve ter ao menos 12 anos de idade.")
        return data_nascimento
