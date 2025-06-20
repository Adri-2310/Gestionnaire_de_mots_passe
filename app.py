"""
Author: Adrien Mertens
Version: 1.0
"""

# Import necessary modules
import os
import sqlite3
import sys
from models.data import Datas
from views.mainView import MainWindow

db_name = "db_gestionnaire_password.db"

def create_db()->None:
    """
    Creates a database table named 'data' if it does not already exist.

    This function executes an SQL query to create a table named 'data' in an SQLite
    database. The table includes the following columns:

    - id: An integer that serves as the primary key and auto-increments.
    - name: A non-nullable text field for storing names.
    - username: A non-nullable text field for storing usernames.
    - password: A non-nullable text field for storing passwords.
    - source: A text field for storing the source information.

    If the table already exists, the operation is skipped. In the case of an error
    during database connection or query execution, an appropriate exception is
    raised.

    :raises sqlite3.Error: If an error occurs during the creation of the database or
        during query execution.
    :return: None
    """
    # SQL query to create the 'data' table
    sql = '''CREATE TABLE IF NOT EXISTS data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        source TEXT)'''
    try:
        with sqlite3.connect(db_name) as db:
            db.execute(sql)
    except sqlite3.Error as e:
        raise sqlite3.Error(f"An error occurred while creating the database: {e}")

def main()->None:
    """
    Main entry point of the application.

    This function performs an essential role in the initialization and setup of the
    application. It ensures the database file exists, creates the database if it does
    not, and initializes the main application components, such as the main application
    window and database connection.

    The function attempts to manage different kinds of errors that might occur
    during runtime, including file-related errors, data value issues, and database
    errors. These errors are logged to standard error output and re-raised for
    higher-level handling if necessary.

    :raises FileNotFoundError: If there is an issue creating the database file.
    :raises ValueError: If there is an issue initializing or setting up the
                        provided data.
    :raises sqlite3.Error: If there is an issue related to accessing or
                           operating on the SQLite database.
    :returns: None
    """
    try:
        if not os.path.exists(db_name):
            create_db()
        data_base = Datas(db_name)
        MainWindow("Easy Password", data_base)
    except FileNotFoundError as e:
        print(f"An error occurred while creating the database file: {e}", file=sys.stderr)
        raise
    except ValueError as e:
        print(f"An error occurred while initializing data: {e}", file=sys.stderr)
        raise
    except sqlite3.Error as e:
        print(f"An error occurred while accessing the database: {e}", file=sys.stderr)
        raise

# Main entry point of the script
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)
