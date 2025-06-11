"""
__author__ = "Adrien Mertens"
__version__ = "1.0"
"""
import ttkbootstrap as ttk
from views.addDataView import AddDataView
from views.changeDataView import ChangeDataView


class Menu(ttk.Frame):
    def __init__(self,master,treeview):
        super().__init__(master)
        __master = master
        self.__treeview = treeview
        self.widgets()

    def widgets(self):

        # Créer un style personnalisé pour chaque bouton
        style = ttk.Style()

        style.configure('AllButton.TButton', borderwidth=1, relief="solid",bordercolor="#4e5d6c")
        # Note: 'background' is not directly supported for ttk buttons, use 'style.map' for state-specific colors
        style.map('AllButton.TButton',
                  background=[('active', '#ABB6C2'), ('!active', '#4e5d6c')],
                  foreground=[('active', 'black'), ('!active', 'white')])


        ttk.Button(self, text="AJOUTER", command=self.add_data_in_db,style="AllButton.TButton").pack(side="left",padx=5,pady=10)
        change_button = ttk.Button(self, text="MODIFICATION", command=self.change_data_selected,style="AllButton.TButton")
        change_button.pack(side="left",padx=5,pady=10)
        delete_button = ttk.Button(self, text="SUPPRIMER", command=self.delete_data_selected,style="AllButton.TButton")
        delete_button.pack(side="left",padx=5,pady=10)
        show_button = ttk.Button(self, text="AFFICHIER", command=self.show_data_selected,style="AllButton.TButton")
        show_button.pack(side="left",padx=5,pady=10)
        ttk.Button(self,text="QUITTER",command=self.master.quit,style="AllButton.TButton").pack(side="left",padx=5,pady=10)

    def add_data_in_db(self):
        AddDataView(self.master)

    def change_data_selected(self):
        ChangeDataView(self.master, self.__treeview)

    def delete_data_selected(self):
        pass

    def show_data_selected(self):
        pass
