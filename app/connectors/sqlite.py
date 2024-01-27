import sqlite3
import json

class SQLiteDBConnector():

    def __init__(self, db_path):
        """
        Initializes the connector

        Parameters:
        db_path : path to local SQLite3 database file
        """
        self.db_path = db_path

    def get_table_names(self):
        """
        Gets the names of all tables in the database using the query:
        SELECT name FROM sqlite_master WHERE type='table';

        Returns:
        table_names : a list of strings containing the names of all tables in the database
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Execute a query to retrieve a list of all tables.
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

        table_names = cursor.fetchall()

        cursor.close()
        conn.close()

        return table_names
    
    def process_schema(self, schema):
        """
        Converts the schema for a given table into a parseable string to be passed on to the LLM
        """
        columns = []
        for i, column in enumerate(schema):
            columns.append({'column_number': i, 'column_name': column[1], 'data_type': column[2]})
        return columns

    def get_schemas(self, table_names=None, output=None):
        """
        Gets the schemas of all tables in the databases or in the `table_names` parameter

        Parameters:
        `table_names` : names of tables to get schemas for. If None, then all tables will be searched
        `output` : output path to save schemas JSON to

        Returns:
        table_dict : a dictionary containing the schemas for each table
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if not table_names:
            table_names = self.get_table_names()
        table_dict = {}

        for table in table_names:
            query = f"pragma table_info({table[0]});"
            cursor.execute(query)
            table_dict[table[0]] = self.process_schema(cursor.fetchall())
        cursor.close()
        conn.close()
        
        if output:
            print(f'Writing to {output}')
            with open(output, 'w') as f:
                json.dump(table_dict, f, indent=1)
        else:
            return table_dict

    def execute_query(self, query: str):
        """
        Execute a query on an SQLite database.

        Parameters:
        - database_path (str): The path to the SQLite database file.
        - query (str): The SQL query to execute.

        Returns:
        - result: The result of the query execution (may vary based on the query type).
        """
        # Connect to the database
        database_path = self.db_path
        connection = sqlite3.connect(database_path)

        try:
            # Create a cursor object to execute queries
            cursor = connection.cursor()

            # Execute the query
            cursor.execute(query)

            # Commit the changes to the database (for write operations)
            connection.commit()

            # Fetch the result (for read operations)
            result = cursor.fetchall()

            return result

        finally:
            # Close the connection
            connection.close()

    