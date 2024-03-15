import psycopg2
from psycopg2.extras import execute_batch

class DatabaseFunctions:

    def __init__(self, dbname: str, host: str, port: str, user: str, password: str):
        self.dbname = dbname
        self.host = host
        self.port = port
        self.user = user
        self.password = password

        self._conn = self._open_connection()
        self._cursor = self._conn.cursor()
    
    def _open_connection(self):
        return psycopg2.connect(
                            dbname = self.dbname,
                            host = self.host,
                            port = self.port,
                            user = self.user,
                            password = self.password
                            )

    def data_query(self, statement: str):
        try:
            self._cursor.execute(statement)
            return self._cursor
        except Exception as e:
            raise Exception(e)
    
    def data_manipulation(self, statement: str):
        try:
            self._cursor.execute(statement)
            self._conn.commit()
        except Exception as e:
            self._conn.rollback()
            raise Exception(e)
    
    def data_manipulation_with_return(self, statement: str):
        try:
            self._cursor.execute(statement)
            self._conn.commit()
            return self._cursor
        except Exception as e:
            self._conn.rollback()
            raise Exception(e)
    
    def data_manipulation_in_batches(self, statement: str, values: list):
        try:
            execute_batch(self._cursor, statement, values)
            self._conn.commit()
        except Exception as e:
            self._conn.rollback()
            raise Exception(e)
    
    def close_conn(self):
        self._conn.close()


