__author__ = "Adrien Mertens"
__version__ = "1.0"

import os.path
import sqlite3

def init_db() -> None:
    """
    Initialise la base de données et crée la table 'data' si elle n'existe pas.
    """
    conn = sqlite3.connect(r'..\datas.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT NOT NULL,
        password TEXT NOT NULL,
        source TEXT)''')
    conn.commit()
    cursor.close()
    conn.close()

def registre_data(user: str, password: str, source: str) -> bool:
    """
    Enregistre les données d'un utilisateur dans la base de données si elles n'existent pas déjà.

    :param user: Nom d'utilisateur
    :param password: Mot de passe de l'utilisateur
    :param source: Source associée à l'utilisateur
    :return: True si l'insertion a réussi, False si les données existent déjà
    """
    check_if_datas_exists()
    if not check_if_user_data_exists(new_user=user, new_password=password, new_source=source):
        conn = sqlite3.connect(r'..\datas.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO data (user, password, source) VALUES (?, ?, ?)''', (user, password, source))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    else:
        return False

def remove_data(user: str, password: str, source: str) -> bool:
    """
    Supprime les données d'un utilisateur de la base de données.

    :param user: Nom d'utilisateur
    :param password: Mot de passe de l'utilisateur
    :param source: Source associée à l'utilisateur
    :return: True si la suppression a réussi, False sinon
    """
    pass

def modify_data(old_user: str, old_password: str, old_source: str, new_user: str, new_password: str, new_source: str) -> bool:
    """
    Modifie les données d'un utilisateur dans la base de données.

    :param old_user: Ancien nom d'utilisateur
    :param old_password: Ancien mot de passe de l'utilisateur
    :param old_source: Ancienne source associée à l'utilisateur
    :param new_user: Nouveau nom d'utilisateur
    :param new_password: Nouveau mot de passe de l'utilisateur
    :param new_source: Nouvelle source associée à l'utilisateur
    :return: True si la modification a réussi, False sinon
    """
    pass

def search_data_all_data_user(user: str, password: str, source: str) -> list:
    """
    Recherche toutes les données de chaque enregistrement dans la base de données.

    :param user: Nom d'utilisateur
    :param password: Mot de passe de l'utilisateur
    :param source: Source associée à l'utilisateur
    :return: Liste des enregistrements trouvés
    """
    pass

def search_data_one_user(user: str, password: str, source: str) -> tuple:
    """
    Recherche un enregistrement spécifique de l'utilisateur dans la base de données.

    :param user: Nom d'utilisateur
    :param password: Mot de passe de l'utilisateur
    :param source: Source associée à l'utilisateur
    :return: Tuple représentant l'enregistrement trouvé, ou None si aucun enregistrement n'est trouvé
    """
    pass

def check_if_datas_exists() -> None:
    """
    Vérifie si le fichier de la base de données existe. Si non, initialise la base de données.
    """
    if not os.path.exists(r'..\datas.db'):
        init_db()

def check_if_user_data_exists(new_user: str, new_password: str, new_source: str) -> bool:
    """
    Vérifie si les données d'un utilisateur existent déjà dans la base de données.

    :param new_user: Nom d'utilisateur à vérifier
    :param new_password: Mot de passe à vérifier
    :param new_source: Source à vérifier
    :return: True si les données existent, False sinon
    """
    conn = sqlite3.connect(r'..\datas.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT 1 FROM data WHERE user = ? AND password = ? AND source = ?''', (new_user, new_password, new_source))
    exists = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    return exists

if __name__ == '__main__':
    # Exemple d'utilisation de la fonction registre_data
    result = registre_data("adrien", "1234", "https://youtube.com")
    print(result)  # Afficher le résultat de l'insertion
