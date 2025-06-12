"""
Module pour la gestion des données utilisateur dans une base de données SQLite.
Auteur : Adrien Mertens
Version : 1.0
"""

from dataclasses import dataclass, field
import sqlite3
from contextlib import closing
from typing import Optional, List

@dataclass
class Data:
    """
    Une classe pour représenter les données d'un utilisateur.
    Cette dataclass contient les informations de base d'un utilisateur.
    """
    name: str  # Le nom de l'utilisateur
    username: str  # Le nom d'utilisateur
    password: str  # Le mot de passe de l'utilisateur
    source: str  # La source des données de l'utilisateur
    id: int = field(default=-1)  # L'identifiant unique de l'utilisateur, par défaut -1

class Datas:
    """
    Une classe pour gérer les opérations de base de données pour les données utilisateur.
    Cette classe fournit des méthodes pour insérer, mettre à jour, supprimer et rechercher des données utilisateur.
    """

    def __init__(self, path_db: str = "../db_gestionnaire_password.db"):
        """
        Initialise la connexion à la base de données.

        Args:
            path_db (str): Le chemin vers le fichier de la base de données SQLite.
        """
        self.path_db = path_db

    def _get_connection(self):
        """
        Crée et retourne une connexion à la base de données en utilisant un gestionnaire de contexte.

        Returns:
            sqlite3.Connection: Une connexion à la base de données SQLite.
        """
        return sqlite3.connect(self.path_db)

    def execute_query(self, sql: str, params: tuple = ()) -> bool:
        """
        Exécute une requête SQL avec gestion des erreurs.

        Args:
            sql (str): La requête SQL à exécuter.
            params (tuple): Les paramètres à passer à la requête SQL.

        Returns:
            bool: True si la requête a été exécutée avec succès, False sinon.
        """
        try:
            with self._get_connection() as conn:
                with closing(conn.cursor()) as cursor:
                    cursor.execute(sql, params)
                conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error executing the query: {e}")
            return False

    def fetch_one(self, sql: str, params: tuple = ()) -> Optional[tuple]:
        """
        Récupère un seul enregistrement de la base de données.

        Args:
            sql (str): La requête SQL à exécuter.
            params (tuple): Les paramètres à passer à la requête SQL.

        Returns:
            Optional[tuple]: Un tuple représentant un enregistrement, ou None si aucun enregistrement n'est trouvé.
        """
        try:
            with self._get_connection() as conn:
                with closing(conn.cursor()) as cursor:
                    cursor.execute(sql, params)
                    return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error retrieving data: {e}")
            return None

    def fetch_all(self, sql: str, params: tuple = ()) -> List[tuple]:
        """
        Récupère tous les enregistrements de la base de données.

        Args:
            sql (str): La requête SQL à exécuter.
            params (tuple): Les paramètres à passer à la requête SQL.

        Returns:
            List[tuple]: Une liste de tuples représentant les enregistrements.
        """
        try:
            with self._get_connection() as conn:
                with closing(conn.cursor()) as cursor:
                    cursor.execute(sql, params)
                    return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving data: {e}")
            return []

    def check_if_user_data_exists(self, data: Data) -> bool:
        """
        Vérifie si les données d'un utilisateur existent déjà dans la base de données.

        Args:
            data (Data): Un objet Data contenant les informations de l'utilisateur.

        Returns:
            bool: True si les données existent déjà, False sinon.
        """
        sql = '''SELECT 1 FROM data WHERE username = ? AND password = ? AND source = ? AND name = ?'''
        return self.fetch_one(sql, (data.username, data.password, data.source, data.name)) is not None

    def register_data(self, data: Data) -> bool:
        """
        Enregistre les données d'un utilisateur dans la base de données si elles n'existent pas déjà.

        Args:
            data (Data): Un objet Data contenant les informations de l'utilisateur.

        Returns:
            bool: True si les données ont été enregistrées avec succès, False sinon.
        """
        if not self.check_if_user_data_exists(data):
            sql = '''INSERT INTO data (name, username, password, source) VALUES (?, ?, ?, ?)'''
            return self.execute_query(sql, (data.name, data.username, data.password, data.source))
        else:
            return False

    def remove_data(self, id_data: int) -> bool:
        """
        Supprime les données d'un utilisateur de la base de données.

        Args:
            id_data (int): L'identifiant unique des données à supprimer.

        Returns:
            bool: True si les données ont été supprimées avec succès, False sinon.
        """
        if self.get_one_data_in_db(id_data):
            sql = '''DELETE FROM data WHERE id = ?'''
            return self.execute_query(sql, (id_data,))
        return False

    def modify_data(self, data_id: int, new_data: Data) -> bool:
        """
        Modifie les données d'un utilisateur dans la base de données.

        Args:
            data_id (int): L'identifiant unique des données à modifier.
            new_data (Data): Un objet Data contenant les nouvelles informations de l'utilisateur.

        Returns:
            bool: True si les données ont été modifiées avec succès, False sinon.
        """
        if self.get_one_data_in_db(data_id):
            sql = '''UPDATE data SET name = ?, username = ?, password = ?, source = ? WHERE id = ?'''
            return self.execute_query(sql, (new_data.name, new_data.username, new_data.password, new_data.source, data_id))
        return False

    def get_all_Data_in_db(self) -> List[Data]:
        """
        Retrieves all records from the data table in the database and returns them
        as a list of Data objects. This method interacts with the database to
        fetch all rows in the data table and transforms each row into an instance
        of the Data class.

        :raises DatabaseError: If there is a failure in fetching data from the
            database.

        :return: A list of Data objects, where each object represents a record from
            the data table.
        :rtype: List[Data]
        """
        sql = '''SELECT * FROM data'''
        results = self.fetch_all(sql)
        return [Data(id=row[0], name=row[1], username=row[2], password=row[3], source=row[4]) for row in results]

    def get_one_data_in_db(self, data_id: int) -> Optional[Data]:
        """
        Recherche un enregistrement spécifique de l'utilisateur dans la base de données et le retourne sous forme d'objet Data.

        Args:
            data_id (int): L'identifiant unique des données à rechercher.

        Returns:
            Optional[Data]: Un objet Data représentant l'enregistrement, ou None si aucun enregistrement n'est trouvé.
        """
        sql = '''SELECT * FROM data WHERE id = ?'''
        row = self.fetch_one(sql, (data_id,))
        if row:
            return Data(id=row[0], name=row[1], username=row[2], password=row[3], source=row[4])
        return None
