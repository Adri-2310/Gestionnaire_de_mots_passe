import ttkbootstrap as ttk
import ttkbootstrap.constants as ttkc

class BoardView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Créez un Frame pour contenir le Treeview
        self.tree_frame = ttk.Frame(self, height=250)
        self.tree_frame.pack_propagate(False)  # Empêche le Frame de redimensionner en fonction de son contenu
        self.tree_frame.pack(fill="both", expand=False)

        # Créez un Treeview avec un nombre limité de lignes visibles
        self.board = ttk.Treeview(self.tree_frame, height=5, show="headings")

        # Ajoutez les colonnes au tableau
        self.board["columns"] = ("id", "name")
        self.board.column("id", minwidth=75, width=75, stretch=ttkc.NO,anchor=ttk.CENTER)
        self.board.column("name", minwidth=100, width=100, stretch=ttkc.YES,anchor=ttk.CENTER)

        # Ajoutez des en-têtes de colonne
        self.board.heading("id", text="Numéro",anchor=ttk.CENTER)
        self.board.heading("name", text="Nom",anchor=ttk.CENTER)

        # Insérez des données d'exemple
        self.board.insert('', 'end', values=('1', 'test1'))
        self.board.insert('', 'end', values=('2', 'test2'))
        self.board.insert('', 'end', values=('3', 'test3'))
        self.board.insert('', 'end', values=('4', 'test4'))
        self.board.insert('', 'end', values=('5', 'test5'))
        self.board.insert('', 'end', values=('6', 'test6'))

        # Ajoutez une barre de défilement verticale
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.board.yview)
        self.board.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.board.pack(side="left", fill="both", expand=True)
