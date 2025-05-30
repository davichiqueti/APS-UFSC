from abc import ABC, abstractmethod
import sqlalchemy
from database import connection_factory


class RepositorioBase(ABC):
    @abstractmethod
    def __init__(self, connection: sqlalchemy.engine.Connection | None = None):
        if connection is None:
            connection = connection_factory.db_connection   # Usa a conexão padrão caso não especificada
        self._conn = connection
