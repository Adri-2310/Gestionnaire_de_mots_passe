"""
Author: Adrien Mertens
Version: 1.0
"""

import sys
import ttkbootstrap as ttk
import ttkbootstrap.dialogs as dialogs
from views.menu import Menu
from views.boardView import BoardView
from controllers.controllersDatas import ControllersDatas
from models.data import Datas

class MainWindow(ttk.Window):
    """
    Represents the main window of the application, managing its components, layout,
    and functionality. The class is responsible for initializing and rendering the
    main user interface, including the treeview, menu, and their respective controllers.

    The main window is centered on the screen, configured as non-resizable, and
    populated with data upon initialization. It ensures that appropriate error
    messages are displayed if any issues arise during the initialization process
    of its components.

    :ivar treeview: The board view displayed within the main application window,
                    initializing and controlling the treeview interface.
    :type treeview: BoardView
    :ivar menu: The menu displayed within the main application window, initializing
                and controlling the menu interface.
    :type menu: Menu
    """
    def __init__(self, title: str, datas: Datas)->None:
        """
        Initializes the main application window and its components, including a
        treeview and menu with their respective controllers. Handles initialization
        errors and ensures proper layout and functionality for the user interface.
        Centers the window on the screen, configures window properties such as
        non-resizability, and sets the given title. Automatically refreshes the
        data board on initialization by querying the database, and reports
        any issues during this process or other stages of initialization.

        :param title: The title to be displayed on the application window.
        :type title: str
        :param datas: An instance containing the data used to initialize
                      the treeview and its controller.
        :type datas: Datas
        """
        try:
            super().__init__(themename="superhero")
            self.title(title)
            self.resizable(False, False)
            self.place_window_center()

            # Initialize the treeview and its controller
            self.treeview = BoardView(self)
            self.treeview.controller = ControllersDatas(datas=datas)
            self.treeview.grid(row=1, column=0, sticky='nsew', padx=10, pady=8)

            # Refresh the data board from the database
            try:
                self.treeview.refresh_data_board_from_db()
            except Exception as e:
                dialogs.Messagebox.show_error(
                    message=f"Une erreur est survenue lors du rafraîchissement des données : {e}",
                    title="Erreur de rafraîchissement",
                    parent=self
                )
                print(f"Une erreur est survenue lors du rafraîchissement des données : {e}", file=sys.stderr)

            # Initialize the menu and its controller
            self.menu = Menu(self, self.treeview)
            self.menu.controller = ControllersDatas(datas=datas)
            self.menu.grid(row=0, column=0, sticky='nsew', padx=10, pady=8)

        except Exception as e:
            dialogs.Messagebox.show_error(
                message=f"Une erreur inattendue est survenue lors de l'initialisation de la fenêtre principale : {e}",
                title="Erreur d'initialisation",
                parent=self
            )
            print(f"Une erreur inattendue est survenue lors de l'initialisation de la fenêtre principale : {e}",
                  file=sys.stderr)
            self.destroy()
            sys.exit(1)

        self.mainloop()
