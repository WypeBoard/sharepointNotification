import sqlite3

from connector.QueryType import QueryType


class SQLite:

    def __init__(self, file: str = 'database.db'):
        self.file = file
        self.query_type = None
        self.conn = sqlite3.connect(self.file)

    def __exit__(self, exit_type, exit_value, exit_traceback):
        if self.conn:
            if self.query_type == QueryType.INSERT:
                self.conn.commit()
            self.conn.close()

    def set_query_type(self, query_type: QueryType):
        self.query_type = query_type

    def get_cursor(self):
        return self.conn.cursor()


def create_database():
    with SQLite as conn:
        conn.
        __crete_tables(conn.get_cursor())


def __crete_tables(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS NOTIFICATION (
            ID TEXT PRIMARY KEY,
            CASE_ID TEXT NOT NULL UNIQUE,
            CASE_TITLE TEXT,
            TYPE TEXT NOT NULL,
            STATUS TEXT NOT NULL,
            NEXT_NOTIFICATION DATETIME,
            OPRETTET DATETIME NOT NULL,
            OPRETTET_AF TEXT NOT NULL,
            AENDRET DATETIME NOT NULL,
            AENDRET_AF TEXT NOT NULL
        )           
    ''')

