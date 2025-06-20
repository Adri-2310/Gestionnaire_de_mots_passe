"""
Author: Adrien Mertens
Version: 1.0
"""

# Import necessary modules
import sys
from models.data import Datas
from views.mainView import MainWindow

db_name = "db_gestionnaire_password.db"

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
        data_base = Datas(db_name)
        MainWindow("Easy Password", data_base)
    except FileNotFoundError as e:
        print(f"An error occurred while creating the database file: {e}", file=sys.stderr)
        raise
    except ValueError as e:
        print(f"An error occurred while initializing data: {e}", file=sys.stderr)
        raise

# Main entry point of the script
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)
