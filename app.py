"""
Author: Adrien Mertens
Version: 1.0
"""

# Import necessary modules
import os
import sqlite3
from models.data import Datas
from views.mainView import MainWindow

db_name = "db_gestionnaire_password.db"

def create_db()->None:
    """
    Creates a new SQLite database table named 'data' if it does not already exist.
    The table is designed to store user-related information, including an auto-incrementing
    primary key, a name, username, password, and an optional source field. This function
    ensures the table structure is created in the SQLite database file specified.

    :return: None
    """
    # SQL query to create the 'data' table
    sql = '''CREATE TABLE IF NOT EXISTS data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        source TEXT)'''

    with sqlite3.connect(db_name) as db:
        db.execute(sql)

def main()->None:
    """
    Executes the main function of the program. It initializes the database if it
    does not exist and sets up the main window for the application.

    :param: None
    :return: None
    """
    if not os.path.exists(db_name):
        create_db()

    data_base = Datas(db_name)
    MainWindow("Password Manager", data_base)

# Main entry point of the script
if __name__ == '__main__':
    main()
