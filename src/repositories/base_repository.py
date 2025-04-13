from abc import ABC, abstractmethod
import sqlalchemy


class BaseRepository(ABC):
    @abstractmethod
    def __init__(self, connection: sqlalchemy.engine.Connection):
        self._conn = connection
