from connector.QueryType import QueryType
from connector.SQLite import SQLite
from abc import ABC


class Repository(ABC):

    def __int__(self, query_type: QueryType):
        self.cur = SQLite(query_type)
        self.complete = False

    def complete(self):
        self.complete = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__close()

    def __close(self):
