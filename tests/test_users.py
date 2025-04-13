import pytest
from controllers.user_controller import UserController
from repositories.user_repository import UserRepository
from database.connection_factory import db_connection
from datetime import date


user_repository = UserRepository(db_connection)
user_controller = UserController(user_repository)
# Valores padrões para teste
test_username = 'test'
test_cpf = '12345678910'
test_email = 'test@email'
test_birthdate = date(year=2000, month=1, day=1)
test_password = 'Senhaforte123@'
actual_date = date.today()


def test_create_user():
    user_controller.create_user(
        cpf=test_cpf,
        username=test_username,
        email=test_email,
        birthdate=test_birthdate,
        password=test_password
    )
    user = user_controller.get_user_by_username(test_username)
    assert user.username == test_username


def test_create_user_cpf_validation():
    # Testando cpf não numerico
    with pytest.raises(expected_exception=ValueError, match='CPF inválido*'):
        user_controller.create_user(
            cpf='abcdefghijk',
            username=test_username,
            email=test_email,
            birthdate=test_birthdate,
            password=test_password
        )
    # Testando cpf com número de caracteres errados
    with pytest.raises(expected_exception=ValueError, match='CPF inválido*'):
        user_controller.create_user(
            cpf='1',
            username=test_username,
            email=test_email,
            birthdate=test_birthdate,
            password=test_password
        )

def test_create_user_age_validation():
    test_username = 'test'
    test_cpf = '12345678910'
    test_email = 'test@email'
    # Testando idade menor que 12 anos
    with pytest.raises(expected_exception=ValueError, match='Data de nascimento inválida*'):
            user_controller.create_user(
                cpf=test_cpf,
                username=test_username,
                email=test_email,
                password=test_password,
                birthdate=actual_date
        )
    # Teste de pessoa com 12 anos incompletos, com aniversário a acontecer este ano
    with pytest.raises(expected_exception=ValueError, match='Data de nascimento inválida*'):
        user_controller.create_user(
            cpf=test_cpf,
            username=test_username,
            email=test_email,
            password=test_password,
            birthdate=date(year=actual_date.year - 12, month=actual_date.month + 1, day=actual_date.day)
        )
    # Teste de pessoa com 12 anos completos, com aniversário que já ocorreu este ano
    user_controller.create_user(
        cpf=test_cpf,
        username=test_username,
        email=test_email,
        password=test_password,
        birthdate=date(year=actual_date.year - 12, month=actual_date.month - 1, day=actual_date.day)
    )
    user = user_controller.get_user_by_username(test_username)
    assert user.username == test_username
    # Teste para pessoa com 12 anos completos, que aniversário ocorreu hoje
    user_controller.create_user(
        cpf=test_cpf,
        username=test_username,
        email=test_email,
        password=test_password,
        birthdate=date(year=actual_date.year - 12, month=actual_date.month, day=actual_date.day)
    )
    user = user_controller.get_user_by_username(test_username)
    assert user.username == test_username
