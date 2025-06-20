"""
__author__ = "Adrien Mertens"
__version__ = "1.0"
"""
import sys
import ttkbootstrap as ttk
import ttkbootstrap.dialogs as dialogs


class ShowDataView(ttk.Toplevel):
    def __init__(self, master, board,controller)->None:
        """
        Initializes the class instance, sets up the GUI window, initializes variables, and creates widgets.
        Attempts to set data based on the selected item in the provided data board. Handles potential
        exceptions during data retrieval.

        :param master: The parent widget or application window where this object is placed.
        :param board: The data board object which provides the selection for retrieval.
        :param controller: The controller responsible for handling logic or operations between the model
            and the view.

        :raises IndexError: Raised if no item is selected in the data board.
        :raises Exception: Raised for any general error during data retrieval.
        """
        super().__init__(master)
        self.title("Affichage")
        self.resizable(False,False)
        self.place_window_center()
        self.__controller = controller
        self.var_name = ttk.StringVar()
        self.var_username = ttk.StringVar()
        self.var_password = ttk.StringVar()
        self.var_source = ttk.StringVar()
        self.widgets()
        try:
            self.set_data(int(board.board.selection()[0]))
        except IndexError:
            dialogs.Messagebox.show_error(
                message="Veuillez sélectionner un élément dans la liste",
                title="Erreur",
                parent=self
            )
            self.destroy()
        except Exception as e:
            dialogs.Messagebox.show_error(
                message=f"Une erreur est survenue lors de la récupération des données : {e}",
                title="Erreur",
                parent=self
            )
            print(f"Une erreur est survenue lors de la récupération des données : {e}", file=sys.stderr)
            self.destroy()


    def widgets(self)->None:
        """
        Creates and configures GUI components for user interface interactions.

        This function initializes and applies specific styles to various widgets
        such as frames, labels, entries, and buttons, using the ttk.Style object.
        It defines the layout structure by creating frames and placing labels,
        entry fields, and a 'QUIT' button inside these frames. The entry fields
        display read-only data based on the provided tkinter variable bindings.

        In case of any error during the widget creation or configuration process,
        an error message is displayed in a dialog box, and the error is logged to
        the standard error output.

        :param self: Reference to the current object.
        :type self: Any

        :return: None
        """
        try:
            style = ttk.Style()
            style.configure("AllFrame.TFrame", borderwidth=1, relief="solid", bordercolor="#4e5d6c",
                            background="#4e5d6c")
            style.configure("TLabel", foreground="#17191b", background="#4e5d6c", font=('Helvetica', 10, 'bold'))


            # Configurer les styles pour les boutons ANNULER
            style.configure("CancelButton.TButton", borderwidth=1, relief="solid", bordercolor="#FF5722")
            style.map("CancelButton.TButton",
                      background=[('active', '#c8441a'), ('!active', '#fd531e')],
                      foreground=[('active', 'white'), ('!active', 'white')])

            top_frame = ttk.Frame(self)
            top_frame.pack(side="top", padx=10, pady=10)

            name_frame = ttk.Frame(top_frame, style="AllFrame.TFrame")
            name_frame.pack(side="top", expand=True, fill="x")
            ttk.Label(name_frame, text="Nom :").pack(side="left", padx=10, pady=10)
            ttk.Label(name_frame, width=20, textvariable=self.var_name,anchor="center").pack(side="right", padx=10,pady=10)

            username_frame = ttk.Frame(top_frame, style="AllFrame.TFrame")
            username_frame.pack(side="top", expand=True, fill="x")
            ttk.Label(username_frame, text="Nom d'utilisateur :").pack(side="left", padx=10, pady=10)
            ttk.Label(username_frame, width=20, textvariable=self.var_username,anchor="center").pack(side="right",
                                                                                                       padx=10, pady=10)

            password_frame = ttk.Frame(top_frame, style="AllFrame.TFrame")
            password_frame.pack(side="top", expand=True, fill="x")
            ttk.Label(password_frame, text="Mot de passe :").pack(side="left", padx=10, pady=10)
            ttk.Label(password_frame, width=20, textvariable=self.var_password,anchor="center").pack(side="right",
                                                                                                       padx=10, pady=10)

            source_frame = ttk.Frame(top_frame, style="AllFrame.TFrame")
            source_frame.pack(side="top", expand=True, fill="x")
            ttk.Label(source_frame, text="Source :").pack(side="left", padx=10, pady=10)
            ttk.Label(source_frame, width=20, textvariable=self.var_source,anchor="center").pack(side="right",
                                                                                                   padx=10, pady=10)

            bottom_frame = ttk.Frame(self, style="AllFrame.TFrame")
            bottom_frame.pack(side="bottom", padx=10, pady=10, expand=True, fill="x")
            bottom_frame.columnconfigure(0, weight=1)
            ttk.Button(bottom_frame, text="QUITTER", command=self.destroy, style="CancelButton.TButton").pack(
                side="top", fill="x", expand=True)
        except Exception as e:
            dialogs.Messagebox.show_error(
                message=f"Une erreur est survenue lors de la création des widgets : {e}",
                title="Erreur",
                parent=self
            )
            print(f"Une erreur est survenue lors de la création des widgets : {e}", file=sys.stderr)

    def set_data(self,data_id:int)->None:
        """
        Updates the current instance with data retrieved using the provided data ID. It fetches
        data through the internal controller and sets relevant instance variables. If an error
        occurs during data retrieval, it shows an error message dialog and logs the error to the
        standard error stream.

        :param data_id: ID of the data to be fetched
        :type data_id: int
        :return: None
        :rtype: None
        """
        try:
            data = self.__controller.get_one_data(data_id=data_id)
            self.var_name.set(data.name)
            self.var_username.set(data.username)
            self.var_password.set(data.password)
            self.var_source.set(data.source)
        except Exception as e:
            dialogs.Messagebox.show_error(
                message=f"Une erreur est survenue lors de la récupération des données : {e}",
                title="Erreur",
                parent=self
            )
            print(f"Une erreur est survenue lors de la récupération des données : {e}", file=sys.stderr)
