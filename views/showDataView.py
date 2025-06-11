"""
__author__ = "Adrien Mertens"
__version__ = "1.0"
"""
import ttkbootstrap as ttk

class ShowDataView(ttk.Toplevel):
    def __init__(self,master,data_selected):
        super().__init__(master)
        self.title("Affichage")
        self.resizable(False,False)
        self.place_window_center()
        self.__data_selected = data_selected
        self.widgets()

    def widgets(self):
        style = ttk.Style()
        style.configure("AllFrame.TFrame", borderwidth=1, relief="solid", bordercolor="#4e5d6c", background="#4e5d6c")
        style.configure("TLabel", foreground="white", background="#4e5d6c", font=('Helvetica', 10, 'bold'))
        style.configure("TEntry", foreground="white", background="#4e5d6c", font=('Helvetica', 10))

        # Configurer les styles pour les boutons VALIDER et ANNULER
        style.configure("CancelButton.TButton", borderwidth=1, relief="solid", bordercolor="#FF5722")
        style.map("CancelButton.TButton",
                  background=[('active', '#c8441a'), ('!active', '#fd531e')],
                  foreground=[('active', 'white'), ('!active', 'white')])

        top_frame = ttk.Frame(self)
        top_frame.pack(side="top", padx=10, pady=10)

        username_frame = ttk.Frame(top_frame, style="AllFrame.TFrame")
        username_frame.pack(side="top", expand=True, fill="x")
        ttk.Label(username_frame, text="Nom d'utilisateur :").pack(side="left", padx=10, pady=10)
        self.username_entry = ttk.Entry(username_frame, width=20)
        self.username_entry.pack(side="right", padx=10, pady=10)

        password_frame = ttk.Frame(top_frame, style="AllFrame.TFrame")
        password_frame.pack(side="top", expand=True, fill="x")
        ttk.Label(password_frame, text="Mots de passe :").pack(side="left", padx=10, pady=10)
        self.password_entry = ttk.Entry(password_frame, width=20)
        self.password_entry.pack(side="right", padx=10, pady=10)

        source_frame = ttk.Frame(top_frame, style="AllFrame.TFrame")
        source_frame.pack(side="top", expand=True, fill="x")
        ttk.Label(source_frame, text="Source :").pack(side="left", padx=10, pady=10)
        self.source_entry = ttk.Entry(source_frame, width=20)
        self.source_entry.pack(side="right", padx=10, pady=10)

        bottom_frame = ttk.Frame(self, style="AllFrame.TFrame")
        bottom_frame.pack(side="bottom", padx=10, pady=10, expand=True, fill="x")
        bottom_frame.columnconfigure(0, weight=1)
        self.cancel_button = ttk.Button(bottom_frame, text="QUITTER", command=self.destroy,
                                        style="CancelButton.TButton")
        self.cancel_button.pack(side="top",fill="x",expand=True)