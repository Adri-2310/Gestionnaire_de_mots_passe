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

    def check_if_user_data_exists(self, username: str, password: str, source: str) -> bool:
        """
        Vérifie si les données d'un utilisateur existent déjà dans la base de données.
        """
        sql = '''SELECT 1 FROM data WHERE username = ? AND password = ? AND source = ?'''
        try:
            with closing(self.cursor) as cursor:
                cursor.execute(sql, (username, password, source))
                exists = cursor.fetchone() is not None
            return exists
        except sqlite3.Error as e:
            print(f"Erreur lors de la vérification des données : {e}")


    def registre_data(self, username: str, password: str, source: str) -> bool:
        """
        Enregistre les données d'un utilisateur dans la base de données si elles n'existent pas déjà.
        """
        try:
            if not self.check_if_user_data_exists(username=username, password=password, source=source):
                sql = '''INSERT INTO data (username, password, source) VALUES (?, ?, ?)'''
                with closing(self.cursor) as cursor:
                    cursor.execute(sql, (username, password, source))
                self.commit()
                return True
            return False
        except sqlite3.Error as e:
            print(f"Erreur lors de l'enregistrement des données : {e}")

    def remove_data(self, id_data: str) -> bool:
        """
        Supprime les données d'un utilisateur de la base de données.
        """
        try:
            if self.search_data_one_user(id_data=id_data):
                sql = '''DELETE FROM data WHERE id = ?'''
                with closing(self.cursor) as cursor:
                    cursor.execute(sql, (id_data,))
                self.commit()
                return True
            return False
        except sqlite3.Error as e:
            print(f"Erreur lors de la suppression des données : {e}")


    def modify_data(self, old_id: int, old_username: str, old_password: str, old_source: str,
                    new_username: str, new_password: str, new_source: str) -> bool:
        """
        Modifie les données d'un utilisateur dans la base de données.
        """
        try:
            if self.check_if_user_data_exists(username=old_username, password=old_password, source=old_source):
                sql = '''UPDATE data SET username = ?, password = ?, source = ? WHERE id = ?'''
                with closing(self.cursor) as cursor:
                    cursor.execute(sql, (new_username, new_password, new_source, old_id))
                self.commit()
                return True
            return False
        except sqlite3.Error as e:
            print(f"Erreur lors de la modification des données : {e}")


    def search_data_all_data_user(self) -> list:
        """
        Recherche toutes les données de chaque enregistrement dans la base de données.
        """
        try:
            sql = '''SELECT * FROM data'''
            with closing(self.cursor) as cursor:
                cursor.execute(sql)
                all_datas = cursor.fetchall()
            return all_datas
        except sqlite3.Error as e:
            print(f"Erreur lors de la recherche des données : {e}")
            return []

    def search_data_one_user(self, id_data: str) -> tuple:
        """
        Recherche un enregistrement spécifique de l'utilisateur dans la base de données.
        """
        try:
            sql = '''SELECT * FROM data WHERE id = ?'''
            with closing(self.cursor) as cursor:
                cursor.execute(sql, (id_data,))
                data = cursor.fetchone()
            return data
        except sqlite3.Error as e:
            print(f"Erreur lors de la recherche de l'utilisateur : {e}")
            return ()

if __name__ == '__main__':
    datas = Datas()
    answer = datas.registre_data(username="test", password="<PASSWORD>", source="test")
    print(answer)
