import sqlite3

from connector.QueryType import QueryType


class SQLite:

    def __init__(self, query_type: QueryType, file: str = 'database.db'):
        self.file = file
        self.query_type = query_type
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        return self.conn.cursor()

    def __exit__(self, exit_type, exit_value, exit_traceback):
        if self.conn:
            if self.query_type == QueryType.INSERT:
                self.conn.commit()
            self.conn.close()


def create_database():
    with SQLite(QueryType.INSERT) as cur:
        __crete_tables(cur)


def __crete_tables(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS NOTIFICATION (
            ID TEXT PRIMARY KEY,
            CASE_ID TEXT NOT NULL UNIQUE,
            CASE_TITLE TEXT,
            STATUS TEXT NOT NULL,
            NEXT_NOTIFICATION DATETIME,
            OPRETTET DATETIME NOT NULL,
            OPRETTET_AF TEXT NOT NULL,
            AENDRET DATETIME NOT NULL,
            AENDRET_AF TEXT NOT NULL
        )           
    ''')
