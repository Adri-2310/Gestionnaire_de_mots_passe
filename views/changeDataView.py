"""
__author__ = "Adrien Mertens"
__version__ = "1.0"
"""
import sys
from views.topLevelValidateAndCancelForUseDB import TopLevelValidateAndCancelForUseDB
from models.data import Data
import ttkbootstrap.dialogs as dialogs

class ChangeDataView(TopLevelValidateAndCancelForUseDB):
    def __init__(self, master,data_id,board,controller)->None:
        """
        Constructor to initialize the class instance for managing and modifying data.
        This initialization involves setting up required attributes like board,
        controller, and data_id. It also retrieves and pre-sets old data values into
        class variables to allow modification. In case of error during data retrieval,
        displays an error message using a message box and closes the instance.

        :param master: The parent widget for this instance.
        :type master: Any
        :param data_id: The unique identifier for the data to be modified.
        :type data_id: int
        :param board: The board context relevant to this instance.
        :type board: Any
        :param controller: The controller responsible for managing data operations.
        :type controller: Any
        """
        super().__init__(master, "Modifier une données", self.change_data)
        self.board = board
        self.__controller = controller
        self.__data_id = data_id
        try:
            data_old = self.__controller.get_one_data(data_id)
            self.var_name.set(data_old.name)
            self.var_username.set(data_old.username)
            self.var_password.set(data_old.password)
            self.var_source.set(data_old.source)
        except Exception as e:
            dialogs.Messagebox.show_error(
                message=f"Une erreur est survenue lors de la récupération des données : {e}",
                title="Erreur",
                parent=self
            )
            self.destroy()

    def change_data(self)->None:
        """
        Attempts to update existing data within the system by invoking the appropriate
        controller function. The method gathers necessary input, validates the operation
        through the controller, and provides user feedback depending on the outcome.
        If the operation is successful, the data will be refreshed in the interface,
        and the current window will close. Otherwise, the user will be notified of the
        failure or any encountered errors.

        :raises ValueError: If a validation error occurs in the provided data.
        :raises Exception: If any unexpected error occurs during the operation.
        :return: None
        """
        try:
            if self.__controller.modif_data(
                        data_id=self.__data_id,
                        new_data=Data(
                        name=self.var_name.get(),
                        username=self.var_username.get(),
                        password=self.var_password.get(),
                        source=self.var_source.get()
                    )
            ):
                dialogs.Messagebox.ok(
                    message="Les informations ont bien été modifiées !",
                    title="Information",
                    parent=self
                )
                self.board.refresh_data_board_from_db()
                self.destroy()
            else:
                dialogs.Messagebox.show_warning(
                    message="Les données n'ont pas été modifiées.",
                    title="Attention",
                    parent=self
                )
        except ValueError as ve:
            dialogs.Messagebox.show_error(
                message=f"Une erreur de validation est survenue : {ve}",
                title="Erreur de validation",
                parent=self
            )
        except Exception as e:
            dialogs.Messagebox.show_error(
                message=f"Une erreur inattendue est survenue : {e}",
                title="Erreur",
                parent=self
            )
            print(f"Une erreur inattendue est survenue : {e}", file=sys.stderr)


