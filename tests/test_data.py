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
def datas_instance(tmp_path)->Datas:
    """
    Creates a pytest fixture for the Datas class instance. This fixture initializes
    a temporary database file, provides a Datas instance connected to this database,
    and ensures cleanup by removing the database file after test execution.

    :param tmp_path: A pytest fixture providing a temporary file path for the test
        database.
    :return: Yields an instance of Datas configured with the test database.
    """
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

def test_datas_connection(datas_instance)->None:
    """
    Tests the connection obtained from the Datas instance to ensure it is not None.

    This function establishes a connection using the `_get_connection`
    method of the provided Datas instance and verifies that the returned
    connection object exists (is not `None`). It is designed to verify
    the correctness of the connection retrieval logic implemented
    within the Datas instance.

    :param datas_instance: The Datas instance whose connection needs
        to be tested.
    :type datas_instance: Datas
    :return: None
    """
    with datas_instance._get_connection() as conn:
        assert conn is not None

def test_execute_query_success(datas_instance)->None:
    """
    Tests the successful execution of a SQL query using the provided datas_instance.
    This function ensures that the `execute_query` method of the given
    datas_instance properly runs a query to create a table named `data`,
    if it does not already exist. It verifies the execution result for
    correctness.

    :param datas_instance: The instance of the database connection or wrapper
        used to execute queries.
    :return: None
    """
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

def test_execute_query_fail(datas_instance)->None:
    """
    Executes a test to ensure that an invalid SQL query fails successfully.

    This function attempts to execute an invalid query on the provided
    datas_instance and checks whether the method correctly identifies and
    returns a failure status.

    :param datas_instance: The instance of the database or data service
                           to be tested for executing queries.
    :type datas_instance: object
    :return: None
    """
    invalid_query = "INVALID QUERY"
    assert not datas_instance.execute_query(invalid_query)

def test_register_and_fetch_data(datas_instance)->None:
    """
    This function tests the registration of a new data entry and retrieval of all data
    entries from the database. It verifies that the data is correctly inserted into the
    database and that the retrieval function fetches the expected data.

    :param datas_instance: An instance of the database handling class. Used to execute
        queries, register new data entries, and retrieve data from the database.
    :type datas_instance: object
    :return: None
    """
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

def test_remove_data(datas_instance)->None:
    """
    Tests the removal of data from the database using the provided `datas_instance`.

    This function creates a table for testing purposes, registers new data, fetches
    all data to confirm insertion, removes the data, and then verifies that the
    database no longer contains the removed data.

    :param datas_instance: Instance of the data handling class that provides
        methods to execute database queries, register data, and fetch or remove
        data records.
    :type datas_instance: Datas
    :return: None
    """
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

def test_data_class_is_created()->None:
    """
    Tests the creation and initialization of the Data class instance.

    This function verifies the correct instantiation of a Data class object
    with the provided attributes: `name`, `username`, `password`, and
    `source`. It ensures that all specified attribute values are set
    appropriately during the creation of the object.

    :raises AssertionError: If the initialization of the Data object does
        not properly assign the provided attribute values or if any
        attribute values do not match the expected values.
    :return: None
    """
    data = Data(name="test", username="test", password="<PASSWORD>", source="test")
    assert data.name == "test"
    assert data.username == "test"
    assert data.password == "<PASSWORD>"
    assert data.source == "test"

def test_data_class_attributes()->None:
    """
    Tests the attributes of the `Data` class to ensure they have the expected
    values when instantiated. This test checks the `name`, `username`,
    `password`, and `source` attributes of the `Data` object to confirm
    that the assignment of their respective values occurs correctly.

    :return: None
    """
    data = Data(name="another_test", username="another_user", password="<ANOTHER_PASSWORD>", source="another_source")
    assert data.name == "another_test"
    assert data.username == "another_user"
    assert data.password == "<ANOTHER_PASSWORD>"
    assert data.source == "another_source"

def test_data_class_default_values()->None:
    """
    Tests the default values of the Data class.

    This function creates an instance of the `Data` class with a given name and checks
    that its attributes are assigned their intended default values. Specifically, it
    verifies that only the `name` attribute is set explicitly, while the other attributes
    (`username`, `password`, and `source`) retain their default `None` values.

    :return: None
    """
    data = Data(name="default_test")
    assert data.name == "default_test"
    assert data.username is None
    assert data.password is None
    assert data.source is None

def test_data_class_modification()->None:
    """
    Tests the modification of attributes in a `Data` class instance. This function ensures that
    the attributes of a `Data` object can be updated correctly and the updated values persist.

    :return: None
    """
    data = Data(name="initial_name", username="initial_user", password="<INITIAL_PASSWORD>", source="initial_source")
    data.name = "modified_name"
    data.username = "modified_user"
    data.password = "<MODIFIED_PASSWORD>"
    data.source = "modified_source"
    assert data.name == "modified_name"
    assert data.username == "modified_user"
    assert data.password == "<MODIFIED_PASSWORD>"
    assert data.source == "modified_source"
