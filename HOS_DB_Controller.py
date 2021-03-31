
import pyodbc

class HOS_DB_Coontroller:

    def __init__(self):
        self.cnxn = pyodbc.connect('DSN=HOS_DB;UID=itko_lisa;PWD=S8Jxj3LY')
        self.db = self.cnxn.cursor()

    def close_connection(self, db):
        self.db.close()
        self.cnxn.close()

    def execute_parametrized_query(self, query, *params):
        self.db.execute(query, *params)
        for (BINARY_PAYLOAD) in self.db:
            response = BINARY_PAYLOAD

        self.close_connection(self.db)

        return response

