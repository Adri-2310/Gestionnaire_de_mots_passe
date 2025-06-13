"""
Author: Adrien Mertens
Version: 1.0
"""

import ttkbootstrap as ttk
from views.menu import Menu
from views.boardView import BoardView
from controllers.controllersDatas import ControllersDatas
from models.data import Datas

class MainWindow(ttk.Window):
    """
    Represents the main application window for the user interface.

    The MainWindow class sets up the main application window using a Tkinter-themed
    interface with a title, menu, and treeview components. It ensures the window is
    non-resizable, centers it on the screen, and integrates with controllers to manage
    data operations. This class is the starting point of the GUI application.

    :ivar treeview: A Treeview widget for displaying and interacting with data.
    :type treeview: BoardView
    :ivar treeview.controller: Controller for managing data operations for the treeview.
    :type treeview.controller: ControllersDatas
    :ivar menu: A Menu widget providing application controls.
    :type menu: Menu
    :ivar menu.controller: Controller for managing data operations for the menu.
    :type menu.controller: ControllersDatas
    """
    def __init__(self, title: str, datas: Datas):
        """
        Initializes the main application window with specified title and data configurations.
        Sets up a themed window, centers it on the screen, and configures it to be non-resizable.
        Initializes the treeview and menu components along with their respective controllers.

        :param title: The title of the main application window.
        :type title: Str
        :param datas: A Datas object containing the data structure to be used by the application.
        :type datas: Datas
        """
        super().__init__(themename="superhero")
        self.title(title)
        self.resizable(False, False)
        self.place_window_center()

        # Initialize the treeview and its controller
        self.treeview = BoardView(self)
        self.treeview.controller = ControllersDatas(datas=datas)
        self.treeview.grid(row=1, column=0, sticky='nsew', padx=10, pady=8)
        self.treeview.refresh_data_board_from_db()

        # Initialize the menu and its controller
        self.menu = Menu(self, self.treeview)
        self.menu.controller = ControllersDatas(datas=datas)
        self.menu.grid(row=0, column=0, sticky='nsew', padx=10, pady=8)

        self.mainloop()
