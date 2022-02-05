from enum import Enum, auto


class QueryType(Enum):
    SELECT = auto()
    INSERT = auto()