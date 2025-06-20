"""
Auteur : Adrien Mertens
Version : 1.0
"""

import sys
from dataclasses import dataclass, field
import sqlite3
from contextlib import closing
from typing import Optional, List
import ttkbootstrap.dialogs as dialogs

@dataclass
class Data:
    """
    Represents a structured data object to hold user information.

    This class is a model for representing user data, including attributes such as
    name, username, password, data source, and a unique identifier. It is designed
    to be used in managing and organizing user-related information, providing
    fields for storing essential details about a user.

    :ivar name: The name of the user.
    :type name: str
    :ivar username: The username of the user.
    :type username: str
    :ivar password: The user's password.
    :type password: str
    :ivar source: The data source of the user's information.
    :type source: str
    :ivar id: The unique identifier for the user. Defaults to -1 if not provided.
    :type id: int
    """
    name: str  # Le nom de l'utilisateur
    username: str  # Le nom d'utilisateur
    password: str  # Le mot de passe de l'utilisateur
    source: str  # La source des données de l'utilisateur
    id: int = field(default=-1)  # L'identifiant unique de l'utilisateur, par défaut -1

class Datas:
    """
    Handles interactions with a SQLite database to manage user data.

    This class provides methods for connecting to the database, executing
    queries, retrieving data, and managing CRUD operations for user records.

    :ivar path_db: The file path to the SQLite database.
    :type path_db: str
    """

    def __init__(self, path_db: str = "../db_gestionnaire_password.db")->None:
        """
        Initializes the class with a specific database path.

        :param path_db: The path of the database file to be used.
        :type path_db: str
        """
        self.path_db = path_db

    def _get_connection(self)->sqlite3.Connection:
        """
        Establishes and returns a connection to the SQLite database specified
        by the attribute `self.path_db`. If the connection fails due to an
        SQLite error, an error message is displayed, logged to stderr, and the
        error is re-raised.

        :raises sqlite3.Error: Raised when there is an error occurring during
            the database connection process.
        :return: SQLite connection object.
        :rtype: sqlite3.Connection
        """
        try:
            return sqlite3.connect(self.path_db)
        except sqlite3.Error as e:
            dialogs.Messagebox.show_error(
                message=f"Une erreur est survenue lors de la connexion à la base de données : {e}",
                title="Erreur de connexion"
            )
            print(f"Une erreur est survenue lors de la connexion à la base de données : {e}", file=sys.stderr)
            raise

    def execute_query(self, sql: str, params: tuple = ()) -> bool:
        """
        Executes a SQL query with the given parameters on the associated database connection. On successful
        execution, the query changes are committed to the database. If an error occurs during execution,
        an error message is displayed and the operation logs the error message to the standard error stream.

        :param sql: The SQL query string to be executed.
        :param params: A tuple containing the parameters to be used in the SQL query. Defaults to an
            empty tuple if no parameters are provided.
        :return: A boolean value indicating the success or failure of the query execution. Returns True
            if the query was successfully executed and committed, otherwise False.
        """
        try:
            with self._get_connection() as conn:
                with closing(conn.cursor()) as cursor:
                    cursor.execute(sql, params)
                conn.commit()
            return True
        except sqlite3.Error as e:
            dialogs.Messagebox.show_error(
                message=f"Erreur lors de l'exécution de la requête : {e}",
                title="Erreur de requête"
            )
            print(f"Erreur lors de l'exécution de la requête : {e}", file=sys.stderr)
            return False

    def fetch_one(self, sql: str, params: tuple = ()) -> Optional[tuple]:
        """
        Executes a SQL query and fetches a single row from the result set.

        The method establishes a connection to the database, executes the specified
        SQL query with the provided parameters, and retrieves the first row from the
        result set if available. If an error occurs during the execution or fetching
        process, an error message is displayed, and the error is logged to standard
        error output. The method will return None if no row is found or in case of
        an error.

        :param sql: The SQL query to be executed.
        :type sql: str
        :param params: A tuple containing the parameters to substitute in the SQL query.
                       Defaults to an empty tuple.
        :type params: tuple
        :return: A tuple representing the first row of the result set, or None if no
                 row is available or an error occurs.
        :rtype: Optional[tuple]
        """
        try:
            with self._get_connection() as conn:
                with closing(conn.cursor()) as cursor:
                    cursor.execute(sql, params)
                    return cursor.fetchone()
        except sqlite3.Error as e:
            dialogs.Messagebox.show_error(
                message=f"Erreur lors de la récupération des données : {e}",
                title="Erreur de récupération"
            )
            print(f"Erreur lors de la récupération des données : {e}", file=sys.stderr)
            return None

    def fetch_all(self, sql: str, params: tuple = ()) -> List[tuple]:
        """
        Fetches all rows from the database for a given SQL query with optional
        parameters.

        This method executes a provided SQL query and retrieves all resulting records
        from the database. It allows specifying optional parameters to prevent SQL
        injection and ensures secure execution of the query. If any errors occur during
        the execution or connection, an error message will be displayed to the user,
        and an empty list will be returned.

        :param sql: The SQL query string to execute.
        :param params: Optional tuple containing parameters to safely substitute into
                       the SQL query.
        :return: A list of tuples representing fetched rows. Each element in the list
                 corresponds to a database row.
        """
        try:
            with self._get_connection() as conn:
                with closing(conn.cursor()) as cursor:
                    cursor.execute(sql, params)
                    return cursor.fetchall()
        except sqlite3.Error as e:
            dialogs.Messagebox.show_error(
                message=f"Erreur lors de la récupération des données : {e}",
                title="Erreur de récupération"
            )
            print(f"Erreur lors de la récupération des données : {e}", file=sys.stderr)
            return []

    def check_if_user_data_exists(self, data: Data) -> bool:
        """
        Determines whether a specific user data record exists in the database by
        checking for a match based on username, password, source, and name.

        :param data: An instance of the Data class containing the username,
            password, source, and name attributes used to identify the record.
        :return: A boolean value indicating whether a matching data record exists
            in the database.
        """
        sql = '''SELECT 1 FROM data WHERE username = ? AND password = ? AND source = ? AND name = ?'''
        return self.fetch_one(sql, (data.username, data.password, data.source, data.name)) is not None

    def register_data(self, data: Data) -> bool:
        """
        Registers a user's data into the database if it does not already exist.

        This method checks if the user's data exists in the database. If the data
        is not present, it inserts the user's details into the `data` table. The
        fields inserted include the name, username, password, and source. If the
        data already exists, the method returns `False`.

        :param data: The user data object containing `name`, `username`, `password`,
            and `source` attributes which are used for the database entry.
        :type data: Data
        :return: A boolean value indicating whether the data was successfully
            registered. Returns `True` if registration is successful, otherwise
            `False`.
        :rtype: bool
        """
        if not self.check_if_user_data_exists(data):
            sql = '''INSERT INTO data (name, username, password, source) VALUES (?, ?, ?, ?)'''
            return self.execute_query(sql, (data.name, data.username, data.password, data.source))
        else:
            return False

    def remove_data(self, id_data: int) -> bool:
        """
        Removes a data entry from the database given its unique identifier. This method
        verifies if the specified data exists in the database before proceeding to delete it.
        If the data exists, it executes a query to remove the corresponding record from the
        database. If the data does not exist, the method does nothing and returns False.

        :param id_data: The unique identifier of the data entry to be removed.
        :type id_data: int
        :return: Boolean indicating if the data removal was successful. Returns True if the
            data was removed, or False if the data does not exist.
        :rtype: bool
        """
        if self.get_one_data_in_db(id_data):
            sql = '''DELETE FROM data WHERE id = ?'''
            return self.execute_query(sql, (id_data,))
        return False

    def modify_data(self, data_id: int, new_data: Data) -> bool:
        """
        Modifies an existing data record in the database by updating the fields with
        the provided new data. If the data record corresponding to the supplied
        data ID does not exist, the operation will not be performed.

        :param data_id: The unique identifier of the data record to be modified.
        :type data_id: int
        :param new_data: An object containing the updated data fields to replace the
            existing record.
        :type new_data: Data
        :return: Returns True if the update was successful; False otherwise.
        :rtype: bool
        """
        if self.get_one_data_in_db(data_id):
            sql = '''UPDATE data SET name = ?, username = ?, password = ?, source = ? WHERE id = ?'''
            return self.execute_query(sql, (new_data.name, new_data.username, new_data.password, new_data.source, data_id))
        return False

    def get_all_Data_in_db(self) -> List[Data]:
        """
        Fetch and return all records from the `data` table in the database.

        This method executes a SQL query to retrieve all entries present in the `data`
        table of the database. It processes the query results and maps each row to an
        instance of the `Data` class.

        :returns:
            A list of `Data` objects, where each object encapsulates the details
            of a single row from the `data` table.
        :rtype: List[Data]
        """
        sql = '''SELECT * FROM data'''
        results = self.fetch_all(sql)
        return [Data(id=row[0], name=row[1], username=row[2], password=row[3], source=row[4]) for row in results]

    def get_one_data_in_db(self, data_id: int) -> Optional[Data]:
        """
        Retrieve a single entry from the database using its unique identifier.

        This method queries the database for a specific entry based on the provided
        data ID. If an entry is found matching the given ID, an instance of the
        `Data` class is returned containing the row's details. If no matching
        entry is found, `None` is returned.

        :param data_id: The unique identifier of the data entry to retrieve.
        :type data_id: int
        :return: An instance of `Data` representing the retrieved database entry,
            or `None` if no matching entry exists.
        :rtype: Optional[Data]
        """
        sql = '''SELECT * FROM data WHERE id = ?'''
        row = self.fetch_one(sql, (data_id,))
        if row:
            return Data(id=row[0], name=row[1], username=row[2], password=row[3], source=row[4])
        return None
