"""
__author__ = "Adrien Mertens"
__version__ = "1.0"
"""
import sys
import ttkbootstrap as ttk
import ttkbootstrap.dialogs as dialogs

class TopLevelValidateAndCancelForUseDB(ttk.Toplevel):
    def __init__(self,master,title:str,command_for_validateButton)->None:
        """
        Initializes a new instance of the class, setting up window configuration,
        creating and initializing variables, and preparing the widgets. Handles errors
        during initialization by displaying an error message and destroying the
        instance.

        :param master: Parent widget for the top-level window.
        :type master: any
        :param title: Title of the window.
        :type title: str
        :param command_for_validateButton: Command to be executed when the validate button is pressed.
        :type command_for_validateButton: callable
        :raises Exception: If an error occurs during the initialization process.
        """
        try:
            # Configuration de la top level
            super().__init__(master)
            self.title(title)
            self.resizable(False, False)
            self.__command_for_validateButton = command_for_validateButton
            self.place_window_center()

            # Variable ttk pour les entrys
            self.var_id = ttk.IntVar()
            self.var_name = ttk.StringVar()
            self.var_username = ttk.StringVar()
            self.var_password = ttk.StringVar()
            self.var_source = ttk.StringVar()

            # Création de widgets
            self.widgets()
        except Exception as e:
            dialogs.Messagebox.show_error(
                message=f"Une erreur est survenue lors de l'initialisation de la fenêtre : {e}",
                title="Erreur",
                parent=self
            )
            print(f"Une erreur est survenue lors de l'initialisation de la fenêtre : {e}", file=sys.stderr)
            self.destroy()

    def widgets(self)->None:
        """
        Builds and configures widgets for a graphical user interface, including frames, labels, entry fields, and buttons with
        customized styles. This function integrates components for capturing user input such as name, username, password, and
        source, and additional buttons for user controls like validating or canceling actions.

        :raises Exception: if an error occurs during widget configuration or instantiation.
        :return: None
        """
        try:
            style = ttk.Style()
            style.configure("AllFrame.TFrame", borderwidth=1, relief="solid", bordercolor="#4e5d6c",
                            background="#4e5d6c")
            style.configure("TLabel", foreground="white", background="#4e5d6c", font=('Helvetica', 10, 'bold'))
            style.configure("TEntry", foreground="white", background="#4e5d6c", font=('Helvetica', 10))

            # Configurer les styles pour les boutons VALIDER et ANNULER
            style.configure("ValidateButton.TButton", borderwidth=1, relief="solid", bordercolor="#4CAF50")
            style.map("ValidateButton.TButton",
                      background=[('active', '#45a049'), ('!active', '#53bf57')],
                      foreground=[('active', 'white'), ('!active', 'white')])

            style.configure("CancelButton.TButton", borderwidth=1, relief="solid", bordercolor="#FF5722")
            style.map("CancelButton.TButton",
                      background=[('active', '#c8441a'), ('!active', '#fd531e')],
                      foreground=[('active', 'white'), ('!active', 'white')])

            top_frame = ttk.Frame(self)
            top_frame.pack(side="top", padx=10, pady=10)

            name_frame = ttk.Frame(top_frame, style="AllFrame.TFrame")
            name_frame.pack(side="top", expand=True, fill="x")
            ttk.Label(name_frame, text="Nom :").pack(side="left", padx=10, pady=10)
            ttk.Entry(name_frame, width=20, textvariable=self.var_name).pack(side="right", padx=10, pady=10)

            username_frame = ttk.Frame(top_frame, style="AllFrame.TFrame")
            username_frame.pack(side="top", expand=True, fill="x")
            ttk.Label(username_frame, text="Nom d'utilisateur :").pack(side="left", padx=10, pady=10)
            ttk.Entry(username_frame, width=20, textvariable=self.var_username).pack(side="right", padx=10, pady=10)

            password_frame = ttk.Frame(top_frame, style="AllFrame.TFrame")
            password_frame.pack(side="top", expand=True, fill="x")
            ttk.Label(password_frame, text="Mot de passe :").pack(side="left", padx=10, pady=10)
            ttk.Entry(password_frame, width=20, textvariable=self.var_password).pack(side="right", padx=10, pady=10)

            source_frame = ttk.Frame(top_frame, style="AllFrame.TFrame")
            source_frame.pack(side="top", expand=True, fill="x")
            ttk.Label(source_frame, text="Source :").pack(side="left", padx=10, pady=10)
            ttk.Entry(source_frame, width=20, textvariable=self.var_source).pack(side="right", padx=10, pady=10)

            bottom_frame = ttk.Frame(self, style="AllFrame.TFrame")
            bottom_frame.pack(side="bottom", padx=10, pady=10, expand=True, fill="x")
            bottom_frame.columnconfigure(0, weight=1)
            bottom_frame.columnconfigure(1, weight=1)

            ttk.Button(bottom_frame, text="VALIDER", command=self.validate,
                                         style="ValidateButton.TButton").grid(row=0, column=0, padx=10, pady=10)
            ttk.Button(bottom_frame, text="ANNULER", command=self.destroy,
                                            style="CancelButton.TButton").grid(row=0, column=1, padx=10, pady=10)
        except Exception as e:
            dialogs.Messagebox.show_error(
                message=f"Une erreur est survenue lors de la création des widgets : {e}",
                title="Erreur",
                parent=self
            )
            print(f"Une erreur est survenue lors de la création des widgets : {e}", file=sys.stderr)

    def validate(self)->None:
        """
        Validates the fields by calling the validation method and triggers further
        processing if the validation is successful. In case of an error during
        the process, displays an error message dialog and logs the error.

        :raises Exception: Propagates any exceptions encountered during the
            validation process.
        """
        try:
            if self.validate_fields():
                self.__command_for_validateButton()
        except Exception as e:
            dialogs.Messagebox.show_error(
                message=f"Une erreur est survenue lors de la validation : {e}",
                title="Erreur",
                parent=self
            )
            print(f"Une erreur est survenue lors de la validation : {e}", file=sys.stderr)



    def validate_fields(self)->bool:
        """
        Validates that all required fields have non-empty values. Each field is checked, and
        if one is empty, a warning message box is displayed with the corresponding error
        message. If all fields are validated, the function returns True.

        :raises: Displays a warning message box if a field is empty.
        :return: True if all fields are valid, otherwise False.
        :rtype: bool
        """
        fields = [
            (self.var_name.get(), "Le nom est manquant"),
            (self.var_username.get(), "Le nom d'utilisateur est manquant"),
            (self.var_password.get(), "Le mot de passe est manquant"),
            (self.var_source.get(), "La source est manquante")
        ]

        for field_value, error_message in fields:
            if not field_value:
                dialogs.Messagebox.show_warning(
                    message=error_message,
                    title="Attention",
                    parent=self
                )
                return False
        return True