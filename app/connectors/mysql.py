import mysql.connector
import json

class MySQLConnector():

    def __init__(self, config=None, host=None, user=None, password=None, database=None):

        if not config and not host:
            raise ValueError('Config and host not provided. If config is not provided, then host, user, password and database must be provided')
        
        if config:
            with open(config, 'r') as f:
                connection = json.load(f)
        else:
            connection = {
                'host':host,
                'user':user,
                'password':password,
                'database': database
            }

        self.host = connection['host']
        self.user = connection['user']
        self.password = connection['password']
        self.database = connection['database']
        self.connection = self.connect(return_connection=True)

    # Function to establish a MySQL database connection
    def connect(self, return_connection=False):
        try:
            # Replace these values with your MySQL server details
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                buffered=True
            )
            print("Connected to MySQL database")
            if return_connection:
                return conn
            else:
                self.connection = conn
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
    
    def get_connection(self, conn=None):
        if not conn:
            return self.connection

    def get_all_table_names(self, conn=None):
        conn = self.get_connection(conn=conn)
        query = "SHOW TABLES;"
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            res = cursor.fetchall()
            cursor.reset()
            return [table[0] for table in res]
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def get_table_schema(self, table_name, conn=None):
        conn = self.get_connection(conn=conn)
        query = f"DESCRIBE {table_name}"

        try:
            cursor = conn.cursor()
            cursor.execute(query)
            res = cursor.fetchall()
            cursor.reset()
            cursor.close()

            processed = []
            for column in res:
                _dict = {
                    'column_name': column[0],
                    'column_data_type': column[1].decode()
                }
                processed.append(_dict)
            
            return processed
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def get_schemas(self):
        try:
            table_names = self.get_all_table_names()
            schemas = {}
            for table in table_names:
                schema = self.get_table_schema(table)
                schemas[table] = schema
            return schemas
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    
    def execute_query(self, query, conn=None):
        conn = self.get_connection(conn=conn)
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            res = cursor.fetchall()
            cursor.reset()
            cursor.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        print(res)