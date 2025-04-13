import pytest
from database.connection_factory import db_engine


@pytest.fixture
def db_transaction():
    connection = db_engine.connect()  # Cria uma conexão exclusiva para o teste
    transaction = connection.begin()  # Inicia uma transação
    yield connection  # Fornece a conexão para o teste
    transaction.rollback()  # Reverte a transação após o teste
    connection.close()  # Fecha a conexão
