"""
Author: Adrien Mertens
Version: 1.0
"""

import ttkbootstrap as ttk
from views.addDataView import AddDataView
from views.changeDataView import ChangeDataView
from views.showDataView import ShowDataView
import ttkbootstrap.dialogs as dialogs

class Menu(ttk.Frame):
    """
    A class to represent the main menu of the application.
    This menu allows adding, modifying, deleting, displaying data, and quitting the application.
    """

    def __init__(self, master, board):
        """
        Initializes the main menu.

        Args:
            master: The parent widget.
            board: The Treeview widget to display the data.
        """
        super().__init__(master)
        self.__master = master
        self.board = board
        self.__controller = None
        self.widgets()

    def widgets(self):
        """
        Creates and configures the menu widgets.
        """
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

    def add_data(self):
        """
        Opens the view to add data.
        """
        AddDataView(self.__master, self.__controller, self.board)

    def change_data_selected(self):
        """
        Opens the view to modify the selected data.
        """
        try:
            selected_item = self.board.board.selection()
            if not selected_item:
                raise IndexError("No data selected")

            ChangeDataView(master=self.__master, board=self.board, data_id=int(self.board.board.selection()[0]), controller=self.__controller)
        except IndexError:
            dialogs.Messagebox.show_info(message="Veuillez sélectionner un élément dans la liste",title="Attention",parent=self.__master)

    def delete_data_selected(self):
        """
        Deletes the selected data in the Treeview.
        """
        try:
            selected_item = self.board.board.selection()
            if not selected_item:
                raise IndexError("No data selected")
            # Ask for confirmation before deleting
            confirm = dialogs.Messagebox.yesno(message="Êtes-vous sûr de supprimer les données ?",title="Confirmation",parent=self.__master,icon="warning")
            if confirm == "Oui":
                # Add a dialog box to confirm deletion
                selected_item = self.board.board.selection()
                if selected_item:
                    if self.__controller.delete_data(data_id=int(selected_item[0])):
                        self.board.board.delete(selected_item)
        except IndexError:
            dialogs.Messagebox.show_info(message="Veuillez sélectionner un élément dans la liste",title="Attention",parent=self.__master)

    def show_data_selected(self):
        """
        Opens the view to display the selected data.
        """
        try:
            selected_item = self.board.board.selection()
            if not selected_item:
                raise IndexError("No data selected")

            ShowDataView(master=self.__master, board=self.board, controller=self.__controller)
        except IndexError:
            dialogs.Messagebox.show_info(message="Veuillez sélectionner un élément dans la liste",title="Attention",parent=self.__master)

    @property
    def controller(self):
        """
        Gets the controller associated with this menu.

        Returns:
            The associated controller.

        Raises:
            AttributeError: If the controller is not defined, quits the application.
        """
        try:
            return self.__controller
        except AttributeError:
            self.__master.quit()

    @controller.setter
    def controller(self, controller):
        """
        Sets the controller associated with this menu.

        Args:
            controller: The controller to associate.
        """
        self.__controller = controller
