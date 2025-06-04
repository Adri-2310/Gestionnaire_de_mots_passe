__author__ = "Adrien Mertens"
__version__ = "1.0"

from dataclasses import dataclass, field
import sqlite3
from contextlib import closing

@dataclass
class Data:
    username: str
    password: str
    source: str
    id: int = field(default=-1)

class Datas:
    def __init__(self):
        """Constructeur"""
        self.database = sqlite3.connect("../db_gestionnaire_password.db")

    @property
    def cursor(self) -> sqlite3.Cursor:
        """Créer le curseur"""
        return self.database.cursor()

    def commit(self):
        """Sauvegarde les modifications appliquées à la table"""
        self.database.commit()

    def execute_query(self, sql: str, params: tuple = ()) -> bool:
        """Exécute une requête SQL avec gestion des erreurs."""
        try:
            with closing(self.cursor) as cursor:
                cursor.execute(sql, params)
            self.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erreur lors de l'exécution de la requête : {e}")
            return False

    def fetch_one(self, sql: str, params: tuple = ()):
        """Récupère un seul enregistrement."""
        try:
            with closing(self.cursor) as cursor:
                cursor.execute(sql, params)
                return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des données : {e}")
            return None

    def fetch_all(self, sql: str, params: tuple = ()):
        """Récupère tous les enregistrements."""
        try:
            with closing(self.cursor) as cursor:
                cursor.execute(sql, params)
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des données : {e}")
            return []

    def check_if_user_data_exists(self, username: str, password: str, source: str) -> bool:
        """Vérifie si les données d'un utilisateur existent déjà dans la base de données."""
        sql = '''SELECT 1 FROM data WHERE username = ? AND password = ? AND source = ?'''
        return self.fetch_one(sql, (username, password, source)) is not None

    def registre_data(self, username: str, password: str, source: str) -> bool:
        """Enregistre les données d'un utilisateur dans la base de données si elles n'existent pas déjà."""
        if not self.check_if_user_data_exists(username=username, password=password, source=source):
            sql = '''INSERT INTO data (username, password, source) VALUES (?, ?, ?)'''
            return self.execute_query(sql, (username, password, source))
        return False

    def remove_data(self, id_data: str) -> bool:
        """Supprime les données d'un utilisateur de la base de données."""
        if self.search_data_one_user(id_data=id_data):
            sql = '''DELETE FROM data WHERE id = ?'''
            return self.execute_query(sql, (id_data,))
        return False

    def modify_data(self, old_id: int, new_username: str, new_password: str, new_source: str) -> bool:
        """Modifie les données d'un utilisateur dans la base de données."""
        data = self.search_data_one_user(id_data=old_id)
        if data:
            sql = '''UPDATE data SET username = ?, password = ?, source = ? WHERE id = ?'''
            return self.execute_query(sql, (new_username, new_password, new_source, old_id))
        return False

    def search_data_all_data_user(self) -> list:
        """Recherche toutes les données de chaque enregistrement dans la base de données."""
        sql = '''SELECT * FROM data'''
        return self.fetch_all(sql)

    def search_data_one_user(self, id_data: str) -> tuple:
        """Recherche un enregistrement spécifique de l'utilisateur dans la base de données."""
        sql = '''SELECT * FROM data WHERE id = ?'''
        return self.fetch_one(sql, (id_data,))

