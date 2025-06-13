"""
Author: Adrien Mertens
Version: 1.0
"""
import ttkbootstrap as ttk
import ttkbootstrap.constants as ttkc

class BoardView(ttk.Frame):
    """
    Represents a graphical table view for displaying data in a tree structure using a ttk.Treeview widget.

    This class provides a user interface component for displaying data in rows and columns with styled headers,
    custom row styling for even and odd rows, and a vertical scrollbar for navigation. It also includes
    functionality to refresh the displayed data from a database.

    :ivar tree_frame: A frame that contains the Treeview widget and its scrollbar.
    :type tree_frame: ttk.Frame
    :ivar board: The main Treeview widget used to display data.
    :type board: ttk.Treeview
    :ivar controller: A property representing the controller responsible for managing data
                     and interactions for the displayed board.
    :type controller: object
    """
    def __init__(self, parent)->None:
        """
        Initializes the class instance by creating a custom-styled Treeview widget
        with a specific color configuration, headers, columns, and a scrollbar.

        The implementation includes styling for different elements such as data rows,
        headers, and selection states, ensuring a visually distinct and well-organized
        table. A Frame is created to contain the Treeview, which does not resize based
        on its content individually. Columns, header configurations, color tagging for
        rows, and event-based color mapping are applied to enhance the Treeview's
        appearance and usability.

        :param parent: The parent widget where this Treeview widget will be placed.
        :type parent: tkinter.Widget
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
        Provides access to the `controller` attribute which is a private member variable
        of the class. This property is used to retrieve the value of the `__controller`.
        If the attribute `__controller` is not set, it triggers the `quit` method of
        `__parent`.

        :return: The value of the `__controller` attribute if it exists, otherwise
                 initiates the `quit` method of the parent context.
        :rtype: Any
        """
        try:
            return self.__controller
        except AttributeError:
            self.__parent.quit()

    @controller.setter
    def controller(self, controller)->None:
        """
        Sets the controller property.

        This setter method modifies the private instance variable
        `__controller` with the given controller value.

        :param controller: The new controller to set.
        :type controller: Any
        """
        self.__controller = controller

    def refresh_data_board_from_db(self)->None:
        """
        Refreshes the data displayed on the TreeView by fetching updated data
        from the database. Existing data on the board will be cleared and
        repopulated based on new records retrieved.

        :raises DatabaseError: If there are issues interacting with the database.
        :param self: The instance of the class that holds the controller and
            TreeView (board).
        :rtype: None
        """
        # Retrieve all data from the database
        data_list = self.__controller.get_all_datas()
        # Clear all existing data in the Treeview
        for item in self.board.get_children():
            self.board.delete(item)

        # Insert new data
        for index, data in enumerate(data_list):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            self.board.insert('', ttkc.END, iid=data.id, values=data.name, tags=(tag,))
