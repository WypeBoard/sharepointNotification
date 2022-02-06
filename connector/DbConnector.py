from typing import List, Tuple

from connector.QueryType import QueryType
from connector.SQLite import SQLite


def persist_entity(query: str, params: Tuple):
    with SQLite(query_type=QueryType.INSERT) as cur:
        cur.execute(query, params)


def fetch_unique_entity(query: str, params: Tuple) -> tuple:
    fetched_data = fetch_entities(query, params)
    if len(fetched_data) > 1:
        raise Exception  # TODO specific exception
    if not fetched_data:
        return ()
    return fetched_data[0]


def fetch_entities(query: str, params: Tuple) -> List[tuple]:
    with SQLite(query_type=QueryType.SELECT) as cur:
        entities = cur.execute(query, params).fetchall()
    return entities
