import os
import sys
from dataclasses import dataclass, field
import sqlite3
from contextlib import contextmanager
from typing import Optional, List

@dataclass
class Data:
    """
    Represents a data structure for storing user-related information.

    This class is designed to encapsulate basic details about a user, including
    their name, username, password, source of data, and an optional identifier.
    It primarily serves as a container for holding these attributes.

    :ivar name: The full name of the user.
    :type name: str
    :ivar username: The username or unique identifier for the user.
    :type username: str
    :ivar password: The password associated with the user's account.
    :type password: str
    :ivar source: The source from which the data originates.
    :type source: str
    :ivar id: A unique identifier for the user. Defaults to -1 if not provided.
    :type id: int
    """
    name: str = field(default=None)
    username: str = field(default=None)
    password: str = field(default=None)
    source: str = field(default=None)
    id: int = field(default=-1)

class Datas:
    """
    Manages SQLite database interactions, including table creation, data manipulation,
    and retrieval operations.

    The Datas class provides methods for executing various database operations,
    such as adding, updating, deleting, and retrieving records from a SQLite database.
    It can handle user data and ensures the existence of the 'data' table within the database.

    :ivar path_db: The file path to the SQLite database. Defaults to an in-memory database.
    :type path_db: str
    """
    def __init__(self, path_db: str = ":memory:"):
        """Initializes the database and ensures the 'data' table exists."""
        self.path_db = path_db
        self._create_table_if_not_exists()

    @contextmanager
    def _get_connection(self)->sqlite3.Connection:
        """
        Provides a context manager for obtaining a database connection. This method ensures
        that the database connection is properly established and closed, handling any errors
        that may occur during the connection process. It connects to the database using the
        path provided in the `path_db` attribute.

        The context manager is designed to streamline the usage of SQLite connections,
        ensuring their proper cleanup in a reliable manner.

        :yield: A valid SQLite connection object for interacting with the database.
        :rtype: sqlite3.Connection

        :raises sqlite3.Error: If an error occurs while connecting to the database.
        """
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

    def _create_table_if_not_exists(self)->None:
        """
        Creates a table named 'data' if it does not already exist in the database. The table
        includes the following columns: 'id' as the primary key with auto-increment,
        'name', 'username', and 'password' as non-nullable fields, and 'source' as an
        optional field.

        This method ensures the database schema includes the necessary structure
        for storing data.

        :raises sqlite3.Error: If there is an issue during the execution of the SQL
            command or database connection.
        :return: None
        """
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
        """
        Executes a given SQL query with optional parameters, committing
        the transaction if successful and returning the operation status.

        This method interacts with a database connection to execute
        queries, typically used for insert, update, or delete
        operations. It ensures that the transaction is committed
        if the execution is successful, and handles any database
        errors gracefully by returning a failure status.

        :param sql: The SQL query to be executed.
        :param params: A tuple containing the parameters to be substituted
            into the SQL query. Defaults to an empty tuple.
        :return: A boolean indicating whether the query execution was
            successful. Returns True if the operation succeeded, and False
            otherwise.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, params)
                conn.commit()
            return True
        except sqlite3.Error:
            return False

    def fetch_one(self, sql: str, params: tuple = ()) -> Optional[tuple]:
        """
        Fetches a single row from the database by executing the provided SQL query with
        optional parameters. Uses a database connection obtained from the `_get_connection`
        method to execute the query.

        This function ensures safe execution of SQL queries using parameter substitution to
        prevent SQL injection. If an error occurs during query execution, an appropriate
        message is printed to stderr, and the function returns None.

        :param sql: The SQL query to execute.
        :param params: A tuple containing the parameters for the SQL query. Defaults to an
            empty tuple.
        :return: A single row from the result set of the query as a tuple, or None if no
            rows are found or an error occurs.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, params)
                return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"An error occurred while fetching data: {e}", file=sys.stderr)
            return None

    def fetch_all(self, sql: str, params: tuple = ()) -> List[tuple]:
        """
        Executes a SQL query and retrieves all rows from the result set. This
        method establishes a database connection, executes the query using
        the supplied SQL string and parameters, and fetches all resulting
        records as a list of tuples. If an error occurs during execution,
        it logs the error to the standard error and returns an empty list.

        :param sql: The SQL query to be executed.
        :param params: A tuple of parameters to substitute into the query. Optional.
        :return: A list of tuples containing the rows fetched from the query result.
                 Returns an empty list if an error occurs.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, params)
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred while fetching data: {e}", file=sys.stderr)
            return []

    def check_if_user_data_exists(self, data: Data) -> bool:
        """
        Checks if the user data exists in the database by querying for specific
        records with the provided name. This function sends a query to the database
        and evaluates whether the specified user data is present.

        :param data: A `Data` object containing the `name` attribute
                     to search for in the database.
        :return: A boolean indicating whether the user data exists
                 (`True`) or not (`False`).
        """
        sql = '''SELECT 1 FROM data WHERE name = ?'''
        result = self.fetch_one(sql, (data.name,))
        return result is not None

    def register_data(self, data: Data) -> bool:
        """
        Registers the provided user data into the database. The method checks if the user
        data already exists. If it does not exist, the data is inserted into the database.
        If it already exists, the operation is skipped, and the method returns False.

        :param data: The user data object containing the name, username, password,
                     and source details to be registered in the database of type `Data`.
        :return: True if the data is successfully inserted into the database. Returns
                 False if the data already exists.
        """
        if not self.check_if_user_data_exists(data):
            sql = '''INSERT INTO data (name, username, password, source) VALUES (?, ?, ?, ?)'''
            return self.execute_query(sql, (data.name, data.username, data.password, data.source))
        else:
            return False

    def remove_data(self, id_data: int) -> bool:
        """
        Removes a data entry from the database based on the provided ID.

        This function checks if a data entry exists in the database with the given
        ID. If the entry exists, it executes an SQL query to remove it from the
        database. The function returns a boolean value indicating the success of the
        removal operation.

        :param id_data: The ID of the data entry to be removed.
        :type id_data: int
        :return: True if the data entry was successfully removed, otherwise False.
        :rtype: bool
        """
        if self.get_one_data_in_db(id_data):
            sql = '''DELETE FROM data WHERE id = ?'''
            return self.execute_query(sql, (id_data,))
        return False

    def modify_data(self, data_id: int, new_data: Data) -> bool:
        """
        Modifies an existing data entry in the database with the new data provided.

        The method checks if the data entry with the specified ID exists in the database.
        If it exists, the entry is updated with the new data. If it does not exist, the
        method returns False.

        :param data_id: The unique identifier of the data entry to be modified.
        :param new_data: The new data to update the existing data entry. Contains fields
                         such as name, username, password, and source.
        :return: Returns True if the data was successfully updated, and False otherwise.
        """
        if self.get_one_data_in_db(data_id):
            sql = '''UPDATE data SET name = ?, username = ?, password = ?, source = ? WHERE id = ?'''
            return self.execute_query(sql, (new_data.name, new_data.username, new_data.password, new_data.source, data_id))
        return False

    def get_all_Data_in_db(self) -> List[Data]:
        """
        Retrieve all data entries from the database.

        This method executes a SQL query to fetch all rows from the "data" table
        and maps each row to a `Data` object. The resulting list of `Data` objects
        is then returned.

        :raises DatabaseError: If there is an issue with executing the SQL query.

        :return: A list of `Data` objects representing all entries in the database.
        :rtype: List[Data]
        """
        sql = '''SELECT * FROM data'''
        results = self.fetch_all(sql)
        return [Data(id=row[0], name=row[1], username=row[2], password=row[3], source=row[4]) for row in results]

    def get_one_data_in_db(self, data_id: int) -> Optional[Data]:
        """
        Retrieves a single data entry from the database by its unique identifier. This method
        executes an SQL query to fetch the corresponding data entry. If the data with the
        given identifier exists, it returns the data wrapped in a `Data` object; otherwise,
        it returns None.

        :param data_id: Unique identifier of the data entry to be retrieved.
        :type data_id: int
        :return: A `Data` object containing the fetched database entry if it exists, or
            None if no entry is found.
        :rtype: Optional[Data]
        """
        sql = '''SELECT * FROM data WHERE id = ?'''
        row = self.fetch_one(sql, (data_id,))
        if row:
            return Data(id=row[0], name=row[1], username=row[2], password=row[3], source=row[4])
        return None
