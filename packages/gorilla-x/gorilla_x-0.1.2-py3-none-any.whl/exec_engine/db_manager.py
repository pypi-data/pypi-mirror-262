"""
    This module will handle all database interactions
    The DBManager class is the base class for all database managers
"""

class DBManager:
    """Base class for all DB connectors.

    Attributes:
        db_path (type): path to the database file.

    Methods:
        connect: Establish connections to the DB
        execute_sql_call: Execute SQL call
        commit_sql_calls: Commit SQL calls
        rollback_sql_calls: Rollback SQL calls
        close: Close the connection to the database

    """

    def __init__(self, connection_config):
        """Initialize the DBManager.
        
        Args:
            connection_config (dict): Configuration for connecting to the database. This can be a path for file-based databases or connection details for server-based databases.

        """
        self.connection_config = connection_config

    def connect(self):
        """Establish connection to the database."""
        raise NotImplementedError
    
    def format_all_schemas_for_prompt(self, task_description):
        """Format the schemas of all tables into a prompt for GPT, including a task description."""
        raise NotImplementedError

    def execute_sql_call(self, call):
        """Execute SQL call.
        
        Args:
            call (str): SQL call to execute.
        """
        raise NotImplementedError
    
    def fetch_sql_call(self, call):
        raise NotImplementedError
    
    def commit_sql_calls(self):
        """Commit SQL calls."""
        raise NotImplementedError
    
    def rollback_sql_calls(self):
        """Rollback SQL calls not committed"""
        raise NotImplementedError

    def close(self):
        """Close the connection to the database."""
        raise NotImplementedError


class SQLLiteManager(DBManager):
    """SQLite database manager.
    
    Attributes:
        _sqlite_imported (bool): flag to check if sqlite3 is imported.
        
    Methods:
        connect: Establish connections to the DB
        execute_sql_call: Execute SQL call
        commit_sql_calls: Commit SQL calls
        rollback_sql_calls: Rollback SQL calls
        close: Close the connection to the database
    """
    _sqlite_imported = False  # flag to check if sqlite3 is imported
    def __init__(self, connection_config):
        """Initialize the SQLLiteManager.

        Args:
            db_path (str): path to the database file.
        """
        if not SQLLiteManager._sqlite_imported:
            global sqlite3
            import sqlite3
            SQLLiteManager._sqlite_imported = True
        super().__init__(connection_config)

    def connect(self):
        """Establish connection to the SQLLite3 database and create a cursor."""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
    
    def execute_sql_call(self, call):
        try:
            self.cursor.execute(call)
            return 0
        except Exception as e:
            return 1

    
    def fetch_sql_call(self, call):
        self.execute_sql_call(call)
        return self.cursor.fetchall()

    def commit_sql_calls(self):
        """Commit SQL calls."""
        self.conn.commit()

    def rollback_sql_calls(self):
        """Rollback SQL calls not committed"""
        self.conn.rollback()
        self.cursor.close()
        self.conn.close()
        self.connect()

    def close(self):
        self.cursor.close()
        self.conn.close()


class MySQLManager(DBManager):
    """MySQL database manager.
    
    Attributes:
        _mysql_imported (bool): flag to check if mysql.connector is imported.
        
    Methods:
        connect: Establish connections to the DB
        execute_sql_call: Execute SQL call
        commit_sql_calls: Commit SQL calls
        rollback_sql_calls: Rollback SQL calls
        close: Close the connection to the database
    """
    _mysql_imported = False  # flag to check if mysql.connector is imported

    def __init__(self, connection_config):
        """Initialize the MySQLManager.

        Args:
            connection_config (dict): configuration for the database connection, including keys for 'user', 'password', 'host', and 'database'.
        """
        if not MySQLManager._mysql_imported:
            global pymysql
            import pymysql
            MySQLManager._mysql_imported = True
        self.connection_config = connection_config
        super().__init__(connection_config)

    def connect(self):
        """Establish connection to the MySQL database and create a cursor."""
        self.conn = pymysql.connect(**self.connection_config)
        self.cursor = self.conn.cursor()
        self.update_schema_info()

    def update_schema_info(self):
        schema_info = {}
        
        self.cursor.execute("SHOW TABLES")
        tables = self.cursor.fetchall()
        for (table_name,) in tables:
            self.cursor.execute(f"DESCRIBE {table_name}")
            schema_info[table_name] = self.cursor.fetchall()
        
        self.schema = schema_info

    def format_all_schemas_for_prompt(self, task_description):
        """Format the schemas of all tables into a prompt for GPT, including a task description."""
        if not self.schema:
            return "No schema information available."
        
        prompt = "Given the following table schemas in a MySQL database:\n\n"
        for table_name, schema in self.schema.items():
            prompt += f"Table '{table_name}':\n"
            for column in schema:
                column_name, column_type, is_nullable, key, default, extra = column
                prompt += f"- Column '{column_name}' of type '{column_type}'"
                if is_nullable == 'NO':
                    prompt += ", not nullable"
                if key == 'PRI':
                    prompt += ", primary key"
                prompt += "\n"
            prompt += "\n"
        
        prompt += f"Task: {task_description}\n\n"
        prompt += "Based on the task, select the most appropriate table and generate an SQL command to complete the task. In the output, only include SQL code."
        return prompt
    
    def execute_sql_call(self, call):
        """Execute a SQL call using the cursor."""
        if not self.conn:
            self.connect()
        try:
            self.cursor.execute(call)
            self.update_schema_info()
            return 0
        except Exception as e:
            return 1

    def fetch_sql_call(self, call: str) -> list[dict]:
        """Execute a SQL call and return the results.
        
        Args:
            call (str): SQL query to execute.
        
        Returns:
            list[dict]: A list of dictionaries representing each row in the query result.
        """
        if not self.conn:
            self.connect()
        try:
            self.cursor.execute(call)
            ret_val = self.cursor.fetchall()
            self.update_schema_info()
            return ret_val
        except Exception as e:
            return []

    def commit_sql_calls(self):
        """Commit SQL calls."""
        if not self.conn:
            self.connect()
        self.conn.commit()

    def rollback_sql_calls(self):
        """Rollback SQL calls not committed."""
        if not self.conn:
            self.connect()
        self.conn.rollback()

    def close(self):
        """Close the cursor and the connection to the database."""
        if self.conn:
            self.cursor.close()
            self.conn.close()
