import pytest
import sqlite3
from models.data import Datas

@pytest.fixture
def datas():
    # Crée une instance de la classe Datas pour les tests
    return Datas("test_db_gestionnaire_password.db")

@pytest.fixture
def setup_database():
    # Crée une base de données en mémoire pour les tests
    conn = sqlite3.connect(":memory:")
    conn.execute('''
        CREATE TABLE data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            source TEXT NOT NULL
        )
    ''')
    conn.commit()
    yield conn
    conn.close()

def test_registre_data(datas, setup_database):
    # Teste l'ajout de données
    assert datas.registre_data("user1", "pass1", "source1") == True
    assert datas.registre_data("user1", "pass1", "source1") == False  # Test pour éviter les doublons

def test_remove_data(datas, setup_database):
    # Ajoute une donnée pour le test de suppression
    datas.registre_data("user2", "pass2", "source2")
    data_id = datas.fetch_one("SELECT id FROM data WHERE username = ? AND password = ? AND source = ?", ("user2", "pass2", "source2"))[0]
    assert datas.remove_data(str(data_id)) == True
    assert datas.remove_data("9999") == False  # Test avec un ID inexistant

def test_modify_data(datas, setup_database):
    # Ajoute une donnée pour le test de modification
    datas.registre_data("user3", "pass3", "source3")
    data_id = datas.fetch_one("SELECT id FROM data WHERE username = ? AND password = ? AND source = ?", ("user3", "pass3", "source3"))[0]
    assert datas.modify_data(data_id, "user3_new", "pass3_new", "source3_new") == True
    assert datas.modify_data(9999, "user3_new", "pass3_new", "source3_new") == False  # Test avec un ID inexistant

def test_search_data_all_data_user(datas, setup_database):
    # Ajoute des données pour le test de recherche
    datas.registre_data("user4", "pass4", "source4")
    datas.registre_data("user5", "pass5", "source5")
    results = datas.search_data_all_data_user()
    assert len(results) == 2

def test_search_data_one_user(datas, setup_database):
    # Ajoute une donnée pour le test de recherche unique
    datas.registre_data("user6", "pass6", "source6")
    data_id = datas.fetch_one("SELECT id FROM data WHERE username = ? AND password = ? AND source = ?", ("user6", "pass6", "source6"))[0]
    result = datas.search_data_one_user(str(data_id))
    assert result is not None
    assert datas.search_data_one_user("9999") is None  # Test avec un ID inexistant
