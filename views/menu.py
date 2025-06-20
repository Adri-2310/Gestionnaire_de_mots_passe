"""
Author: Adrien Mertens
Version: 1.0
"""
import sys
import ttkbootstrap as ttk
from views.addDataView import AddDataView
from views.changeDataView import ChangeDataView
from views.showDataView import ShowDataView
import ttkbootstrap.dialogs as dialogs

class Menu(ttk.Frame):
    """
    Represents a menu interface within a graphical user interface, designed for managing
    various actions such as adding, modifying, deleting, and displaying data. It provides
    a structured set of buttons with specific functionalities, utilizing custom styles and
    error handling mechanisms.

    This class is built to operate within a parent ttk.Frame container, integrating closely
    with a board object to manage data operations. Customizations and error handling are
    integral to its design, ensuring robustness and a smooth user experience.

    :ivar board: Represents the board object responsible for data management operations.
    :type board: Any
    :ivar __master: Refers to the parent container or window where the menu is placed.
    :type __master: Any
    :ivar __controller: Provides a reference to the controller managing the menu's functionality.
    :type __controller: object or None
    """

    def __init__(self, master, board)->None:
        """
        Initializes an instance of the class and sets up the required attributes.

        :param master: The parent container or window where the widget is
            placed.
        :param board: The board object representing the game's state or
            relevant data structure.

        """
        super().__init__(master)
        self.__master = master
        self.board = board
        self.__controller = None
        self.widgets()

    def widgets(self)->None:
        """
        Creates widget buttons with custom style and functionalities for a user interface.

        This method defines a custom `ttk.Style` specifically for buttons and sets multiple
        properties, such as background and foreground colors for the active and inactive states.
        It configures a list of buttons with pre-defined labels and commands, packs them into
        the user interface horizontally, and applies the custom styles. Additionally, it handles
        exceptions to notify the user in case of widget creation errors.

        :raises Exception: If an error occurs during the creation of the widgets.
        """
        try:
            # Create a custom style for each button
            style = ttk.Style()
            style.configure('AllButton.TButton', borderwidth=1, relief="solid", bordercolor="#4e5d6c")
            style.map('AllButton.TButton',
                      background=[('active', '#ABB6C2'), ('!active', '#4e5d6c')],
                      foreground=[('active', 'black'), ('!active', 'white')])

            # Button configurations
            buttons_config = [
                ("AJOUTER", self.add_data),
                ("MODIFIER", self.change_data_selected),
                ("SUPPRIMER", self.delete_data_selected),
                ("AFFICHER", self.show_data_selected),
                ("QUITTER", self.__master.quit)
            ]

            for text, command in buttons_config:
                button = ttk.Button(self, text=text, command=command, style="AllButton.TButton")
                button.pack(side="left", padx=5, pady=10)
        except Exception as e:
            dialogs.Messagebox.show_error(
                message=f"Une erreur est survenue lors de la création des widgets : {e}",
                title="Erreur",
                parent=self.__master
            )
            print(f"Une erreur est survenue lors de la création des widgets : {e}", file=sys.stderr)

    def add_data(self)->None:
        """
        Handles the creation of an instance of the AddDataView class, linked to the specified master widget,
        controller, and board. If an exception occurs during the process, it displays an error message through
        a dialog box and logs the error to the standard error output.

        :raises Exception: Captures any unexpected errors during the initialization of the AddDataView and
                           provides an error message indicating the issue.
        """
        try:
            AddDataView(self.__master, self.__controller, self.board)
        except Exception as e:
            dialogs.Messagebox.show_error(
                message=f"Une erreur est survenue lors de l'ouverture de la vue d'ajout de données : {e}",
                title="Erreur",
                parent=self.__master
            )
            print(f"Une erreur est survenue lors de l'ouverture de la vue d'ajout de données : {e}", file=sys.stderr)

    def change_data_selected(self)->None:
        """
        Handles the process of changing data for a selected item in a graphical user interface.

        This method retrieves the currently selected item from a list or table and attempts to open a new
        view for modifying the associated data. If no item is selected, or an unexpected error occurs during
        the process, appropriate error messages are displayed to the user.

        :raises IndexError: Raised when no item is selected from the list or table.
        :raises Exception: Raised when an unexpected error occurs during the process.

        :return: None
        """
        try:
            selected_item = self.board.board.selection()
            if not selected_item:
                raise IndexError("Aucune donnée sélectionnée")
            ChangeDataView(master=self.__master, board=self.board, data_id=int(self.board.board.selection()[0]),
                           controller=self.__controller)
        except IndexError:
            dialogs.Messagebox.show_info(
                message="Veuillez sélectionner un élément dans la liste",
                title="Attention",
                parent=self.__master
            )
        except Exception as e:
            dialogs.Messagebox.show_error(
                message=f"Une erreur est survenue lors de l'ouverture de la vue de modification des données : {e}",
                title="Erreur",
                parent=self.__master
            )
            print(f"Une erreur est survenue lors de l'ouverture de la vue de modification des données : {e}",
                  file=sys.stderr)

    def delete_data_selected(self)->None:
        """
        Deletes the currently selected data entry from a graphical list or table. This
        function ensures that the user has selected an item and confirms their intent
        to delete it before proceeding. If an error occurs during the process,
        appropriate dialogs are displayed to inform the user.

        Raises:
            IndexError: Raised when no data item is selected from the list/table.

        :return: None
        """
        try:
            selected_item = self.board.board.selection()
            if not selected_item:
                raise IndexError("Aucune donnée sélectionnée")

            # Ask for confirmation before deleting
            confirm = dialogs.Messagebox.yesno(
                message="Êtes-vous sûr de vouloir supprimer les données ?",
                title="Confirmation",
                parent=self.__master,
            )

            if confirm == "Oui":
                selected_item = self.board.board.selection()
                if selected_item:
                    if self.__controller.delete_data(data_id=int(selected_item[0])):
                        self.board.board.delete(selected_item)
        except IndexError:
            dialogs.Messagebox.show_info(
                message="Veuillez sélectionner un élément dans la liste",
                title="Attention",
                parent=self.__master
            )
        except Exception as e:
            dialogs.Messagebox.show_error(
                message=f"Une erreur est survenue lors de la suppression des données : {e}",
                title="Erreur",
                parent=self.__master
            )
            print(f"Une erreur est survenue lors de la suppression des données : {e}", file=sys.stderr)

    def show_data_selected(self)->None:
        """
        Handles the event of showing data for a selected item in the board. This method
        retrieves the user's selection, opens a view to display the data, and handles
        any errors that may arise during the process. If no selection is made, an
        informational message is shown. If any unexpected error occurs, it is recorded,
        and an error message is displayed.

        :return: None
        :raises IndexError: When no item is selected in the board.
        :raises Exception: For any unexpected errors encountered during execution.
        """
        try:
            selected_item = self.board.board.selection()
            if not selected_item:
                raise IndexError("Aucune donnée sélectionnée")
            ShowDataView(master=self.__master, board=self.board, controller=self.__controller)
            self.board.board.selection_remove(selected_item)
        except IndexError:
            dialogs.Messagebox.show_info(
                message="Veuillez sélectionner un élément dans la liste",
                title="Attention",
                parent=self.__master
            )
        except Exception as e:
            dialogs.Messagebox.show_error(
                message=f"Une erreur est survenue lors de l'ouverture de la vue d'affichage des données : {e}",
                title="Erreur",
                parent=self.__master
            )
            print(f"Une erreur est survenue lors de l'ouverture de la vue d'affichage des données : {e}",
                  file=sys.stderr)

    @property
    def controller(self)->object:
        """
        Provides access to a private controller attribute while handling potential exceptions
        to ensure robustness. If the attribute is not defined, it triggers the master quit
        operation to gracefully terminate the associated process.

        :raises AttributeError: If the private attribute __controller is not defined.

        :return: The value of the private attribute __controller if it exists, otherwise
                 initiates the termination sequence of the master.
        :rtype: object
        """
        try:
            return self.__controller
        except AttributeError:
            self.__master.quit()

    @controller.setter
    def controller(self, controller)->None:
        """
        Sets the controller attribute to the provided value.

        :param controller: The new value to set for the controller attribute.
        :type controller: Any
        :return: None
        :rtype: None
        """
        self.__controller = controller
