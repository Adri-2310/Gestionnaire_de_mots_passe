import os
import pytest
from controllers.controllersDatas import ControllersDatas
from models.data import Data, Datas

@pytest.fixture
def datas_instance(tmp_path):
    """
    Creates a pytest fixture for the Datas class instance. This fixture initializes
    a temporary database file, provides a Datas instance connected to this database,
    and ensures cleanup by removing the database file after test execution.
    :param tmp_path: A pytest fixture providing a temporary file path for the test database.
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

@pytest.fixture
def controllers_datas_instance(datas_instance):
    """
    Fixture for creating a ControllersDatas instance.
    :param datas_instance: A fixture providing a Datas instance.
    :return: Yields an instance of ControllersDatas configured with the Datas instance.
    """
    return ControllersDatas(datas_instance)

def test_add_data(controllers_datas_instance):
    """
    Tests adding data through the ControllersDatas instance.
    """
    data = Data(name="John Doe", username="jdoe", password="password123", source="source1")
    result = controllers_datas_instance.add_data(data)
    assert result is True

def test_modif_data(controllers_datas_instance):
    """
    Tests modifying data through the ControllersDatas instance.
    """
    data = Data(name="John Doe", username="jdoe", password="password123", source="source1")
    controllers_datas_instance.add_data(data)
    new_data = Data(name="Jane Doe", username="janedoe", password="newpassword456", source="source2")
    result = controllers_datas_instance.modif_data(1, new_data)
    assert result is True

def test_delete_data(controllers_datas_instance):
    """
    Tests deleting data through the ControllersDatas instance.
    """
    data = Data(name="John Doe", username="jdoe", password="password123", source="source1")
    controllers_datas_instance.add_data(data)
    result = controllers_datas_instance.delete_data(1)
    assert result is True

def test_get_all_datas(controllers_datas_instance):
    """
    Tests retrieving all data through the ControllersDatas instance.
    """
    data1 = Data(name="John Doe", username="jdoe", password="password123", source="source1")
    data2 = Data(name="Jane Doe", username="janedoe", password="newpassword456", source="source2")
    controllers_datas_instance.add_data(data1)
    controllers_datas_instance.add_data(data2)
    all_data = controllers_datas_instance.get_all_datas()
    assert len(all_data) == 2
    assert all_data[0].username == "jdoe"
    assert all_data[1].username == "janedoe"

def test_get_one_data(controllers_datas_instance):
    """
    Tests retrieving a single data entry through the ControllersDatas instance.
    """
    data = Data(name="John Doe", username="jdoe", password="password123", source="source1")
    controllers_datas_instance.add_data(data)
    retrieved_data = controllers_datas_instance.get_one_data(1)
    assert retrieved_data is not None
    assert retrieved_data.username == "jdoe"
