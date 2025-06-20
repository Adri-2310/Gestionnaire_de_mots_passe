"""
__author__ = "Adrien Mertens"
__version__ = "1.0"
"""
import sys
from views.topLevelValidateAndCancelForUseDB import TopLevelValidateAndCancelForUseDB
from models.data import Data
import ttkbootstrap.dialogs as dialogs


class AddDataView(TopLevelValidateAndCancelForUseDB):
    """
    Represents a view for adding data entries into a board. This class manages the
    user interface for data input, interacts with a controller for data storage,
    and updates the visual representation of the board after an operation. It
    provides feedback to users regarding the success, duplication, or failure of
    the data addition process using dialog boxes.

    :ivar board: The board to which the new data entries will be added.
    :type board: Any
    :ivar __controller: The controller responsible for handling the logic of adding
        data entries to the database or storage.
    :type __controller: Any
    """
    def __init__(self,master,controller,board):
        super().__init__(master,"Ajouter une données",self.command)
        self.board = board
        self.__controller = controller

    def command(self)->None:
        """
        Handles the addition of a new entry by validating input data, calling the controller to store
        the data, and updating the user interface accordingly. Displays appropriate dialog messages
        for successful, duplicate, or failed operations. Catches and processes potential validation
        and general exceptions.

        :param self: Reference to the instance of the class where this method is called.
        :type self: Any

        :return: None
        :rtype: None
        """
        try:
            if self.__controller.add_data(Data(
                    name=self.var_name.get(),
                    username=self.var_username.get(),
                    password=self.var_password.get(),
                    source=self.var_source.get()
            )):
                dialogs.Messagebox.show_info(
                    message="L'enregistrement a bien été effectué !",
                    title="Information",
                    parent=self
                )
                self.board.refresh_data_board_from_db()
                self.destroy()
            else:
                dialogs.Messagebox.show_warning(
                    message="La donnée existe déjà !",
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
            print(f"An unexpected error occurred: {e}", file=sys.stderr)

