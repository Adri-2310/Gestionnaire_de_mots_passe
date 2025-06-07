import ttkbootstrap as ttk
import ttkbootstrap.constants as ttkc

class BoardView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Créer un style personnalisé
        style = ttk.Style()

        # Configurer les couleurs pour les lignes de données
        style.configure("Treeview",
                        foreground="white",  # Texte noir pour les lignes
                        font=('Helvetica', 10))  # Fond des cellules

        # Configurer les couleurs pour l'en-tête
        style.configure("Treeview.Heading",
                        background="#4e5d6c",  # Gris foncé pour l'en-tête
                        foreground="white",  # Texte blanc pour l'en-tête
                        font=('Helvetica', 10, 'bold'))

        # Configurer les couleurs pour les différents états du Treeview
        style.map("Treeview",
                  background=[('selected', '#2d3e4f'),
                              ('active', '#3a4d5e')],)

        # Créez un Frame pour contenir le Treeview
        self.tree_frame = ttk.Frame(self, height=250)
        self.tree_frame.pack_propagate(False)  # Empêche le Frame de redimensionner en fonction de son contenu
        self.tree_frame.pack(fill="both", expand=False)

        # Créez un Treeview avec un nombre limité de lignes visibles
        self.board = ttk.Treeview(self.tree_frame, height=5, show="headings", style="Treeview")

        # Ajoutez les colonnes au tableau
        self.board["columns"] = ("id", "name")
        self.board.column("id", minwidth=75, width=75, stretch=ttkc.NO,anchor=ttk.CENTER)
        self.board.column("name", minwidth=100, width=100, stretch=ttkc.YES,anchor=ttk.CENTER)

        # Ajoutez des en-têtes de colonne
        self.board.heading("id", text="NUMÉRO",anchor=ttk.CENTER)
        self.board.heading("name", text="NOM",anchor=ttk.CENTER)

        # Configurer les couleurs pour les lignes paires et impaires
        self.board.tag_configure('evenrow', background='#475562')  # Gris foncé pour les lignes paires
        self.board.tag_configure('oddrow', background='#5d6f81')  # Gris clair pour les lignes impaires

        # Insérer des données d'exemple avec des tags pour les couleurs alternées
        for i in range(30):
            if i % 2 == 0:
                self.board.insert('', 'end', values=(f'{i + 1}', f'test{i + 1}'), tags=('evenrow',))
            else:
                self.board.insert('', 'end', values=(f'{i + 1}', f'test{i + 1}'), tags=('oddrow',))

        # Ajoutez une barre de défilement verticale
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.board.yview)
        self.board.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.board.pack(side="left", fill="both", expand=True)
