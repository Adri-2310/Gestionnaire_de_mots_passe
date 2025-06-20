# -*- coding: utf-8 -*-
"""
__author__ = "<Adrien Mertens>"
__version__ = "1.0"
"""

import os
import pytest
from models.data import Data, Datas

# Fixture pour créer une instance de Datas avec une base de données temporaire
@pytest.fixture
def datas_instance(tmp_path):
    db_path = tmp_path / "test_database.db"
    datas = Datas(path_db=str(db_path))
    yield datas
    # Supprime le fichier de la base de données après l'exécution des tests
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except PermissionError:
            # Si le fichier est encore utilisé, attendez un peu et réessayez
            import time
            time.sleep(1)
            if os.path.exists(db_path):
                os.remove(db_path)

def test_datas_connection(datas_instance):
    with datas_instance._get_connection() as conn:
        assert conn is not None

def test_execute_query_success(datas_instance):
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS data
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            source TEXT
        )
    '''
    assert datas_instance.execute_query(create_table_query)

def test_execute_query_fail(datas_instance):
    invalid_query = "INVALID QUERY"
    assert not datas_instance.execute_query(invalid_query)

def test_register_and_fetch_data(datas_instance):
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS data
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            source TEXT
        )
    '''
    datas_instance.execute_query(create_table_query)

    new_data = Data(name="Test User", username="testuser", password="password123", source="source1")
    assert datas_instance.register_data(new_data)

    fetched_data = datas_instance.get_all_Data_in_db()
    assert len(fetched_data) == 1
    assert fetched_data[0].name == "Test User"

def test_remove_data(datas_instance):
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS data
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            source TEXT
        )
    '''
    datas_instance.execute_query(create_table_query)

    new_data = Data(name="User To Remove", username="removeuser", password="password123", source="source1")
    assert datas_instance.register_data(new_data)

    fetched_data = datas_instance.get_all_Data_in_db()
    assert len(fetched_data) == 1
    data_id = fetched_data[0].id

    assert datas_instance.remove_data(data_id)

    remaining_data = datas_instance.get_all_Data_in_db()
    assert len(remaining_data) == 0

def test_data_class_is_created():
    data = Data(name="test", username="test", password="<PASSWORD>", source="test")
    assert data.name == "test"
    assert data.username == "test"
    assert data.password == "<PASSWORD>"
    assert data.source == "test"

def test_data_class_attributes():
    data = Data(name="another_test", username="another_user", password="<ANOTHER_PASSWORD>", source="another_source")
    assert data.name == "another_test"
    assert data.username == "another_user"
    assert data.password == "<ANOTHER_PASSWORD>"
    assert data.source == "another_source"

def test_data_class_default_values():
    data = Data(name="default_test")
    assert data.name == "default_test"
    assert data.username is None
    assert data.password is None
    assert data.source is None

def test_data_class_modification():
    data = Data(name="initial_name", username="initial_user", password="<INITIAL_PASSWORD>", source="initial_source")
    data.name = "modified_name"
    data.username = "modified_user"
    data.password = "<MODIFIED_PASSWORD>"
    data.source = "modified_source"
    assert data.name == "modified_name"
    assert data.username == "modified_user"
    assert data.password == "<MODIFIED_PASSWORD>"
    assert data.source == "modified_source"
