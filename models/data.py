import os
import sys
from dataclasses import dataclass, field
import sqlite3
from contextlib import contextmanager
from typing import Optional, List

@dataclass
class Data:
    """Represents a data structure for storing user-related information."""
    name: str = field(default=None)
    username: str = field(default=None)
    password: str = field(default=None)
    source: str = field(default=None)
    id: int = field(default=-1)

class Datas:
    """Handles interactions with a SQLite database to manage user data."""
    def __init__(self, path_db: str = ":memory:"):
        """Initializes the database and ensures the 'data' table exists."""
        self.path_db = path_db
        self._create_table_if_not_exists()

    @contextmanager
    def _get_connection(self):
        """Establishes and returns a connection to the SQLite database."""
        conn = None
        try:
            conn = sqlite3.connect(self.path_db)
            yield conn
        except sqlite3.Error as e:
            print(f"An error occurred while connecting to the database: {e}", file=sys.stderr)
            raise
        finally:
            if conn:
                conn.close()

    def _create_table_if_not_exists(self):
        """Creates the 'data' table if it does not exist."""
        sql = '''CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            source TEXT
        )'''
        try:
            with self._get_connection() as db:
                db.execute(sql)
        except sqlite3.Error as e:
            raise sqlite3.Error(f"An error occurred while creating the database: {e}")

    def execute_query(self, sql: str, params: tuple = ()) -> bool:
        """Executes a SQL query with the given parameters."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, params)
                conn.commit()
            return True
        except sqlite3.Error:
            return False

    def fetch_one(self, sql: str, params: tuple = ()) -> Optional[tuple]:
        """Fetches a single row from the database."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, params)
                return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"An error occurred while fetching data: {e}", file=sys.stderr)
            return None

    def fetch_all(self, sql: str, params: tuple = ()) -> List[tuple]:
        """Fetches all rows from the database."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, params)
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred while fetching data: {e}", file=sys.stderr)
            return []

    def check_if_user_data_exists(self, data: Data) -> bool:
        """Checks if a user data record exists in the database."""
        sql = '''SELECT 1 FROM data WHERE name = ?'''
        result = self.fetch_one(sql, (data.name,))
        return result is not None

    def register_data(self, data: Data) -> bool:
        """Registers a user's data into the database if it does not already exist."""
        if not self.check_if_user_data_exists(data):
            sql = '''INSERT INTO data (name, username, password, source) VALUES (?, ?, ?, ?)'''
            return self.execute_query(sql, (data.name, data.username, data.password, data.source))
        else:
            return False

    def remove_data(self, id_data: int) -> bool:
        """Removes a data entry from the database given its unique identifier."""
        if self.get_one_data_in_db(id_data):
            sql = '''DELETE FROM data WHERE id = ?'''
            return self.execute_query(sql, (id_data,))
        return False

    def modify_data(self, data_id: int, new_data: Data) -> bool:
        """Modifies an existing data record in the database."""
        if self.get_one_data_in_db(data_id):
            sql = '''UPDATE data SET name = ?, username = ?, password = ?, source = ? WHERE id = ?'''
            return self.execute_query(sql, (new_data.name, new_data.username, new_data.password, new_data.source, data_id))
        return False

    def get_all_Data_in_db(self) -> List[Data]:
        """Fetches and returns all records from the `data` table in the database."""
        sql = '''SELECT * FROM data'''
        results = self.fetch_all(sql)
        return [Data(id=row[0], name=row[1], username=row[2], password=row[3], source=row[4]) for row in results]

    def get_one_data_in_db(self, data_id: int) -> Optional[Data]:
        """Retrieves a single entry from the database using its unique identifier."""
        sql = '''SELECT * FROM data WHERE id = ?'''
        row = self.fetch_one(sql, (data_id,))
        if row:
            return Data(id=row[0], name=row[1], username=row[2], password=row[3], source=row[4])
        return None
