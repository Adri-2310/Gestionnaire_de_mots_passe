"""
Author: Adrien Mertens
Version: 1.0
"""
import sys
import ttkbootstrap as ttk
import ttkbootstrap.constants as ttkc
import ttkbootstrap.dialogs as dialogs

class BoardView(ttk.Frame):
    """
    Represents a custom-styled Treeview contained within a Frame, designed for
    displaying tabular data with aesthetic and functional features, such as
    color tagging for rows, mapped interactions for states, and an integrated
    vertical scrollbar for navigation.

    The class utilizes a controller to manage retrieving and updating data,
    allowing dynamic interaction with backend sources like a database.

    :ivar tree_frame: The Frame containing the Treeview widget and its scrollbar.
    :type tree_frame: ttk.Frame
    :ivar board: The Treeview widget styled and configured for data display.
    :type board: ttk.Treeview
    :ivar __parent: The parent widget that contains this Frame.
    :type __parent: tkinter.Widget
    :ivar __controller: A controller object responsible for managing data
        operations, such as retrieving and updating the displayed data.
    :type __controller: object
    """
    def __init__(self, parent)->None:
        """
        Initializes the Treeview and associated Frame, styling, headers, and rows with
        customized appearance and scroll behavior.

        This constructor sets up the interface for a Treeview table widget within a
        parent container, applying styles for headers, rows, and states. It also includes
        a scrollbar for managing limited visible rows and adds configuration for the columns
        and headers.

        :param parent: The parent container in which the Treeview and its associated
                       components will be placed.
        :type parent: Any
        """
        super().__init__(parent)
        self.__controller = None
        self.__parent = parent
        # Create a custom style
        style = ttk.Style()

        # Configure colors for data rows
        style.configure("Treeview",
                        foreground="white",  # Black text for rows
                        font=('Helvetica', 10))  # Cell background

        # Configure colors for the header
        style.configure("Treeview.Heading",
                        background="#4e5d6c",  # Dark gray for the header
                        foreground="white",  # White text for the header
                        font=('Helvetica', 10, 'bold'))

        # Configure colors for different states of the Treeview
        style.map("Treeview",
                  background=[('selected', '#2d3e4f'),
                              ('active', '#3a4d5e')],)

        # Create a Frame to contain the Treeview
        self.tree_frame = ttk.Frame(self, height=250)
        self.tree_frame.pack_propagate(False)  # Prevent the Frame from resizing based on its content
        self.tree_frame.pack(fill="both", expand=False)

        # Create a Treeview with a limited number of visible rows
        self.board = ttk.Treeview(self.tree_frame, height=5, show="headings", style="Treeview")

        # Add columns to the table
        self.board["columns"] = "name"
        self.board.column("name", minwidth=100, width=100, stretch=ttkc.YES, anchor=ttk.CENTER)

        # Add column headers
        self.board.heading("name", text="NAME", anchor=ttk.CENTER)

        # Configure colors for even and odd rows
        self.board.tag_configure('evenrow', background='#475562')  # Dark gray for even rows
        self.board.tag_configure('oddrow', background='#5d6f81')  # Light gray for odd rows

        # Add a vertical scrollbar
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.board.yview)
        self.board.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.board.pack(side="left", fill="both", expand=True)

    @property
    def controller(self)->object:
        """
        Gets the controller object.

        This property retrieves the private `__controller` attribute. If the
        attribute does not exist (raised as AttributeError), it ensures proper
        application shutdown by calling the `quit` method on its parent.

        :raises AttributeError: If `__controller` attribute is not set.
        :return: The controller object.
        :rtype: object
        """
        try:
            return self.__controller
        except AttributeError:
            self.__parent.quit()

    @controller.setter
    def controller(self, controller)->None:
        """
        Sets the controller attribute to the provided value. This ensures the controller
        is properly assigned for further usage.

        :param controller: The new value to set for the controller attribute. Expected
            to be a valid controller instance or value.
        :return: None
        """
        self.__controller = controller

    def refresh_data_board_from_db(self)->None:
        """
        Refreshes and updates the contents of the data board by synchronizing it with the
        most recent data retrieved from the database. This method ensures that the board
        displays up-to-date information by clearing old data, applying styling to rows based
        on their index (even or odd), and handling any exceptions that occur during this process.

        :raises AttributeError: If there is an issue accessing attributes of the controller.
        :raises Exception: If an unexpected error occurs during the data refresh process.
        :return: None
        """
        try:
            # Retrieve all data from the database
            data_list = self.controller.get_all_datas()

            # Clear all existing data in the Treeview
            for item in self.board.get_children():
                self.board.delete(item)

            # Insert new data
            for index, data in enumerate(data_list):
                tag = 'evenrow' if index % 2 == 0 else 'oddrow'
                self.board.insert('', ttkc.END, iid=data.id, values=data.name, tags=(tag,))

        except AttributeError as ae:
            dialogs.Messagebox.show_error(
                message=f"Une erreur est survenue lors de l'accès aux attributs du contrôleur : {ae}",
                title="Erreur d'attribut",
                parent=self
            )
        except Exception as e:
            dialogs.Messagebox.show_error(
                message=f"Une erreur inattendue est survenue : {e}",
                title="Erreur",
                parent=self
            )
            print(f"Une erreur inattendue est survenue : {e}", file=sys.stderr)
