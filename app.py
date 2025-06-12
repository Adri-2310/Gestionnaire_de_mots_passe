"""
__author__ = "Adrien Mertens"
__version__ = "1.0"
"""
import os
import sqlite3
from models.data import Datas
from views.mainView import MainWindow
def create_db():
    """
            Initialise la base de données et crée la table 'data' si elle n'existe pas.
            """
    sql = '''CREATE TABLE IF NOT EXISTS data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        source TEXT)'''
    db = sqlite3.connect("db_gestionnaire_password.db")
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    db.close()




# lancement de mon application
if __name__ == '__main__':
    if not os.path.exists("db_gestionnaire_password.db"):
        create_db()
    data_base = Datas("db_gestionnaire_password.db")
    app = MainWindow("Gestionnaire mots de passe","db_gestionnaire_password.db")