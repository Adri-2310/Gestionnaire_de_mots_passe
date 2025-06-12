"""
__author__ = "Adrien Mertens"
__version__ = "1.0"
"""
import ttkbootstrap as ttk

class TopLevelValidateAndCancelForUseDB(ttk.Toplevel):
    def __init__(self,master,title:str,command_for_validateButton):
        #configuration de la top level
        super().__init__(master)
        self.title(title)
        self.resizable(False,False)
        self.__command_for_validateButton = command_for_validateButton
        self.place_window_center()

        #variable ttk pour les entrys
        self.var_id = ttk.IntVar()
        self.var_name = ttk.StringVar()
        self.var_username = ttk.StringVar()
        self.var_password = ttk.StringVar()
        self.var_source = ttk.StringVar()
        #création de widgets
        self.widgets()

    def widgets(self):
        style = ttk.Style()
        style.configure("AllFrame.TFrame", borderwidth=1, relief="solid",bordercolor="#4e5d6c",background="#4e5d6c")
        style.configure("TLabel",foreground="white",background="#4e5d6c",font=('Helvetica', 10, 'bold'))
        style.configure("TEntry", foreground="white", background="#4e5d6c", font=('Helvetica', 10))

        # Configurer les styles pour les boutons VALIDER et ANNULER
        style.configure("ValidateButton.TButton", borderwidth=1, relief="solid", bordercolor="#4CAF50",)
        style.map("ValidateButton.TButton",
                  background=[('active', '#45a049'), ('!active', '#53bf57')],
                  foreground=[('active', 'white'), ('!active', 'white')])

        style.configure("CancelButton.TButton", borderwidth=1, relief="solid", bordercolor="#FF5722")
        style.map("CancelButton.TButton",
                  background=[('active', '#c8441a'), ('!active', '#fd531e')],
                  foreground=[('active', 'white'), ('!active', 'white')])

        top_frame = ttk.Frame(self)
        top_frame.pack(side="top",padx=10,pady=10)

        name_frame = ttk.Frame(top_frame, style="AllFrame.TFrame")
        name_frame.pack(side="top", expand=True, fill="x")
        ttk.Label(name_frame, text="Nom :").pack(side="left", padx=10, pady=10)
        self.name_entry = ttk.Entry(name_frame, width=20, textvariable=self.var_name)
        self.name_entry.pack(side="right", padx=10, pady=10)

        username_frame = ttk.Frame(top_frame, style="AllFrame.TFrame")
        username_frame.pack(side="top", expand=True, fill="x")
        ttk.Label(username_frame,text="Nom d'utilisateur :").pack(side="left",padx=10,pady=10)
        self.username_entry = ttk.Entry(username_frame,width=20,textvariable=self.var_username)
        self.username_entry.pack(side="right",padx=10,pady=10)

        password_frame = ttk.Frame(top_frame,style="AllFrame.TFrame")
        password_frame.pack(side="top",expand=True,fill="x")
        ttk.Label(password_frame, text="Mots de passe :").pack(side="left",padx=10,pady=10)
        self.password_entry = ttk.Entry(password_frame,width=20,textvariable=self.var_password)
        self.password_entry.pack(side="right",padx=10,pady=10)

        source_frame = ttk.Frame(top_frame,style="AllFrame.TFrame")
        source_frame.pack(side="top",expand=True,fill="x")
        ttk.Label(source_frame, text="Source :").pack(side="left",padx=10,pady=10)
        self.source_entry = ttk.Entry(source_frame,width=20,textvariable=self.var_source)
        self.source_entry.pack(side="right",padx=10,pady=10)

        bottom_frame = ttk.Frame(self,style="AllFrame.TFrame")
        bottom_frame.pack(side="bottom",padx=10,pady=10,expand=True,fill="x")
        bottom_frame.columnconfigure(0,weight=1)
        bottom_frame.columnconfigure(1,weight=1)
        self.add_button = ttk.Button(bottom_frame,text="VALIDER",command=self.validate,style="ValidateButton.TButton")
        self.cancel_button = ttk.Button(bottom_frame,text="ANNULER",command=self.destroy,style="CancelButton.TButton")
        self.add_button.grid(row=0,column=0,padx=10,pady=10)
        self.cancel_button.grid(row=0,column=1,padx=10,pady=10)

    def validate(self):
        """Valide les entrées et exécute la commande de validation."""
        if self.validate_fields():
            self.__command_for_validateButton()



    def validate_fields(self) -> bool:
        """
        Valide les champs de saisie de l'utilisateur.

        Returns:
            bool: True si tous les champs sont valides, False sinon.
        """
        fields = [
            (self.var_name.get(), "Le nom est manquant"),
            (self.var_username.get(), "Le nom d'utilisateur est manquant"),
            (self.var_password.get(), "Le mot de passe est manquant"),
            (self.var_source.get(), "La source est manquante")
        ]

        for field_value, error_message in fields:
            if not field_value:
                print(f"Erreur : {error_message}")
                return False

        return True